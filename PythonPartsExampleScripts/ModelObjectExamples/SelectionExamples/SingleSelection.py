"""Example script showing the implementation of an interactor PythonPart that prompts the user
to select a single element. The purpose of this script is to show different element
search methods of the Allplan Interactor Framework (Allplan_IFW) as well as different
filtering options, this framework offers"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_Input as AllplanIFW
from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from StringTableService import StringTableService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SingleSelectionBuildingElement import SingleSelectionBuildingElement
else:
    SingleSelectionBuildingElement = BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties],
                      modify_uuid_list        : list[str]) -> SingleSelectionInteractor:
    """Function for the interactor creation, called when PythonPart is initialized.
    When called, the PythonPart framework performs the following steps:

    -   reads the parameters and their values from the xxx.pyp file and stores them in the build_ele_list
    -   if tag `ReadLastInput` is set to True: read the parameter values from the last input,
        (stored in ...\\Usr\\_user_name_\\tmp\\_python_part_name.pyv) and assign them to the parameters
        in build_ele_list
    -   if starting an input by Match from the context menu or double right click: read the parameter
        values from the attribute @611@ of the matched PythonPart and assign them to the parameters
        in build_ele_list
    -   if in modification mode: read the parameter values from the attribute @611@ of the selected
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

    return SingleSelectionInteractor(coord_input,
                                     pyp_path,
                                     global_str_table_service,
                                     build_ele_list,
                                     build_ele_composite,
                                     control_props_list,
                                     modify_uuid_list)


