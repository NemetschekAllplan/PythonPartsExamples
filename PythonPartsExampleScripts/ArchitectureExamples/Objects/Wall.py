"""Example script showing the creation of an architectural wall"""
from __future__ import annotations

import re

from typing import TYPE_CHECKING, Any

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.LineInteractor import LineInteractor, LineInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.WallBuildingElement import WallBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a simplified wall representation for library preview

    Args:
        _build_ele:   building element with the parameter properties
        _doc:         input document

    Returns:
        Preview elements
    """

    common_props = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()
    wall_geo = AllplanGeometry.Polyhedron3D.CreateCuboid(3500, 300, 500)

    return CreateElementResult([AllplanBasisElements.ModelElement3D(common_props, wall_geo)])


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return WallScript(build_ele, script_object_data)


class WallScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural multilayer wall

    This script objects prompts the user to input a 2D-Line by specifying
    start and end point and subsequently creates a wall
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ function description

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.axis_input_result        = LineInteractorResult()
        self.build_ele                = build_ele
        self.reverse_offset_direction = False


    def start_input(self):
        """Starts the wall axis input at the beginning of the script runtime"""

        self.script_object_interactor = LineInteractor(self.axis_input_result, True, "Draw wall axis",
                                                       preview_function = lambda line: [self.wall_element(AllplanGeometry.Line2D(line))])


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

        return CreateElementResult([self.wall_element(axis)],
                                   placement_point = AllplanGeometry.Point2D())  # wall is already in the global coordinate system


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
    def wall_properties(self) -> AllplanArchElements.WallProperties:
        """Properties of the wall element, based on the values from the property palette

        Returns:
            wall properties
        """

        wall_prop = AllplanArchElements.WallProperties()

        #--------- Define properties specific to a wall as a whole

        wall_prop.Axis                    = self.axis_properties
        wall_prop.TierCount               = self.build_ele.TierCount.value
        wall_prop.StartNewJoinedWallGroup = True

        # ^^ when creating multiple walls, setting this to False on second and subsequent walls will join all of them together
        # since this script creates only one wall at a time, the value is hard coded to True to NOT join the walls

        #--------- Define properties specific to wall tiers

        calc_modes = ["m³","m²","m","Pcs","kg"]

        for tier_index in range(wall_prop.TierCount):
            wall_tier_prop = wall_prop.GetWallTierProperties(tier_index + 1)        # tier indices starts with 1!

            wall_tier_prop.PlaneReferences = self.build_ele.PlaneReferences.value[tier_index]

            #--------- Define standard architecture attributes

            wall_tier_prop.CalculationMode = calc_modes.index(self.build_ele.CalculationMode.value[tier_index])
            wall_tier_prop.Trade           = self.build_ele.Trade.value[tier_index]
            wall_tier_prop.Priority        = self.build_ele.Priority.value[tier_index]
            wall_tier_prop.Factor          = self.build_ele.Factor.value[tier_index]
            wall_tier_prop.Thickness       = self.build_ele.Thickness.value[tier_index]

            #--------- Define surface elements

            wall_tier_prop.SurfaceElementProperties = self.build_ele.SurfaceElemProp.value[tier_index]

            #--------- Define format and texture properties

            wall_tier_prop.CommonProperties = self.build_ele.CommonProp.value[tier_index]

            if self.build_ele.IsSurface.value[tier_index]:
                wall_tier_prop.Surface = self.build_ele.SurfaceName.value[tier_index]

        return wall_prop


    @property
    def axis_properties(self) -> AllplanArchElements.AxisProperties:
        """Properties of the wall's axis, based on the values from the property palette

        Returns:
            axis properties
        """

        axis_prop          = AllplanArchElements.AxisProperties()

        axis_prop.OnTier   = self.build_ele.AxisOnTier.value
        axis_prop.Position = AllplanArchElements.WallAxisPosition.values[self.build_ele.AxisPosition.value]  # type: ignore

        # distance must be set independently from axis position

        axis_prop.Distance = 0

        if axis_prop.OnTier >= 2:
            axis_prop.Distance += sum(self.build_ele.Thickness.value[:axis_prop.OnTier - 1])

        match AllplanArchElements.WallAxisPosition.values[self.build_ele.AxisPosition.value]:
            case AllplanArchElements.WallAxisPosition.eLeft:
                axis_prop.Distance += 0

            case AllplanArchElements.WallAxisPosition.eCenter:
                axis_prop.Distance += self.build_ele.Thickness.value[axis_prop.OnTier-1] / 2

            case AllplanArchElements.WallAxisPosition.eRight:
                axis_prop.Distance += self.build_ele.Thickness.value[axis_prop.OnTier-1]

            case AllplanArchElements.WallAxisPosition.eFree:
                axis_prop.Distance = self.build_ele.AxisOffset.value

        axis_prop.Extension = 1 if self.reverse_offset_direction else -1

        return axis_prop


    def wall_element(self, axis: AllplanGeometry.Line2D) -> AllplanArchElements.WallElement:
        """Creates a WallElement based on axis (2d line)

        Args:
            axis:   wall axis

        Returns:
            Wall element
        """

        return AllplanArchElements.WallElement(self.wall_properties, axis)
