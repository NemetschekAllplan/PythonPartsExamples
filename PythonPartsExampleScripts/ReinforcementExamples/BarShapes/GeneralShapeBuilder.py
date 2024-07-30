"""Example script showing the implementation of the functions from the
GeneralReinfShapeBuilder module
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinforcement
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from StdReinfShapeBuilder import GeneralReinfShapeBuilder
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections import ModelEleList
from Utils import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeneralShapeBuilderBuildingElement import \
        GeneralShapeBuilderBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: GeneralShapeBuilder.py')


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
                               preview_elements = create_shape_outline(build_ele))


def create_shape(build_ele: BuildingElement) -> AllplanReinforcement.BendingShape:
    """Create rebar shape using functions from the GeneralReinfShapeBuilder module
    based on the parameter values given by the user in the property palette

    Args:
        build_ele: building element containing parameters specified by the user in the palette

    Returns:
        bending shape
    """

    # ------------ read parameter values from palette

    # read geometrical dimensions
    length        : float  = build_ele.Length.value
    width         : float  = build_ele.Width.value
    second_width  : float  = build_ele.SecondWidth.value    # only for u-link variable
    height        : float  = build_ele.Height.value         # only for spacer
    radius        : float  = build_ele.Radius.value         # only for circle stirrup

    # set concrete covers based on the values from the property palette
    concrete_covers = ConcreteCoverProperties(left   = build_ele.ConcreteCoverLeft.value,
                                              bottom = build_ele.ConcreteCoverBottom.value,
                                              right  = build_ele.ConcreteCoverRight.value,
                                              top    = build_ele.ConcreteCoverTop.value)

    # set shape properties based on the values from the property palette
    shape_props = ReinforcementShapeProperties.rebar(build_ele.Diameter.value,
                                                     build_ele.BendingRoller.value,
                                                     build_ele.SteelGrade.value,
                                                     build_ele.ConcreteGrade.value,
                                                     AllplanReinforcement.BendingShapeType.names[build_ele.BendingShapeType.value])

    # read the data relevant for the GeneralReinfShapeBuilder from the property palette
    start_hook       = build_ele.StartHook.value
    end_hook         = build_ele.EndHook.value
    hook_length      = build_ele.HookLength.value
    start_hook_angle = build_ele.StartHookAngle.value
    end_hook_angle   = build_ele.EndHookAngle.value
    start_anchorage  = build_ele.StartAnchorage.value       # only for straight bar with anchorage
    end_anchorage    = build_ele.EndAnchorage.value         # only for straight bar with anchorage
    overlap          = build_ele.Overlap.value              # only for circle stirrup

    # setting hook type to -1 makes the GeneralReinfShapeBuilder determine the right type based on hook angle
    start_hook_type = AllplanReinforcement.HookType.names[build_ele.StartHookType.value] if build_ele.StartHookType.value != "based on hook angle" else -1
    end_hook_type   = AllplanReinforcement.HookType.names[build_ele.EndHookType.value] if build_ele.EndHookType.value != "based on hook angle" else -1

    stirrup_type    = AllplanReinforcement.StirrupType.names[build_ele.StirrupType.value]    # only for stirrups


    # ------------ create the shape using functions from GeneralReinfShapeBuilder module

    if build_ele.ShapeType.value == "Circle stirrup with user hooks":
        shape = GeneralReinfShapeBuilder.create_circle_stirrup_with_user_hooks(radius,
                                                                               RotationUtil(0, 0, 0),
                                                                               shape_props,
                                                                               concrete_covers.left,
                                                                               overlap,
                                                                               start_hook,
                                                                               start_hook_angle,
                                                                               end_hook,
                                                                               end_hook_angle)

    elif build_ele.ShapeType.value == "Straight bar with anchorage":
        shape = GeneralReinfShapeBuilder.create_longitudinal_shape_with_anchorage(AllplanGeo.Point3D(),
                                                                                  AllplanGeo.Point3D(length, 0, 0),
                                                                                  shape_props,
                                                                                  concrete_covers,
                                                                                  start_anchorage,
                                                                                  end_anchorage)

    elif build_ele.ShapeType.value == "Straight bar with hooks":
        shape = GeneralReinfShapeBuilder.create_longitudinal_shape_with_hooks(length,
                                                                              RotationUtil(0, 0, 0),
                                                                              shape_props,
                                                                              concrete_covers,
                                                                              start_hook,
                                                                              end_hook)

    elif build_ele.ShapeType.value == "Straight bar with user defined hooks":
        shape = GeneralReinfShapeBuilder.create_longitudinal_shape_with_user_hooks(length,
                                                                                   RotationUtil(0, 0, 0),
                                                                                   shape_props,
                                                                                   concrete_covers,
                                                                                   start_hook,
                                                                                   end_hook,
                                                                                   start_hook_angle,
                                                                                   end_hook_angle,
                                                                                   start_hook_type,
                                                                                   end_hook_type)

    elif build_ele.ShapeType.value == "L-shape with hooks":
        shape = GeneralReinfShapeBuilder.create_l_shape_with_hooks(length,
                                                                   width,
                                                                   RotationUtil(0, 0, 0),
                                                                   shape_props,
                                                                   concrete_covers,
                                                                   start_hook,
                                                                   end_hook)

    elif build_ele.ShapeType.value == "Hook stirrup":
        shape = GeneralReinfShapeBuilder.create_hook_stirrup(length,
                                                             RotationUtil(0, 0, 0),
                                                             shape_props,
                                                             concrete_covers,
                                                             hook_length,
                                                             start_hook_angle,
                                                             end_hook_angle)

    elif build_ele.ShapeType.value == "Open stirrup":
        shape = GeneralReinfShapeBuilder.create_open_stirrup(length,
                                                             width,
                                                             RotationUtil(0, 0, 0),
                                                             shape_props,
                                                             concrete_covers,
                                                             start_hook,
                                                             end_hook,
                                                             start_hook_angle,
                                                             end_hook_angle,
                                                             start_hook_type)

    elif build_ele.ShapeType.value == "S-hook":
        shape = GeneralReinfShapeBuilder.create_s_hook(length,
                                                       RotationUtil(0, 0, 0),
                                                       shape_props,
                                                       concrete_covers,
                                                       hook_length)

    elif build_ele.ShapeType.value == "Spacer":
        shape = GeneralReinfShapeBuilder.create_spacer(length,
                                                       width,
                                                       height,
                                                       RotationUtil(0, 0, 0),
                                                       shape_props)

    elif build_ele.ShapeType.value == "Stirrup":
        shape = GeneralReinfShapeBuilder.create_stirrup(length,
                                                        width,
                                                        RotationUtil(0, 0, 0),
                                                        shape_props,
                                                        concrete_covers,
                                                        stirrup_type,
                                                        hook_length)

    elif build_ele.ShapeType.value == "Stirrup with user hooks":
        shape = GeneralReinfShapeBuilder.create_stirrup_with_user_hooks(length,
                                                                        width,
                                                                        RotationUtil(0, 0, 0),
                                                                        shape_props,
                                                                        concrete_covers,
                                                                        stirrup_type,
                                                                        start_hook,
                                                                        start_hook_angle,
                                                                        end_hook,
                                                                        end_hook_angle)

    elif build_ele.ShapeType.value == "U-link":
        shape = GeneralReinfShapeBuilder.create_u_link(length,
                                                       width,
                                                       RotationUtil(0, 0, 0),
                                                       shape_props,
                                                       concrete_covers,
                                                       hook_length)

    elif build_ele.ShapeType.value == "U-link variable":
        shape = GeneralReinfShapeBuilder.create_u_link_variable(length,
                                                                width,
                                                                second_width,
                                                                RotationUtil(0, 0, 0),
                                                                shape_props,
                                                                concrete_covers,
                                                                start_hook,
                                                                end_hook,
                                                                start_hook_angle,
                                                                end_hook_angle,
                                                                start_hook_type,
                                                                end_hook_type)
    else:
        return AllplanReinforcement.BendingShape()

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
    """Creates a list with 2d lines representing the outline of the bending shape
    For shapes defined by length only, a single 2d line is created
    For shapes defined by length and width, a rectangle is created
    For the circle stirrup, circle is created

    Args:
        build_ele: building element containing parameters from the property palette

    Returns:
        list with the model elements representing the lines
    """
    common_properties = AllplanBaseElements.CommonProperties()
    common_properties.Color = 6

    # in case of circle stirrup create a circle
    if build_ele.ShapeType.value == "Circle stirrup with user hooks":
        outline = AllplanGeo.Arc2D(center = AllplanGeo.Point2D(),
                                   radius = build_ele.Radius.value)

    # in case of straight bars, s-hook and hook stirrup, create a line
    elif "Straight bar" in build_ele.ShapeType.value or build_ele.ShapeType.value in ["Hook stirrup", "S-hook"]:
        outline = AllplanGeo.Line2D(AllplanGeo.Point2D(0, 0),
                                    AllplanGeo.Point2D(build_ele.Length.value, 0))

    # in other cases create a rectangle
    else:
        corner1 = AllplanGeo.Point2D()
        corner2 = AllplanGeo.Point2D(x = build_ele.Length.value,
                                     y = build_ele.Width.value)
        outline = AllplanGeo.Polygon2D.CreateRectangle(corner1, corner2)

    model_elements = ModelEleList(common_properties)
    model_elements.append_geometry_2d(outline)

    return model_elements
