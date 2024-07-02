"""Example script showing labeling the reinforcement with a label with fan"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from PreviewSymbols import PreviewSymbols
from StdReinfShapeBuilder.BarShapePlacementUtil import BarShapePlacementUtil
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelWithFanBuildingElement import LabelWithFanBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement



print('Load LabelWithFan.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of the stirrups and labels

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        created elements
    """
    stirrups = create_stirrups()
    longitudinal_bars = create_longitudinal_bars(stirrups)

    reinforcement: list[AllplanReinf.BarPlacement] = []
    reinforcement.append(stirrups)
    reinforcement.extend(longitudinal_bars)

    label    = create_label(build_ele)

    longitudinal_bars[0].SetLabel(label, AllplanElementAdapter.AssocViewElementAdapter())

    return CreateElementResult(reinforcement,
                               preview_symbols = create_preview_symbols(build_ele))


def create_stirrups() -> AllplanReinf.BarPlacement:
    """Create rectangular, closed stirrups:

    -   in YZ plane
    -   300 mm long and 500 mm wide
    -   8 mm diameter
    -   placed along X+ axis
    -   with 200 mm spacing

    Returns:
        Linear placement of the stirrups
    """

    shape_props = ReinforcementShapeProperties.rebar(diameter           = 8,
                                                     bending_roller     = 4.0,
                                                     steel_grade        = -1,
                                                     concrete_grade     = -1,
                                                     bending_shape_type = AllplanReinf.Stirrup)

    stirrup_shape = GeneralShapeBuilder.create_stirrup(length               = 300,
                                                       width                = 500,
                                                       model_angles         = RotationAngles(0, 0, 0),
                                                       shape_props          = shape_props,
                                                       concrete_cover_props = ConcreteCoverProperties.all(0),
                                                       stirrup_type         = AllplanReinf.StirrupType.Normal)

    return LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(position             = 1,
                                                                        shape                = stirrup_shape,
                                                                        from_point           = AllplanGeo.Point3D(),
                                                                        to_point             = AllplanGeo.Point3D(0, 0, 2000),
                                                                        concrete_cover_left  = 0,
                                                                        concrete_cover_right = 0,
                                                                        bar_distance         = 200)

def create_longitudinal_bars(stirrup_placement: AllplanReinf.BarPlacement) -> list[AllplanReinf.BarPlacement]:
    """Place the longitudinal bar in the corner of the stirrups.

    Args:
        stirrup_placement:  placement of rectangular, closed stirrups

    Returns:
        placement of longitudinal bar placements
    """

    longitudinal_bar_props = ReinforcementShapeProperties.rebar(diameter           = 20,
                                                                bending_roller     = 4.0,
                                                                steel_grade        = -1,
                                                                concrete_grade     = -1,
                                                                bending_shape_type = AllplanReinf.LongitudinalBar)

    place_util = BarShapePlacementUtil()
    place_util.add_shape("stirrup", stirrup_placement.GetBendingShape())

    # calculate the placement points in all four corners of the stirrup
    placement_pnts = [place_util.get_placement_in_corner("stirrup",
                                                         corner_number      = i,
                                                         placement_diameter = longitudinal_bar_props.diameter,
                                                         local_angles       = RotationAngles(0,0,0))
                      for i in range(1,5)]

    longitudinal_bar_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(
        length               = 2000,
        model_angles         = RotationAngles(0,-90,0),
        shape_props          = longitudinal_bar_props,
        concrete_cover_props = ConcreteCoverProperties.all(0),
        start_hook           = -1,
        end_hook             = -1)

    bars = []

    for placement_pnt in placement_pnts:
        shape_copy = AllplanReinf.BendingShape(longitudinal_bar_shape)
        shape_copy.Move(AllplanGeo.Vector3D(placement_pnt))
        bars.append(AllplanReinf.BarPlacement(2,1,
                                              AllplanGeo.Vector3D(),
                                              AllplanGeo.Point3D(),
                                              AllplanGeo.Point3D(),
                                              shape_copy))
    return bars

def create_label(build_ele: BuildingElement) -> AllplanReinf.ReinforcementLabel:
    """Create labels of the reinforcement based on the parameters in the property palette

    Args:
        build_ele:      building element with parameter properties

    Returns:
        Reinforcement label
    """

    # label properties
    label_props                    = AllplanReinf.ReinforcementLabelProperties()
    label_props.ShowPositionNumber = build_ele.ShowPositionNumber.value
    label_props.ShowBarDiameter    = build_ele.ShowBarDiameter.value
    label_props.ShowBarCount       = build_ele.ShowBarCount.value
    label_props.ShowBendingShape   = build_ele.ShowBendingShape.value
    label_props.ShowBarPlace       = build_ele.ShowBarPlace.value
    label_props.ShowBarLength      = build_ele.ShowBarLength.value
    label_props.ShowSteelGrade     = build_ele.ShowSteelGrade.value
    label_props.ShowPositionAtEnd  = build_ele.ShowPositionAtEnd.value
    # label_props.ShowTwoLineText    = build_ele.ShowTwoLineText.value      # this property can't be set to True in 2024-0-1

    # text properties
    text_props           = AllplanBasisElements.TextProperties()
    text_props.Alignment = AllplanBasisElements.TextAlignment.names[build_ele.TextAlignment.value]


    label = AllplanReinf.ReinforcementLabel(reinforcementType    = AllplanReinf.Bar,
                                            type                 = AllplanReinf.LabelWithFan,
                                            positionNumber       = 2,
                                            labelProp            = label_props,
                                            labelPoint           = build_ele.LabelPoint.value,
                                            angle                = AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

    # set custom text at the end of the label
    if build_ele.SetAdditionalText.value:
        label.SetAdditionalText(build_ele.AdditionalText.value)

    label.SetTextProperties(text_props)
    label.SetShowTextPointer(build_ele.ShowTextPointer.value)
    label.SetShowTextPointerEndSymbol(build_ele.ShowTextPointerEndSymbol.value)

    return label

def create_preview_symbols(build_ele: BuildingElement) -> PreviewSymbols:
    """Creates a cross indicating reference point of the label

    Args:
        build_ele:      building element with parameter properties

    Returns:
        preview symbols object containing the cross
    """

    preview_symbols = PreviewSymbols()
    preview_symbols.add_cross(AllplanGeo.Point3D(build_ele.LabelPoint.value),
                              width = 40,
                              color = 6)

    return preview_symbols