class SingleSelectionInteractor(BaseInteractor):
    """Implementation of the single selection interactor

    This interactor prompts the user to select an element in the viewport. The selection
    result is just printed in the trace. Depending on the selected options in the
    property palette, the interactor searches for an element or for a geometry. Beside that,
    optionally a point search can be performed.

    Attributes:
        build_ele:      building element with the properties from the property pallette
        coord_input:    API object representing the coordinate input and element selection
                        in the Allplan viewport
    """

    def __init__(self,
                 coord_input              : AllplanIFW.CoordinateInput,
                 _pyp_path                : str,
                 _global_str_table_service: StringTableService,
                 build_ele_list           : list[BuildingElement],
                 build_ele_composite      : BuildingElementComposite,
                 control_props_list       : list[BuildingElementControlProperties],
                 _modify_uuid_list        : list[str])                :
        """ Constructor

        Args:
            coord_input:               coordinate input
            _pyp_path:                 path of the pyp file
            _global_str_table_service: global string table service for default strings
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
            _modify_uuid_list:         UUIDs of the existing elements in the modification mode
        """
        # set initial values
        self.build_ele   = cast(SingleSelectionBuildingElement,build_ele_list[0])
        self.coord_input = coord_input

        # initialize needed services
        self.palette_service = BuildingElementPaletteService(build_ele_list,
                                                             build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list,                #type: ignore
                                                             self.build_ele.pyp_file_name)

        # show palette and start input
        self.palette_service.show_palette(self.build_ele.pyp_file_name)
        self.initialize_selection()

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any) -> None:
        """ Called after each property modification in the property palette

        Args:
            page:   index of the page, beginning with 0
            name:   name of the modified property
            value:  new property value
        """
        self.palette_service.modify_element_property(page, name, value)

        # allow selection in the wizard window
        if name == "EnableAssistWndClick":
            self.coord_input.EnableAssistWndClick(value)
            print("Selection in wizard window " + ("activated" if value else "deactivated"))

        # if the option SelectAlways is active, set the checkbox also at the option AllowCenter
        elif name == "SelectAlways" and value:
            self.build_ele.AllowCenter.value = True

        # reinitialize the element selection after each modification in property palette
        self.initialize_selection()

        self.palette_service.update_palette(page, False)

    def on_control_event(self, event_id: int) -> None:
        """ Called when an event is triggered by a palette control (ex. button)

        Args:
            event_id:   id of the triggered event, defined in the tag `<EventId>`
        """

    def on_mouse_leave(self) -> None:
        """ Called when the mouse leaves the viewport window """

    def on_preview_draw(self) -> None:
        """ Called when an input in the dialog line is done (e.g. input of a coordinate)."""

    def on_value_input_control_enter(self) -> bool:
        """Called when enter key is pressed inside the value input control

        Returns:
            True/False for success.
        """

        print("-----------------New value in the dialog line----------------------",
              f"{'Input control integer value:' :<{30}}{self.coord_input.GetInputControlIntValue()}",
              f"{'Input control value:'         :<{30}}{self.coord_input.GetInputControlValue()}",
              f"{'Input control text:'          :<{30}}{self.coord_input.GetInputControlText()}",
              "--------------------------------------------------------------------",
              "\n",
              sep="\n")

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeometry.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """ Method called on each mouse movement, button click or release.

        Args:
            mouse_msg:  the mouse message (e.g. 512 - mouse movement)
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """
        # perform the element search or geometry search, depending on the option selected in the property palette
        if self.build_ele.ElementSearchType.value == "ElementSearch":
            ele_found = self.coord_input.SelectElement(mouse_msg,
                                                       pnt,
                                                       msg_info,
                                                       self.build_ele.HighlightElements.value,
                                                       self.build_ele.SelectAlways.value,
                                                       self.build_ele.AllowCenter.value)
        else:
            AllplanIFW.HighlightService.CancelAllHighlightedElements(self.coord_input.GetInputViewDocumentID())
            ele_found = self.coord_input.SelectGeometryElement(mouse_msg, pnt, msg_info,
                                                               self.build_ele.HighlightCompleteElement.value)

        # perform point search when the corresponding option is set in the palette
        coord_input_result = self.coord_input.GetInputPoint(mouse_msg,
                                                            pnt,
                                                            msg_info) if self.build_ele.PointSearch.value else None

        # return, if mouse was only moved or no element was found
        if self.coord_input.IsMouseMove(mouse_msg) or not ele_found:
            return True

        # read the found element
        selected_element     = self.coord_input.GetSelectedElement()
        selected_geo_element = self.coord_input.GetSelectedGeometryElement()

        # print some data of the selected element
        print("--------------------------Selected element-------------------------")
        print(f"{'Selected element:' :<{30}}{selected_element.GetDisplayName() if ele_found else 'no element found'}",
              f"{'Selected geometry element:':<{30}}{type(selected_geo_element).__name__}",
              f"{'Input point:' :<{30}}{coord_input_result.GetPoint() if coord_input_result is not None else 'no point found'}",
              "-------------------------------------------------------------------",
              "\n",
              sep="\n")

        # reinitialize the input after each element selection
        self.initialize_selection()

        return True

    def on_cancel_function(self) -> bool:
        """ Called when ESC key is pressed.

        Returns:
            True when the PythonPart framework should terminate the PythonPart, False otherwise.
        """

        self.palette_service.close_palette()

        return True


    def on_shortcut_control_input(self,
                                  value: int) -> bool:
        """ Handles the input inside the shortcut control

        Args:
            value: shortcut value

        Returns:
            True/False for success.
        """

        print("-----------------Shortcut input----------------")
        print(f"value ={value}")

        return True


    def on_input_undo(self) -> bool:
        """ Process the input undo event

        Returns:
            message was processed: True/False
        """

        print("-----------------Undo select----------------")

        return False


    def initialize_selection(self) -> None:
        """Initialize the element input. Depending on the option set in the property palette, with or without
        an additional input control in the dialog line.

        After the initialization, following selection filters are set:
        -   Document filter
        -   Layer filter
        -   ElementFilter or GeometryElementFilter, depending on the selected type of element search
            (element search or geometry search respectively)
        """

        # initialize the element input with an additional input control in the dialog line
        if self.build_ele.EnableInputControl.value:
            prompt_txt = AllplanIFW.InputStringConvert("Select the element; input value:")

            input_control_type = AllplanIFW.eValueInputControlType.names[self.build_ele.InputControlType.value]

            if input_control_type == AllplanIFW.eValueInputControlType.eINT_COMBOBOX:
                input_control = AllplanIFW.ValueInputControlData(input_control_type,
                                                                 3, 1, 10,
                                                                 bSetFocus     = False,
                                                                 bDisableCoord = False)
            else:
                input_control = AllplanIFW.ValueInputControlData(input_control_type,
                                                                 bSetFocus     = False,
                                                                 bDisableCoord = False)

            self.coord_input.InitFirstElementValueInput(prompt_txt, input_control)

        # initialize the element input with just a prompt in the dialog line
        else:
            prompt_txt = AllplanIFW.InputStringConvert("Select the element")
            self.coord_input.InitFirstElementInput(prompt_txt)

        # set up the document and layer filters
        ele_select_filter = AllplanIFW.ElementSelectFilterSetting()
        ele_select_filter.SetDocumentSelectType(AllplanIFW.eDocumentSnoopType.names[self.build_ele.DocumentSnoopType.value])
        ele_select_filter.SetLayerSelectType(AllplanIFW.eLayerSnoopType.names[self.build_ele.LayerSnoopType.value])

        # set up the element filter (relevant only for CoordinateInput.SelectElement)
        if self.build_ele.ElementSearchType.value == "ElementSearch":
            self.coord_input.SetElementFilter(ele_select_filter)

        # set up the snoop geometry filter (relevant only for CoordinateInput.SelectGeometryElement
        elif self.build_ele.ElementSearchType.value == "ElementGemetrySearch":
            self.coord_input.SetGeometryElementFilter(ele_select_filter)
