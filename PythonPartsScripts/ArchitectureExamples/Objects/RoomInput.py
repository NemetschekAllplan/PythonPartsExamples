""" Script for RoomInput
"""

from __future__ import annotations

from typing import Any, List, TYPE_CHECKING, cast

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_AllplanSettings as AllplanSettings

from AttributeIdValue import AttributeIdValue
from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

from Utils import LibraryBitmapPreview, ElementPropertiesAttributeUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.RoomInputBuildingElement import RoomInputBuildingElement
else:
    RoomInputBuildingElement = BuildingElement

print('Load RoomInput.py')


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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\RoomInput.png"))

def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : List[BuildingElementControlProperties],
                      _modify_uuid_list        : list) -> object:
    """ Create the interactor

    Args:
        coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            list with the building elements
        build_ele_composite:       building element composite with the building element constraints
        control_props_list:        control properties list
        _modify_uuid_list:         list with the UUIDs of the modified elements

    Returns:
          Created interactor object
    """

    return RoomInput(coord_input, build_ele_list, build_ele_composite, control_props_list)


class RoomInput(BaseInteractor):
    """ Definition of class RoomInput
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:         API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list:      list with the building elements
            build_ele_composite: building element composite with the building element constraints
            control_props_list:  control properties list
        """

        self.build_ele_list = build_ele_list
        self.build_ele      = cast(RoomInputBuildingElement, build_ele_list[0])
        self.polygon_input  = AllplanIFW.PolygonInput(coord_input, False, True)
        self.room_prop      = AllplanArchEle.RoomProperties()


        #----------------- get the default attributes

        usr_attr = self.build_ele.UserAttributes.value

        room_attr = {230, 246, 501, 502, 503, 504, 505, 506, 507}

        fav_attr = {attr.attribute_id for attr in usr_attr}

        for attr_id, attr_value in self.room_prop.GetAttributes(coord_input.GetInputViewDocument(), True):
            if attr_id not in room_attr and attr_id not in fav_attr:
                usr_attr.insert(-1, AttributeIdValue(attr_id, attr_value))


        #----------------- create the palette

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: str):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

        self.draw_preview(self.polygon_input.GetPolygon())


    def on_control_event(self,
                         event_id: int):
        """ Handles on control event

        Args:
            event_id: event id of the clicked button control
        """

    def on_cancel_function(self) -> bool:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False for success.
        """

        _, room_polygon = AllplanGeo.ConvertTo2D(self.polygon_input.GetPolygon())

        if not room_polygon.IsValid():
            self.palette_service.close_palette()

            return True

        build_ele = self.build_ele
        room_prop = self.room_prop

        room_prop.StoreyCode      = build_ele.StoreyCode.value
        room_prop.Name            = build_ele.Name.value
        room_prop.Function        = build_ele.Function.value
        room_prop.Factor          = build_ele.Factor.value

        for index, text in enumerate(build_ele.Texts.value):
            room_prop.SetText(text, index + 1)

        ElementPropertiesAttributeUtil.set_attributes(self.polygon_input.GetActiveViewDocument(),
                                                      room_prop, build_ele.UserAttributes.value)

        room_ele = AllplanArchEle.RoomElement(room_prop, room_polygon)

        room_ele.CommonProperties = build_ele.CommonProp.value

        AllplanBaseEle.CreateElements(self.polygon_input.GetInputViewDocument(),
                                      AllplanGeo.Matrix3D(), [room_ele], [], None)

        self.polygon_input.StartNewInput()

        return False

    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        self.draw_preview(self.polygon_input.GetPreviewPolygon())

    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.draw_preview(self.polygon_input.GetPolygon())

    def on_value_input_control_enter(self) -> bool:
        """ Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Process the mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        self.polygon_input.ExecuteInput(mouse_msg, pnt, msg_info)

        self.draw_preview(self.polygon_input.GetPreviewPolygon())

        return True


    def draw_preview(self,
                     polygon: AllplanGeo.Polygon3D):
        """ draw the preview

        Args:
            polygon: input polygon
        """

        build_ele = self.build_ele

        result, room_polygon = AllplanGeo.ConvertTo2D(polygon)

        if not result:
            AllplanBaseEle.DrawElementPreview(self.polygon_input.GetInputViewDocument(),
                                              AllplanGeo.Matrix3D(),
                                              [AllplanBasisEle.ModelElement3D(build_ele.CommonProp.value, polygon)],
                                              True, None)

            return

        self.room_prop.PlaneReferences  = build_ele.PlaneReferences.value

        room_ele = AllplanArchEle.RoomElement(self.room_prop, room_polygon)

        room_ele.CommonProperties = build_ele.CommonProp.value

        AllplanBaseEle.DrawElementPreview(self.polygon_input.GetInputViewDocument(),
                                          AllplanGeo.Matrix3D(), [room_ele], True, None)


    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
