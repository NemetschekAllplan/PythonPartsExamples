"""Example script showing labeling the reinforcement with a label with pointer"""

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
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from Utils.TextReferencePointPosition import TextReferencePointPosition

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelWithPointerBuildingElement import \
        LabelWithPointerBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load LabelWithPointer.py')


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
    label    = create_label(build_ele)

    stirrups.SetLabel(label, AllplanElementAdapter.AssocViewElementAdapter())

    preview_symbols = create_preview_symbols(build_ele, stirrups.GetBendingShape())

    return CreateElementResult([stirrups],
                               preview_symbols=preview_symbols)


def create_stirrups() -> AllplanReinf.BarPlacement:
    """Create rectangular, closed stirrups:

    -   in XY plane
    -   500 mm long and 1000 mm wide
    -   8 mm diameter
    -   placed along Z+ axis
    -   with 200 mm spacing

    Returns:
        Linear placement of the stirrups
    """

    shape_props = ReinforcementShapeProperties.rebar(diameter           = 8,
                                                     bending_roller     = 4.0,
                                                     steel_grade        = -1,
                                                     concrete_grade     = -1,
                                                     bending_shape_type = AllplanReinf.Stirrup)

    stirrup_shape = GeneralShapeBuilder.create_stirrup(length               = 500,
                                                       width                = 1000,
                                                       model_angles         = RotationAngles(0, 0, 0),
                                                       shape_props          = shape_props,
                                                       concrete_cover_props = ConcreteCoverProperties.all(0),
                                                       stirrup_type         = AllplanReinf.StirrupType.Normal)

    return LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(position             = 1,
                                                                        shape                = stirrup_shape,
                                                                        from_point           = AllplanGeo.Point3D(),
                                                                        to_point             = AllplanGeo.Point3D(0, 0, 1000),
                                                                        concrete_cover_left  = 0,
                                                                        concrete_cover_right = 0,
                                                                        bar_distance         = 200)


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
    label_props.ShowBarDistance    = build_ele.ShowBarDistance.value
    label_props.ShowBarCount       = build_ele.ShowBarCount.value
    label_props.ShowBendingShape   = build_ele.ShowBendingShape.value
    label_props.ShowBarPlace       = build_ele.ShowBarPlace.value
    label_props.ShowBarLength      = build_ele.ShowBarLength.value
    label_props.ShowSteelGrade     = build_ele.ShowSteelGrade.value
    label_props.ShowPositionAtEnd  = build_ele.ShowPositionAtEnd.value
    label_props.ShowTwoLineText    = build_ele.ShowTwoLineText.value

    # text properties
    text_props           = AllplanBasisElements.TextProperties()
    text_props.Alignment = AllplanBasisElements.TextAlignment.names[build_ele.TextAlignment.value]

    # place label by point
    if build_ele.LabelPositionDefinition.value == 1:
        label = AllplanReinf.ReinforcementLabel(reinforcementType = AllplanReinf.Bar,
                                                type              = AllplanReinf.LabelType.LabelWithPointer,
                                                positionNumber    = 1,
                                                labelProp         = label_props,
                                                labelPoint        = build_ele.LabelPoint.value,
                                                angle             = AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

    # place label by shape leg and offset to it
    else:
        label = AllplanReinf.ReinforcementLabel(reinforcementType = AllplanReinf.ReinforcementType.Bar,
                                                type              = AllplanReinf.LabelType.LabelWithPointer,
                                                positionNumber    = 1,
                                                labelProp         = label_props,
                                                shapeSide         = build_ele.ShapeSide.value,
                                                shapeSideFactor   = build_ele.ShapeSideFactor.value,
                                                labelOffset       = build_ele.LabelOffset.value,
                                                angle             = AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

    # additional label properties

    if build_ele.SetPointerStartPoint.value:
        label.SetPointerStartPoint(build_ele.PointerStartPoint.value)

    if build_ele.SetAdditionalText.value:
        label.SetAdditionalText(build_ele.AdditionalText.value)

    label.SetTextProperties(text_props)
    label.SetShowTextPointer(build_ele.ShowTextPointer.value)
    label.SetShowTextPointerEndSymbol(build_ele.ShowTextPointerEndSymbol.value)

    return label

def create_preview_symbols(build_ele: BuildingElement,
                           bending_shape: AllplanReinf.BendingShape) -> PreviewSymbols:
    """Creates symbols for preview, depending on label placement option:

    -   Create label by point:                  a cross indicating placement point of the label is created
    -   Create label by shape leg and offset:   numbers indicating the legs indices are created

    Args:
        build_ele:      building element with parameter properties
        bending_shape:  labeled bending shape

    Returns:
        preview symbols object containing the cross/numbers
    """

    preview_symbols = PreviewSymbols()

    if build_ele.LabelPositionDefinition.value == 1:
        preview_symbols.add_cross(AllplanGeo.Point3D(build_ele.LabelPoint.value),
                                  width = 40,
                                  color = 6)
    else:
        shape_lines = bending_shape.GetShapePolyline().GetLines()
        for idx, line in enumerate(shape_lines, start= 1):
            _, line_center = AllplanGeo.CenterCalculus.Calculate(line)
            preview_symbols.add_text(str(idx),
                                     line_center,
                                     TextReferencePointPosition.CENTER_CENTER,
                                     height         = 40,
                                     color          = 6,
                                     rotation_angle = AllplanGeo.Angle())
    return preview_symbols
