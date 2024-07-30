"""Module containing base classes used by the examples in the sub directories"""
from typing import Any, List, Union

import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementPaletteService import BuildingElementPaletteService
from ControlProperties import ControlProperties


class OperationExampleBaseInteractor(BaseInteractor):
    """Operation example base interactor is a base class used by the interactors
    in the example scripts in the GeometryExamples/Operations. the purpose of
    this class is solely to reduce the size of the example scripts and improve
    the readability of their source code by gathering all the common methods
    inside this base class.

    Attributes:
        coord_input:            coordinate input
        post_element_selection: object containing selected elements after successful selection
        palette_service:        service class for the property palette
    """

    def __init__(self,
                 coord_input        : AllplanIFWInput.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[ControlProperties]):
        """ Constructor

        Args:
            coord_input        : coordinate input
            build_ele_list     : list with the building elements containing parameter properties
            build_ele_composite: building element composite
            control_props_list : control properties list
        """

        #set initial values
        self.coord_input            = coord_input
        self.post_element_selection = None

        #start necessary services
        self.palette_service = BuildingElementPaletteService(build_ele_list,
                                                             build_ele_composite,
                                                             build_ele_list[0].script_name,
                                                             control_props_list,
                                                             build_ele_list[0].pyp_file_name)

        # show the palette
        self.palette_service.show_palette(build_ele_list[0].pyp_file_name)


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

    def on_control_event(self,
                         event_id: int) -> None:
        """ Called when an event is triggered by a palette control (ex. button)

        Args:
            event_id:   id of the triggered event, defined in the tag `<EventId>`
        """
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
        self.palette_service.update_palette(-1, False)


    def on_cancel_function(self) -> bool:
        """ Called when ESC key is pressed.

        Returns:
            True when the PythonPart framework should terminate the PythonPart, False otherwise.
        """
        self.palette_service.close_palette()
        return True


    def on_cancel_by_menu_function(self) -> None:
        """ Called when the user has started another menu function during the runtime of
        the PythonPart. The PythonPart will always be terminated after this function is completed.
        """
        self.palette_service.close_palette()


    def start_geometry_selection(self,
                                 prompt_msg: str,
                                 whitelist : Union[None, List[type]] = None) -> None:
        """Starts the geometry element selection.

        Args:
            prompt_msg:             message displayed in the dialog line in Allplan
            whitelist (optional):   list of geometry types to be filtered
        """
        class GeometryFilter():
            """ Implementation of the geometry filter

            It filters only model objects with a geometry represented by a the geometry
            types specified in the whitelist. If no whitelist is specified, only general objects
            are accepted (e.g., no architecture objects)
            """

            def __call__(self, element: AllplanElementAdapter.BaseElementAdapter) -> bool:
                """ Execute the filtering

                Args:
                    element: element adapter to filter

                Returns:
                    True, when element adapter's geometry is in the whitelist
                """
                # whitelist of the geometry types
                if whitelist is None:
                    return element.IsGeneralElement()

                return type(element.GetGeometry()) in whitelist

        sel_query   = AllplanIFWInput.SelectionQuery([GeometryFilter()])
        sel_setting = AllplanIFWInput.ElementSelectFilterSetting(filter            = sel_query,
                                                                 bSnoopAllElements = False)

        self.post_element_selection = AllplanIFWInput.PostElementSelection()

        AllplanIFWInput.InputFunctionStarter.StartElementSelect(text                 = prompt_msg,
                                                                selectSetting        = sel_setting,
                                                                postSel              = self.post_element_selection,
                                                                markSelectedElements = True,
                                                                selectionMode        = AllplanIFWInput.SelectionMode.eSelectGeometry)

    def start_point_input(self, prompt_msg: str) -> None:
        """Starts the coordinate input

        Args:
            prompt_msg:     message displayed in the dialog line in Allplan
        """
        input_str = AllplanIFWInput.InputStringConvert(prompt_msg)
        input_mode = AllplanIFWInput.CoordinateInputMode()

        self.coord_input.InitFirstPointInput(input_str, input_mode)
