""" Script for TextDyn
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.TextDynBuildingElement \
        import TextDynBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load TextDyn.py')


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
                               r"Examples\PythonParts\PaletteExamples\OptionalTags\TextDyn.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = TextDyn(doc)

    return element.create(build_ele)


class TextDyn():
    """ Definition of class TextDyn
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class TextDyn

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

        start_pnt = AllplanGeo.Point2D()

        length =  build_ele.Dimension.value if build_ele.DistanceHeader.value == 1 else -build_ele.Dimension.value

        angle = math.radians(build_ele.Angle.value)

        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        for dist in build_ele.DistanceList.value:
            start_pnt.Y = dist

            end_pnt = AllplanGeo.Point2D(start_pnt.X + length + cos_angle, start_pnt.Y + length * sin_angle)

            model_ele_list.append_geometry_2d(AllplanGeo.Line2D(start_pnt, end_pnt))

            start_pnt.X = start_pnt.X + build_ele.Dimension.value


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
