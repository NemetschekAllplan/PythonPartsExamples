""" Example script for showing the usage of the AnyValueByType
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from AnyValueByType import AnyValueByType
from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.AnyValueByTypeBuildingElement import AnyValueByTypeBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


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
                               r"Examples\PythonParts\PaletteExamples\BasicControls\AnyValueByTypeControls.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return AnyValueByTypeControls(build_ele, coord_input)


class AnyValueByTypeControls(BaseScriptObject):
    """ Definition of class AnyValueByType
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele


        #--------------------- set the data

        if not (value := build_ele.AnyValueByTypeList.value):
            value.append(AnyValueByType("Integer", "Integer value", 1, min_value = "0"))
            value.append(AnyValueByType("Double", "Double value", 1.5, max_value = "10"))
            value.append(AnyValueByType("Length", "Length value", 2000))
            value.append(AnyValueByType("CheckBox", "Checkbox", False))
            value.append(AnyValueByType("StringComboBox", "Language", "German", "German|English|French|Italian"))


        #--------------------- create the geometry

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(3000, 2000, 1000 if isinstance(build_ele.EditControl.value.value, str) else \
                                                       build_ele.EditControl.value.value)

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(polyhed)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
