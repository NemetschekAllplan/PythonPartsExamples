"""Example script showing the methods offered by the BarShapePlacementUtil
that helps when placing longitudinal bars inside multiple stirrups shapes, e.g.:

-   in the corner of a stirrup
-   along a specified leg of a stirrups
-   at the intersection of two stirrup legs
-   along stirrup leg between two other stirrup legs
"""

#pylint: enable=W1401
# Only disabled for comment part

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from NemAll_Python_IFW_ElementAdapter import DocumentAdapter
from StdReinfShapeBuilder.BarShapePlacementUtil import BarShapePlacementUtil
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from TypeCollections.ModelEleList import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LongitudinalBarPlacementBuildingElement import \
        LongitudinalBarPlacementBuildingElement as BuildingElement
else:
    from BuildingElement import BuildingElement

print('Loading script LongitudinalBarPlacement.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele : BuildingElement,
                   _doc      : DocumentAdapter) -> CreateElementResult:
    """Creation of element

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        result of element creation
    """
    rebar_placement = RebarPlacement(build_ele)

    return CreateElementResult(elements         = rebar_placement.model_ele_list,
                               preview_elements = rebar_placement.preview_elements)


class RebarPlacement():
    """This class creates four rebar placements:

        -   rectangular closed stirrups are placed along Y axis in a hard coded spacing
        -   vertical and a horizontal S-hooks are placed along with the stirrup
        -   a single longitudinal bar (along Y axis) is placed inside the closed stirrup

    The purpose is to show the possibilities of placing the longitudinal bar.
    The position of the longitudinal bar is determined using the BarShapePlacementUtil
    in relation to the stirrups e.g., in corner or along specified stirrup leg, so that
    the bar can be placed there.

    Attributes:
        model_ele_list:     list of elements to create in the model,
                            all bar placements are appended to this list
        preview_elements:   list of elements to display as preview
                            contains the bounding box
        length:             X-dimension of the bounding box
        width:              Y-dimension of the bounding box
        height:             Z-dimension of the bounding box
        concrete_cover:     concrete cover applied on ALL sides
        stirrup_diameter:   diameter of stirrups
        bending_roller:     diameter of the bending pin roller of the stirrups as multiply of their diameter
        global_to_local:    rotation angles to transform from global coordinate system to local coordinate
                            system of the stirrups
        stirrup_shapes:     dictionary containing all three stirrup shapes
    """

    def __init__(self, build_ele : BuildingElement):
        """ Constructor

        Args:
            build_ele:     building element containing the parameter properties from the palette
        """

        self.model_ele_list        = ModelEleList()

        preview_common_props       = AllplanBaseElements.CommonProperties()
        preview_common_props.Color = 6
        self.preview_elements      = ModelEleList(preview_common_props)

        self.length                = 2000
        self.width                 = 3000
        self.height                = 1000
        self.concrete_cover        = 25

        self.stirrup_diameter      : float = build_ele.DiameterStirrups.value
        self.bending_roller        : float = build_ele.BendingRollerStirrups.value


        # create the bounding box for the preview
        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(),
                                                       AllplanGeo.Point3D(self.length,
                                                                          self.width,
                                                                          self.height))

        self.preview_elements.append_geometry_3d(polyhed)

        # define the shape of the longitudinal bar
        longitudinal_shape_props = ReinforcementShapeProperties.rebar(build_ele.DiameterLongitudinal.value,
                                                                      bending_roller     =  4,
                                                                      steel_grade        = -1,
                                                                      concrete_grade     = -1,
                                                                      bending_shape_type = AllplanReinf.BendingShapeType.LongitudinalBar)

        self.longitudinal_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks( \
                    self.width,
                    RotationAngles(90, 0 , 90),
                    longitudinal_shape_props,
                    ConcreteCoverProperties.all(0),     # when all covers are set to 0, the bar's axis coincides with its local X axis
                    start_hook = -1,
                    end_hook   = -1)

        # define transformations for stirrups
        self.global_to_local = RotationAngles(-90, 0, 0)
        self.local_to_global = self.global_to_local.change_rotation()

        # create dictionary with stirrup shapes
        self.stirrup_shapes = self.create_stirrups()

        # place longitudinal bar at the position specified by the user
        if build_ele.PlacementType.value == "in_corner":
            self.place_longitudinal_bar_in_corner(shape_key     = build_ele.ReferenceShape.value,
                                                  corner_number = build_ele.CornerId.value)

        elif build_ele.PlacementType.value == "on_side":
            self.place_longitudinal_bar_on_side(shape_key   = build_ele.ReferenceShape.value,
                                                side_number = build_ele.SideId.value,
                                                bar_count   = build_ele.BarCount.value)

        elif build_ele.PlacementType.value == "at_intersection":
            self.place_longitudinal_bar_at_intersection(shape1_key         = build_ele.ReferenceShape.value,
                                                        shape1_side_number = build_ele.SideId.value,
                                                        shape1_above_side  = build_ele.AboveFirstSide.value,
                                                        shape2_key         = build_ele.SecondReferenceShape.value,
                                                        shape2_side_number = build_ele.SecondShapeSideId.value,
                                                        shape2_above_side  = build_ele.AboveSecondSide.value)

        elif build_ele.PlacementType.value == "on_side_between_legs":
            self.place_longitudinal_bar_on_side_between_legs(shape1_key         = build_ele.ReferenceShape.value,
                                                             shape1_side_number = build_ele.SideId.value,
                                                             shape2_key         = build_ele.SecondReferenceShape.value,
                                                             shape2_side_number = build_ele.SecondShapeSideId.value,
                                                             shape3_key         = build_ele.ThirdReferenceShape.value,
                                                             shape3_side_number = build_ele.ThirdShapeSideId.value,
                                                             shape3_above_side  = build_ele.AboveThirdSide.value,
                                                             bar_count          = build_ele.BarCount.value)

    def place_longitudinal_bar_in_corner(self, shape_key: str, corner_number: int):
        """Place the longitudinal bar in the corner of a stirrup.
        The placement is appended to the model_ele_list.

        Args:
            shape_key:      id of the stirrup shape, where the longitudinal bar should be placed
            corner_number:  index of the corner to place the longidutinal bar in, beginning with 1
        """

        # Initialize the placement utility by adding all the stirrup shapes to it
        place_util = BarShapePlacementUtil()

        for key, shape in self.stirrup_shapes.items():
            place_util.add_shape(key, shape)

        # calculate the placement point in the corner in local coordinate system
        local_placement_pnt = place_util.get_placement_in_corner(shape_key,
                                                                 corner_number,
                                                                 self.longitudinal_shape.GetDiameter(),
                                                                 self.global_to_local)

        # rotate the placement point to global coordinate system
        global_placement_pnt = local_placement_pnt * self.local_to_global.get_rotation_matrix()

        # move the shape to the global placement point and place it there 1x time
        self.longitudinal_shape.Move(AllplanGeo.Vector3D(global_placement_pnt))

        self.model_ele_list.append(AllplanReinf.BarPlacement(4,
                                                             1,
                                                             AllplanGeo.Vector3D(),
                                                             AllplanGeo.Point3D(),
                                                             AllplanGeo.Point3D(),
                                                             self.longitudinal_shape))

    def place_longitudinal_bar_on_side(self, shape_key: str, side_number: int, bar_count: int):
        """Place the longitudinal bars on specified leg of the stirrup, along the entire
        length of this leg. This linear placement is then appended to the model_ele_list.

        Args:
            shape_key:      id of the stirrup shape, where the longitudinal bar should be placed
            side_number:    index of the stirrup's leg to place the longidutinal bar on, beginning with 1
            bar_count:      count of longitudinal to place
        """

        # Initialize the placement utility by adding all the stirrup shapes to it
        place_util = BarShapePlacementUtil()

        for key, shape in self.stirrup_shapes.items():
            place_util.add_shape(key, shape)

        # get the line, along which to place the longitudinal bar in local coordinate system of the stirrup
        local_placement_line, placement_cover_left, placement_cover_right = \
            place_util.get_placement_in_side_corners(shape_key,
                                                     side_number,
                                                     self.longitudinal_shape.GetDiameter(),
                                                     self.global_to_local)

        # convert the line to 3D and transform it to the global coordinate system
        global_placement_line = AllplanGeo.Line3D(local_placement_line)
        global_placement_line *= self.local_to_global.get_rotation_matrix()

        # place the longitudinal bar along the placement line
        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_count(  \
                    4, self.longitudinal_shape,
                    global_placement_line.StartPoint,
                    global_placement_line.EndPoint,
                    placement_cover_left,
                    placement_cover_right,
                    bar_count))

    def place_longitudinal_bar_at_intersection(self,
                                               shape1_key        : str,
                                               shape1_side_number: int,
                                               shape1_above_side : bool,
                                               shape2_key        : str,
                                               shape2_side_number: int,
                                               shape2_above_side : bool):
        """Place the longitudinal bar in the intersection of two stirrup legs. The legs can belong
        to two different stirrups or they can be two legs of the same stirrup.

        Args:
            shape1_key:         id of the first reference stirrup shape
            shape1_side_number: number of the leg of the first reference stirrup
            shape1_above_side:  whether to place the longitudinal bar above the first leg or below
            shape2_key:         id of the second reference stirrup shape
            shape2_side_number: number of the leg of the second reference stirrup
            shape2_above_side:  whether to place the longitudinal bar above the second leg or below
        """

        # Initialize the placement utility by adding all the stirrup shapes to it
        place_util = BarShapePlacementUtil()

        for key, shape in self.stirrup_shapes.items():
            place_util.add_shape(key, shape)

        # calculate the placement point in the intersection of two stirrup legs
        # in local coordinate system of the stirrups
        local_placement_pnt = place_util.get_placement_in_side_intersection(shape1_key,
                                                                            shape1_side_number,
                                                                            shape1_above_side,
                                                                            shape2_key,
                                                                            shape2_side_number,
                                                                            shape2_above_side ,
                                                                            self.longitudinal_shape.GetDiameter(),
                                                                            self.global_to_local)

        # tranfsorm the calculated point into the global coordinate system
        global_placement_pnt = AllplanGeo.Point3D(local_placement_pnt) * self.local_to_global.get_rotation_matrix()

        # move the shape to the global placement point and place it there 1x time
        self.longitudinal_shape.Move(AllplanGeo.Vector3D(global_placement_pnt))

        self.model_ele_list.append(AllplanReinf.BarPlacement(4,
                                                             1,
                                                             AllplanGeo.Vector3D(),
                                                             AllplanGeo.Point3D(),
                                                             AllplanGeo.Point3D(),
                                                             self.longitudinal_shape))

    def place_longitudinal_bar_on_side_between_legs(self,
                                                    shape1_key        : str,
                                                    shape1_side_number: int,
                                                    shape2_key        : str,
                                                    shape2_side_number: int,
                                                    shape3_key        : str,
                                                    shape3_side_number: int,
                                                    shape3_above_side : bool,
                                                    bar_count         : int):
        """Place the longitudinal bars on specified leg (third reference leg) of the stirrup. The bars are
        placed not along the entire leg, but from an intersection point with another leg (first reference leg)
        to an intersection point with another leg (second reference leg). All three legs can (but not must!)
        belong to three different stirrups.

        This linear placement is then appended to the model_ele_list.

        Args:
            shape1_key:         id of the first reference stirrup shape
            shape1_side_number: number of the leg of the first reference stirrup
            shape2_key:         id of the second reference stirrup shape
            shape2_side_number: number of the leg of the second reference stirrup
            shape3_key:         id of the third reference stirrup shape
            shape3_side_number: number of the leg of the third reference stirrup
            shape3_above_side:  whether to place the longitudinal bar above the thirs reference leg or below
            bar_count:          count of longitudinal to place
        """

        # Initialize the placement utility by adding all the stirrup shapes to it
        place_util = BarShapePlacementUtil()

        for key, shape in self.stirrup_shapes.items():
            place_util.add_shape(key, shape)


        local_placement_line, placement_cover_left, placement_cover_right = \
            place_util.get_placement_at_shape_side_intersection(shape1_key,
                                                                shape1_side_number,
                                                                shape2_key,
                                                                shape2_side_number,
                                                                shape3_key,
                                                                shape3_side_number,
                                                                bool(shape3_above_side),
                                                                self.longitudinal_shape.GetDiameter(),
                                                                self.global_to_local)
        global_placement_line = AllplanGeo.Line3D(local_placement_line)
        global_placement_line *= self.local_to_global.get_rotation_matrix()

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_count(  \
                    4,
                    self.longitudinal_shape,
                    global_placement_line.StartPoint,
                    global_placement_line.EndPoint,
                    placement_cover_left,
                    placement_cover_right,
                    bar_count))


    def create_stirrups(self) -> dict[str, AllplanReinf.BendingShape]:
        """Create dictionary with three stirrup shapes. The stirrups are created in the XZ plane.

        -   rectangular closed stirrup (key: "closed stirrup")
        -   a horizontal S-hook in the middle if the rectangular stirrup (key: "horizontal S-hook")
        -   a vertical S-hook in the middle if the rectangular stirrup (key: "vertical S-hook")

        The stirrups are placed linearly along the Y axis with a spacing of 20 cm.
        The placements are then appended to the model_ele_list.


        Returns:
            dictionary with three stirrup shapes
        """

        concrete_cover_props = ConcreteCoverProperties.all(self.concrete_cover)

        local_to_global = RotationAngles(90, 0 , 0)

        shape_props = ReinforcementShapeProperties.rebar(self.stirrup_diameter,
                                                         self.bending_roller,
                                                         steel_grade        = -1,
                                                         concrete_grade     = -1,
                                                         bending_shape_type = AllplanReinf.BendingShapeType.Stirrup)

        stirrup_shapes: dict[str, AllplanReinf.BendingShape] = {}

        # create the rectangular, closed stirrup shape
        stirrup_shapes["closed stirrup"] = GeneralShapeBuilder.create_stirrup(self.length,
                                                                              self.height,
                                                                              local_to_global,
                                                                              shape_props,
                                                                              concrete_cover_props)

        # create horizontal S-hook shape
        stirrup_shapes["horizontal S-hook"] = GeneralShapeBuilder.create_s_hook(self.length,
                                                                                local_to_global,
                                                                                shape_props,
                                                                                concrete_cover_props)

        stirrup_shapes["horizontal S-hook"].Move(AllplanGeo.Vector3D(0, 0, self.height / 2))

        # create vertical S-hook shape
        local_to_global = RotationAngles(90, -90, 0)

        stirrup_shapes["vertical S-hook"] = GeneralShapeBuilder.create_s_hook(self.height,
                                                                              local_to_global,
                                                                              shape_props,
                                                                              concrete_cover_props)

        stirrup_shapes["vertical S-hook"].Move(AllplanGeo.Vector3D(self.length / 2, 0, 0))

        # place the stirrups along Y axis and append the pacements to the list

        for i, shape in enumerate(stirrup_shapes.values(), 2):
            self.model_ele_list.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(i,
                                                                             shape,
                                                                             AllplanGeo.Point3D(),
                                                                             AllplanGeo.Point3D(0, self.width, 0),
                                                                             self.concrete_cover + self.stirrup_diameter,
                                                                             self.concrete_cover,
                                                                             200))

        return stirrup_shapes
