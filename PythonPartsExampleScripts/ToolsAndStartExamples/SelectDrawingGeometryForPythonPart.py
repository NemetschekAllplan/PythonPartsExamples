"""
Script for SelectGeometryForPythonPart
"""

from typing import List, Any

import subprocess

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementPaletteService import BuildingElementPaletteService
from ControlProperties import ControlProperties
from StringTableService import StringTableService

from Utils.GeometryStringValueConverter import GeometryStringValueConverter


print('Load SelectGeometryForPythonPart.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : List[List[ControlProperties]],
                      _modify_uuid_list        : List[str]) -> Any :
    """
    Create the interactor

    Args:
        coord_input:               coordinate input
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            building element list
        build_ele_composite:       building element composite
        control_props_list         control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

    Returns:
        created interactor
    """

    return SelectGeometryForPythonPart(coord_input, build_ele_list, build_ele_composite,  control_props_list)


class SelectGeometryForPythonPart(BaseInteractor):
    """
    Definition of class SelectGeometryForPythonPart
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[List[ControlProperties]]):
        """
        Initialization of class SelectGeometryForPythonPart

        Args:
            coord_input:               coordinate input
            build_ele_list:            building element list
            build_ele_composite:       building element composite
            control_props_list         control properties list
        """

        self.coord_input = coord_input

        self.post_element_selection = None
        self.is_ref_point_sel       = False
        self.sel_elements           = []
        self.build_ele              = build_ele_list[0]

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             None, control_props_list, "")

        self.palette_service.show_palette("SelectGeometryForPythonPart")

        self.start_selection()


    def start_selection(self):
        """ start the selection """

        sel_query   = AllplanIFW.SelectionQuery()
        sel_setting = AllplanIFW.ElementSelectFilterSetting(sel_query, True)

        self.post_element_selection = AllplanIFW.PostElementSelection()

        AllplanIFW.InputFunctionStarter.StartElementSelect("Select the geometry objects", sel_setting, self.post_element_selection, True)


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_control_event(self, event_id: int):
        """
        Handles the on control event

        Args:
            event_id: event id of button control.
        """


    def on_value_input_control_enter(self) -> bool:
        """
        Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return False


    def on_cancel_function(self) -> bool:
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        if self.post_element_selection:
            AllplanIFW.InputFunctionStarter.RemoveFunction()

        return True


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        self.palette_service.modify_element_property(page, name, value)


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        #----------------- get the elements and start the reference point input

        if self.post_element_selection:
            sel_elements = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())

            if not sel_elements:
                self.start_selection()

                return True

            for ele in sel_elements:
                parent_ele = AllplanElementAdapter.BaseElementAdapterParentElementService.GetParentElement(ele)

                if parent_ele == AllplanElementAdapter.ElementGroup_TypeUUID:
                    self.sel_elements += AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(parent_ele)
                else:
                    self.sel_elements.append(ele)

            self.post_element_selection = None

            self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("Select the reference point"))


        #----------------- get the reference point

        ref_point = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        #----------------- get the geometry data as string

        ref_pnt_vec    = AllplanGeo.Vector3D(ref_point, AllplanGeo.Point3D())
        ref_pnt_vec_2d = AllplanGeo.Vector2D(ref_pnt_vec)

        sel_geo_str = []

        for ele in self.sel_elements:
            geo_elements = ele.GetModelGeometry()

            if not isinstance(geo_elements, list):
                geo_elements = [geo_elements]

            for geo_ele in geo_elements:
                if str(type(geo_ele)).find("2D") != -1:
                    geo_ele = AllplanGeo.Move(geo_ele, ref_pnt_vec_2d)
                else:
                    geo_ele = AllplanGeo.Move(geo_ele, ref_pnt_vec)

                sel_geo_str.append(GeometryStringValueConverter.to_string(geo_ele))


        #----------------- copy to the clipboard

        indent = " " * self.build_ele.Indent.value

        text = "\n" + indent + "geo_ele_strings = [\"" + ("\",\n                   " + indent + "\"").join(sel_geo_str) + "\"]\n\n"

        text += indent + "geo_elements = GeometryStringValueConverter.get_elements(geo_ele_strings, False)\n\n"

        if text:
            subprocess.run(['clip.exe'], input = text.encode("UTF-16"), check = True)

            AllplanUtil.ShowMessageBox("The created string is copied to the clipboard", AllplanUtil.MB_OK)

        self.sel_elements = []

        self.start_selection()

        return True
