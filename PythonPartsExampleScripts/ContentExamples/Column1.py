"""
Script for Column1
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.CorbelReinfShapeBuilder as CorbelShapeBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

print('Load Column1.py')


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
    element = Column1(doc)

    return element.create(build_ele)


def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class Column1():
    """
    Definition of class Column1
    """

    def __init__(self, doc):
        """
        Initialisation of class Column1

        Args:
            doc: input document
        """

        self.model_ele_list = None
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
        #----------------- Create geometry
        geometry = self.create_geometry(build_ele)

        #----------------- Create reinforcement
        reinforcement = []
        if geometry is not None:
            reinforcement = self.create_reinforcement(build_ele)

        views = []
        views = [View2D3D ([geometry])]

        #----------------- Create PythonPart
        pythonpart = PythonPart ("Column",
                                 parameter_list = build_ele.get_params_list(),
                                 hash_value     = build_ele.get_hash(),
                                 python_file    = build_ele.pyp_file_name,
                                 views          = views,
                                 reinforcement  = reinforcement)
        self.model_ele_list = pythonpart.create()

        return (self.model_ele_list, self.handle_list)


    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        column_width = build_ele.ColumnWidth.value
        column_thickness = build_ele.ColumnThickness.value
        column_height = build_ele.ColumnHeight.value
        corbel_width = build_ele.CorbelWidth.value
        corbel_height = build_ele.CorbelHeight.value
        corbel_top = build_ele.CorbelTop.value


        #------------------ Create the column

        column = AllplanGeo.Polyhedron3D.CreateCuboid(column_width, column_thickness, column_height)

        pnt1 = AllplanGeo.Point3D(column_width, 0, corbel_top - corbel_height)
        pnt2 = AllplanGeo.Point3D(column_width + corbel_width, column_thickness, corbel_top)

        corbel = AllplanGeo.Polyhedron3D.CreateCuboid(pnt1, pnt2)

        err, polyhed = AllplanGeo.MakeUnion(column, corbel)

        if not GeometryValidate.polyhedron(err):
            return False

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        element = AllplanBasisElements.ModelElement3D(com_prop, polyhed)


        #------------------ Create the handles

        self.handle_list = [
            HandleProperties("ColumnWidthHandle",
                             AllplanGeo.Point3D(column_width, column_thickness / 2, 0),
                             AllplanGeo.Point3D(0,            column_thickness / 2, 0),
                             [("ColumnWidth", HandleDirection.x_dir)],
                             HandleDirection.x_dir),
            HandleProperties("ColumnThicknessHandle",
                             AllplanGeo.Point3D(column_width / 2, column_thickness, 0),
                             AllplanGeo.Point3D(column_width / 2, 0               , 0),
                             [("ColumnThickness", HandleDirection.y_dir)],
                             HandleDirection.y_dir),
            HandleProperties("ColumnHeightHandle",
                             AllplanGeo.Point3D(column_width, column_thickness, column_height),
                             AllplanGeo.Point3D(column_width, column_thickness, 0),
                             [("ColumnHeight", HandleDirection.z_dir)],
                             HandleDirection.z_dir),
            HandleProperties("CorbelTopHandle",
                             AllplanGeo.Point3D(column_width, 0, corbel_top),
                             AllplanGeo.Point3D(column_width, 0, 0),
                             [("CorbelTop", HandleDirection.z_dir)],
                             HandleDirection.z_dir),
            HandleProperties("CorbelHeightHandle",
                             AllplanGeo.Point3D(column_width + corbel_width, 0, corbel_top - corbel_height),
                             AllplanGeo.Point3D(column_width + corbel_width, 0, corbel_top),
                             [("CorbelHeight", HandleDirection.z_dir)],
                             HandleDirection.z_dir),
            HandleProperties("CorbelWidthHandle",
                             AllplanGeo.Point3D(column_width + corbel_width, column_thickness / 2, corbel_top),
                             AllplanGeo.Point3D(column_width               , column_thickness / 2, corbel_top),
                             [("CorbelWidth", HandleDirection.x_dir)],
                             HandleDirection.x_dir)
            ]

        return element


    def create_reinforcement(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        column_width = build_ele.ColumnWidth.value
        column_thickness = build_ele.ColumnThickness.value
        column_height = build_ele.ColumnHeight.value
        corbel_width = build_ele.CorbelWidth.value
        corbel_height = build_ele.CorbelHeight.value
        corbel_top = build_ele.CorbelTop.value

        steel_grade = 4
        diameter1 = 10
        corbel_diameter = 12
        bending_roller = 4

        concrete_cover = 25.

        stirrup_distance = 200.

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)


        #----------------- Create the stirrups

        shape_props = ReinforcementShapeProperties.rebar(diameter1, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralShapeBuilder.create_stirrup(column_width, column_thickness,
                                                   RotationAngles(0, 0, 0),
                                                   shape_props, concrete_cover_props)

        reinforcement = []

        if shape.IsValid():
            shape1 = AllplanReinf.BendingShape(shape)  # clone the shape

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, shape, AllplanGeo.Point3D(),
                    AllplanGeo.Point3D(0, 0, corbel_top - corbel_height),
                    concrete_cover, concrete_cover, stirrup_distance))

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    2, shape1, AllplanGeo.Point3D(0, 0, corbel_top),
                    AllplanGeo.Point3D(0, 0, column_height),
                    concrete_cover, concrete_cover, stirrup_distance))



        #------------------ Create the reinforcement inside the corbel

        shape_props = ReinforcementShapeProperties.rebar(corbel_diameter, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Freeform)

        shape = CorbelShapeBuilder.column_corbel_shape_type1(column_width, column_thickness,
                                                             corbel_width, corbel_top,
                                                             RotationAngles(90, 0, 0),
                                                             shape_props, concrete_cover)

        if shape.IsValid():
            place_pnt = AllplanGeo.Point3D(0, concrete_cover + corbel_diameter / 2., 0)

            shape.Move(AllplanGeo.Vector3D(place_pnt))

            reinforcement.append(
                AllplanReinf.BarPlacement(3, 1, AllplanGeo.Vector3D(0, 0, 0), place_pnt, place_pnt, shape))

        return reinforcement

