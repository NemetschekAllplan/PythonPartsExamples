"""Example script showing the implementation of the ReinforcementShapeBuilder class
from the NemAll_Python_Reinforcement module to create a closed stirrup.
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
from StdReinfShapeBuilder.BarShapePointDataList import BarShapePointDataList
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections import ModelEleList
from Utils.TextReferencePointPosition import TextReferencePointPosition

if TYPE_CHECKING:
    from __BuildingElementStubFiles.StirrupReinforcementShapeBuilderBuildingElement import \
        StirrupReinforcementShapeBuilderBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: StirrupReinforcementShapeBuilder.py')


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

    return CreateElementResult(elements         = [placement],
                               preview_elements = create_shape_outline(build_ele),
                               preview_symbols  = create_point_numbers(build_ele))


def create_shape(build_ele: BuildingElement) -> AllplanReinforcement.BendingShape:
    """Create a closed stirrup shape using the ReinforcementShapeBuilder
    class from the NemAll_Python_Reinforcement module based on the parameter values
    given by the user in the property palette

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
    # the points are defined as a list of tuples (shape_point: Point2D, concrete_cover: float)
    shape_data = BarShapePointDataList(build_ele.BarShapePointData.value)

    # initialise the shape builder
    shape_builder = AllplanReinforcement.ReinforcementShapeBuilder()

    shape_builder.AddPoints(shape_data)

    # if the option was set in the palette, override the standard hook with other values
    if build_ele.SetStartHook.value:
        shape_builder.SetHookStart(length = build_ele.StartHookLength.value,
                                   angle  = build_ele.StartHookAngle.value,
                                   type   = AllplanReinforcement.HookType.names[build_ele.StartHookType.value])

    if build_ele.SetEndHook.value:
        shape_builder.SetHookEnd(length = build_ele.EndHookLength.value,
                                 angle  = build_ele.EndHookAngle.value,
                                 type   = AllplanReinforcement.HookType.names[build_ele.EndHookType.value])

    # create the stirrup bending shape
    shape = shape_builder.CreateStirrup(shape_props,
                                        AllplanReinforcement.StirrupType.names[build_ele.StirrupType.value])


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


def create_shape_outline(build_ele: BuildingElement) -> ModelEleList:
    """Creates a polyline based on the points defined in the property palette
    to be shown as preview to indicate the outline of the bending shape

    Args:
        build_ele: building element containing parameters from the property palette

    Returns:
        one-element model element list with the polyline
    """
    common_properties = AllplanBaseElements.CommonProperties()
    common_properties.Color = 6


    outline        = AllplanGeo.Polyline2D()
    outline.Points = [shape_point[0] for shape_point in build_ele.BarShapePointData.value]

    model_elements = ModelEleList(common_properties)
    model_elements.append_geometry_2d(outline)

    return model_elements


def create_point_numbers(build_ele: BuildingElement) -> PreviewSymbols:
    """Creates numbers as preview symbols to indicate the index of the shape point

    Args:
        build_ele: building element containing shape points defined in the property palette

    Returns:
        preview symbols located near the shape points showing the index of this shape point
    """
    points = [AllplanGeo.Point3D(shape_point[0]) for shape_point in build_ele.BarShapePointData.value]

    preview_numbers = PreviewSymbols()

    for idx, point in enumerate(points):
        preview_numbers.add_text(text            = str(idx),
                                 reference_point = point + AllplanGeo.Point3D(20,20,0),
                                 ref_pnt_pos     = TextReferencePointPosition.TOP_LEFT,
                                 height          = 50.0,
                                 color           = 6,
                                 rotation_angle  = AllplanGeo.Angle())
    return preview_numbers
