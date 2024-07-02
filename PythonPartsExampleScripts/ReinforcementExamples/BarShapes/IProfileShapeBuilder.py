"""Example script showing the implementation of the functions from the
IProfileReinfShapeBuilder module
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinforcement
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from StdReinfShapeBuilder import IProfileReinfShapeBuilder
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections import ModelEleList
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IProfileShapeBuilderBuildingElement import \
        IProfileShapeBuilderBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: IProfileShapeBuilder.py')


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
    """Create rebar shape using functions from the IProfileReinfShapeBuilder module
    based on the parameter values given by the user in the property palette.

    Args:
        build_ele: building element containing parameters specified by the user in the palette

    Returns:
        bending shape
    """

    # ------------ read parameter values from palette

    # create the profile 3D polyline in YZ plane out of 2D points defined in the palette
    profile_polyline = AllplanGeo.Polyline3D([AllplanGeo.Point3D(point_2d) for point_2d in build_ele.ProfilePoints.value])
    profile_polyline *= RotationUtil(90,0,90).get_rotation_matrix()

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

    # create the shape using IProfileReinfShapeBuilder

    if build_ele.ShapeType.value == "Bottom flange":
        shape = IProfileReinfShapeBuilder.create_bottom_flange_shape(profile_polyline,
                                                                     shape_props,
                                                                     concrete_covers)

    elif build_ele.ShapeType.value == "Bottom flange 2":
        shape = IProfileReinfShapeBuilder.create_bottom_flange_shape_2(profile_polyline,
                                                                       shape_props,
                                                                       concrete_covers,
                                                                       build_ele.SideLength.value)

    elif build_ele.ShapeType.value == "Top flange":
        shape = IProfileReinfShapeBuilder.create_top_flange_shape(profile_polyline,
                                                                  shape_props,
                                                                  concrete_covers)

    elif build_ele.ShapeType.value == "Top flange 2":
        shape = IProfileReinfShapeBuilder.create_top_flange_shape_2(profile_polyline,
                                                                    shape_props,
                                                                    concrete_covers,
                                                                    build_ele.SideLength.value)

    elif build_ele.ShapeType.value == "Web shape":
        shape = IProfileReinfShapeBuilder.create_web_shape(profile_polyline,
                                                           shape_props,
                                                           concrete_covers,
                                                           build_ele.SideLength.value,
                                                           build_ele.Distance.value)

    elif build_ele.ShapeType.value == "Web stirrup":
        shape = IProfileReinfShapeBuilder.create_web_stirrup(profile_polyline,
                                                             shape_props,
                                                             concrete_covers)

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
    end_point = AllplanGeo.Point3D(1000, 0, 0)

    return LinearBarBuilder.create_linear_bar_placement_from_to_by_count(position             = 1,
                                                                         shape                = shape,
                                                                         from_point           = start_point,
                                                                         to_point             = end_point,
                                                                         concrete_cover_left  = 0,
                                                                         concrete_cover_right = 0,
                                                                         bar_count            = 1)


def create_shape_outline(build_ele: BuildingElement) -> ModelEleList:
    """Creates a model element list with 3d polyline representing
    the outline of the I profile

    Args:
        build_ele: building element containing parameters from the property palette

    Returns:
        list with the model elements representing the polyline
    """
    common_properties       = AllplanBaseElements.CommonProperties()
    common_properties.Color = 6

    outline = AllplanGeo.Polyline3D([AllplanGeo.Point3D(point_2d) for point_2d in build_ele.ProfilePoints.value])
    outline += outline.GetStartPoint()
    outline *= RotationUtil(90,0,90).get_rotation_matrix()

    model_elements = ModelEleList(common_properties)
    model_elements.append_geometry_3d(outline)

    return model_elements
