"""Example script showing labeling the reinforcement with a label with dimension line"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_Utility as AllplanUtil
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelWithDimensionLineBuildingElement import \
        LabelWithDimensionLineBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load LabelWithDimensionLine.py')


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

    return CreateElementResult([stirrups])


def create_stirrups() -> AllplanReinf.BarPlacement:
    """Create rectangular, closed stirrups:

    -   in YZ plane
    -   500 mm long and 1000 mm wide
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

    stirrup_shape = GeneralShapeBuilder.create_stirrup(length               = 500,
                                                       width                = 1000,
                                                       model_angles         = RotationAngles(90, 0, -90),
                                                       shape_props          = shape_props,
                                                       concrete_cover_props = ConcreteCoverProperties.all(0),
                                                       stirrup_type         = AllplanReinf.StirrupType.Normal)

    return LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(position             = 1,
                                                                        shape                = stirrup_shape,
                                                                        from_point           = AllplanGeo.Point3D(),
                                                                        to_point             = AllplanGeo.Point3D(2000, 0, 0),
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


    label = AllplanReinf.ReinforcementLabel(reinforcementType    = AllplanReinf.Bar,
                                            type                 = AllplanReinf.LabelWithDimensionLine,
                                            positionNumber       = 1,
                                            labelProp            = label_props,
                                            bDimLineAtShapeStart = build_ele.DimLineAtShapeStart.value,
                                            dimLineOffset        = build_ele.DimLineOffset.value)


    # additional label properties

    # show only selected bars in the linear placement
    if build_ele.SetVisibleBars.value:
        visible_bar_ids = [int(id) for id in build_ele.VisibleBars.value.split(',')]
        label.SetVisibleBars(AllplanUtil.VecIntList(visible_bar_ids))

    # move the label away from the dimension line
    if build_ele.SetLabelOffset.value:
        label.SetLabelOffset(build_ele.LabelOffset.value)

    # set custom text at the end of the label
    if build_ele.SetAdditionalText.value:
        label.SetAdditionalText(build_ele.AdditionalText.value)

    # show bar markers on the dimension line for all bars or just the first and last one
    label.ShowAllBars(build_ele.ShowAllBars.value)

    label.TextProperties           = text_props
    label.ShowTextPointer          = build_ele.ShowTextPointer.value
    label.PointerProperties        = build_ele.PointerProperties.value

    return label
