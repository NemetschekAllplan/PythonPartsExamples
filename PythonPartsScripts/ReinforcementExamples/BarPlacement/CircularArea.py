""" Example Script showing how to place rebars in a circular shape.

-   Circular bars are placed with CircularAreaPlacement
-   Radial bars are placed with BarPlacement
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from StdReinfShapeBuilder import GeneralReinfShapeBuilder
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections.ModelEleList import ModelEleList
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CircularAreaBuildingElement import CircularAreaBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: CircularArea.py')


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

    element = CircularArea(build_ele, doc)

    return element.create()


class CircularArea():
    """ Definition of class CircularArea
    """

    def __init__(self,
                 build_ele: BuildingElement,
                 doc      : AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class CircularArea

        Args:
            build_ele: building element with the parameter properties
            doc:       document of the Allplan drawing files
        """

        self.build_ele = build_ele
        self.document  = doc

        #----------------- format parameter values

        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()


        #----------------- Extract palette geometry parameter values

        self.outer_radius = build_ele.OuterRadius.value
        self.inner_radius = build_ele.InnerRadius.value
        self.rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0, 0, 0),
                                               AllplanGeo.Point3D(0, 0, 1))



    def create(self) -> CreateElementResult:
        """ Create the elements: the outline of the circular area to reinforce,
        circular reinforcement placement and/or radial reinforcement placement

        Returns:
            created element result
        """

        model_ele_list = self.create_outline(self.build_ele)

        reinforcement_elements = []
        if self.build_ele.CreateCircularReinf.value:
            reinforcement_elements.append(self.create_circumferential_reinforcement(self.build_ele))

        if self.build_ele.CreateRadialReinf.value:
            reinforcement_elements.append(self.create_radial_reinforcement(self.build_ele))

        #----------------- create model elements

        if not self.build_ele.IsPythonPart.value:
            model_ele_list += reinforcement_elements

            return CreateElementResult(model_ele_list)


        #----------------- create as a PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)
        pyp_util.add_reinforcement_elements(reinforcement_elements)

        return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))

    def create_outline(self,
                       build_ele: BuildingElement) -> ModelEleList:
        """Create the outline of the reinforcement placement as 2D lines

        Returns:
            model element list containing 2d outer arc, inner arc and lines connecting them
        """
        model_ele_list = ModelEleList(self.build_ele.CommonProp.value)

        # create the outer arc
        outer_arc = AllplanGeo.Arc2D(center           = AllplanGeo.Point2D(),
                                     major            = self.outer_radius,
                                     minor            = self.outer_radius,
                                     axisangle        = 0,
                                     startangle       = float(AllplanGeo.Angle.FromDeg(build_ele.OuterAngleStart.value)),
                                     endangle         = float(AllplanGeo.Angle.FromDeg(build_ele.OuterAngleEnd.value)),
                                     counterClockwise = True)

        model_ele_list.append_geometry_2d(outer_arc)

        # create the inner arc
        inner_arc = AllplanGeo.Arc2D(center           = AllplanGeo.Point2D(),
                                     major            = self.inner_radius,
                                     minor            = self.inner_radius,
                                     axisangle        = 0,
                                     startangle       = float(AllplanGeo.Angle.FromDeg(build_ele.InnerAngleStart.value)),
                                     endangle         = float(AllplanGeo.Angle.FromDeg(build_ele.InnerAngleEnd.value)),
                                     counterClockwise = True)

        model_ele_list.append_geometry_2d(inner_arc)

        # connect start and end points of both arcs to create a visually closed area
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(inner_arc.StartPoint,outer_arc.StartPoint))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(inner_arc.EndPoint,outer_arc.EndPoint))

        return model_ele_list


    def create_circumferential_reinforcement(self,
                                             build_ele: BuildingElement) -> AllplanReinf.CircularAreaElement:
        """ Create a circular reinforcement placement using the CircularAreaPlacement
        based on values provided by the user in the pallete page CircularReinforcement

        Args:
            build_ele: building element with the parameter properties

        Returns:
            rebar placement of the circular bars
        """

        contour = AllplanGeo.Polyline3D()
        contour += AllplanGeo.Point3D(self.inner_radius, 0, 0)
        contour += AllplanGeo.Point3D(self.outer_radius, 0, 0)

        circular_area = AllplanReinf.CircularAreaElement(2,
                                                         build_ele.CircularBarDiameter.value,
                                                         -1,
                                                         -1,
                                                         self.rotation_axis,
                                                         contour,
                                                         build_ele.OuterAngleStart.value,
                                                         build_ele.OuterAngleEnd.value,
                                                         build_ele.InnerAngleStart.value,
                                                         build_ele.InnerAngleEnd.value,
                                                         build_ele.CircularConcreteCoverStart.value,
                                                         build_ele.CircularConcreteCoverEnd.value,
                                                         build_ele.CircularConcreteCoverContour.value)

        circular_area.SetBarProperties(build_ele.Distance.value,
                                       build_ele.MaxBarLength.value,
                                       build_ele.MinBarLength.value,
                                       build_ele.PlacementRule.value,
                                       build_ele.OddFirstBarLength.value,
                                       build_ele.EvenFirstBarLength.value,
                                       build_ele.MinBarRadius.value,
                                       build_ele.MaxBarRise.value,)

        circular_area.SetOverlap(build_ele.OddOverlapStart.value,
                                 build_ele.EvenOverlapStart.value,
                                 build_ele.OverlapStartAsCircle.value,
                                 build_ele.OddOverlapEnd.value,
                                 build_ele.EvenOverlapEnd.value,
                                 build_ele.OverlapEndAsCircle.value,
                                 build_ele.OverlapLength.value)


        circular_area.PlacePerLinearMeter = build_ele.PlaceCircularPerLinearMeter.value

        if build_ele.PlaceCircularPerLinearMeter.value:
            circular_area.LengthFactor = build_ele.CircularLengthFactor.value

        return circular_area

    def create_radial_reinforcement(self,
                                    build_ele: BuildingElement) -> AllplanReinf.BarPlacement:
        """Create a radial reinforcement placement using the BarPlacement class based on values
        provided by the user in the pallete page RadialReinforcement

        Args:
            build_ele: building element with the parameter properties
        """

        # set concrete covers
        concrete_covers = ConcreteCoverProperties.left_right_bottom(build_ele.RadialConcreteCoverLeft.value,
                                                                    build_ele.RadialConcreteCoverRight.value,
                                                                    build_ele.RadialConcreteCoverBottom.value)

        # set shape properties based on the values from the property palette
        shape_props = ReinforcementShapeProperties.rebar(build_ele.RadialBarDiameter.value,
                                                        4,
                                                        -1,
                                                        -1,
                                                        AllplanReinf.BendingShapeType.LongitudinalBar)

        # a shape to be placed is a straight bar created along the X axis, staring at inner radius, endig at the outer radius
        radial_bar_shape = GeneralReinfShapeBuilder.create_longitudinal_shape_with_hooks(self.outer_radius - self.inner_radius,
                                                                                         RotationUtil(90,0,0),
                                                                                         shape_props,
                                                                                         concrete_covers,
                                                                                         -1,
                                                                                         -1)

        # transforming (moving and rotating) the rebar from its local to global coordinate system
        local_to_global = AllplanGeo.Matrix3D()
        local_to_global.SetTranslation(AllplanGeo.Vector3D(self.inner_radius,0,0))
        local_to_global.Rotation(line  = self.rotation_axis,
                                 angle = AllplanGeo.Angle.FromDeg(build_ele.InnerAngleStart.value))

        radial_bar_shape.Transform(local_to_global)

        # determine the delta angle, between each rebar
        rotation_angle = AllplanGeo.Angle.FromDeg(-(build_ele.InnerAngleEnd.value - build_ele.InnerAngleStart.value)/(build_ele.RadialBarCount.value - 1))
        self.rotation_axis.Reverse()

        # create the radial placement
        return AllplanReinf.BarPlacement(1,
                                         build_ele.RadialBarCount.value,
                                         self.rotation_axis,
                                         rotation_angle,
                                         radial_bar_shape)
