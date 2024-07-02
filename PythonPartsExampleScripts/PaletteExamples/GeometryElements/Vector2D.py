""" Script for Vector2D geometry example
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
    from __BuildingElementStubFiles.Vector2DBuildingElement import Vector2DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Vector2D.py')


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
                               r"Examples\PythonParts\PaletteExamples\GeometryElements\Vector2D.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = Vector2D(doc)

    return element.create(build_ele)


class Vector2D():
    """ Definition of class Vector2D
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class Vector2D

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

        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(AllplanGeo.Point2D() + build_ele.Vector1.value,
                                                            AllplanGeo.Point2D() + build_ele.Vector2.value))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(AllplanGeo.Point2D(3000, 2000),
                                                            AllplanGeo.Point2D(3000, 2000) + build_ele.Sizes.value))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(AllplanGeo.Point2D(5000, 0) + build_ele.StartVector.value,
                                                            AllplanGeo.Point2D(5000, 0) + build_ele.EndVector.value))
        model_ele_list.append_geometry_2d(AllplanGeo.Polyline2D(
            [AllplanGeo.Point2D(2000, 0) + vector for vector in build_ele.VectorList.value]))


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
