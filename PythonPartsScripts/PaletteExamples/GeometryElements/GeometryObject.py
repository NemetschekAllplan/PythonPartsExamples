""" Script for GeometryObject geometry example
"""

from __future__ import annotations

from typing import TYPE_CHECKING, get_args

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections.ModelEleList import ModelEleList, ModelEle2D

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeometryObjectBuildingElement import GeometryObjectBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load GeometryObject.py')


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
                               r"Examples\PythonParts\PaletteExamples\GeometryElements\GeometryObject.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = GeometryObject(doc)

    return element.create(build_ele)


class GeometryObject():
    """ Definition of class GeometryObject
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class GeometryObject

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

        model_ele_list.append_geometry_3d(build_ele.GeometryObject.value)

        for geo_ele in build_ele.GeometryObjectList.value:
            if isinstance(geo_ele, get_args(ModelEle2D)):
                model_ele_list.append_geometry_2d(geo_ele)
            else:
                model_ele_list.append_geometry_3d(geo_ele)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
