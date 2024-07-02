""" Script for the bar placement
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.LinearBarPlacementBuilder import StartEndPlacementRule
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections.ModelEleList import ModelEleList
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BarPlacementBuildingElement import BarPlacementBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load RebarPlacement.py')


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


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = BarPlacement(build_ele, doc)

    return element.create()


class BarPlacement():
    """ Definition of class RebarPlacement
    """

    def __init__(self,
                 build_ele: BuildingElement,
                 doc      : AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class TextDyn

        Args:
            build_ele: building element with the parameter properties
            doc:       document of the Allplan drawing files
        """

        self.build_ele = build_ele
        self.document  = doc

        self.length = build_ele.Sizes.value.X
        self.width  = build_ele.Sizes.value.Y
        self.height = build_ele.Sizes.value.Z

        self.concrete_cover        = build_ele.ConcreteCover.value
        self.steel_grade           = build_ele.SteelGrade.value

        self.diameter_stirrup      = build_ele.DiameterStirrup.value
        self.diameter_longitudinal = build_ele.DiameterLongitudinal.value

        self.distance_stirrup       = build_ele.DistanceStirrup.value
        self.placement_rule_stirrup = StartEndPlacementRule[build_ele.PlacementRuleStirrup.value]

        self.bar_count_longitudinal = build_ele.BarCountLongitudinal.value


        # determine the bending rollers based on the norm
        self.bending_roller_stirrup = AllplanReinf.BendingRollerService.GetBendingRollerFactor(self.diameter_stirrup,
                                                                                               self.steel_grade,
                                                                                               -1,
                                                                                               True)
        self.bending_roller_longitudinal = AllplanReinf.BendingRollerService.GetBendingRollerFactor(self.diameter_longitudinal,
                                                                                                    self.steel_grade,
                                                                                                    -1,
                                                                                                    False)

    def create(self) -> CreateElementResult:
        """ Create the elements

        Returns:
            created element result
        """

        # create the geometry of the bounding box

        model_ele_list = ModelEleList(self.build_ele.CommonProp.value)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(self.length, self.width, self.height)

        model_ele_list.append_geometry_3d(polyhed)


        # create the reinforcement placements

        reinf_ele_list = ModelEleList()

        reinf_ele_list.append(self.create_stirrup())

        reinf_ele_list += self.create_longitudinal()


        # create the PythonPart, if the option was selected in the palette

        if self.build_ele.IsPythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(model_ele_list)
            pyp_util.add_reinforcement_elements(reinf_ele_list)

            return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))

        return CreateElementResult(elements= model_ele_list + reinf_ele_list)


    def create_stirrup(self) -> AllplanReinf.BarPlacement:
        """ Create the stirrup placement

        Returns:
            stirrup placement
        """

        # rotation angles to transform the stirrup shape from its local to the global coordinate system
        local_to_global = RotationUtil(90, 0 , 0)

        # define the bending shape and its properties
        shape_props = ReinforcementShapeProperties.rebar(self.diameter_stirrup,
                                                         self.bending_roller_stirrup,
                                                         self.steel_grade,
                                                         -1,                # get the concrete grade from current Allplan settings
                                                         AllplanReinf.BendingShapeType.Stirrup)

        concrete_cover_props = ConcreteCoverProperties.all(self.concrete_cover)

        shape = GeneralShapeBuilder.create_stirrup(self.length,
                                                   self.height,
                                                   local_to_global,
                                                   shape_props,
                                                   concrete_cover_props)

        # define the stirrup placement
        from_pnt = AllplanGeo.Point3D()
        to_point = from_pnt + AllplanGeo.Point3D(0, self.width, 0)

        placement = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1,
                                                                                 shape,
                                                                                 from_pnt,
                                                                                 to_point,
                                                                                 self.concrete_cover,
                                                                                 self.concrete_cover - self.diameter_stirrup,
                                                                                 self.distance_stirrup,
                                                                                 self.placement_rule_stirrup)

        # if selected in the palette, set placement type to per linear meter and the length factor
        placement.PlacePerLinearMeter = self.build_ele.PlacePerLinearMeter.value

        if self.build_ele.PlacePerLinearMeter.value:
            placement.LengthFactor = self.build_ele.LengthFactor.value

        return placement


    def create_longitudinal(self) -> list[AllplanReinf.BarPlacement]:
        """ Create the longitudinal bar placement

        Returns:
            list with both placements: top and bottom longitudinal bars
        """

        # define the bending shape properties for both top and bottom longitudinal bar shapes
        cover_side = self.concrete_cover + (1 + self.bending_roller_stirrup * self.diameter_stirrup) / 2

        shape_props = ReinforcementShapeProperties.rebar(self.diameter_longitudinal,
                                                         self.bending_roller_longitudinal,
                                                         self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        cover_props = ConcreteCoverProperties.left_right_bottom(self.concrete_cover,
                                                                self.concrete_cover,
                                                                self.concrete_cover + self.diameter_stirrup)

        # define the bottom shape
        bottom_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(self.width,
                                                                                RotationUtil(90, 0 , 90),
                                                                                shape_props,
                                                                                cover_props)

        # define the top shape by rotating and moving the bottom one
        top_shape = AllplanReinf.BendingShape(bottom_shape)
        top_shape.Rotate(RotationUtil(0, 180, 0))                   # rotate the bottom shape around the global Y axis
        top_shape.Move(AllplanGeo.Vector3D(0, 0, self.height))      # move the rotated shape to the top of the cube

        # define the start and end points for the placement
        from_pnt = AllplanGeo.Point3D(0, 0, 0)
        to_pnt   = from_pnt + AllplanGeo.Point3D(self.length, 0, 0)

        # create list with both placements
        longitudinal_bar_placements : list[AllplanReinf.BarPlacement] = []

        for mark_nr, shape in enumerate([top_shape, bottom_shape], start= 2):
            placement = LinearBarBuilder.create_linear_bar_placement_from_to_by_count(mark_nr,
                                                                                      shape,
                                                                                      from_pnt,
                                                                                      to_pnt,
                                                                                      cover_side,
                                                                                      cover_side,
                                                                                      self.bar_count_longitudinal)
            # if selected in the palette, set placement type to per linear meter and the length factor
            placement.PlacePerLinearMeter = self.build_ele.PlacePerLinearMeterLongitudinal.value

            if self.build_ele.PlacePerLinearMeterLongitudinal.value:
                placement.LengthFactor = self.build_ele.LengthFactorLongitudinal.value

            longitudinal_bar_placements.append(placement)

        return longitudinal_bar_placements
