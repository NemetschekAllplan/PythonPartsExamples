"""Example script showing the modification of an architectural wall"""
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from pathlib import Path
from Utils import LibraryBitmapPreview

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from BuildingElementListService import BuildingElementListService
from HandleProperties import HandleProperties
from Utils.HandleCreator import HandleCreator

from TypeCollections.ModelEleList import ModelEleList
from Utils.HideElementsService import HideElementsService

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


def create_preview(build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a simplified wall representation for library preview

    Args:
        _build_ele:   building element with the parameter properties
        _doc:         input document

    Returns:
        Preview elements
    """

    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
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

    return ModifyWall(build_ele, script_object_data)


class ModifyWall(BaseScriptObject):
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

        self.wall_sel_result          = SingleElementSelectResult()
        self.build_ele                = build_ele
        self.reverse_offset_direction = False
        self.wall_ele                 = AllplanArchEle.WallElement()
        self.hide_ele_service         = HideElementsService()
        self.axis                     = AllplanGeo.Line2D()


    def start_input(self):
        """Starts the wall axis input at the beginning of the script runtime"""


        self.script_object_interactor = SingleElementSelectInteractor(self.wall_sel_result,
                                                                      [AllplanEleAdapter.Wall_TypeUUID],
                                                                      "Select the wall")


    def start_next_input(self):
        """Terminate the axis input after successful input of start and end point"""

        build_ele = self.build_ele

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.WALL_SELECTED

        #----------------- get the wall element
        self.wall_ele   = cast(AllplanArchEle.WallElement, AllplanBaseEle.GetElement(self.wall_sel_result.sel_element))

        self.axis       = self.wall_ele.GetGeometryObject()

        #----------------- get the properties
        wall_props = self.wall_ele.Properties
        build_ele.TierCount.value = wall_props.TierCount

        axis_prop                                 = wall_props.GetAxis()

        build_ele.AxisPosition.value              = axis_prop.Position
        build_ele.AxisOffset.value                = axis_prop.Distance
        build_ele.AxisOnTier.value                = axis_prop.OnTier


        if (axis_prop.Extension == -1):
            self.reverse_offset_direction = False
        else:
            self.reverse_offset_direction = True

        CommonPropList, SurfaceElemPropList, PlaneReferencesList, ThicknessList                           = [],[],[],[]
        TradeList, PriorityList, CalculationModeList, FactorList, IsSurfaceValueList, SurfaceNameList     = [],[],[],[],[],[]

        #----------------- loop through tiers and assign new list
        for iCnt in range(wall_props.TierCount):
            CommonPropList.append(wall_props.GetWallTierProperties(iCnt+1).CommonProperties)
            SurfaceElemPropList.append(wall_props.GetWallTierProperties(iCnt+1).SurfaceElementProperties)
            PlaneReferencesList.append(wall_props.GetWallTierProperties(iCnt+1).PlaneReferences)
            ThicknessList.append(wall_props.GetWallTierProperties(iCnt+1).Thickness)
            TradeList.append(wall_props.GetWallTierProperties(iCnt+1).Trade)
            PriorityList.append(wall_props.GetWallTierProperties(iCnt+1).Priority)
            CalculationModeList.append(AllplanBaseEle.AttributeService.GetEnumValueStringFromID(120,wall_props.GetWallTierProperties(iCnt+1).CalculationMode))
            FactorList.append(wall_props.GetWallTierProperties(iCnt+1).Factor)
            IsSurfaceValueList.append(wall_props.GetWallTierProperties(iCnt+1).Surface.strip() != "")
            SurfaceNameList.append(wall_props.GetWallTierProperties(iCnt+1).Surface)

        build_ele.CommonProp.value          = CommonPropList
        build_ele.SurfaceElemProp.value     = SurfaceElemPropList
        build_ele.PlaneReferences.value     = PlaneReferencesList
        build_ele.Thickness.value           = ThicknessList
        build_ele.Trade.value               = TradeList
        build_ele.Priority.value            = PriorityList
        build_ele.CalculationMode.value     = CalculationModeList
        build_ele.Factor.value              = FactorList
        build_ele.IsSurface.value           = IsSurfaceValueList
        build_ele.SurfaceName.value         = SurfaceNameList

        #----------------- start the beam modification
        self.hide_ele_service.hide_element(self.wall_sel_result.sel_element)

    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        return CreateElementResult(self.wall_element(),self.create_handles(),
                                   placement_point = AllplanGeo.Point2D())  # wall is already in the global coordinate system

    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            handles
        """

        handle_list = []

        HandleCreator.move(handle_list, "PlacementPointStart", (self.axis.StartPoint.To3D))
        HandleCreator.move(handle_list, "PlacementPointEnd", (self.axis.EndPoint.To3D))

        return handle_list

    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        match handle_prop.handle_id:
            case "PlacementPointStart":
                self.axis.StartPoint = input_pnt.To2D

        match handle_prop.handle_id:
            case "PlacementPointEnd":
                self.axis.EndPoint = input_pnt.To2D


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        self.hide_ele_service.show_elements()

        if (self.wall_sel_result != SingleElementSelectResult()):
            AllplanBaseEle.ModifyElements(self.document, self.wall_element())

        return OnCancelFunctionResult.CANCEL_INPUT

    def on_control_event(self, event_id: int):
        """Handle the event of hitting a button in the property palette

        Args:
            event_id: id of the event triggered by the pressed button
        """

        match event_id:
            case self.build_ele.REVERSE_OFFSET_DIRECTION:
                self.reverse_offset_direction = not self.reverse_offset_direction

    def axis_properties(self) -> AllplanArchEle.AxisProperties:
        """Properties of the wall's axis, based on the values from the property palette

        Returns:
            axis properties
        """

        axis_prop          = AllplanArchEle.AxisProperties()

        axis_prop.OnTier   = self.build_ele.AxisOnTier.value
        axis_prop.Position = AllplanArchEle.WallAxisPosition.values[self.build_ele.AxisPosition.value]  # type: ignore

        # distance must be set independently from axis position

        axis_prop.Distance = 0

        if axis_prop.OnTier >= 2:
            axis_prop.Distance += sum(self.build_ele.Thickness.value[:axis_prop.OnTier - 1])

        match AllplanArchEle.WallAxisPosition.values[self.build_ele.AxisPosition.value]:
            case AllplanArchEle.WallAxisPosition.eLeft:
                axis_prop.Distance += 0

            case AllplanArchEle.WallAxisPosition.eCenter:
                axis_prop.Distance += self.build_ele.Thickness.value[axis_prop.OnTier-1] / 2

            case AllplanArchEle.WallAxisPosition.eRight:
                axis_prop.Distance += self.build_ele.Thickness.value[axis_prop.OnTier-1]

            case AllplanArchEle.WallAxisPosition.eFree:
                axis_prop.Distance = self.build_ele.AxisOffset.value

        axis_prop.Extension = 1 if self.reverse_offset_direction else -1

        return axis_prop

    def wall_element(self) -> AllplanArchEle.WallElement:
        """Creates a WallElement based on axis (2d line)

        Args:
            axis:   wall axis

        Returns:
            Wall element
        """
        build_ele =  self.build_ele

        #----------------- create the properties
        wall_props              = self.wall_ele.Properties
        wall_props.TierCount    = build_ele.TierCount.value
        wall_props.Axis         = self.axis_properties()
        wall_props.StartNewJoinedWallGroup = True

        #----------------- loop through tiers
        for iCnt in range(wall_props.TierCount):
            wall_props.GetWallTierProperties(iCnt+1).CommonProperties = build_ele.CommonProp.value[iCnt]
            wall_props.GetWallTierProperties(iCnt+1).SurfaceElementProperties = build_ele.SurfaceElemProp.value[iCnt]
            wall_props.GetWallTierProperties(iCnt+1).PlaneReferences = build_ele.PlaneReferences.value[iCnt]
            wall_props.GetWallTierProperties(iCnt+1).Thickness = build_ele.Thickness.value[iCnt]
            wall_props.GetWallTierProperties(iCnt+1).Trade = build_ele.Trade.value[iCnt]
            wall_props.GetWallTierProperties(iCnt+1).Priority= build_ele.Priority.value[iCnt]
            wall_props.GetWallTierProperties(iCnt+1).CalculationMode = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(120,build_ele.CalculationMode.value[iCnt] )
            wall_props.GetWallTierProperties(iCnt+1).Factor = build_ele.Factor.value[iCnt]

            if self.build_ele.IsSurface.value[iCnt]:
                wall_props.GetWallTierProperties(iCnt+1).Surface = self.build_ele.SurfaceName.value[iCnt]

        self.wall_ele.SetProperties(wall_props)

        #----------------- create the element

        model_ele_list = ModelEleList()

        model_ele_list.append(self.wall_ele)

        return model_ele_list
