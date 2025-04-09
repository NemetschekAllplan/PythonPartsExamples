""" Example Script for the window opening
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from ValueListUtil import ValueListUtil

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil
from Utils.Architecture.OpeningHandlesUtil import OpeningHandlesUtil
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

from ParameterUtils.OpeningRevealPropertiesParameterUtil import OpeningRevealPropertiesParameterUtil
from ParameterUtils.OpeningSymbolsPropertiesParameterUtil import OpeningSymbolsPropertiesParameterUtil
from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil
from ParameterUtils.OpeningTierOffsetPropertiesParameterUtil import OpeningTierOffsetPropertiesParameterUtil

from .OpeningBase import OpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.WindowOpeningBuildingElement import WindowOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load WindowOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\WindowOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return WindowOpening(build_ele, script_object_data)


class WindowOpening(OpeningBase):
    """ Definition of class WindowOpening
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

        build_ele = cast(BuildingElement, self.build_ele)

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

        build_ele = cast(BuildingElement, self.build_ele)


        #----------------- create the properties

        opening_prop = AllplanArchEle.WindowOpeningProperties()

        opening_prop.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value
        opening_prop.PlaneReferences          = build_ele.HeightSettings.value

        self.opening_geo_param_util.create_opening_geo_properties(build_ele, opening_prop.GetGeometryProperties())

        OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())
        OpeningRevealPropertiesParameterUtil.create_reveal_properties(build_ele, "", opening_prop.GetRevealProperties())
        OpeningTierOffsetPropertiesParameterUtil.create_tier_offset_properties(build_ele, "", opening_prop.GetTierOffsetProperties())
        OpeningSymbolsPropertiesParameterUtil.create_opening_symbols_properties(build_ele, "", opening_prop.GetOpeningSymbolsProperties())


        #----------------- create the opening

        self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_axis_element(self.opening_start_pnt.To2D,
                                                                                            build_ele.Width.value,
                                                                                            self.placement_ele_axis,
                                                                                            self.placement_ele_geo,
                                                                                            self.placement_line).To3D

        opening_ele = AllplanArchEle.WindowOpeningElement(opening_prop, self.placement_ele,
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

        build_ele = cast(BuildingElement, self.build_ele)

        handle_list : list[HandleProperties] = []

        bottom_pnt = AllplanGeo.Point3D(0, 0,
                                        build_ele.HeightSettings.value.AbsBottomElevation - build_ele.HeightSettings.value.BottomElevation)

        OpeningHandlesUtil.create_opening_handles(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                                                  self.offset_start_pnt, self.offset_end_pnt,
                                                  self.placement_ele_axis, self.placement_arc, self.input_field_above, bottom_pnt,
                                                  handle_list)

        if (prop := build_ele.get_property("SmartSymbolGroup")) is not None and prop.value:
            self.opening_tier_center, self.opening_tier_ref_pnt = \
                OpeningHandlesUtil.create_opening_symbol_handles(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                                                                 build_ele.Width.value, build_ele.Depth.value, self.placement_ele,
                                                                 build_ele.OpeningSymbolTierIndex.value, True,
                                                                 build_ele.OpeningSymbolRefPntIndex.value,
                                                                 bottom_pnt, handle_list)


        return handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        build_ele = cast(BuildingElement, self.build_ele)

        match handle_prop.handle_id:
            case "SymbolPlacement":
                build_ele.OpeningSymbolTierIndex.value = OpeningPointsUtil.select_opening_tier(input_pnt, self.opening_tier_center)

            case _:
                super().move_handle(handle_prop, input_pnt)
