""" A template script for creating an interactor PythonPart
"""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.EventsBuildingElement import EventsBuildingElement
else:
    EventsBuildingElement = BuildingElement

print("Loaded Events.py")

def check_allplan_version(build_ele: BuildingElement,
                          version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        build_ele: building element with the parameter properties
        version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True

def migrate_parameter(parameter_list: list,
                      version: float) -> None:
    """Migrate the parameter

    This function is called only during the modification of a PythonPart

        Args:
            parameter_list: parameter list
            version:        current PythonPart version
    """

def create_preview(build_ele:   BuildingElement,
                   doc:         AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Create the library preview

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """
    return CreateElementResult(elements=[...])

def create_interactor(coord_input:                 AllplanIFWInput.CoordinateInput,
                      pyp_path:                    str,
                      global_str_table_service:    StringTableService,
                      build_ele_list:              list[BuildingElement],
                      build_ele_composite:         BuildingElementComposite,
                      control_props_list:          list[BuildingElementControlProperties],
                      modify_uuid_list:            list[str]) -> "Interactor":
    """Function for the interactor creation, called when PythonPart is initialized.
    When called, the PythonPart framework performs the following steps:

    - reads the parameters and their values from the xxx.pyp file and stores them in the buld_ele_list
    - if tag `ReadLastInput` is set to True: read the parameter values from the last input,
        (stored in ...\\Usr\\_user_name_\\tmp\\_python_part_name.pyv) and assign them to the parameters
        in build_ele_list
    - if starting an input by Match from the context menu or double right click: read the parameter
        values from the attribute @611@ of the matched PythonPart and assign them to the parameters
        in build_ele_list
    - if in modification mode: read the parameter values from the attribute @611@ of the selected
        PythonPart and assign them to the parameters in build_ele_list

    Args:
        coord_input:               coordinate input
        pyp_path:                  path of the pyp file
        global_str_table_service:  global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        modify_uuid_list:          UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return Interactor(coord_input, pyp_path, global_str_table_service, build_ele_list,
                      build_ele_composite, control_props_list, modify_uuid_list)


class Interactor(BaseInteractor):
    """ Implementation of a PythonPart interactor that prints the currently triggered event.

    The purpose of this example interactor is to give an overview, what events are triggered
    (and can be handled inside an Interactor), when a user takes a certain action in Allplan GUI
    during the runtime of the PyhtonPart, like e.g. changing a page f the property palette
    """

    def __init__(self,
                 coord_input             : AllplanIFWInput.CoordinateInput,
                 pyp_path                : str,
                 global_str_table_service: StringTableService,
                 build_ele_list          : list[BuildingElement],
                 build_ele_composite     : BuildingElementComposite,
                 control_props_list      : list[BuildingElementControlProperties],
                 modify_uuid_list        : list[str])                            :
        """Initialize the interactor"""

        self.build_ele = cast(EventsBuildingElement,build_ele_list[0])
        self.esc_pressed = False
        input_control_data = AllplanIFWInput.ValueInputControlData(AllplanIFWInput.eValueInputControlType.eTEXT_EDIT,
                                                                   bDisableCoord= False)

        coord_input.InitFirstPointValueInput(AllplanIFWInput.InputStringConvert("See infos printed in trace"),
                                             input_control_data)

        self.palette_service = BuildingElementPaletteService(build_ele_list,
                                                             build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list,
                                                             self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)

        print("=====================  Interactor initialized  =====================")

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """Handle the event of changing an element property in the property palette

        Args:
            page:   Page of the modified property
            name:   Name of the modified property.
            value:  New value of the modified property.
        """
        self.palette_service.modify_element_property(page,name,value)
        self.palette_service.update_palette(-1,False)

        print("\n\n------------  modify_element_property  ------------")
        print(f"page:\t\t\t{page}")
        print(f"name:\t\t\t{name}")
        print(f"value:\t\t\t{value}")
        self.print_current_time()

    def set_active_palette_page_index(self, active_page_index: int) -> None:
        """Handle the event of changing the tab of the property palette

        Args:
            active_page_index: index of the switched page, starting from 0
        """
        print("\n\n------------  set_active_palette_page  ------------")
        print(f"active_page_index:\t{active_page_index}")
        self.print_current_time()

    def on_control_event(self, event_id: int):
        """Handle the event of hitting a button in the property palette

        Args:
            event_id:   id of the event assigned to the button in the tag EventId
        """
        print("\n\n----------------  on_control_event  ----------------")
        print(f"event_id:\t\t{event_id}")
        self.print_current_time()

    def on_mouse_leave(self):
        """ Handle the event of mouse leaving the viewport."""

        if self.build_ele.PrintOnMouseLeave.value:
            print("\n\n-----------------  on_mouse_leave  -----------------")
            self.print_current_time()

    def on_preview_draw(self):
        """ Handles the preview draw event.

        This event is triggered e.g., when an input in the dialog line is done (e.g. input of a coordinate).
        """
        if self.build_ele.PrintOnPreviewDraw.value:
            print("\n\n----------------  on_preview_draw  ----------------")
            self.print_current_time()

    def on_value_input_control_enter(self) -> bool:
        """ Handle the event of hitting the enter key during the input in the dialog line.

        Returns:
            True/False for success.
        """
        print("\n\n----------  on_value_input_control_enter  ----------")
        self.print_current_time()
        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeometry.Point2D,
                          msg_info : AllplanIFWInput.AddMsgInfo) -> bool:
        """ Handle the event of mouse sending a message (being moves, clicked, etc...)

        Args:
            mouse_msg:  The mouse message.
            pnt:        The input point in view coordinates. The origin is the mid point of the viewport
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """
        if self.build_ele.PrintProcessMouseMsg.value:
            print("\n\n---------------  process_mouse_msg  ---------------")
            print(f"mouse_msg:\t\t{mouse_msg}")
            print(f"pnt:\t\t\t{pnt}")
            self.print_current_time()

        return True

    def on_shortcut_control_input(self,
                                  value: int) -> bool:
        print("\n\n-----------  on_shortcut_control_input  -----------")
        print(f"value:\t\t{value}")
        self.print_current_time()

        return True

    def execute_save_favorite(self,
                              file_name: str) -> None:
        print("\n\n-------------  execute_save_favorite  -------------")
        print(f"file_name:\t\t{file_name}")
        self.print_current_time()

    def execute_load_favorite(self,
                              file_name: str) -> None:
        print("\n\n-------------  execute_load_favorite  -------------")
        print(f"file_name:\t\t{file_name}")
        self.print_current_time()

    def reset_param_values(self,
                           build_ele_list: list[BuildingElement]) -> None:

        print("\n\n--------------  reset_param_values  --------------")
        print(f"build_ele:\t\t{build_ele_list[0]}")
        self.print_current_time()

    def update_after_favorite_read(self) -> None:
        print("\n\n--------  update_after_favorite_file_read  --------")

    def on_cancel_by_menu_function(self) -> None:
        print("\n\n----------  on_cancel_by_menu_function  ----------")

        self.palette_service.close_palette()
        print("\n==================  Interactor terminated  ===================\n")

    def on_cancel_function(self) -> bool:
        print("\n\n----------  on_cancel_function  ----------")

        if self.esc_pressed:
            print("\n==================  Interactor terminated  ===================\n")
            self.palette_service.close_palette()
            return True

        self.esc_pressed = True
        print("Press ESC again to close the PythonPart")
        return False

    @staticmethod
    def print_current_time() -> None:
        current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
        print(f"triggered at:\t\t{current_time}")
