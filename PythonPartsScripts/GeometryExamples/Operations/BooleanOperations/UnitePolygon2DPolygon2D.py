""" Script for UnitePolygon2DPolygon2D
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

if TYPE_CHECKING:
    from __BuildingElementStubFiles.UnitePolygon2DPolygon2DBuildingElement \
        import UnitePolygon2DPolygon2DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load UnitePolygon2DPolygon2D.py')


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
                               r"Examples\PythonParts\GeometryExamples\BooleanOperations\UnitePolygon2DPolygon2D.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = UnitePolygon2DPolygon2D(doc)

    return element.create(build_ele)


class UnitePolygon2DPolygon2D():
    """ Definition of class UnitePolygon2DPolygon2D
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class UnitePolygon2DPolygon2D

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

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        polygon1 = AllplanGeo.Polygon2D.CreateRectangle(AllplanGeo.Point2D(), AllplanGeo.Point2D(*build_ele.Polygon1.value.Values()))

        polygon2 = AllplanGeo.Polygon2D.CreateRectangle(build_ele.PlacementPoint.value,
                                                        build_ele.PlacementPoint.value + build_ele.Polygon2.value)

        error, polygon = AllplanGeo.MakeUnion(polygon1, polygon2)

        if error == AllplanGeo.eOK:
            model_ele_list.append_geometry_2d(polygon)
        else:
            model_ele_list.set_stroke(2)
            model_ele_list.append_geometry_2d(polygon1)
            model_ele_list.append_geometry_2d(polygon2)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
