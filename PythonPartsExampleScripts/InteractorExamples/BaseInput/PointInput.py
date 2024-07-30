"""Example script showing the functionality of coordinate input of the Allplan
Interactor Framework"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_Input as AllplanIFW
from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from StringTableService import StringTableService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PointInputBuildingElement import PointInputBuildingElement
else:
    PointInputBuildingElement = BuildingElement


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


def create_interactor(coord_input: AllplanIFW.CoordinateInput,
                      pyp_path: str,
                      global_str_table_service: StringTableService,
                      build_ele_list: list[BuildingElement],
                      build_ele_composite: BuildingElementComposite,
                      control_props_list: list[BuildingElementControlProperties],
                      modify_uuid_list: list[str]) -> ...:
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

    return PointInputInteractor(coord_input,
                                pyp_path,
                                global_str_table_service,
                                build_ele_list,
                                build_ele_composite,
                                control_props_list,
                                modify_uuid_list)


class PointInputInteractor(BaseInteractor):
    """Implementation of the coordinate input interactor

    This interactor prompts the user to input a point in the viewport. The identified
    point is printed in the trace. If element identification was activated in the
    palette, also the type of the identified geometry is printed in the trace.

    Optionally, a 3D point symbol (terrain point) is created in the drawing file.

    Attributes:
        build_ele:      building element with the properties from the property pallette
        coord_input:    API object representing the coordinate input and element selection
                        in the Allplan viewport
        input_pnt:      last input point
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
        self.build_ele   = cast(PointInputBuildingElement, build_ele_list[0])
        self.coord_input = coord_input
        self.input_pnt   = None

        # initialize needed services
        self.palette_service = BuildingElementPaletteService(build_ele_list,
                                                             build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list,
                                                             self.build_ele.pyp_file_name)

        # show palette and start input
        self.palette_service.show_palette(self.build_ele.pyp_file_name)
        self.initialize_coord_input()

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
        match name:
            case "EnableAssistWndClick":
                self.coord_input.EnableAssistWndClick(value)
                print(f"Selection in wizard window {'activated' if value else 'deactivated'}")

            case "EnableZCoordinate":
                self.coord_input.EnableZCoord(value)
                print(f"Input of Z-coordinate {'enabled' if value else 'disabled'}")

            case "EnableUndoStep":
                self.coord_input.EnableUndoStep(value)
                print(f"Undo button in the dialog line {'enabled' if value else 'disabled'}")

        # reinitialize the element selection after each modification in property palette
        self.initialize_coord_input()

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
        self.coord_input.GetCurrentPoint()  # redraw the point symbol after each modification inside the dialog line

    def on_value_input_control_enter(self) -> bool:
        """Called when enter key is pressed inside the value input control

        Returns:
            True/False for success.
        """

        print("-----------------New value in the dialog line----------------------",
              f"{'Input control integer value:' :<{30}}{self.coord_input.GetInputControlIntValue()}",
              f"{'Input control value:'         :<{30}}{self.coord_input.GetInputControlValue()}",
              "--------------------------------------------------------------------",
              "\n",
              sep="\n")

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeometry.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """Method called on each mouse movement, button click or release.

        Args:
            mouse_msg:  the mouse message (e.g. 512 - mouse movement)
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """
        # trace tracking to nothing but user-defined tracking points
        if self.build_ele.TrackTo.value == "Nothing":
            coord_input_result = self.coord_input.GetInputPoint(mouse_msg,
                                                                pnt,
                                                                msg_info)
        # trace tracking to last input point
        elif self.build_ele.TrackTo.value == "LastInputPoint":
            coord_input_result = self.coord_input.GetInputPoint(mouse_msg,
                                                                pnt,
                                                                msg_info,
                                                                True)
        # trace tracking to defined point
        else:
            coord_input_result = self.coord_input.GetInputPoint(mouse_msg,
                                                                pnt,
                                                                msg_info,
                                                                self.build_ele.TrackPoint.value,
                                                                True)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        # get the input point and reference line
        self.input_pnt = coord_input_result.GetPoint()
        ref_line       = AllplanGeometry.Line2D() #self.coord_input.GetReferenceLine()
        geo_element    = self.coord_input.GetSelectedGeometryElement()

        # create a point symbol in the drawing file
        if self.build_ele.CreateSymbol.value:
            self.create_point_symbol()

        # print the result in trace
        col = 15    # column width
        print(f"\n{'-'*14} Identified point {'-'*14}",
              f"{'X':^{col}} {'Y':^{col}} {'Z':^{col}}",
              f"{round(self.input_pnt.X, 3):^{col}} {round(self.input_pnt.Y,3):^{col}} {round(self.input_pnt.Z,3):^{col}}\n",
              sep="\n")

        if ref_line != AllplanGeometry.Line2D():
            print(f"{'-'*15} Reference line {'-'*15}",
                  f"{' ':^{col}} {'X':^{col}} {'Y':^{col}}",
                  f"{'Start:':>{col}} {round(ref_line.StartPoint.X):^{col}} {round(ref_line.StartPoint.Y):^{col}}",
                  f"{'End:':>{col}} {round(ref_line.EndPoint.X):^{col}} {round(ref_line.EndPoint.Y):^{col}}\n",
                  sep="\n")

        if geo_element is not None:
            print(f"{'-'*12} Identified geometry {'-' * 13}",
                  f"{'Type:':>{col}} {type(geo_element).__name__:^{col}}\n",
                  sep="\n")

        print("-" * 46)

        # reinitialize the input after each element selection
        self.initialize_coord_input()

        return True

    def on_cancel_function(self) -> bool:
        """ Called when ESC key is pressed.

        Returns:
            True when the PythonPart framework should terminate the PythonPart, False otherwise.
        """

        self.palette_service.close_palette()

        return True

    def on_input_undo(self) -> bool:
        """ Process the input undo event

        This event is triggered, when during coordinate input the user hits the undo button
        in the dialog line.

        Returns:
            message was processed: True/False
        """

        print(f"{'-'*13} Undo button pressed {'-'*12}")
        return True

    def initialize_coord_input(self) -> None:
        """Initialize the point input. Depending on the option set in the property palette, with or without
        an additional input control in the dialog line.

        After the initialization, following settings are applied:
        -   Input plane (if option was selected)
        -   Snoop geometry filter (relevant for point and element identification modes only)
        """
        # define prompt message
        prompt_msg = AllplanIFW.InputStringConvert("Input first point" if self.input_pnt is None else "Input next point")

        input_mode = AllplanIFW.CoordinateInputMode(
            identMode       = AllplanIFW.eIdentificationMode.names[self.build_ele.IndentificationMode.value],
            drawPointSymbol = AllplanIFW.eDrawElementIdentPointSymbols.names[self.build_ele.DrawElementIdentPoint.value])

        # initialize the coordinate input with an additional input control in the dialog line
        if self.build_ele.EnableInputControl.value:
            input_control_type = AllplanIFW.eValueInputControlType.names[self.build_ele.InputControlType.value]
            input_control      = AllplanIFW.ValueInputControlData(input_control_type,
                                                                  bSetFocus     = self.build_ele.SetFocus.value,
                                                                  bDisableCoord = self.build_ele.DisableCoord.value)
            if self.input_pnt is None:
                self.coord_input.InitFirstPointValueInput(prompt_msg,
                                                          input_control,
                                                          input_mode)
            else:
                self.coord_input.InitNextPointValueInput(prompt_msg,
                                                         input_control,
                                                         input_mode)

        # initialize the coordinate input with just a prompt message in the dialog line
        else:
            if self.input_pnt is None:
                self.coord_input.InitFirstPointInput(prompt_msg,
                                                     input_mode)
            else:
                self.coord_input.InitNextPointInput(prompt_msg,
                                                    input_mode)

        # set the geometry filter
        geometry_snoop = AllplanIFW.SnoopElementGeometryFilter(
            bFindBaseGeometry        = self.build_ele.FindBaseGeometry.value,
            bFindAreaGeometry        = self.build_ele.FindAreaGeometry.value,
            bPerpendicularOnElement  = self.build_ele.PerpendicularOnElement.value,
            bFindNonPassiveOnly      = self.build_ele.FindNonPassiveOnly.value,
            bSplitAreaGeometries     = self.build_ele.SplitAreaGeometries.value,
            bIdentifyEmbeddedElement = self.build_ele.IdentifyEmbeddedElement.value,
            bFindCompleteFootprint   = self.build_ele.FindCompleteFootprint.value,
            splitElement3D           = AllplanIFW.eSplitElement3D.names[self.build_ele.SplitElement3D.value],
        )

        self.coord_input.SetGeometryFilter(geometry_snoop)

        # set the input plane
        if self.build_ele.SetInputPlane.value:
            input_plane = AllplanGeometry.Plane3D(self.build_ele.InputPlanePoint.value,
                                                  self.build_ele.InputPlaneVector.value)
            self.coord_input.SetInputPlane(input_plane)

        # set the projection base to 0
        self.coord_input.SetProjectionBase0(self.build_ele.SetProjectionBase0.value)

    def create_point_symbol(self):
        """Creates a point symbol (terrain point) in the drawing file representing
        the current input_pnt
        """
        symbol_props                  = AllplanBasisElements.Symbol3DProperties()
        symbol_props.IsScaleDependent = False                                           # type: ignore
        symbol_props.SymbolID         = 1                                               # type: ignore

        common_props = self.build_ele.SymbolCommonProps.value

        symbol = AllplanBasisElements.Symbol3DElement(common_props, symbol_props, self.input_pnt)

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeometry.Matrix3D(),
                                           [symbol], [], None)
