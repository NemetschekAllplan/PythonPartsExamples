""" Example Script for the window opening
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from ValueListUtil import ValueListUtil

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

from ParameterUtils.OpeningDoorSwingPropertiesParameterUtil import OpeningDoorSwingPropertiesParameterUtil
from ParameterUtils.OpeningRevealPropertiesParameterUtil import OpeningRevealPropertiesParameterUtil
from ParameterUtils.OpeningSymbolsPropertiesParameterUtil import OpeningSymbolsPropertiesParameterUtil
from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil
from ParameterUtils.OpeningTierOffsetPropertiesParameterUtil import OpeningTierOffsetPropertiesParameterUtil

from .OpeningBase import OpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.DoorOpeningBuildingElement import DoorOpeningBuildingElement
else:
    DoorOpeningBuildingElement = BuildingElement

print('Load DoorOpening.py')

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

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\ArchitectureExamples\Objects\DoorOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return DoorOpening(build_ele, script_object_data)


class DoorOpening(OpeningBase):
    """ Definition of class DoorOpening
    """

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = ArchPointInteractor(self.arch_pnt_result,
                                                            ArchitectureElementsQueryUtil.create_arch_door_window_opening_elements_query(),
                                                            "Set properties or click a component line",
                                                            self.draw_placement_preview)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        if self.placement_line is None:
            return

        build_ele = cast(DoorOpeningBuildingElement, self.build_ele)

        super().start_next_input()


        #----------------- check the size of the offsets

        tier_count = self.build_ele.ElementTierCount.value

        ValueListUtil.resize_1_dim_list(build_ele.LeftOffsets.value, tier_count, 0.)
        ValueListUtil.resize_1_dim_list(build_ele.RightOffsets.value, tier_count, 0.)
        ValueListUtil.resize_1_dim_list(build_ele.BottomOffsets.value, tier_count, 0.)
        ValueListUtil.resize_1_dim_list(build_ele.TopOffsets.value, tier_count, 0.)


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = cast(DoorOpeningBuildingElement, self.build_ele)


        #----------------- create the properties

        opening_prop = AllplanArchEle.DoorOpeningProperties()

        opening_prop.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value
        opening_prop.PlaneReferences          = build_ele.HeightSettings.value
        opening_prop.FrenchDoor               = build_ele.IsFrenchWindow.value

        self.opening_geo_param_util.create_opening_geo_properties(build_ele, opening_prop.GetGeometryProperties())

        OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())
        OpeningRevealPropertiesParameterUtil.create_reveal_properties(build_ele, "", opening_prop.GetRevealProperties())
        OpeningTierOffsetPropertiesParameterUtil.create_tier_offset_properties(build_ele, "", opening_prop.GetTierOffsetProperties())
        OpeningSymbolsPropertiesParameterUtil.create_opening_symbols_properties(build_ele, "", opening_prop.GetOpeningSymbolsProperties())

        if not build_ele.SmartSymbolGroup.value:
            OpeningDoorSwingPropertiesParameterUtil.create_door_swing_properties(build_ele, "", opening_prop.GetDoorSwingProperties())


        #----------------- create the opening

        self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_axis_element(self.opening_start_pnt.To2D,
                                                                                           build_ele.Width.value,
                                                                                           self.general_ele_axis,
                                                                                           self.general_ele_geo,
                                                                                           self.placement_line).To3D

        opening_ele = AllplanArchEle.DoorOpeningElement(opening_prop, self.general_ele,
                                                        self.opening_start_pnt.To2D,
                                                        self.opening_end_pnt.To2D,
                                                        build_ele.InputMode.value == build_ele.ELEMENT_SELECT)

        model_ele_list = ModelEleList()

        model_ele_list.append(opening_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        build_ele = cast(DoorOpeningBuildingElement, self.build_ele)

        handle_list : list[HandleProperties] = []

        self.create_opening_handles(handle_list)


        #----------------- door swing handle

        bottom_pnt = AllplanGeo.Point3D(0, 0,
                                        build_ele.HeightSettings.value.AbsBottomElevation - build_ele.HeightSettings.value.BottomElevation)

        opening_start_pnt = self.opening_start_pnt + bottom_pnt
        opening_end_pnt   = self.opening_end_pnt + bottom_pnt

        base_line = AllplanGeo.Line2D(opening_start_pnt.To2D, opening_end_pnt.To2D)

        handle_pnt = AllplanGeo.TransformCoord.PointGlobal(base_line, AllplanGeo.Point2D(build_ele.Width.value / 2,
                                                                                         -build_ele.Width.value / 2)) \
                        if build_ele.DoorSwingBasePointIndex.value in {1, 2} else \
                     AllplanGeo.TransformCoord.PointGlobal(base_line, AllplanGeo.Point2D(build_ele.Width.value / 2,
                                                                                         build_ele.ElementThickness.value / 2 + \
                                                                                         build_ele.Width.value / 2))

        HandleCreator.point(handle_list, "DoorSwing", handle_pnt, info_text = "Door swing placement")

        handle_list[-1].handle_type = AllplanIFW.ElementHandleType.HANDLE_ARROW

        return handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D) -> CreateElementResult:
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point

        Returns:
            created element result
        """

        match handle_prop.handle_id:
            case "DoorSwing":
                self.calc_door_swing_base_point_index(input_pnt)

            case _:
                return super().move_handle(handle_prop, input_pnt)

        return self.execute()


    def calc_door_swing_base_point_index(self,
                                         input_pnt: AllplanGeo.Point3D):
        """ calculate the door swing base point index

        Args:
            input_pnt: input point
        """

        build_ele = self.build_ele

        input_pnt_2d = input_pnt.To2D

        min_dist         = 1.0e10
        base_point_index = 1

        for index, pnt in enumerate(OpeningPointsUtil.create_opening_points_for_axis_element(self.opening_start_pnt.To2D,
                                                                                             self.opening_end_pnt.To2D,
                                                                                             build_ele.Width.value,
                                                                                             build_ele.ElementThickness.value)):
            if (dist := AllplanGeo.Vector2D(pnt, input_pnt_2d).GetLength()) < min_dist:
                min_dist = dist
                base_point_index = index + 1

        build_ele = cast(DoorOpeningBuildingElement, self.build_ele)

        build_ele.DoorSwingBasePointIndex.value = base_point_index
