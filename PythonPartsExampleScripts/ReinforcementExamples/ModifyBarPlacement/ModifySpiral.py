""" Example Script for the spiral modification
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Reinforcement as AllplanReinf

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from BuildingElementListService import BuildingElementListService
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult

from TypeCollections.ElementModificationDataList import ElementModificationDataList
from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils.ElementFilter.ReinforcementElementsFilterUtil import ReinforcementElementsFilterUtil
from Utils.HideElementsService import HideElementsService
from Utils.Reinforcement.ReinforcementElementUitl import ReinforcementElementUtil
from Utils.HandleCreator.CurveHandlesCreator import CurveHandlesCreator
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifySpiralBuildingElement import ModifySpiralBuildingElement
else:
    ModifySpiralBuildingElement = BuildingElement

print('Load ModifySpiral.py')

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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifySpiral(build_ele, script_object_data)


class ModifySpiral(BaseScriptObject):
    """ Definition of class ModifySpiral
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

        self.spiral_sel_result = MultiElementSelectInteractorResult()

        self.build_ele = cast(ModifySpiralBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.hide_ele_service = HideElementsService()
        self.spirals          = ElementModificationDataList[AllplanReinf.SpiralElement, AllplanGeo.Polyline3D]()


    def create_library_preview(self) -> CreateElementResult:
        """ create the library preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def start_input(self):
        """ start the input
        # """

        self.script_object_interactor = MultiElementSelectInteractor(self.spiral_sel_result,
                                                                     ReinforcementElementsFilterUtil.create_spiral_bar_placement_filter(),
                                                                     "Select the spiral")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        build_ele.reset()

        build_ele.InputMode.value = build_ele.SPIRAL_INPUT

        self.script_object_interactor = None


        #----------------- get the spiral elements data

        self.spirals.clear()

        for spiral_bar_ele in self.spiral_sel_result.sel_elements:
            spiral = ReinforcementElementUtil.get_spiral_from_placement(spiral_bar_ele)

            spiral_ele = cast(AllplanReinf.SpiralElement, AllplanBaseEle.GetElement(spiral))

            self.spirals.add_elements(spiral, spiral_ele, spiral_ele.ContourPoints)

            build_ele.PlacePerLinearMeter.varied_value  = spiral_ele.PlacePerLinearMeter
            build_ele.StartHookLength.varied_value      = spiral_ele.HookLengthStart
            build_ele.StartHookAngle.varied_value       = spiral_ele.HookAngleStart
            build_ele.EndHookLength.varied_value        = spiral_ele.HookLengthEnd
            build_ele.EndHookAngle.varied_value         = spiral_ele.HookAngleEnd
            build_ele.Diameter.varied_value             = spiral_ele.Diameter
            build_ele.SteelGrade.varied_value           = spiral_ele.SteelGrade
            build_ele.Pitch.varied_value                = spiral_ele.Pitch
            build_ele.ConcreteCoverStart.varied_value   = spiral_ele.ConcreteCoverStart
            build_ele.ConcreteCoverContour.varied_value = spiral_ele.ConcreteCoverContour
            build_ele.ConcreteCoverEnd.varied_value     = spiral_ele.ConcreteCoverEnd
            build_ele.LengthFactor.varied_value         = spiral_ele.LengthFactor
            build_ele.LoopsStart.varied_value           = spiral_ele.NumberLoopsStart
            build_ele.LoopsEnd.varied_value             = spiral_ele.NumberLoopsEnd

            pitch_sections = spiral_ele.GetPitchSections()
            pitch_lengths  = spiral_ele.GetLengthSections()

            build_ele.Pitch1.varied_value  = pitch_sections[0]
            build_ele.Length1.varied_value = pitch_lengths[0]
            build_ele.Pitch2.varied_value  = pitch_sections[1]
            build_ele.Length2.varied_value = pitch_lengths[1]
            build_ele.Pitch3.varied_value  = pitch_sections[2]
            build_ele.Length3.varied_value = pitch_lengths[2]
            build_ele.Pitch4.varied_value  = pitch_sections[3]
            build_ele.Length4.varied_value = pitch_lengths[3]


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        preview_ele = self.create_spiral_elements() if self.spirals.is_modified else ModelEleList()

        return CreateElementResult(ModelEleList(), self.create_handles(), preview_ele,
                                   multi_placement   = True,
                                   placement_point   = AllplanGeo.Point3D(),
                                   as_static_preview = True)


    def create_spiral_elements(self) -> ModelEleList:
        """ create the spiral elements

        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        model_ele_list = ModelEleList()

        for spiral_data in self.spirals:
            spiral_ele = spiral_data.element

            spiral_ele.PlacePerLinearMeter  = build_ele.PlacePerLinearMeter.get_unique_value(spiral_ele.PlacePerLinearMeter)
            spiral_ele.HookLengthStart      = build_ele.StartHookLength.get_unique_value(spiral_ele.HookLengthStart)
            spiral_ele.HookAngleStart       = build_ele.StartHookAngle.get_unique_value(spiral_ele.HookAngleStart)
            spiral_ele.HookLengthEnd        = build_ele.EndHookLength.get_unique_value(spiral_ele.HookLengthEnd)
            spiral_ele.HookAngleEnd         = build_ele.EndHookAngle.get_unique_value(spiral_ele.HookAngleEnd)
            spiral_ele.Diameter             = build_ele.Diameter.get_unique_value(spiral_ele.Diameter)
            spiral_ele.SteelGrade           = build_ele.SteelGrade.get_unique_value(spiral_ele.SteelGrade)
            spiral_ele.Pitch                = build_ele.Pitch.get_unique_value(spiral_ele.Pitch)
            spiral_ele.ConcreteCoverStart   = build_ele.ConcreteCoverStart.get_unique_value(spiral_ele.ConcreteCoverStart)
            spiral_ele.ConcreteCoverContour = build_ele.ConcreteCoverContour.get_unique_value(spiral_ele.ConcreteCoverContour)
            spiral_ele.ConcreteCoverEnd     = build_ele.ConcreteCoverEnd.get_unique_value(spiral_ele.ConcreteCoverEnd)
            spiral_ele.LengthFactor         = build_ele.LengthFactor.get_unique_value(spiral_ele.LengthFactor)
            spiral_ele.NumberLoopsStart     = build_ele.LoopsStart.get_unique_value(spiral_ele.NumberLoopsStart)
            spiral_ele.NumberLoopsEnd       = build_ele.LoopsEnd.get_unique_value(spiral_ele.NumberLoopsEnd)

            pitch_sections = spiral_ele.GetPitchSections()
            pitch_lengths  = spiral_ele.GetLengthSections()

            spiral_ele.SetPitchSections(build_ele.Pitch1.get_unique_value(pitch_sections[0]),
                                        build_ele.Length1.get_unique_value(pitch_lengths[0]),
                                        build_ele.Pitch2.get_unique_value(pitch_sections[1]),
                                        build_ele.Length2.get_unique_value(pitch_lengths[1]),
                                        build_ele.Pitch3.get_unique_value(pitch_sections[2]),
                                        build_ele.Length3.get_unique_value(pitch_lengths[2]),
                                        build_ele.Pitch4.get_unique_value(pitch_sections[3]),
                                        build_ele.Length4.get_unique_value(pitch_lengths[3]))

            spiral_ele.ContourPoints = spiral_data.additional_data

            model_ele_list.append(spiral_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            handles
        """

        handle_list = HandleList()

        for spiral_data in self.spirals:
            CurveHandlesCreator.poly_curve(handle_list, "", spiral_data.additional_data, True,
                                          owner_element = spiral_data.adapter_element)

        return handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        if not self.spirals.is_modified:
            self.hide_ele_service.hide_elements(self.spirals.adapter_elements)

        HandlePropertiesService.update_property_value(self.build_ele, handle_prop, input_pnt)

        self.spirals.set_handle_modification(handle_prop.owner_element)


    def modify_element_property(self,
                                _name : str,
                                _value: Any) -> bool:
        """ modify the element property

        Args:
            _name:  name
            _value: value

        Returns:
            update palette state
        """

        if not self.spirals.is_modified:
            self.hide_ele_service.hide_elements(self.spirals.adapter_elements)

        self.spirals.set_property_modification()

        return False


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT


        #----------------- modify the elements

        if self.spirals.is_modified:
            self.create_spiral_elements()

            AllplanBaseEle.ModifyElements(self.document, self.spirals.get_modified_elements())

        self.hide_ele_service.show_elements()

        AllplanIFW.HandleService().RemoveHandles()
        AllplanIFW.BuildingElementInputControls().CloseControls()

        return OnCancelFunctionResult.RESTART
