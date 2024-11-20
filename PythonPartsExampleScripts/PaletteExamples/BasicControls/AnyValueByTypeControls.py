""" Example script for showing the usage of the AnyValueByType
"""

from __future__ import annotations

import re

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from AnyValueByType import AnyValueByType
from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from TypeCollections.ModelEleList import ModelEleList
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.AnyValueByTypeControlsBuildingElement import \
        AnyValueByTypeControlsBuildingElement as BuildingElement  # type: ignore
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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return AnyValueByTypeControls(build_ele, script_object_data)


class AnyValueByTypeControls(BaseScriptObject):
    """ Definition of class AnyValueByType
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

        self.build_ele = build_ele

    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        #--------------------- create the geometry

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(3000, 2000, 1000 if isinstance(build_ele.EditControl.value.value, str) else \
                                                       build_ele.EditControl.value.value)

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(polyhed)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    def on_control_event(self, event_id: int) -> bool:
        """ handle the event of pressing a button

        Args:
            event_id: event id of the event

        Returns:
            True if the palette should be updated
        """
        new_control = AnyValueByType(self.build_ele.NewControlValueType.value, self.build_ele.NewControlText.value)

        # set initial value with the correct type
        if new_control.value_type in {"Text", "String", "StringComboBox"}:
            new_control.value = ""
        elif new_control.value_type in {"Double", "Length", "Integer", "IntegerComboBox"}:
            new_control.value = 0
        else:
            new_control.value = False

        # in case of an IntegerComboBox, check the value list for matching pattern "1|2|3"
        integer_value_list_pattern = r"^(\d+\|)*\d+$"

        if new_control.value_type == "IntegerComboBox" and not re.match(integer_value_list_pattern, self.build_ele.NewControlValueList.value):
            AllplanUtil.ShowMessageBox("The value list must be a set of integers separated by '|', e.g. like: '1|2|3'", AllplanUtil.IDOK)
            return False

        # set the value list
        if "ComboBox" in new_control.value_type:
            new_control.value_list = self.build_ele.NewControlValueList.value

        # add or remove the control
        if event_id == self.build_ele.ADD_CONTROL_BEGINNING:
            self.build_ele.AnyValueByTypeList.value.insert(0, new_control)
        elif event_id == self.build_ele.ADD_CONTROL_END:
            self.build_ele.AnyValueByTypeList.value.append(new_control)
        elif event_id == self.build_ele.REMOVE_CONTROL and self.build_ele.AnyValueByTypeList.value:
            self.build_ele.AnyValueByTypeList.value.pop()

        return True
