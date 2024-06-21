""" Script for UnitePolyhedronsWithVoid
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview

from TypeCollections import ModelEleList
from TypeCollections import PolyhedronTypesList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.UnitePolyhedronsWithVoidBuildingElement \
        import UnitePolyhedronsWithVoidBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load UnitePolyhedronsWithVoid.py')


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
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\GeometryExamples\BooleanOperations\UnitePolyhedronsWithVoid.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = UnitePolyhedronsWithVoid(doc)

    return element.create(build_ele)


class UnitePolyhedronsWithVoid():
    """ Definition of class UnitePolyhedronsWithVoid
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class UnitePolyhedronsWithVoid

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc

    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        #----------------- create the polyhedron

        sizes = build_ele.Polyhedron.value

        polyheds = PolyhedronTypesList([AllplanGeo.Polyhedron3D.CreateCuboid(*sizes.Values())])

        polyheds += [AllplanGeo.Move(polyheds[0], build_ele.Distance.value * index) for index in range(1, build_ele.Count.value)]

        wall_thickness = build_ele.WallThickness.value

        voids = PolyhedronTypesList([AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(wall_thickness, wall_thickness, 0),
                                                                          AllplanGeo.Point3D(sizes.X - wall_thickness,
                                                                                             sizes.Y - wall_thickness, sizes.Z))])

        voids += [AllplanGeo.Move(voids[0], build_ele.Distance.value * index) for index in range(1, build_ele.Count.value)]


        #----------------- create the union

        error, polyhed_union = AllplanGeo.MakeUnion(polyheds, voids)

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        if error == AllplanGeo.eOK:
            model_ele_list.append_geometry_3d(polyhed_union)

        else:
            model_ele_list.set_stroke(2)
            model_ele_list.set_color(6)

            model_ele_list.append_geometry_3d(polyheds)
            model_ele_list.append_geometry_3d(voids)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
