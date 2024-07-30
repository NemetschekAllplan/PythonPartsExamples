"""Example script showing the implementation of the ReinforcementShapeBuilder class
from the NemAll_Python_Reinforcement module to create a free form, two-dimensional
bar shape consisting of straight legs and using BarShapeSideDataList
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinforcement
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from PreviewSymbols import PreviewSymbols
from StdReinfShapeBuilder.BarShapeSideDataList import BarShapeSideDataList
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections import ModelEleList
from Utils.TextReferencePointPosition import TextReferencePointPosition

if TYPE_CHECKING:
    from __BuildingElementStubFiles.FreeFormReinforcementShapeBuilderBuildingElement import \
        FreeFormReinforcementShapeBuilderBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: FreeFormReinforcementShapeBuilder.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version: str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element containing parameters specified by the user in the palette
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of element

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        created elements
    """
    shape     = create_shape(build_ele)
    placement = create_placement(shape)

    print("\n-------------- Shape ----------------")
    print(shape)
    print("-------------------------------------")

    lines, numbering = create_reference_lines(build_ele)

    return CreateElementResult(elements         = [placement],
                               preview_elements = lines,
                               preview_symbols  = numbering)


def create_shape(build_ele: BuildingElement) -> AllplanReinforcement.BendingShape:
    """Create a free form shape using the ReinforcementShapeBuilder class from
    the NemAll_Python_Reinforcement module based on the parameter values
    given by the user in the property palette.

    Args:
        build_ele: building element containing parameter values from the palette

    Returns:
        bending shape
    """
    # set shape properties based on the values from the property palette
    shape_props = ReinforcementShapeProperties.rebar(build_ele.Diameter.value,
                                                     build_ele.BendingRoller.value,
                                                     build_ele.SteelGrade.value,
                                                     build_ele.ConcreteGrade.value,
                                                     AllplanReinforcement.BendingShapeType.names[build_ele.BendingShapeType.value])

    # create the shape data based on the values from the property palette
    # the sides are defined as a list of three element tuples like:
    # (side_start: Point2D, side_end: Point2D, concrete_cover: float)

    shape_data = BarShapeSideDataList([build_ele.CoverAtStart.value] +
                                      build_ele.BarShapeSideData.value +
                                      [build_ele.CoverAtEnd.value])

    # initialize the shape builder and add sides
    shape_builder = AllplanReinforcement.ReinforcementShapeBuilder()
    shape_builder.AddSides(shape_data)

    # if the option was set in the palette, create a hook at start and/or end of the rebar
    if build_ele.SetStartHook.value:
        shape_builder.SetHookStart(length = build_ele.StartHookLength.value,
                                   angle  = build_ele.StartHookAngle.value,
                                   type   = AllplanReinforcement.HookType.names[build_ele.StartHookType.value])

    if build_ele.SetEndHook.value:
        shape_builder.SetHookEnd(length = build_ele.EndHookLength.value,
                                 angle  = build_ele.EndHookAngle.value,
                                 type   = AllplanReinforcement.HookType.names[build_ele.EndHookType.value])

    # if the option was set in the palette, change the length of the first and/or last leg
    # of the rebar to anchor the rebar or override the leg's length

    if build_ele.SetAtStart.value == "Anchorage":
        shape_builder.SetAnchorageLengthStart(build_ele.StartSideOrAnchorageLength.value)

    elif build_ele.SetAtStart.value == "SideLength":
        shape_builder.SetSideLengthStart(build_ele.StartSideOrAnchorageLength.value)

    if build_ele.SetAtEnd.value == "Anchorage":
        shape_builder.SetAnchorageLengthEnd(build_ele.EndSideOrAnchorageLength.value)

    if build_ele.SetAtEnd.value == "SideLength":
        shape_builder.SetSideLengthEnd(build_ele.EndSideOrAnchorageLength.value)

    # create the bending shape
    shape = shape_builder.CreateShape(shape_props)

    return shape if shape.IsValid else AllplanReinforcement.BendingShape()


def create_placement(shape: AllplanReinforcement.BendingShape) -> AllplanReinforcement.BarPlacement:
    """Create the rebar placement containing only one rebar of the given shape

    Args:
       shape:   bending shape to create placement for

    Returns:
        rebar placement with one rebar
    """

    # define placement start and end point
    start_point = AllplanGeo.Point3D(0, 0, 0)
    end_point   = AllplanGeo.Point3D(0, 0, 1000)

    return LinearBarBuilder.create_linear_bar_placement_from_to_by_count(position             = 1,
                                                                         shape                = shape,
                                                                         from_point           = start_point,
                                                                         to_point             = end_point,
                                                                         concrete_cover_left  = 0,
                                                                         concrete_cover_right = 0,
                                                                         bar_count            = 1)


def create_reference_lines(build_ele: BuildingElement) -> tuple[ModelEleList, PreviewSymbols]:
    """Creates the model elements and preview symbols representing the reference
    lines of the rebar shape sides with arrows indicating the side direction
    and a number of the side

    Args:
        build_ele: building element containing parameters from the property palette

    Returns:
         model element list with the 2D lines
         preview elements with side numbers and arrows
    """
    common_properties = AllplanBaseElements.CommonProperties()
    common_properties.Color = 6

    # create the 2d lines

    line_elements = ModelEleList(common_properties)
    lines: list[AllplanGeo.Line2D] = []

    for shape_side in build_ele.BarShapeSideData.value:
        line_2d = AllplanGeo.Line2D(shape_side[0], shape_side[1])
        lines.append(line_2d)
        line_elements.append_geometry_2d(line_2d)

    # create the preview symbols: arrows indicating the line direction and numbers

    numbering = PreviewSymbols()

    for idx, line in enumerate(lines):
        if AllplanGeo.CalcLength(line) == 0:
            continue
        line_center = AllplanGeo.Point3D(line.GetCenterPoint())

        numbering.add_arrow(line_center,
                            width          = 10,
                            color          = 6,
                            rotation_angle = line.GetAngle())

        move_vector = line.GetVector().Orthogonal()
        move_vector.Reverse()
        move_vector.Normalize(50)
        text_ref_point = AllplanGeo.Move(line_center,
                                         AllplanGeo.Vector3D(move_vector.X,
                                                             move_vector.Y,
                                                             0))

        numbering.add_text(text            = str(idx),
                           reference_point = text_ref_point,
                           ref_pnt_pos     = TextReferencePointPosition.CENTER_CENTER,
                           height          = 50.0,
                           color           = 6,
                           rotation_angle  = AllplanGeo.Angle())

    return line_elements, numbering
