"""
Script for the general reinforcement shape builder example
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from StdReinfShapeBuilder import MeshPlacementBuilder
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

print('Load HookLengthConstraint.py')


def check_allplan_version(build_ele: BuildingElement,
                          version:   float):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = HookLengthConstraint(doc)

    return element.create(build_ele)


class HookLengthConstraint():
    """
    Definition of class HookLengthConstraint
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class HookLengthConstraint

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = []
        self.document       = doc
        self.concrete_cover = 2


    def create(self,
               build_ele: BuildingElement):
        """
        create the longitudinal bar with hooks

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        model_angles = RotationAngles(0, 0 , 0)

        shape_props = ReinforcementShapeProperties.rebar(build_ele.BarDiameter.value, 4,
                                                         build_ele.SteelGrade.value, build_ele.ConcreteGrade.value,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        concrete_cover_props = ConcreteCoverProperties.left_right_bottom(self.concrete_cover * 2,
                                                                         self.concrete_cover * 2,
                                                                         self.concrete_cover)

        hook_angle       = build_ele.BarHookAngle.value
        hook_length      = build_ele.BarHookLength.value
        hook_type        = AllplanReinf.HookType(build_ele.BarHookType.value)

        shape = GeneralShapeBuilder.create_longitudinal_shape_with_user_hooks(1000,
                                                                              model_angles,
                                                                              shape_props,
                                                                              concrete_cover_props,
                                                                              hook_length, hook_length,
                                                                              hook_angle, hook_angle,
                                                                              hook_type, hook_type)

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, shape,
                                                                         AllplanGeo.Point3D(), AllplanGeo.Point3D(0, 0, 1000),
                                                                         0, 0, 200))


        #----------------- create the longitudinal mesh with hooks

        hook_angle       = build_ele.MeshHookAngle.value
        hook_length      = build_ele.MeshHookLength.value
        hook_type        = AllplanReinf.HookType(build_ele.MeshHookType.value)
        mesh_type        = build_ele.MeshType.value
        mesh_bending_dir = AllplanReinf.MeshBendingDirection(build_ele.MeshBendingDirection.value)

        shape_props = ReinforcementShapeProperties.mesh(mesh_type, mesh_bending_dir,
                                                        4, build_ele.ConcreteGrade.value,
                                                        AllplanReinf.BendingShapeType.LongitudinalBar)

        shape = GeneralShapeBuilder.create_longitudinal_shape_with_user_hooks(1000,
                                                                              model_angles,
                                                                              shape_props,
                                                                              concrete_cover_props,
                                                                              hook_length, hook_length,
                                                                              hook_angle, hook_angle,
                                                                              hook_type, hook_type)

        ref_pnt = AllplanGeo.Point3D(0, -500, 0)

        value_list = [(shape, 500)]

        MeshPlacementBuilder.create_mesh_placement_by_points(value_list,
                                                             ref_pnt,
                                                             ref_pnt + AllplanGeo.Point3D(0, 0, 500),
                                                             1, 2, 2,
                                                             self.model_ele_list)

        return (self.model_ele_list, self.handle_list)
