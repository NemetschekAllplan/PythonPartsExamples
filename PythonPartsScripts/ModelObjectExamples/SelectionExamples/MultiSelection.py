"""Example script showing the implementation of an interactor PythonPart that asks the user
to select multiple elements. The purpose of this example is to show an implementation
of the multiple element selection funtionality using the InputFunctionStarter utility from
the NemAll_Python_IFW_Input module
"""
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
    from __BuildingElementStubFiles.MultiSelectionBuildingElement import MultiSelectionBuildingElement
else:
    MultiSelectionBuildingElement = BuildingElement


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
                      modify_uuid_list        : list[str]) -> MultipleSelectionInteractor:
    """Function for the interactor creation, called when PythonPart is initialized.

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

    return MultipleSelectionInteractor(coord_input,
                                       pyp_path,
                                       global_str_table_service,
                                       build_ele_list,
                                       build_ele_composite,
                                       control_props_list,
                                       modify_uuid_list)


class MultipleSelectionInteractor(BaseInteractor):
    """Implementation of the multiple selection interactor

    This interactor asks the user to select multiple elements in the viewport. The selection
    is done using the standard Allplan element selection: by clicking on element, drawing selection
    rectangle or by activating multiple selection with right-click. The selected elements and
    some basic information about them are printed in the trace.

    Attributes:
        build_ele:              building element with the properties from the property pallette
        document:               current document
        post_element_selection: object, where the result of the element selection is saved
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
        self.build_ele              = cast(MultiSelectionBuildingElement, build_ele_list[0])
        self.document               = coord_input.GetInputViewDocument()
        self.post_element_selection = AllplanIFW.PostElementSelection()

        # initialize needed services
        self.palette_service = BuildingElementPaletteService(build_ele_list,
                                                             build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list,  # type: ignore
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

        # reinitialize the running element selection to apply new settings from the property palette
        self.initialize_selection(remove_running_selection = True)

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

        elements = self.post_element_selection.GetSelectedElements(self.document)

        if len(elements) == 0:
            print("No elements selected")
            self.initialize_selection()
            return True

        # print some information about the selected elements in the trace
        print("\n" + "-" * 45 + " Selected elements " + "-" * 46 + "\n",
              f"\n{'Displayed name':<{25}}",
              f"{'Adapter type':<{35}}",
              f"{'Geometry type':<{15}}",
              f"{'Is 3D':<{7}}",
              f"{'Is general':<{15}}",
              f"{'Is label':<{10}}",
              "\n" + "-" * 110 + "\n")

        for element in elements:
            element_type = element.GetElementAdapterType()
            print(f"{element_type.GetDisplayName():<{25}}",
                  f"{element_type.GetTypeName():<{35}}",
                  f"{type(element.GetGeometry()).__name__:<{15}}",
                  f"{str(element_type.Is3DElement()):<{7}}",
                  f"{str(element.IsGeneralElement()):<{15}}",
                  f"{str(element.IsLabelElement()):<{10}}",
                  )
        print("-" * 110 + "\n")

        # reinitialize the selection
        self.initialize_selection()

        return True

    def on_cancel_function(self) -> bool:
        """ Called when ESC key is pressed.

        Returns:
            True when the PythonPart framework should terminate the PythonPart, False otherwise.
        """

        self.palette_service.close_palette()
        AllplanIFW.InputFunctionStarter.RemoveFunction()
        return True

    def initialize_selection(self, remove_running_selection: bool = False) -> None:
        """Initializes the input function for selecting multiple elements using InputFunctionStarter.
        Before initializing, it sets up needed filters, based on the values from the property palette:

        -   document filter
        -   layer filter

        Args:
            remove_running_selection:   set this option to True, if an already running selection function must
                                        be removed before the initialization
        """

        # set up the document and layer filters
        ele_select_filter = AllplanIFW.ElementSelectFilterSetting()
        ele_select_filter.SetDocumentSelectType(AllplanIFW.eDocumentSnoopType.names[self.build_ele.DocumentSnoopType.value])
        ele_select_filter.SetLayerSelectType(AllplanIFW.eLayerSnoopType.names[self.build_ele.LayerSnoopType.value])

        if remove_running_selection:
            AllplanIFW.InputFunctionStarter.RemoveFunction()

        AllplanIFW.InputFunctionStarter.StartElementSelect(
            text                 = "Select elements",
            selectSetting        = ele_select_filter,
            postSel              = self.post_element_selection,
            markSelectedElements = self.build_ele.MarkSelectedElements.value,
            selectionMode        = AllplanIFW.SelectionMode.names[self.build_ele.SelectionMode.value],
        )
