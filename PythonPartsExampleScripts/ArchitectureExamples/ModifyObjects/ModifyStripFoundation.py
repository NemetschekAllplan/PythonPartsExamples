""" Example Script for strip foundation modification
"""

from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService


if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyStripFoundationBuildingElement import ModifyStripFoundationBuildingElement
else:
    ModifyStripFoundationBuildingElement = BuildingElement

print('Load ModifyStripFoundation.py')

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

    script_path = Path(_build_ele.pyp_file_path) / Path(_build_ele.pyp_file_name).name
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

    return ModifyStripFoundation(build_ele, script_object_data)


class ModifyStripFoundation(BaseScriptObject):
    """ Definition of class ModifyStripFoundation
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.stripfound_sel_result          = SingleElementSelectResult()
        self.build_ele                      = cast(ModifyStripFoundationBuildingElement, build_ele)
        self.hide_ele_service               = HideElementsService()
        self.stripfound_element             = AllplanArchEle.StripFoundationElement()
        self.reverse_offset_direction       = False
        self.axis                           = AllplanGeo.Line2D()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.stripfound_sel_result,
                                                                      [AllplanEleAdapter.StripFoundation_TypeUUID],
                                                                      "Select the strip foundation")

    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.STRIP_FOUND_SELECTED

        #----------------- get the strip foundation element

        self.stripfound_element = cast(AllplanArchEle.StripFoundationElement, AllplanBaseEle.GetElement(self.stripfound_sel_result.sel_element)) # pylint:disable=line-too-long

        #----------------- get the properties
        strip_found_props = self.stripfound_element.Properties

        build_ele.PlaneReferences.value           = strip_found_props.PlaneReferences
        build_ele.Width.value                     = strip_found_props.Width
        build_ele.CommonProp.value                = strip_found_props.CommonProperties
        build_ele.SurfaceElemProp.value           = strip_found_props.SurfaceElementProperties
        build_ele.Trade.value                     = strip_found_props.Trade
        build_ele.Priority.value                  = strip_found_props.Priority
        build_ele.CalculationMode.value           = AllplanBaseEle.AttributeService.GetEnumValueStringFromID(120,strip_found_props.CalculationMode) # pylint:disable=line-too-long
        build_ele.Factor.value                    = strip_found_props.Factor

        self.build_ele.StepChamferWidth.value           = strip_found_props.StepChamferWidth
        self.build_ele.StepChamferHeight.value          = strip_found_props.StepChamferHeight
        self.build_ele.StepChamferEccentricity.value    = strip_found_props.StepChamferEccentricity
        self.build_ele.LeftHaunch.value                 = strip_found_props.LeftHaunch
        self.build_ele.RightHaunch.value                = strip_found_props.RightHaunch
        self.build_ele.StepBounce.value                 = strip_found_props.StepBounce

        self.axis                                 = self.stripfound_element.GetGeometryObject()

        build_ele.SectionType.value               = strip_found_props.ShapeType
        build_ele.Profile.value                   = strip_found_props.ProfileFullName
        build_ele.IsSurface.value                 = strip_found_props.Surface.strip() != ""
        build_ele.SurfaceName.value               = strip_found_props.Surface

        axis_prop                                 = AllplanArchEle.AxisProperties()
        axis_prop                                 = strip_found_props.GetAxis()

        build_ele.AxisPosition.value              = axis_prop.Position
        build_ele.AxisOffset.value                = axis_prop.Distance


        if axis_prop.Extension == -1:
            self.reverse_offset_direction = False
        else:
            self.reverse_offset_direction = True

        #----------------- start the strip foundation modification
        self.hide_ele_service.hide_element(self.stripfound_sel_result.sel_element)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_stripfound_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def create_stripfound_element(self) -> ModelEleList:
        """ create the strip foundation element


        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        #----------------- create the properties
        strip_found_props                          = AllplanArchEle.StripFoundationProperties()

        strip_found_props.PlaneReferences          = build_ele.PlaneReferences.value
        strip_found_props.Width                    = build_ele.Width.value
        strip_found_props.CommonProperties         = build_ele.CommonProp.value
        strip_found_props.SurfaceElementProperties = build_ele.SurfaceElemProp.value
        strip_found_props.Trade                    = build_ele.Trade.value
        strip_found_props.Priority                 = build_ele.Priority.value
        strip_found_props.CalculationMode          = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(120, build_ele.CalculationMode.value) # pylint:disable=line-too-long
        strip_found_props.Factor                   = build_ele.Factor.value
        strip_found_props.ShapeType                = build_ele.SectionType.value
        strip_found_props.ProfileFullName          = build_ele.Profile.value

        strip_found_props.StepChamferWidth         = self.build_ele.StepChamferWidth.value
        strip_found_props.StepChamferHeight        = self.build_ele.StepChamferHeight.value
        strip_found_props.StepChamferEccentricity  = self.build_ele.StepChamferEccentricity.value
        strip_found_props.LeftHaunch               = self.build_ele.LeftHaunch.value
        strip_found_props.RightHaunch              = self.build_ele.RightHaunch.value
        strip_found_props.StepBounce               = self.build_ele.StepBounce.value

        if build_ele.IsSurface.value:
            strip_found_props.Surface            = build_ele.SurfaceName.value

        strip_found_props.SetAxis(self.axis_properties())

        self.stripfound_element.SetProperties(strip_found_props)
        self.stripfound_element.GeometryObject = self.axis


        #----------------- create the element

        model_ele_list = ModelEleList()

        model_ele_list.append(self.stripfound_element)

        return model_ele_list


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
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        self.hide_ele_service.show_elements()

        if self.stripfound_sel_result != SingleElementSelectResult():
            AllplanBaseEle.ModifyElements(self.document, self.create_stripfound_element())

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
        """Properties of the strip foundation's axis, based on the values from the property palette

        Returns:
            axis properties
        """

        axis_prop = AllplanArchEle.AxisProperties()
        axis_prop.Position = AllplanArchEle.WallAxisPosition.values[self.build_ele.AxisPosition.value]  # type: ignore

        # distance must be set independently from axis position

        match AllplanArchEle.WallAxisPosition.values[self.build_ele.AxisPosition.value]:
            case AllplanArchEle.WallAxisPosition.eLeft:
                axis_prop.Distance = 0

            case AllplanArchEle.WallAxisPosition.eCenter:
                axis_prop.Distance = self.build_ele.Width.value / 2

            case AllplanArchEle.WallAxisPosition.eRight:
                axis_prop.Distance = self.build_ele.Width.value

            case AllplanArchEle.WallAxisPosition.eFree:
                axis_prop.Distance = self.build_ele.AxisOffset.value

        axis_prop.Extension = 1 if self.reverse_offset_direction else -1

        return axis_prop
