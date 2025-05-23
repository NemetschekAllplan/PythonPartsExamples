﻿""" base class for the opening modification
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import abc

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService

from ParameterUtils.VerticalOpeningGeometryPropertiesParameterUtil import VerticalOpeningGeometryPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils.HideElementsService import HideElementsService
from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil
from Utils.Architecture.OpeningModificationUtil import OpeningModificationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeneralOpeningBuildingElement import GeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


class ModifyOpeningBase(BaseScriptObject):
    """ base class for the opening modification
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

        self.build_ele = cast(BuildingElement, build_ele)

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT

        self.opening_sel_res   = SingleElementSelectResult()
        self.opening_start_pnt = AllplanGeo.Point3D()
        self.opening_end_pnt   = AllplanGeo.Point3D()
        self.offset_start_pnt  = AllplanGeo.Point3D()
        self.offset_end_pnt    = AllplanGeo.Point3D()

        self.placement_line     : AllplanGeo.Line2D                              = AllplanGeo.Line2D()
        self.placement_arc      : AllplanGeo.Arc2D                               = AllplanGeo.Arc2D()
        self.placement_ele_geo  : (AllplanGeo.Polygon2D | AllplanGeo.Polyline2D) = AllplanGeo.Polygon2D()
        self.placement_ele_axis : (AllplanGeo.Line2D | AllplanGeo.Arc2D)         = AllplanGeo.Line2D()
        self.placement_ele      : AllplanEleAdapter.BaseElementAdapter           = AllplanEleAdapter.BaseElementAdapter()
        self.opening_ele        : AllplanEleAdapter.BaseElementAdapter           = AllplanEleAdapter.BaseElementAdapter()

        self.hide_ele = HideElementsService()

        self.opening_tier_center  : list[AllplanGeo.Point2D]       = []
        self.opening_tier_ref_pnt : tuple[AllplanGeo.Point2D, ...] = tuple()

        self.opening_geo_param_util = VerticalOpeningGeometryPropertiesParameterUtil(build_ele, "")

        self.input_field_above = False


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        build_ele.InputMode.value = build_ele.OPENING_INPUT

        self.script_object_interactor = None

        self.opening_ele = OpeningModificationUtil.get_opening_element(self.opening_sel_res.sel_element)


        #----------------- get the parent data

        self.placement_ele, self.placement_ele_geo, self.placement_line, self.placement_ele_axis = \
            OpeningModificationUtil.get_placement_element(self.opening_ele, self.opening_start_pnt.To2D)

        build_ele.ElementThickness.value = AllplanEleAdapter.AxisElementAdapter(self.placement_ele).GetThickness()
        build_ele.ElementTierCount.value = max(1, AllplanEleAdapter.AxisElementAdapter(self.placement_ele).GetTiersCount())


        #----------------- get the left and right point for the opening offset

        created, start_offset, end_offset = OpeningPointsUtil.get_opening_offset_points(self.placement_ele,
                                                                                        self.opening_start_pnt.To2D,
                                                                                        self.opening_end_pnt.To2D,
                                                                                        self.placement_line)

        if created:
            self.offset_start_pnt = start_offset.To3D
            self.offset_end_pnt   = end_offset.To3D


        #----------------- get the placement arc for the circular axis

        if isinstance(self.placement_ele_axis, AllplanGeo.Arc2D):
            self.placement_arc, place_at_bottom = \
                AllplanArchEle.ArchitectureElementsGeometryService.CreatePlacementArc(self.placement_ele,
                                                                                      self.placement_ele_axis,
                                                                                      self.opening_start_pnt.To2D,
                                                                                      self.opening_end_pnt.To2D)
            self.input_field_above = not place_at_bottom


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.hide_placement_element()

        return CreateElementResult(self.modify_opening_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())

    @abc.abstractmethod
    def modify_opening_element(self) -> ModelEleList:
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


    def hide_placement_element(self):
        """ hide the general element
        """

        build_ele = self.build_ele

        has_independent_interaction = False

        if build_ele.get_property("HasIndependent2DInteraction") is not None:
            has_independent_interaction = build_ele.HasIndependent2DInteraction.value

        self.hide_ele.hide_opening_parent_element(self.placement_ele, has_independent_interaction)


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
                if (result := OpeningPointsUtil.get_start_point_from_start_offset(self.placement_ele_axis, self.offset_start_pnt.To2D,
                                                                                  self.placement_line, self.placement_arc,
                                                                                  self.placement_ele_geo, value)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

                return True

            case "EndPoint" | "EndOffset":
                if (result := OpeningPointsUtil.get_start_point_from_end_offset(self.placement_ele_axis, self.offset_end_pnt.To2D,
                                                                                self.placement_line, self.placement_arc,
                                                                                self.build_ele.Width.value,
                                                                                self.placement_ele_geo, value)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

                return True

        return False


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        build_ele = self.build_ele

        match handle_prop.handle_id:
            case "StartPoint":
                offset = OpeningPointsUtil.get_distance_from_offset_start_point(input_pnt, self.placement_ele_axis,
                                                                                self.offset_start_pnt.To2D,
                                                                                self.placement_line, self.placement_arc,
                                                                                self.placement_ele_geo)

                if (result := OpeningPointsUtil.get_start_point_from_start_offset(self.placement_ele_axis, self.offset_start_pnt.To2D,
                                                                                  self.placement_line, self.placement_arc,
                                                                                  self.placement_ele_geo, offset)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

            case "EndPoint":
                offset = OpeningPointsUtil.get_distance_from_offset_end_point(input_pnt, self.placement_ele_axis,
                                                                              self.offset_end_pnt.To2D,
                                                                              self.placement_line, self.placement_arc,
                                                                              self.placement_ele_geo)

                if (result := OpeningPointsUtil.get_start_point_from_end_offset(self.placement_ele_axis, self.offset_end_pnt.To2D,
                                                                                self.placement_line, self.placement_arc,
                                                                                self.build_ele.Width.value,
                                                                                self.placement_ele_geo, offset)) and result[0]:
                    self.opening_start_pnt = result[1].To3D

            case "OffsetStartPoint":
                self.offset_start_pnt   = input_pnt
                self.offset_start_pnt.Z = 0

            case "OffsetEndPoint":
                self.offset_end_pnt   = input_pnt
                self.offset_end_pnt.Z = 0

            case "SymbolRefPoint":
                build_ele.OpeningSymbolRefPntIndex.value = OpeningPointsUtil.select_opening_symbol_ref_pnt(input_pnt,
                                                                                                           self.opening_tier_ref_pnt)

            case _:
                HandlePropertiesService.update_property_value(self.build_ele, handle_prop, input_pnt)


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

        AllplanIFW.HandleService().RemoveHandles()
        AllplanIFW.BuildingElementInputControls().CloseControls()

        AllplanBaseEle.ModifyElements(self.document, self.modify_opening_element())

        AllplanIFW.HandleService().RemoveHandles()

        return OnCancelFunctionResult.RESTART
