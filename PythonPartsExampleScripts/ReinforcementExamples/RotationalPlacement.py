#pylint: disable=W1401
# Anomalous backslash in string

"""
Script for the polygonal placement example
"""

#pylint: enable=W1401
# Only disabled for comment part

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from PythonPart import View2D3D, PythonPart


print('Load PolygonalPlacement.py')


def check_allplan_version(build_ele, version):
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


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = PolygonalPlacement(doc)

    return element.create(build_ele)


class PolygonalPlacement():
    """
    Definition of class PolygonalPlacement
    """

    def __init__(self, doc):
        """
        Initialisation of class PolygonalPlacement

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc
        self.concrete_cover        = None
        self.diameter              = None
        self.diameter_longitudinal = None
        self.bending_roller        = None
        self.steel_grade           = None
        self.distance              = None
        self.mesh_type             = None
        self.length                = 2000
        self.width                 = 3000
        self.height                = 1000


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """


        #----------------- create the geometry

        radius = 2000
        height = 1000
        apex   = AllplanGeo.Point3D(0, 0, height);

        cylinder = AllplanGeo.Cylinder3D(radius, radius, apex)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        model_cylinder = AllplanBasisElements.ModelElement3D(com_prop, cylinder)


        #----------------- create the reinforcement

        concrete_cover        = build_ele.ConcreteCover.value
        diameter              = build_ele.Diameter.value
        bending_roller        = build_ele.BendingRoller.value
        steel_grade           = build_ele.SteelGrade.value
        count                 = build_ele.Count.value

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

        model_angles = RotationAngles(90, 0, 0)

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller,
                                                         steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralShapeBuilder.create_l_shape_with_hooks(radius, height,
                                                              model_angles,
                                                              shape_props,
                                                              concrete_cover_props,-1)

        rot_angle     = AllplanGeo.Angle()
        rot_angle.Deg = 360.0 / count
        rot_axis      = AllplanGeo.Line3D(AllplanGeo.Point3D(), AllplanGeo.Point3D(0, 0, 1000))

        rot_placement = AllplanReinf.BarPlacement(1, count, rot_axis, rot_angle, shape)


        #----------------- Create PythonPart

        views = [View2D3D ([model_cylinder])]

        pythonpart = PythonPart ("RotationalPlacement",
                                 parameter_list = build_ele.get_params_list(),
                                 hash_value     = build_ele.get_hash(),
                                 python_file    = build_ele.pyp_file_name,
                                 views          = views,
                                 reinforcement  = [rot_placement])

        self.model_ele_list = pythonpart.create()

        return (self.model_ele_list, self.handle_list)
