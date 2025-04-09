""" Script for LabelBarPlacementWithDimLine
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.Reinforcement.DimensionLinePropertiesParameterUtil import DimensionLinePropertiesParameterUtil
from ParameterUtils.Reinforcement.LabelPropertiesParameterUtil import LabelPropertiesParameterUtil

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.ElementFilter.ReinforcementElementsFilterUtil import ReinforcementElementsFilterUtil
from Utils.Reinforcement.BarsDimLinePlacement import BarsDimLinePlacement
from Utils.Reinforcement.BarsRepresentationUtil import BarsRepresentationUtil
from Utils.Reinforcement.BarsRepresentationLineUtil import BarsRepresentationLineUtil
from Utils.Reinforcement.LabelingUtil import LabelingUtil

from ScriptObjectInteractors.BaseFilterObject import BaseFilterObject

from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelBarPlacementWithDimLineBuildingElement \
        import LabelBarPlacementWithDimLineBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load LabelBarPlacementWithDimLine.py')


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
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ReinforcementExamples\Labels\LabelBarPlacementWithDimLine.png"))


def create_script_object(build_ele  : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return LabelBarPlacementWithDimLine(build_ele, script_object_data)


class LabelBarPlacementWithDimLine(BaseScriptObject):
    """ Definition of class LabelBarPlacementWithDimLine
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

        self.build_ele = build_ele

        self.sel_result       = MultiElementSelectInteractorResult()
        self.bars_rep_ele     = list[AllplanReinf.BarsRepresentation]()
        self.is_bars_rep_line = list[bool]()
        self.labeled_bars_rep = list[AllplanReinf.BarsRepresentation]()
        self.handle_list      = list[HandleProperties]()

        self.label_placement: BarsDimLinePlacement
        self.dim_lines      : list[AllplanGeo.Line2D] = []

        self.bars_ref_line_util = BarsRepresentationLineUtil()

        self.hidden_elements  = AllplanEleAdapter.BaseElementAdapterList()
        self.visible_bar_ele = AllplanEleAdapter.BaseElementAdapterList()

        if not build_ele.SetVisibleBarsDimLine.value:
            build_ele.SetVisibleBarsDimLine.value = True


    def start_input(self):
        """ start the input
        """

        class BarsRepLineFilter(BaseFilterObject):
            """ Filter for the bars representation line count
            """

            def __call__(self,
                         element: AllplanEleAdapter.BaseElementAdapter) -> bool:
                """ execute the filtering

                Args:
                    element: element to filter

                Returns:
                    element fulfills the filter: True/False
                """

                bars_rep_util = BarsRepresentationUtil(cast(AllplanReinf.BarsRepresentation, AllplanBaseEle.GetElement(element)))

                return bars_rep_util.is_placement_labeling()[0] and  bars_rep_util.are_all_bars_visible_in_representation()


        bars_rep_filter = ReinforcementElementsFilterUtil.create_linear_bar_placement_filter()
        bars_rep_filter.append(BarsRepLineFilter())

        self.script_object_interactor = MultiElementSelectInteractor(self.sel_result, bars_rep_filter,
                                                                     "Select the bar represetation(s)")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        self.bars_rep_ele.clear()
        self.is_bars_rep_line.clear()

        for bars_rep in AllplanBaseEle.GetElements(self.sel_result.sel_elements):
            bars_rep_util = BarsRepresentationUtil(bars_rep)

            placement_label, is_bars_rep_line = bars_rep_util.is_placement_labeling()

            if placement_label and bars_rep_util.are_all_bars_visible_in_representation():
                self.bars_rep_ele.append(bars_rep)
                self.is_bars_rep_line.append(is_bars_rep_line)

        if not self.bars_rep_ele:
            return

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.LABEL_INPUT

        self.label_placement = BarsDimLinePlacement(self.bars_rep_ele)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.labeled_bars_rep.clear()
        self.label_placement.reset()
        self.dim_lines.clear()

        self.hidden_elements.clear()
        self.visible_bar_ele.clear()

        self.bars_ref_line_util.clear()

        for bars_rep, is_bars_rep_line in zip(self.bars_rep_ele, self.is_bars_rep_line):
            self.create_dim_line_label(bars_rep, is_bars_rep_line)

        self.create_dim_line_handles()

        AllplanIFW.VisibleService.ShowAllElements()
        AllplanIFW.VisibleService.ShowElements(self.hidden_elements, False)
        AllplanIFW.VisibleService.ShowElements(self.visible_bar_ele, True)

        return CreateElementResult(self.labeled_bars_rep, self.handle_list,
                                   placement_point = AllplanGeo.Point3D(), multi_placement = True, as_static_preview = True)


    def create_dim_line_label(self,
                              bars_rep: AllplanReinf.BarsRepresentation,
                              is_bars_rep_line: bool):
        """ Create a dimension line label

        Args:
            bars_rep: bars representation
            is_bars_rep_line: line representation state
        """

        bars_rep_util = BarsRepresentationUtil(bars_rep)

        build_ele = self.build_ele

        text_props = AllplanBasisEle.TextProperties()

        created, at_start, dim_line_offset, text_align, dim_line = \
            self.label_placement.get_dim_line_position(bars_rep,
                                                       bars_rep_util,
                                                       build_ele.DimLineOffset.value,
                                                       build_ele.DimLineDistance.value,
                                                       build_ele.DimLineAngleFrom.value,
                                                       build_ele.DimLineAngleTo.value,
                                                       text_props.Height * self.document.GetScalingFactor())

        if not created:
            return

        text_props.Alignment = text_align

        label_props = LabelPropertiesParameterUtil.create_label_properties(build_ele, "DimLine")

        label = AllplanReinf.ReinforcementLabel(reinforcementType    = AllplanReinf.ReinforcementType.Bar,
                                                type                 = AllplanReinf.LabelType.LabelWithDimensionLine,
                                                positionNumber       = bars_rep.GetBarPlacement().PositionNumber,
                                                labelProp            = label_props,
                                                bDimLineAtShapeStart = at_start,
                                                dimLineOffset        = dim_line_offset)

        DimensionLinePropertiesParameterUtil.create_dim_line_properties(build_ele, label, "DimLine")

        label.TextProperties = text_props


        #----------------- check the visible bars

        if is_bars_rep_line and build_ele.SetVisibleBarsDimLine.value and build_ele.VisibleBarsDimLine.value:
            self.hidden_elements.append(bars_rep.GetBaseElementAdapter())

            label.VisibleBars = self.bars_ref_line_util.get_visible_bars(self.visible_bar_ele, bars_rep,
                                                                         build_ele.VisibleBarsDimLine.value)


        #----------------- set the label point in case of bar intersection

        bars_rep.Label = label

        label.LabelOffset = self.label_placement.get_label_offset(bars_rep, dim_line,
                                                                  self.bars_ref_line_util,
                                                                  label.TextProperties.Height * self.document.GetScalingFactor())

        bars_rep.Label = label

        self.labeled_bars_rep.append(bars_rep)

        self.dim_lines.append(dim_line)


    def create_dim_line_handles(self):
        """ create the dimension line handles
        """

        self.handle_list.clear()

        rot_angle = AllplanGeo.Angle(math.pi / 2)

        left_fac  = 1 / 3
        right_fac = 2 / 3

        for bars_rep, dim_line in zip(self.labeled_bars_rep, self.dim_lines):
            dist_vec = AllplanGeo.Vector2D(dim_line.StartPoint, dim_line.EndPoint)

            dim_line_angle = dist_vec.GetAngle()

            move_fac = right_fac if LabelingUtil.is_swap_text_angle(dim_line_angle) else left_fac

            swap_fac = 1 - move_fac

            HandleCreator.move_in_direction(self.handle_list, f"Move_{bars_rep.GetBaseElementAdapter().GetModelElementUUID()}",
                                            (dim_line.StartPoint + dist_vec * move_fac).To3D,
                                            AllplanGeo.CalcAngle(dim_line)[0] + rot_angle,
                                            "Move dimension line")

            HandleCreator.move(self.handle_list, f"Swap_{bars_rep.GetBaseElementAdapter().GetModelElementUUID()}",
                                (dim_line.StartPoint + dist_vec * swap_fac).To3D,  "Swap dimension line position", True)


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        if cast(str, handle_prop.handle_id).startswith("Swap_"):
            self.label_placement.swap_dim_line_position(AllplanEleAdapter.GUID.FromString(cast(str, handle_prop.handle_id)[5:]))

            return


        #----------------- get the index of the bars representation element

        bars_rep_ele_guid = AllplanEleAdapter.GUID.FromString(cast(str, handle_prop.handle_id)[5:])

        index = next(i for i, ele in enumerate(self.labeled_bars_rep) \
                     if ele.GetBaseElementAdapter().GetModelElementUUID() == bars_rep_ele_guid)


        #----------------- get the new position of the label

        label = self.labeled_bars_rep[index].GetLabel()

        distance = AllplanGeo.TransformCoord.PointLocal(self.dim_lines[index], input_pnt).Y

        label.DimensionLineOffset = label.DimensionLineOffset + (-distance if label.DimensionLineAtShapeStart else distance)

        label.LabelOffset = self.label_placement.get_label_offset(self.labeled_bars_rep[index], self.dim_lines[index],
                                                                 self.bars_ref_line_util,
                                                                 label.TextProperties.Height * self.document.GetScalingFactor())

        self.labeled_bars_rep[index].Label = label

        self.dim_lines[index] = AllplanGeo.Offset(self.dim_lines[index], distance)[1]

        self.create_dim_line_handles()

        self.label_placement.set_dim_line_position(bars_rep_ele_guid, label.DimensionLineOffset, self.dim_lines[index])

        return


    def process_mouse_move(self,
                           input_pnt: AllplanGeo.Point3D):
        """ Process the mouse move event

        Args:
            input_pnt: input point
        """

        AllplanIFW.HighlightService.CancelAllHighlightedElements(self.document.GetDocumentID())

        text_dist = AllplanBasisEle.TextProperties().Height * self.document.GetScalingFactor()

        if (bars_rep_ele_guid := self.label_placement.select_dim_line_bars_rep(input_pnt, self.build_ele.DimLineDistance.value / 2,
                                                                              text_dist)) is not None:
            bars_rep_ele = AllplanEleAdapter.BaseElementAdapter.FromGUID(bars_rep_ele_guid, self.document)

            elements = AllplanEleAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(bars_rep_ele)

            AllplanIFW.HighlightService.HighlightElements(elements)
