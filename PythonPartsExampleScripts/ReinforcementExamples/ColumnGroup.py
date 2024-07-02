"""
Example Script for Columns with reinforcement as python pyrt group
"""

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.MeshPlacementBuilder as MeshPlacementBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

from PythonPart import View2D3D, PythonPart, PythonPartGroup

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
    element = ColumnGroupExample(doc)

    return element.create(build_ele)


class ColumnGroupExample():
    """
    Definition of class ColumnGroupExample
    """

    def __init__(self, doc):
        """
        Initialisation of class ColumnGroupExample

        Args:
            doc: input document
        """
        self.model_elem_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        column = self.create_column_body(build_ele)
        reinforcement = self.create_reinforcement(build_ele) if build_ele.CreateReinf.value else []

        matrix_list = []
        python_parts_for_group = []

        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), build_ele.Radius.value, True)
        path = AllplanGeo.Path2D()
        path += arc
        division = AllplanGeo.DivisionPoints(path, build_ele.Divisions.value-1, 0.0)
        points = division.GetPoints()
        points.append(AllplanGeo.Point3D(arc.GetStartPoint().X, arc.GetStartPoint().Y, 0))
        angles = division.GetPointAngles()
        angles.append(AllplanGeo.Angle(math.pi/2))

        for point, angle in zip(points, angles):
            matrix = AllplanGeo.Matrix3D()
            matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Point3D(0, 0, 1)),
                            angle)
            matrix.Translate(AllplanGeo.Vector3D(point.X, point.Y, 0))
            matrix_list.append(matrix)

        for matrix in matrix_list:
            column_views = [View2D3D ([column])]
            pythonpart = PythonPart ("Column", build_ele.get_params_list(),
                                     build_ele.get_hash(), build_ele.pyp_file_name,
                                     views = column_views, matrix = matrix,
                                     reinforcement = reinforcement)
            python_parts_for_group.append(pythonpart)

        pythonpartgroup = PythonPartGroup ("ColumnGroup", build_ele.get_params_list(), build_ele.get_hash(),
                                           build_ele.pyp_file_name, python_parts_for_group)

        self.model_elem_list = pythonpartgroup.create()

        return (self.model_elem_list, self.handle_list)

    def create_column_body(self, build_ele):
        """
        Create the column geometry

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        column_width     = build_ele.ColumnWidth.value
        column_thickness = build_ele.ColumnThickness.value
        column_height    = build_ele.ColumnHeight.value

        #------------------ Create the column

        column = AllplanGeo.Polyhedron3D.CreateCuboid(column_width, column_thickness, column_height)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        return AllplanBasisElements.ModelElement3D(com_prop, column)

    def create_reinforcement(self, build_ele):
        """
        Create the column reinforcement

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        column_width = build_ele.ColumnWidth.value
        column_thickness = build_ele.ColumnThickness.value
        column_height = build_ele.ColumnHeight.value

        steel_grade      = 4
        diameter1        = 10
        bending_roller   = 4
        concrete_cover   = 25.
        stirrup_distance = 200.

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

        reinf_ele_list = []

        #----------------- Create the stirrups

        shape_props = ReinforcementShapeProperties.rebar(diameter1, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralShapeBuilder.create_stirrup(column_width, column_thickness,
                                                   RotationAngles(0, 0, 0),
                                                   shape_props, concrete_cover_props)

        if shape.IsValid():
            reinf_ele_list.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, shape, AllplanGeo.Point3D(),
                    AllplanGeo.Point3D(0, 0, 1000),
                    concrete_cover, concrete_cover, stirrup_distance))


        #----------------- mesh

        mesh_type        = AllplanReinf.ReinforcementSettings.GetMeshType()
        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        shape_props = ReinforcementShapeProperties.mesh(mesh_type, mesh_bending_dir,
                                                        bending_roller, -1,
                                                        AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralShapeBuilder.create_stirrup(column_width, column_thickness,
                                                   RotationAngles(0, 0, 0),
                                                   shape_props,
                                                   concrete_cover_props)

        if shape.IsValid():
            value_list = [(shape, 0)]

            MeshPlacementBuilder.create_mesh_placement_by_points(value_list,
                                                                 AllplanGeo.Point3D(0, 0, 1000),
                                                                 AllplanGeo.Point3D(0, 0, column_height),
                                                                 1,
                                                                 concrete_cover,
                                                                 concrete_cover,
                                                                 reinf_ele_list)

        return reinf_ele_list
