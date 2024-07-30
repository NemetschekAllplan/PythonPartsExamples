"""Example script showing the implementation of the function column_corbel_shape_type1
from the CorbelReinfShapeBuilder module
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinforcement
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from StdReinfShapeBuilder import CorbelReinfShapeBuilder
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CorbelShapeBuilderBuildingElement import \
        CorbelShapeBuilderBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: CorbelShapeBuilder.py')


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

    return CreateElementResult([placement])


def create_shape(build_ele: BuildingElement) -> AllplanReinforcement.BendingShape:
    """Create rebar shape using functions from the CorbelReinfShapeBuilder module
    based on the parameter values given by the user in the property palette

    Args:
        build_ele: building element containing parameters specified by the user in the palette

    Returns:
        bending shape
    """

    # set shape properties based on the values from the property palette

    shape_props = ReinforcementShapeProperties.rebar(build_ele.Diameter.value,
                                                     build_ele.BendingRoller.value,
                                                     build_ele.SteelGrade.value,
                                                     build_ele.ConcreteGrade.value,
                                                     AllplanReinforcement.BendingShapeType.names[build_ele.BendingShapeType.value])

    # create the shape using CorbelReinfShapeBuilder

    shape = CorbelReinfShapeBuilder.column_corbel_shape_type1(build_ele.ColumnWidth.value,
                                                              build_ele.ColumnThickness.value,
                                                              build_ele.CorbelWidth.value,
                                                              build_ele.CorbelTop.value,
                                                              RotationUtil(90, 0, 0),
                                                              shape_props,
                                                              build_ele.ConcreteCover.value)

    return shape if shape.IsValid else AllplanReinforcement.BendingShape()


def create_placement(shape: AllplanReinforcement.BendingShape) -> AllplanReinforcement.BarPlacement:
    """Create the rebar placement containing only one rebar of the given shape

    Args:
       shape:   bending shape to create placement for

    Returns:
        rebar placement with one rebar
    """
    # define placement start and end point
    start_point = AllplanGeo.Point3D(0,    0, 0)
    end_point   = AllplanGeo.Point3D(1000, 0, 0)

    return LinearBarBuilder.create_linear_bar_placement_from_to_by_count(position             = 1,
                                                                         shape                = shape,
                                                                         from_point           = start_point,
                                                                         to_point             = end_point,
                                                                         concrete_cover_left  = 0,
                                                                         concrete_cover_right = 0,
                                                                         bar_count            = 1)
