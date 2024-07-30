""" Script for ComboBoxControls
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from DocumentManager import DocumentManager
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ComboBoxControlsBuildingElement \
        import ComboBoxControlsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ComboBoxControls.py')


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
                               r"Examples\PythonParts\PaletteExamples\BasicControls\ComboBoxControls.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = ComboBoxControls(doc)

    return element.create(build_ele)


def modify_element_property(build_ele: BuildingElement,
                            name     : str,
                            value    : str):
    """ Modify property of element

    Args:
        build_ele: building element with the parameter properties
        name:      name of the modified property
        value:     new value
    """

    if name == build_ele.DrawingType.name:
        doc = DocumentManager.get_instance().document

        drawing_type = AllplanBaseEle.DrawingTypeService.GetDrawingTypeIdFromDescription(doc, value)

        AllplanBaseEle.DrawingTypeService.SetDrawingTypeId(drawing_type)


class ComboBoxControls():
    """ Definition of class ComboBoxControls
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class ComboBoxControls

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        if not build_ele.DrawingType.value:
            build_ele.DrawingType.value = AllplanBaseEle.DrawingTypeService.GetCurrentDrawingTypeDescription(self.document)

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        angle_cos = math.cos(math.radians(build_ele.Angle.value))
        angle_sin = math.sin(math.radians(build_ele.Angle.value))

        for length, coord in zip(build_ele.LineLength.value, build_ele.LineCoords.value):
            model_ele_list.append_geometry_2d(AllplanGeo.Line2D(coord[0], coord[1], coord[0] + length * angle_cos,
                                                                coord[1] + length * angle_sin))


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
