""" Example Script for room modification
"""

from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, cast

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HideElementsService import HideElementsService
from Utils import ElementPropertiesAttributeUtil

from AttributeIdValue import AttributeIdValue

import Utilities.AttributeIdEnums as AttrEnum

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyRoomBuildingElement import ModifyRoomBuildingElement
else:
    ModifyRoomBuildingElement = BuildingElement

print('Load ModifyRoom.py')

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

    script_path = Path(_build_ele.pyp_file_path) / Path(_build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")
    preview = LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path))

    return CreateElementResult(preview)


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifyRoom(build_ele, script_object_data)


class ModifyRoom(BaseScriptObject):
    """ Definition of class ModifyRoom
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

        self.build_ele = cast(ModifyRoomBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.room_sel_result          = SingleElementSelectResult()
        self.build_ele                = cast(ModifyRoomBuildingElement, build_ele)
        self.hide_ele_service         = HideElementsService()
        self.room_element             = AllplanArchEle.RoomElement
        self.reverse_offset_direction = False
        self.polygon                  = AllplanGeo.Polygon2D()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.room_sel_result,
                                                                      [AllplanEleAdapter.Room_TypeUUID],
                                                                      "Select the room")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.ROOM_SELECTED

        #----------------- get the slab element

        self.room_element = cast(AllplanArchEle.RoomElement, AllplanBaseEle.GetElement(self.room_sel_result.sel_element))

        self.polygon       = self.room_element.GetGeometryObject()

        #----------------- get the properties
        room_props = self.room_element.Properties

        #----------------- get the default attributes
        usr_attr = self.build_ele.UserAttributes.value
   
        room_attr = {AttrEnum.AttributeIdEnums.FACTOR, AttrEnum.AttributeIdEnums.LOCAL_CODE_STORY_NAME, AttrEnum.AttributeIdEnums.TEXT1, 
                     AttrEnum.AttributeIdEnums.TEXT2, AttrEnum.AttributeIdEnums.TEXT3, AttrEnum.AttributeIdEnums.TEXT4, AttrEnum.AttributeIdEnums.TEXT5, 
                     AttrEnum.AttributeIdEnums.FUNCTION, AttrEnum.AttributeIdEnums.NAME}

        fav_attr = {attr.attribute_id for attr in usr_attr}

        for attr_id, attr_value in room_props.GetAttributes(self.document, True):
            if attr_id not in room_attr and attr_id not in fav_attr:
                usr_attr.insert(-1, AttributeIdValue(attr_id, attr_value))

        build_ele.PlaneReferences.value = room_props.PlaneReferences

        #----------------- loop through tiers and assign new list
        build_ele.CommonProp.value = room_props.CommonProperties
        build_ele.StoreyCode.value = room_props.StoreyCode
        build_ele.Name.value       = room_props.Name
        build_ele.Function.value   = room_props.Function
        build_ele.Factor.value     = room_props.Factor

        for index in range(5):
            build_ele.Texts.value[index] = room_props.GetText(index)


        self.hide_ele_service.hide_element(self.room_sel_result.sel_element)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_room_element(),[],
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def create_room_element(self) -> ModelEleList:
        """ create the slab element


        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        #----------------- create the properties
        room_props                          = AllplanArchEle.RoomProperties()
        room_props.PlaneReferences          = build_ele.PlaneReferences.value

        ElementPropertiesAttributeUtil.set_attributes(self.document,room_props, build_ele.UserAttributes.value)

        room_props.CommonProperties = build_ele.CommonProp.value
        room_props.StoreyCode       = build_ele.StoreyCode.value
        room_props.Name             = build_ele.Name.value
        room_props.Function         = build_ele.Function.value
        room_props.Factor           = build_ele.Factor.value

        for index, text in enumerate(build_ele.Texts.value):
            room_props.SetText(text, index + 1)

        self.room_element.Properties = room_props
    
        #----------------- create the element

        model_ele_list = ModelEleList()

        model_ele_list.append(self.room_element)

        return model_ele_list


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value == self.build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        self.hide_ele_service.show_elements()

        if self.room_sel_result != SingleElementSelectResult():
            AllplanBaseEle.ModifyElements(self.document, self.create_room_element())

        return OnCancelFunctionResult.RESTART
