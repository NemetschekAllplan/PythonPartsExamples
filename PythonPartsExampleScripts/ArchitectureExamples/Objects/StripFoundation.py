"""Example script showing the creation of an architectural strip foundation"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.LineInteractor import LineInteractor, LineInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BeamBuildingElement import BeamBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_preview(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a simplified beam representation for library preview

    Args:
        build_ele:   building element with the parameter properties
        _doc:        input document

    Returns:
        Preview elements
    """

    common_props = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()
    beam_geo     = AllplanGeometry.Polyhedron3D.CreateCuboid(3500, build_ele.Width.value, 500)

    return CreateElementResult([AllplanBasisElements.ModelElement3D(common_props, beam_geo)])


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return BeamScript(build_ele, script_object_data)


class BeamScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural upstand/downstand beam

    This script objects prompts the user to input a 2D-Line by specifying
    start and end point and subsequently creates a beam
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialize the beam script object

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.axis_input_result        = LineInteractorResult()
        self.build_ele                = build_ele
        self.reverse_offset_direction = False


    def start_input(self):
        """Starts the beam axis input at the beginning of the script runtime"""

        self.script_object_interactor = LineInteractor(self.axis_input_result, True, "Draw beam axis",
                                                       preview_function = lambda line: [self.beam_element(AllplanGeometry.Line2D(line))])


    def start_next_input(self):
        """Terminate the axis input after successful input of start and end point"""

        if self.axis_input_result != LineInteractorResult():
            self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        _, axis = AllplanGeometry.ConvertTo2D(self.axis_input_result.input_line)

        return CreateElementResult([self.beam_element(axis)],
                                   placement_point = AllplanGeometry.Point2D())  # beam is already in the global coordinate system


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        if self.script_object_interactor:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def on_control_event(self, event_id: int):
        """Handle the event of hitting a button in the property palette

        Args:
            event_id: id of the event triggered by the pressed button
        """

        match event_id:
            case self.build_ele.REVERSE_OFFSET_DIRECTION:
                self.reverse_offset_direction = not self.reverse_offset_direction


    @property
    def beam_properties(self) -> AllplanArchElements.StripFoundationProperties:
        """Properties of the beam element, based on the values from the property palette

        Returns:
            beam properties
        """

        strip_found_props = AllplanArchElements.StripFoundationProperties()

        #--------- Define properties specific to a beam

        strip_found_props.SetAxis(self.axis_properties)

        strip_found_props.PlaneReferences                      = self.build_ele.PlaneReferences.value
        strip_found_props.ShapeType                            = self.build_ele.SectionType.value
        strip_found_props.ProfileFullName                      = self.build_ele.Profile.value
        strip_found_props.Width                                = self.build_ele.Width.value
        strip_found_props.IsStartNewJoinedStripFoundationGroup = True

        strip_found_props.StepChamferWidth                     = self.build_ele.StepChamferWidth.value
        strip_found_props.StepChamferHeight                    = self.build_ele.StepChamferHeight.value
        strip_found_props.StepChamferEccentricity              = self.build_ele.StepChamferEccentricity.value
        strip_found_props.LeftHaunch                           = self.build_ele.LeftHaunch.value
        strip_found_props.RightHaunch                          = self.build_ele.RightHaunch.value
        strip_found_props.StepBounce                           = self.build_ele.StepBounce.value

        # ^^ when creating multiple beams, setting this to False on second and subsequent beams will join all of them
        # since this script creates only one beam at a time, the value is hard coded to True to NOT join the beams

        #--------- Define standard architecture attributes

        strip_found_props.CalculationMode = AllplanBaseElements.AttributeService.GetEnumIDFromValueString(120, self.build_ele.CalculationMode.value)
        strip_found_props.Trade           = self.build_ele.Trade.value
        strip_found_props.Priority        = self.build_ele.Priority.value
        strip_found_props.Factor          = self.build_ele.Factor.value

        #--------- Define surface elements

        strip_found_props.SurfaceElementProperties = self.build_ele.SurfaceElemProp.value

        #--------- Define format and texture properties

        strip_found_props.CommonProperties = self.build_ele.CommonProp.value

        if self.build_ele.IsSurface.value:
            strip_found_props.Surface = self.build_ele.SurfaceName.value

        return strip_found_props


    @property
    def axis_properties(self) -> AllplanArchElements.AxisProperties:
        """Properties of the beam's axis, based on the values from the property palette

        Returns:
            axis properties
        """

        axis_prop = AllplanArchElements.AxisProperties()
        axis_prop.Position = AllplanArchElements.WallAxisPosition.values[self.build_ele.AxisPosition.value]  # type: ignore

        # distance must be set independently from axis position

        match AllplanArchElements.WallAxisPosition.values[self.build_ele.AxisPosition.value]:
            case AllplanArchElements.WallAxisPosition.eLeft:
                axis_prop.Distance = 0

            case AllplanArchElements.WallAxisPosition.eCenter:
                axis_prop.Distance = self.build_ele.Width.value / 2

            case AllplanArchElements.WallAxisPosition.eRight:
                axis_prop.Distance = self.build_ele.Width.value

            case AllplanArchElements.WallAxisPosition.eFree:
                axis_prop.Distance = self.build_ele.AxisOffset.value

        axis_prop.Extension = 1 if self.reverse_offset_direction else -1

        return axis_prop


    def beam_element(self, axis: AllplanGeometry.Line2D) -> AllplanArchElements.StripFoundationElement:
        """Creates a BeamElement based on axis (2d line)

        Args:
            axis:   beam axis

        Returns:
            Beam element
        """

        return AllplanArchElements.StripFoundationElement(self.beam_properties, axis)
