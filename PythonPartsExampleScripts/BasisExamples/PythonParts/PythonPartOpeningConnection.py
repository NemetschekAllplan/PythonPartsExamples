""" implementation of the example for the PythonPart - opening connection"""

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil
from Utils.General.BuildingElementParameterUtil import BuildingElementParameterUtil

from ValueTypes.Data.ElementGeometryConnection import ElementGeometryConnection, GeometryType

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartOpeningConnectionBuildingElement import PythonPartOpeningConnectionBuildingElement
else:
    PythonPartOpeningConnectionBuildingElement = BuildingElement

print('Load PythonPartOpeningConnection.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\BasisExamples\PythonParts\PythonPartOpeningConnection.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PythonPartOpeningConnection(build_ele, script_object_data)


class PythonPartOpeningConnection(BaseScriptObject):
    """ Definition of class PythonPartOpeningConnection
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        build_ele = cast(PythonPartOpeningConnectionBuildingElement, build_ele)

        self.build_ele = build_ele

        self.sel_result = SingleElementSelectResult()

        self.select_opening_for_copy = False

        self.opening_ele = build_ele.OpeningConnection.value.element


        #----------------- check for modification

        if self.execution_event == AllplanSettings.ExecutionEvent.eCreation:
            return

        if self.execution_event == AllplanSettings.ExecutionEvent.eCopy:
            build_ele.InputMode.value = build_ele.PARAMETER_MODIFICATION

            return

        if self.opening_ele.IsNull():
            AllplanUtil.ShowMessageBox("You are modifying a copied PythonPart!\n\n"
                                        "Please select the opening for the connection",
                                        AllplanUtil.MB_OK)

            self.select_opening_for_copy = True

            return

        build_ele.InputMode.value = build_ele.PARAMETER_MODIFICATION


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele


        #----------------- check for modification

        if self.is_only_update or self.execution_event != AllplanSettings.ExecutionEvent.eCreation and not self.select_opening_for_copy:
            return


        #----------------- select the opening

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_result,
                                                                      ArchitectureElementsQueryUtil.create_vertical_arch_opening_query(),
                                                                      "Select the opening")

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        self.opening_ele = self.sel_result.sel_element

        build_ele.InputMode.value = self.build_ele.PARAMETER_MODIFICATION

        build_ele.OpeningConnection.value = ElementGeometryConnection(self.coord_input.GetSelectedElement(), GeometryType.BASE_GEOMETRY)


    def execute(self) -> CreateElementResult:
        """  execute the script

        Returns:
            created result
        """

        build_ele = self.build_ele


        #----------------- calculate multiple opening elements in case of PythonPart copy

        if self.execution_event == AllplanSettings.ExecutionEvent.eCopy:
            if len(self.modification_ele_list.get_base_element_adapter_list(self.document)) > 1:
                model_ele_list = ModelEleList()

                for ele in self.modification_ele_list.get_base_element_adapter_list(self.document):
                    BuildingElementParameterUtil.fill_parameter_from_python_part(build_ele, ele, self.org_and_copy_ele_guids)

                    self.opening_ele = build_ele.OpeningConnection.value.element

                    model_ele_list.extend(self.create_opening_pyp())

                return CreateElementResult(model_ele_list,
                                           placement_point= AllplanGeo.Point3D())



            #------------- if the opening element is not set, return empty result in case of copy

            if self.opening_ele.IsNull():
                return CreateElementResult()


        #----------------- delete the PythonPart

        if self.opening_ele.IsNull() and self.execution_event != AllplanSettings.ExecutionEvent.eCopy:
            return CreateElementResult(ModelEleList(),
                                       elements_to_delete = AllplanEleAdapter.BaseElementAdapterList( \
                                           [self.modification_ele_list.get_base_element_adapter(self.document)]))


        #----------------- create the PythonPart

        return CreateElementResult(self.create_opening_pyp(),
                                   placement_point = AllplanGeo.Point3D(),
                                   multi_placement = True)


    def create_opening_pyp(self) -> ModelEleList:
        """ create the opening PythonPart

        Returns:
            created model elements for the opening PythonPart
        """

        build_ele = self.build_ele

        opening_ele = AllplanBaseEle.GetElement(self.opening_ele)

        if isinstance(opening_ele, AllplanArchEle.GeneralOpeningElement):
            opening_ele_prop = opening_ele.Properties

        elif isinstance(opening_ele, AllplanArchEle.DoorOpeningElement):
            opening_ele_prop = opening_ele.Properties

        elif isinstance(opening_ele, AllplanArchEle.WindowOpeningElement):
            opening_ele_prop = opening_ele.Properties
        else:
            return ModelEleList()


        #----------------- get the opening data

        plane_ref = opening_ele_prop.PlaneReferences

        opening_polygon = build_ele.OpeningConnection.value.geometry

        if isinstance(opening_polygon, AllplanGeo.Polyline2D):
            opening_polygon = AllplanGeo.Polygon2D(opening_polygon.Points)

        opening_height  = plane_ref.AbsTopElevation - plane_ref.AbsBottomElevation
        opening_dir_vec = AllplanGeo.Vector2D(opening_polygon[0], opening_polygon[1])
        opening_width   = opening_dir_vec.GetLength()
        opening_pnt     = opening_polygon[0]


        #----------------- create the placement matrix

        placement_mat = AllplanGeo.Matrix3D()
        placement_mat.SetRotation(AllplanGeo.Line3D(0, 0, 0, 0, 0, 1000), opening_dir_vec.GetAngle())

        offset_vec = AllplanGeo.Vector2D(opening_polygon[0], opening_polygon[3])

        tier_thickness = offset_vec.GetLength()

        offset_vec.Normalize((tier_thickness - build_ele.FrameThickness.value) / 2)

        placement_mat.Translate(AllplanGeo.Vector3D(opening_pnt.X + offset_vec.X,
                                opening_pnt.Y + offset_vec.Y, plane_ref.AbsBottomElevation))


        #----------------- create the frame

        frame_ele = AllplanGeo.Polyhedron3D.CreateCuboid(opening_width, build_ele.FrameThickness.value, opening_height)
        cut_ele   = AllplanGeo.Polyhedron3D.CreateCuboid(opening_width - build_ele.FrameWidth.value * 2,
                                                         build_ele.FrameThickness.value,
                                                         opening_height - build_ele.FrameWidth.value * 2)
        cut_ele   = AllplanGeo.Move(cut_ele, AllplanGeo.Vector3D(build_ele.FrameWidth.value, 0, build_ele.FrameWidth.value))

        err, frame_ele = AllplanGeo.MakeSubtraction(frame_ele, cut_ele)

        if err != AllplanGeo.eGeometryErrorCode.eOK:
            return ModelEleList()

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d_with_texture(AllplanGeo.Transform(frame_ele, placement_mat),
                                                       AllplanBasisEle.TextureDefinition(build_ele.FrameSurface.value))


        #----------------- create the pane

        pane_ele = AllplanGeo.Polyhedron3D.CreateCuboid(opening_width - build_ele.FrameWidth.value * 2,
                                                        build_ele.PaneThickness.value,
                                                        opening_height - build_ele.FrameWidth.value * 2)

        pane_ele = AllplanGeo.Move(pane_ele, AllplanGeo.Vector3D(build_ele.FrameWidth.value,
                                                                 (build_ele.FrameThickness.value - build_ele.PaneThickness.value) / 2,
                                                                  build_ele.FrameWidth.value))

        model_ele_list.append_geometry_3d_with_texture(AllplanGeo.Transform(pane_ele, placement_mat),
                                                       AllplanBasisEle.TextureDefinition(build_ele.PaneSurface.value))

       #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return pyp_util.create_pythonpart(build_ele)

