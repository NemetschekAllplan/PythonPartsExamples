""" Example Script for the general opening
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import abc
import math

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Palette as AllplanPalette

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService

from ParameterUtils.VerticalOpeningGeometryPropertiesParameterUtil import VerticalOpeningGeometryPropertiesParameterUtil

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from TypeCollections.ModelEleList import ModelEleList

from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService
from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeneralOpeningBuildingElement import GeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


class OpeningBase(BaseScriptObject):
    """ Definition of class GeneralOpening
    """

    def __init__(self,
                 build_ele         : Any,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = cast(BuildingElement, build_ele)

        self.arch_pnt_result = ArchPointInteractorResult()

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT

        self.offset_start_pnt   = AllplanGeo.Point3D()
        self.offset_end_pnt     = AllplanGeo.Point3D()
        self.opening_start_pnt  = AllplanGeo.Point3D()
        self.opening_end_pnt    = AllplanGeo.Point3D()

        self.placement_line     : AllplanGeo.Line2D                              = AllplanGeo.Line2D()
        self.placement_arc      : AllplanGeo.Arc2D                               = AllplanGeo.Arc2D()
        self.general_ele_geo    : (AllplanGeo.Polygon2D | AllplanGeo.Polyline2D) = AllplanGeo.Polygon2D()
        self.general_ele_axis   : (AllplanGeo.Line2D | AllplanGeo.Arc2D)         = AllplanGeo.Line2D()

        self.general_ele = AllplanEleAdapter.BaseElementAdapter()
        self.hide_ele    = HideElementsService()

        self.opening_tier_center  : list[AllplanGeo.Point2D] = []
        self.opening_tier_ref_pnt : list[AllplanGeo.Point2D] = []

        self.opening_geo_param_util = VerticalOpeningGeometryPropertiesParameterUtil(build_ele, "")

        self.input_field_above = False


    def start_next_input(self):
        """ start the next input
        """

        if self.placement_line is None:
            return

        build_ele = self.build_ele

        build_ele.InputMode.value = build_ele.OPENING_INPUT

        self.script_object_interactor = None


        #----------------- get the left and right point for the opening offset

        created, start_offset, end_offset = OpeningPointsUtil.get_opening_offset_points(self.general_ele,
                                                                                        self.opening_start_pnt.To2D,
                                                                                        self.placement_line)

        if created:
            self.offset_start_pnt = start_offset.To3D
            self.offset_end_pnt   = end_offset.To3D

        if isinstance(self.general_ele_axis, AllplanGeo.Line2D):
            return


        #----------------- get the placement arc for the circular axis

        if isinstance(self.general_ele_axis, AllplanGeo.Arc2D):
            self.placement_arc, place_at_bottom = \
                AllplanArchEle.ArchitectureElementsGeometryService.CreatePlacementArc(self.general_ele,
                                                                                      self.general_ele_axis,
                                                                                      self.opening_start_pnt.To2D,
                                                                                      self.opening_end_pnt.To2D)
            self.input_field_above = not place_at_bottom


    def draw_placement_preview(self):
        """ draw the placement preview
        """

        build_ele = self.build_ele

        if self.arch_pnt_result.sel_model_ele.IsNull() or self.arch_pnt_result.sel_geo_ele is None:
            return


        #----------------- get the data from the selected element

        self.general_ele       = self.arch_pnt_result.sel_model_ele
        self.general_ele_geo   = self.arch_pnt_result.sel_model_ele_geo
        self.placement_line    = self.arch_pnt_result.sel_geo_ele
        self.offset_start_pnt  = self.placement_line.StartPoint.To3D
        self.offset_end_pnt    = self.placement_line.EndPoint.To3D
        self.opening_start_pnt = self.arch_pnt_result.input_point


        #----------------- draw the preview

        if not (general_axis_ele := AllplanEleAdapter.AxisElementAdapter(self.general_ele)).IsNull():
            self.general_ele_axis = general_axis_ele.GetAxis()

        build_ele.ElementThickness.value = general_axis_ele.GetThickness()
        build_ele.ElementTierCount.value = max(1, general_axis_ele.GetTiersCount())

        if build_ele.get_property("OpeningSymbolTierIndex") is not None:
            build_ele.OpeningSymbolTierIndex.value = min(build_ele.OpeningSymbolTierIndex.value,
                                                            build_ele.ElementTierCount.value)

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(),
                                          self.create_opening_element(), True, None)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.hide_general_element()

        return CreateElementResult(self.create_opening_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())

    @abc.abstractmethod
    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """


    @abc.abstractmethod
    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """


    def hide_general_element(self):
        """ hide the general element
        """

        build_ele = self.build_ele

        has_independent_interaction = 0

        if build_ele.get_property("HasIndependent2DInteraction") is not None:
            has_independent_interaction = build_ele.HasIndependent2DInteraction.value

        if not has_independent_interaction and not self.hide_ele.hidden_elements:
            self.hide_ele.hide_arch_ground_view_elements(self.general_ele)

        elif has_independent_interaction and self.hide_ele.hidden_elements:
            ele_list = AllplanEleAdapter.BaseElementAdapterList([self.general_ele])

            AllplanIFW.VisibleService.ShowElements(ele_list, True)

            self.hide_ele.clear()


    def create_opening_handles(self,
                               handle_list: list[HandleProperties]):
        """ create the opening handles

        Args:
            handle_list: description
        """

        build_ele = self.build_ele

        bottom_z_coordinate = 0

        if build_ele.get_property("HeightSettings") is not None:
            bottom_z_coordinate = build_ele.HeightSettings.value.AbsBottomElevation - build_ele.HeightSettings.value.BottomElevation


        bottom_pnt = AllplanGeo.Point3D(0, 0, bottom_z_coordinate)

        opening_start_pnt = self.opening_start_pnt + bottom_pnt
        opening_end_pnt   = self.opening_end_pnt + bottom_pnt


        #----------------- width input controls

        HandleCreator.point_distance(handle_list, "Width", opening_end_pnt, opening_start_pnt,
                                     show_handles = False, input_field_above = False)


        #----------------- handles for the circular axis

        if isinstance(self.general_ele_axis, AllplanGeo.Arc2D):
            if self.placement_arc.CounterClockwise:
                start_offset_pnt1 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, self.offset_start_pnt)[1]
                start_offset_pnt2 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, opening_start_pnt)[1]
                end_offset_pnt1   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, opening_end_pnt)[1]
                end_offset_pnt2   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, self.offset_end_pnt)[1]
                offset_start_pnt  = start_offset_pnt1
                offset_end_pnt    = end_offset_pnt2
            else:
                start_offset_pnt1 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, opening_start_pnt)[1]
                start_offset_pnt2 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, self.offset_start_pnt)[1]
                end_offset_pnt1   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, self.offset_end_pnt)[1]
                end_offset_pnt2   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, opening_end_pnt)[1]
                offset_start_pnt  = start_offset_pnt2
                offset_end_pnt    = end_offset_pnt1

            if abs(self.placement_arc.MinorRadius - self.placement_arc.MajorRadius) < 1.:
                HandleCreator.point_distance(handle_list, "StartPoint", start_offset_pnt1, start_offset_pnt2,
                                            input_field_above = self.input_field_above,
                                            center_point = self.placement_arc.Center.To3D)
                HandleCreator.point_distance(handle_list, "EndPoint", opening_end_pnt, end_offset_pnt2, False,
                                            center_point = self.placement_arc.Center.To3D)
                HandleCreator.point_distance(handle_list, "EndOffset", end_offset_pnt1, end_offset_pnt2, show_handles = False,
                                            input_field_above = self.input_field_above,
                                            center_point = self.placement_arc.Center.To3D)
                HandleCreator.point_distance(handle_list, "OffsetStartPoint", offset_start_pnt, end_offset_pnt1, False,
                                            center_point = self.placement_arc.Center.To3D)
                HandleCreator.point_distance(handle_list, "OffsetEndPoint", offset_end_pnt, start_offset_pnt2, False,
                                            center_point = self.placement_arc.Center.To3D)
            else:
                HandleCreator.move_xyz(handle_list, "StartPoint", start_offset_pnt1, start_offset_pnt2, False)
                HandleCreator.move_xyz(handle_list, "EndPoint", opening_end_pnt, end_offset_pnt2, False)


        #----------------- handles for the linear axis

        else:
            offset_start_pnt     = self.offset_start_pnt + bottom_pnt
            offset_end_pnt       = self.offset_end_pnt + bottom_pnt

            if isinstance(self.general_ele_axis, AllplanGeo.Line2D):
                HandleCreator.point_distance(handle_list, "StartPoint", opening_start_pnt, offset_start_pnt, input_field_above = False)
                HandleCreator.point_distance(handle_list, "EndPoint", opening_end_pnt, offset_end_pnt)
                HandleCreator.point_distance(handle_list, "OffsetStartPoint", offset_start_pnt, opening_end_pnt, False)
                HandleCreator.point_distance(handle_list, "OffsetEndPoint", offset_end_pnt, opening_start_pnt, False)

            else:
                HandleCreator.point(handle_list, "StartPoint", opening_start_pnt)
                HandleCreator.point(handle_list, "EndPoint", opening_end_pnt)

        if (prop := build_ele.get_property("SmartSymbolGroup")) is not None and prop.value:
            self.create_opening_symbol_handles(handle_list, bottom_pnt)


    def create_opening_symbol_handles(self,
                                      handle_list: list[HandleProperties],
                                      bottom_pnt : AllplanGeo.Point3D):
        """ create the handles for the opening symbol

        Args:
            handle_list: handle list
            bottom_pnt:  bottom of the opening
        """

        build_ele = self.build_ele

        #----------------- handle for the opening symbol move

        opening_line = AllplanGeo.Line2D(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D)

        opening_tier_index = build_ele.OpeningSymbolTierIndex.value - 1

        x_length = AllplanGeo.CalcLength(opening_line)
        x_center = x_length / 2
        y_start  = 0

        symbol_ref_pnt = AllplanGeo.Point2D()

        if self.general_ele.GetElementAdapterType().IsTypeGroup(AllplanEleAdapter.ElementAdapterTypeGroup.eHYPERELEMENT_GROUP) and \
           AllplanEleAdapter.BaseElementAdapterChildElementsService.GetTierElements(self.general_ele) != []:    # pylint: disable=consider-ternary-expression
            tier_thickness = AllplanEleAdapter.AxisElementAdapter(self.general_ele).GetTierThickness()
        else:
            tier_thickness = [build_ele.Depth.value]

        for index, tier_thickness in enumerate(tier_thickness):
            self.opening_tier_center.append(
                AllplanGeo.TransformCoord.PointGlobal(opening_line,
                                                      AllplanGeo.Point2D(x_center, y_start + tier_thickness / 2)).To2D)

            if index == opening_tier_index:
                self.opening_tier_ref_pnt = \
                    [AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(0, y_start + tier_thickness)).To2D,
                     AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(x_length, y_start + tier_thickness)).To2D,
                     AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(x_length, y_start)).To2D,
                     AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(0, y_start)).To2D]

                y_ref_pnt = y_start + 500 if build_ele.OpeningSymbolRefPntIndex.value in {AllplanPalette.RefPointPosition.eTopLeft,
                                                                                           AllplanPalette.RefPointPosition.eTopRight} else \
                            y_start + tier_thickness - 500

                dx = 0 if build_ele.OpeningSymbolRefPntIndex.value in {AllplanPalette.RefPointPosition.eBottomLeft,
                                                                       AllplanPalette.RefPointPosition.eTopLeft} else \
                     self.build_ele.Width.value

                symbol_ref_pnt = AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(dx, y_ref_pnt)).To2D

            y_start += tier_thickness

        HandleCreator.move_in_direction(handle_list, "SymbolPlacement",
                                        self.opening_tier_center[opening_tier_index].To3D + bottom_pnt,
                                        AllplanGeo.CalcAngle(opening_line)[0] + AllplanGeo.Angle(math.pi / 2),
                                        "Move the symbol to the tier")

        HandleCreator.move(handle_list, "SymbolRefPoint", symbol_ref_pnt.To3D + bottom_pnt, "Move the symbol reference point")


    def modify_element_property(self,
                                name : str,
                                value: Any) -> bool:
        """ modify the element property

        Args:
            name:  name
            value: value

        Returns:
            update palette state
        """

        match name:
            case "Shape":
                self.opening_geo_param_util.adapt_plane_references(self.build_ele)

                return True

            case "StartPoint":
                if (result := OpeningPointsUtil.get_start_point_from_start_offset(self.general_ele_axis, self.offset_start_pnt.To2D,
                                                                                  self.placement_line, self.placement_arc,
                                                                                  self.general_ele_geo, value)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

                return True

            case "EndPoint" | "EndOffset":
                if (result := OpeningPointsUtil.get_start_point_from_end_offset(self.general_ele_axis, self.offset_end_pnt.To2D,
                                                                                self.placement_line, self.placement_arc,
                                                                                self.build_ele.Width.value,
                                                                                self.general_ele_geo, value)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

                return True

        return False


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
            case "StartPoint":
                offset = OpeningPointsUtil.get_distance_from_offset_start_point(input_pnt, self.general_ele_axis,
                                                                                self.offset_start_pnt.To2D,
                                                                                self.placement_line, self.placement_arc,
                                                                                self.general_ele_geo)

                if (result := OpeningPointsUtil.get_start_point_from_start_offset(self.general_ele_axis, self.offset_start_pnt.To2D,
                                                                                  self.placement_line, self.placement_arc,
                                                                                  self.general_ele_geo, offset)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

            case "EndPoint":
                offset = OpeningPointsUtil.get_distance_from_offset_end_point(input_pnt, self.general_ele_axis,
                                                                              self.offset_end_pnt.To2D,
                                                                              self.placement_line, self.placement_arc,
                                                                              self.general_ele_geo)

                if (result := OpeningPointsUtil.get_start_point_from_end_offset(self.general_ele_axis, self.offset_end_pnt.To2D,
                                                                                self.placement_line, self.placement_arc,
                                                                                self.build_ele.Width.value,
                                                                                self.general_ele_geo, offset)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

            case "OffsetStartPoint":
                self.offset_start_pnt   = input_pnt
                self.offset_start_pnt.Z = 0

            case "OffsetEndPoint":
                self.offset_end_pnt   = input_pnt
                self.offset_end_pnt.Z = 0

            case "SymbolPlacement":
                self.select_opening_symbol_tier(input_pnt)

            case "SymbolRefPoint":
                self.select_opening_symbol_ref_pnt(input_pnt)

            case _:
                HandlePropertiesService.update_property_value(self.build_ele, handle_prop, input_pnt)

        return self.execute()


    def select_opening_symbol_tier(self,
                                   input_pnt: AllplanGeo.Point3D):
        """ select the tier for the opening symbol

        Args:
            input_pnt: input point
        """

        place_pnt = input_pnt.To2D

        min_dist  = 1.0e10
        build_ele = self.build_ele

        for index, tier_center in enumerate(self.opening_tier_center):
            if (dist := AllplanGeo.Vector2D(place_pnt, tier_center).GetLength()) < min_dist:
                min_dist = dist

                build_ele.OpeningSymbolTierIndex.value = index + 1


    def select_opening_symbol_ref_pnt(self,
                                      input_pnt: AllplanGeo.Point3D):
        """ select the reference point for the opening symbol

        Args:
            input_pnt: input point
        """

        place_pnt = input_pnt.To2D

        min_dist  = 1.0e10
        build_ele = self.build_ele

        for index, tier_ref_pnt in enumerate(self.opening_tier_ref_pnt):
            if (dist := AllplanGeo.Vector2D(place_pnt, tier_ref_pnt).GetLength()) < min_dist:
                min_dist = dist

                build_ele.OpeningSymbolRefPntIndex.value = [AllplanPalette.RefPointPosition.eTopLeft,
                                                            AllplanPalette.RefPointPosition.eTopRight,
                                                            AllplanPalette.RefPointPosition.eBottomRight,
                                                            AllplanPalette.RefPointPosition.eBottomLeft][index]


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        self.hide_ele.show_elements()

        return OnCancelFunctionResult.CREATE_ELEMENTS
