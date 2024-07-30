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

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor, ArchPointInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from TypeCollections.ModelEleList import ModelEleList

from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

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
        self.placement_polyline = AllplanGeo.Polyline2D()

        self.opening_points   : list[AllplanGeo.Point2D]                       = []
        self.placement_ele    : (AllplanGeo.Line2D | AllplanGeo.Arc2D)         = AllplanGeo.Line2D()
        self.general_ele_geo  : (AllplanGeo.Polygon2D | AllplanGeo.Polyline2D) = AllplanGeo.Polygon2D()
        self.general_ele_axis : (AllplanGeo.Line2D | AllplanGeo.Arc2D)         = AllplanGeo.Line2D()

        self.general_ele = AllplanEleAdapter.BaseElementAdapter()
        self.hide_ele    = HideElementsService()

        self.opening_tier_center  : list[AllplanGeo.Point2D] = []
        self.opening_tier_ref_pnt : list[AllplanGeo.Point2D] = []

        self.opening_geo_param_util = VerticalOpeningGeometryPropertiesParameterUtil(build_ele, "")

        self.input_field_above = False


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = ArchPointInteractor(self.arch_pnt_result,
                                                            ArchitectureElementsQueryUtil.create_arch_axis_elements_query(),
                                                            "Set properties or click a component line",
                                                            self.draw_placement_preview)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        if self.placement_ele is None:
            return

        build_ele = self.build_ele

        build_ele.InputMode.value = build_ele.OPENING_INPUT

        self.script_object_interactor = None


        #----------------- get the left and right point for the opening offset

        created, start_offset, end_offset = \
            AllplanArchEle.ArchitectureElementsGeometryService.GetOpeningOffsetPoints(self.general_ele,
                                                                                      self.opening_start_pnt.To2D)

        if created:
            self.offset_start_pnt = start_offset.To3D
            self.offset_end_pnt   = end_offset.To3D

        if self.general_ele != AllplanEleAdapter.CircularWall_TypeUUID:
            return


        #----------------- get the placement polyline and arc for the circular axis

        self.placement_polyline = AllplanArchEle.ArchitectureElementsGeometryService.GetOuterPolyline(
                                        cast(AllplanGeo.Polygon2D, self.general_ele_geo),
                                        cast(AllplanGeo.Line2D, self.placement_ele), self.general_ele_axis)

        self.placement_ele, place_at_bottom = \
            AllplanArchEle.ArchitectureElementsGeometryService.CreatePlacementArc(self.general_ele,
                                                                                  cast(AllplanGeo.Arc2D, self.general_ele_axis),
                                                                                  self.opening_start_pnt.To2D,
                                                                                  self.opening_end_pnt.To2D)

        self.input_field_above = not place_at_bottom


    def draw_placement_preview(self):
        """ draw the placement preview
        """

        if self.arch_pnt_result.sel_model_ele.IsNull() or self.arch_pnt_result.sel_geo_ele is None:
            return

        #----------------- get the data from the selected element

        self.general_ele       = self.arch_pnt_result.sel_model_ele
        self.general_ele_geo   = self.arch_pnt_result.sel_model_ele_geo
        self.placement_ele     = self.arch_pnt_result.sel_geo_ele
        self.offset_start_pnt  = self.placement_ele.StartPoint.To3D
        self.offset_end_pnt    = self.placement_ele.EndPoint.To3D
        self.opening_start_pnt = self.arch_pnt_result.input_point


        #----------------- draw the preview

        general_axis_ele = AllplanEleAdapter.AxisElementAdapter(self.general_ele)

        self.general_ele_axis = cast(AllplanGeo.Arc2D, general_axis_ele.GetAxis())

        self.build_ele.ElementThickness.value = general_axis_ele.GetThickness()
        self.build_ele.ElementTierCount.value = general_axis_ele.GetTiersCount()

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


    def create_opening_points(self):
        """ create the opening points
        """

        build_ele = self.build_ele


        #----------------- opening points for a linear axis

        if self.general_ele.GetElementAdapterType().GetGuid() not in {AllplanEleAdapter.CircularWall_TypeUUID,
                                                                      AllplanEleAdapter.ElementWall_TypeUUID}:
            start_pnt = self.opening_start_pnt.To2D

            loc_start = AllplanGeo.TransformCoord.PointLocal(self.placement_ele, start_pnt).X

            self.opening_end_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele, loc_start + build_ele.Width.value)


        #----------------- opening points for a circular or spline axis

        else:
            if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
                dir_ele = AllplanGeo.Line2D(cast(AllplanGeo.Line2D, self.placement_ele))

            else:
                _, dir_ele = AllplanGeo.Polyline2DUtil.GetPolyline2DSegment(self.placement_polyline,
                                                                            self.opening_start_pnt.To2D)

            dir_ele.TrimEnd(-100)

            err, opening_end_pnt = \
                AllplanGeo.Polygon2DUtil.FindPointOnPolygonWithDistance(AllplanGeo.Polygon2D(self.general_ele_geo.Points),
                                                                        self.opening_start_pnt.To2D,
                                                                        dir_ele.EndPoint,
                                                                        self.general_ele_axis,
                                                                        build_ele.Width.value)

            if not err:
                self.opening_end_pnt = opening_end_pnt.To3D


        #----------------- get the opening points

        base_line = AllplanGeo.Line2D(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D)

        self.opening_points = [self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                               AllplanGeo.TransformCoord.PointGlobal(base_line, AllplanGeo.Point2D(build_ele.Width.value,
                                                                                                   build_ele.ElementThickness.value)).To2D,
                               AllplanGeo.TransformCoord.PointGlobal(base_line, AllplanGeo.Point2D(0,
                                                                                                   build_ele.ElementThickness.value)).To2D]


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

        if self.general_ele == AllplanEleAdapter.CircularWall_TypeUUID:
            axis_arc = cast(AllplanGeo.Arc2D, self.placement_ele)

            if axis_arc.CounterClockwise:
                start_offset_pnt1 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, self.offset_start_pnt)[1]
                start_offset_pnt2 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, opening_start_pnt)[1]
                end_offset_pnt1   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, opening_end_pnt)[1]
                end_offset_pnt2   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, self.offset_end_pnt)[1]
                offset_start_pnt  = start_offset_pnt1
                offset_end_pnt    = end_offset_pnt2
            else:
                start_offset_pnt1 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, opening_start_pnt)[1]
                start_offset_pnt2 = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, self.offset_start_pnt)[1]
                end_offset_pnt1   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, self.offset_end_pnt)[1]
                end_offset_pnt2   = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, opening_end_pnt)[1]
                offset_start_pnt  = start_offset_pnt2
                offset_end_pnt    = end_offset_pnt1

            HandleCreator.point_distance(handle_list, "StartPoint", start_offset_pnt1, start_offset_pnt2,
                                         input_field_above = self.input_field_above,
                                         center_point = axis_arc.Center.To3D)
            HandleCreator.point_distance(handle_list, "EndPoint", opening_end_pnt, end_offset_pnt2, False,
                                         center_point = axis_arc.Center.To3D)
            HandleCreator.point_distance(handle_list, "EndOffset", end_offset_pnt1, end_offset_pnt2, show_handles = False,
                                         input_field_above = self.input_field_above,
                                         center_point = axis_arc.Center.To3D)
            HandleCreator.point_distance(handle_list, "OffsetStartPoint", offset_start_pnt, end_offset_pnt1, False,
                                         center_point = axis_arc.Center.To3D)
            HandleCreator.point_distance(handle_list, "OffsetEndPoint", offset_end_pnt, start_offset_pnt2, False,
                                         center_point = axis_arc.Center.To3D)


        #----------------- handles for the linear axis

        else:
            offset_start_pnt     = self.offset_start_pnt + bottom_pnt
            offset_end_pnt       = self.offset_end_pnt + bottom_pnt

            if isinstance(self.general_ele_axis, AllplanGeo.Line2D):
                HandleCreator.point_distance(handle_list, "StartPoint", opening_start_pnt, offset_start_pnt, input_field_above = False)
                HandleCreator.point_distance(handle_list, "EndPoint", opening_end_pnt, offset_end_pnt)
                HandleCreator.point_distance(handle_list, "OffsetStartPoint", offset_start_pnt, opening_end_pnt, False)
                HandleCreator.point_distance(handle_list, "OffsetEndPoint", offset_end_pnt, opening_start_pnt, False)

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

        for index, tier_thickness in enumerate(AllplanEleAdapter.AxisElementAdapter(self.general_ele).GetTierThickness()):
            self.opening_tier_center.append(
                AllplanGeo.TransformCoord.PointGlobal(opening_line,
                                                      AllplanGeo.Point2D(x_center, y_start + tier_thickness / 2)).To2D)

            if index == opening_tier_index:
                self.opening_tier_ref_pnt = \
                    [AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(0, y_start + tier_thickness)).To2D,
                     AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(x_length, y_start + tier_thickness)).To2D,
                     AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(x_length, y_start)).To2D,
                     AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(0, y_start)).To2D]

                y_ref_pnt = y_start - 1000 if build_ele.OpeningSymbolRefPntIndex.value in {AllplanPalette.RefPointPosition.eTopLeft,
                                                                                           AllplanPalette.RefPointPosition.eTopRight} else \
                            y_start + tier_thickness + 1000

                symbol_ref_pnt = AllplanGeo.TransformCoord.PointGlobal(opening_line, AllplanGeo.Point2D(x_center, y_ref_pnt)).To2D

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
                self.modify_start_offset(value)

                return True

            case "EndPoint" | "EndOffset":
                self.modify_end_offset(value)

                return True

        return False


    def modify_start_offset(self,
                            offset: float):
        """ modify the start offset

        Args:
            offset: offset from the offset start point
        """

        loc_start_pnt_dist = AllplanGeo.TransformCoord.PointLocal(self.placement_ele, self.offset_start_pnt).X


        #----------------- calculate the new start point of the opening for a linear axis

        if isinstance(self.placement_ele, AllplanGeo.Line2D):
            self.opening_start_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele, loc_start_pnt_dist + offset)

            return


        #----------------- calculate the new start point of the opening for a circular axis

        found, opening_start_pnt = self.calc_point_at_placement_poly(loc_start_pnt_dist + offset)

        if found:
            self.opening_start_pnt = opening_start_pnt


    def modify_end_offset(self,
                            offset: float):
        """ modify the end offset

        Args:
            offset: offset from the offset end point
        """

        loc_end_pnt_dist = AllplanGeo.TransformCoord.PointLocal(self.placement_ele, self.offset_end_pnt).X


        #----------------- calculate the new start point of the opening for a linear axis

        if isinstance(self.placement_ele, AllplanGeo.Line2D):
            start_pnt_dist = loc_end_pnt_dist - offset - self.build_ele.Width.value

            self.opening_start_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele, start_pnt_dist)

            return


        #----------------- calculate the new start point of the opening for a circular axis

        found, opening_end_pnt = self.calc_point_at_placement_poly(loc_end_pnt_dist - offset)

        if not found:
            return

        self.opening_end_pnt = opening_end_pnt

        _, dir_ele = AllplanGeo.Polyline2DUtil.GetPolyline2DSegment(self.placement_polyline,
                                                                    self.opening_end_pnt.To2D)

        dir_ele.TrimStart(-100)

        err, opening_start_pnt = \
            AllplanGeo.Polygon2DUtil.FindPointOnPolygonWithDistance(AllplanGeo.Polygon2D(self.general_ele_geo.Points),
                                                                    self.opening_end_pnt.To2D,
                                                                    dir_ele.StartPoint,
                                                                    self.general_ele_axis,
                                                                    self.build_ele.Width.value)

        if not err:
            self.opening_start_pnt = opening_start_pnt.To3D


    def calc_point_at_placement_poly(self,
                                     local_dist: float) -> tuple[bool, AllplanGeo.Point3D]:
        """ calculate the point at the placement polyline for the arc

        Args:
            local_dist: local point distance at the placement arc

        Returns:
            found state, point at the polyline
        """

        ortho_start_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele,
                                                                AllplanGeo.Point2D(local_dist, 1000))
        ortho_end_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele,
                                                                AllplanGeo.Point2D(local_dist, -1000))

        ortho_line = AllplanGeo.Line2D(ortho_start_pnt.To2D, ortho_end_pnt.To2D)

        found, intersect_pnts = AllplanGeo.IntersectionCalculus(ortho_line, self.placement_polyline)

        return (True, intersect_pnts[0]) if found else (False, AllplanGeo.Point3D())


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
                dist = AllplanGeo.TransformCoord.PointLocal(self.placement_ele, input_pnt).X - \
                       AllplanGeo.TransformCoord.PointLocal(self.placement_ele, self.offset_start_pnt).X

                self.modify_start_offset(dist)

            case "EndPoint":
                dist = AllplanGeo.TransformCoord.PointLocal(self.placement_ele, self.offset_end_pnt).X - \
                       AllplanGeo.TransformCoord.PointLocal(self.placement_ele, input_pnt).X

                self.modify_end_offset(dist)

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

                build_ele.OpeningSymbolRefPntIndex.value = [AllplanPalette.RefPointPosition.eBottomLeft,
                                                            AllplanPalette.RefPointPosition.eBottomRight,
                                                            AllplanPalette.RefPointPosition.eTopRight,
                                                            AllplanPalette.RefPointPosition.eTopLeft][index]


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
