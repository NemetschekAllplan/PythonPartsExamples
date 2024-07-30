""" Example script showing the possibilities to repair a polyhedron using PolyhedronUtil
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PolyhedronRepairBuildingElement import \
        PolyhedronRepairBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PolyhedronRepair.py')


def check_allplan_version(_build_ele: BuildingElement,
                          version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        version:    the current Allplan version

    Returns:
        True
    """
    return float(version) > 2025.0


def create_preview(build_ele : BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele:  building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """
    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PolyhedronRepair(build_ele, script_object_data)


class PolyhedronRepair(BaseScriptObject):
    """Implementation of an interactor, where the user has to select a single element
    with a polyhedron geometry. The geometry of this polyhedron will be repaired according
    to the settings in the property palette.
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Default constructor

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """
        super().__init__(script_object_data)

        self.build_ele = build_ele
        self.interaction_result = SingleElementSelectResult()

    def execute(self) -> CreateElementResult:
        """Execute the element creation

        This interactor only modifies elements, so the function actually do not create anything.

        Returns:
            created element
        """
        return CreateElementResult()

    def start_input(self):
        """Start the element selection"""

        allowed_elements = [AllplanEleAdapter.Volume3D_TypeUUID,
                            AllplanEleAdapter.Area3D_TypeUUID]

        self.script_object_interactor = SingleElementSelectInteractor(self.interaction_result,
                                                                      allowed_elements,
                                                                      "Select a polyhedron")

    def start_next_input(self):
        """Repair the polyhedron and restart the input"""

        self.repair_polyhedron(self.interaction_result.sel_element)
        self.start_input()

    def repair_polyhedron(self, volume_element_adapter: AllplanEleAdapter.BaseElementAdapter):
        """Repair the geometry of the given polyhedron

        Args:
            volume_element_adapter: model element with a polyhedron geometry to repair
        """
        # we can assume, the selected element will be a ModelElement3D with Polyhedron3D geomemtry,
        # because we set the filter to Volume3D_TypeUUID elements only.
        model_element_3d = cast(AllplanBasisEle.ModelElement3D, AllplanBaseEle.GetElement(volume_element_adapter))

        polyhedron = cast(AllplanGeometry.Polyhedron3D, model_element_3d.GeometryObject)

        match self.build_ele.RepairType.value:

            # fix the face loops crossed in shape of an "8"
            case "CrossedLoopFaces":
                result = AllplanGeometry.PolyhedronUtil.RepairPolyhedronCrossLoopFaces(polyhedron)

                msg = f"Cross loop faces repair is done.\nResult: {result}"

            # split a face, when an edge is adjacent
            case "SplitFacesAtEdges":
                result, polyhedron, polyhedron_changed = AllplanGeometry.PolyhedronUtil.SplitFacesAtEdges(polyhedron)

                msg = "Splitting faces at edges done.\nPolyhedron "
                msg += "has" if polyhedron_changed else "hasn't"
                msg += f" changed. Result: {result}"

            # repair normal vectors of each face to point to the inside
            case "RepairFaceNormals":
                result, polyhedron, polyhedron_changed = AllplanGeometry.PolyhedronUtil.RepairFaceNormals(polyhedron)

                msg = "Face normals were repaired" if polyhedron_changed else "Face normals are OK. Nothing to do."
                msg += f"\nResult: {result}"

            # perform all three operations above in one step
            case "AllInOne":
                crossed_loop, splitted_faces, normals_changed, err, polyhedron = AllplanGeometry.PolyhedronUtil.RepairPolyhedron(polyhedron)

                msg = "Attempted to repair the polyhedron.\n"
                msg += f"Repaired crossed loops: {crossed_loop}.\n"
                msg += f"Splitted faces at edges: {splitted_faces}\n"
                msg += f"Face normals changed: {normals_changed}.\n"
                msg += f"Overall result code: {err}"

            # merge coplanar and adjacend faces into one
            case "MergePlanarFaces":
                count_before = polyhedron.GetFacesCount()

                AllplanGeometry.PolyhedronUtil.MergePlanarFaces(polyhedron)

                count_after = polyhedron.GetFacesCount()
                msg = "Merging planar faces done.\n"
                msg += "Number of faces "
                msg += "didn't changed." if count_before == count_after else f"was reduced by {count_before - count_after}."

            # simplify the polyhedron by removing overlapping edges
            case "SimplifyPolyhedron":

                result = AllplanGeometry.PolyhedronUtil.SimplifyPolyhedron(polyhedron)

                msg = "Polyhedron was successfully simplified" if result else "Simplification was not performed."


        # apply changed geometry to the model element and save it in the database
        model_element_3d.GeometryObject = polyhedron
        AllplanBaseEle.ModifyElements(self.coord_input.GetInputViewDocument(),[model_element_3d])

        # print results in the trace
        print(f"\n{'='*20} Polyhedron repair results {'='*20}\n")
        print(msg)
        print(f"\n{'='*67}")

        AllplanUtil.ShowMessageBox("The results are shown in the Trace window", AllplanUtil.MB_OK)
