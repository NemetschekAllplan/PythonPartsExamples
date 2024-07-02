""" Example script creating a stirrup placement with multiple placement regions
differing in length, spacing and diameter. The purpose of this script
is to show the implementation of the LInearBarPlacementBuilder in a use-case
of a beam with variable stirrup reinforcement along its length.
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
    from __BuildingElementStubFiles.BarPlacementInRegionsBuildingElement import \
        BarPlacementInRegionsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load RebarPlacementInRegions.py')


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

    element = BarPlacementInRegions(build_ele, doc)

    return element.create()


class BarPlacementInRegions():
    """ Definition of class BarPlacementInRegions
    """

    def __init__(self,
                 build_ele: BuildingElement,
                 doc      : AllplanEleAdapter.DocumentAdapter):
        """ Constructor

        Args:
            build_ele: building element with the parameter properties
            doc:       document of the Allplan drawing files
        """

        self.build_ele = build_ele
        self.document  = doc

        self.length = build_ele.Sizes.value.X
        self.width  = build_ele.Sizes.value.Y
        self.height = build_ele.Sizes.value.Z

        self.concrete_cover = build_ele.ConcreteCover.value
        self.steel_grade    = build_ele.SteelGrade.value

        self.placement_regions = build_ele.PlacementRegions.value


    def create(self) -> CreateElementResult:
        """ Create the elements: reinforcement and bounding box

        Returns:
            created element result
        """

        # create the geometry of the bounding box
        model_ele_list = ModelEleList(self.build_ele.CommonProp.value)
        polyhed        = AllplanGeo.Polyhedron3D.CreateCuboid(self.length, self.width, self.height)
        model_ele_list.append_geometry_3d(polyhed)


        # create the reinforcement placements

        reinf_ele_list = ModelEleList()
        reinf_ele_list.extend(self.place_stirrup_in_regions())

        # create the PythonPart, if the option was selected in the palette

        if self.build_ele.IsPythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(model_ele_list)
            pyp_util.add_reinforcement_elements(reinf_ele_list)

            return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))

        return CreateElementResult(elements= model_ele_list + reinf_ele_list)


    def create_stirrup_shapes(self) -> list[AllplanReinf.BendingShape]:
        """ Create a list of shapes of a rectangular, closed stirrups for each region defined
        in placement_regions. Each region can have different diameter, therefore a separate shape
        with different diameter needs to be defined per region. Shapes are defined in YZ plane

        Returns:
            bending shape of the stirrup stirrup
        """

        # rotation angles to transform the stirrup shape from its local to the global coordinate system
        local_to_global = RotationUtil(90, 0 , 90)

        # all concrete covers are set to the same value
        concrete_cover_props = ConcreteCoverProperties.all(self.concrete_cover)

        # create a list of stirrup shapes
        shapes : list[AllplanReinf.BendingShape] = []

        for placement_region in self.placement_regions:
            bar_diameter = placement_region[2]

            # dermine the bending roller based on normative standards
            bending_roller = AllplanReinf.BendingRollerService.GetBendingRollerFactor(bar_diameter,
                                                                                      self.steel_grade,
                                                                                      -1,
                                                                                      True)

            shape_props = ReinforcementShapeProperties.rebar(bar_diameter,
                                                             bending_roller,
                                                             self.steel_grade,
                                                             -1,                # get the concrete grade from current Allplan settings
                                                             AllplanReinf.BendingShapeType.Stirrup)

            shapes.append(GeneralShapeBuilder.create_stirrup(self.width,
                                                             self.height,
                                                             local_to_global,
                                                             shape_props,
                                                             concrete_cover_props))

        return shapes

    def place_stirrup_in_regions(self) -> list[AllplanReinf.BarPlacement]:
        """Create stirrup placements. Stirrups are placed along X axis. Each placement begins after
        the previous one and its length and bar spacing are specified in placement_regions.

        Returns:
            List with stirrup placements
        """
        shapes     = self.create_stirrup_shapes()
        from_point = AllplanGeo.Point3D()
        to_point   = AllplanGeo.Point3D(self.length,0,0)

        # calculate the list of pairs (start points, end point) for each placement region
        region_start_end_points = LinearBarBuilder.calculate_length_of_regions( self.placement_regions,
                                                                                from_point,
                                                                                to_point,
                                                                                concrete_cover_left  = self.concrete_cover,
                                                                                concrete_cover_right = self.concrete_cover)

        # create list of placements, one for each placement region
        placements = []

        for idx, start_end_point in enumerate(region_start_end_points):
            mark_nr = idx + 1   # index begins with 0, but mark numbering must begin with 1
            region_start_point, region_end_point = start_end_point

            placements.append(LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(mark_nr,
                                                                                           shapes[idx],
                                                                                           region_start_point,
                                                                                           region_end_point,
                                                                                           concrete_cover_left  = 0,    # start and end covers are already considered
                                                                                           concrete_cover_right = 0,    # by calculate_length_of_regions
                                                                                           bar_distance         = self.placement_regions[idx][1]))
        return placements
