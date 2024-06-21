"""
Script for SleeveFoundation
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

import StdReinfShapeBuilder.SleeveFoundationReinfShapeBuilder as SleeveFoundReinfBuilder
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.BarPlacementUtil as BarUtil
import StdReinfShapeBuilder.MeshPlacementBuilder as MeshPlacementBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from HandleService import HandleService
from PythonPart import View2D3D, PythonPart


print('Load SleeveFoundation.py')


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
    Creation of the sleeve foundation

    Args:
        build_ele:  the building element with the table data.
        doc:        Input document
    """

    element = SleeveFoundation(doc)

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

    element = SleeveFoundation(doc)

    return element.create(build_ele)


class SleeveFoundation():
    """
    Definition of class SleeveFoundation
    """

    def __init__(self, doc):
        """
        Initialisation of class SleeveFoundation

        Args:
            doc:  input document
        """
        self.model_ele_list = None
        self.handle_list = []
        self.sleeve_pnt_bot = None
        self.document = doc


    def create(self, build_ele):
        """
        Create the sleeve foundation

        Args:
            buidlEle:  the building element.

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
        pythonpart = PythonPart ("SleeveFoundation",
                                 parameter_list = build_ele.get_params_list(),
                                 hash_value     = build_ele.get_hash(),
                                 python_file    = build_ele.pyp_file_name,
                                 views          = views,
                                 reinforcement  = reinforcement)
        self.model_ele_list = pythonpart.create()

        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(),
                                             build_ele.RotationAngleX.value,
                                             build_ele.RotationAngleY.value,
                                             build_ele.RotationAngleZ.value,
                                             self.model_ele_list)

        rot_angles = RotationAngles(build_ele.RotationAngleX.value,
                                    build_ele.RotationAngleY.value,
                                    build_ele.RotationAngleZ.value)

        HandleService.transform_handles(self.handle_list, rot_angles.get_rotation_matrix())

        return (self.model_ele_list, self.handle_list)


    def create_geometry(self, build_ele):
        """
        Create the geometry

        Args
            buidlEle:  the building element.
        """

        found_length = build_ele.FoundationLength.value
        found_width = build_ele.FoundationWidth.value
        found_height = build_ele.FoundationHeight.value
        sleeve_out_length = build_ele.SleeveOutLength.value
        sleeve_out_width = build_ele.SleeveOutWidth.value
        sleeve_height = build_ele.SleeveHeight.value
        sleeve_chamfer = build_ele.SleeveChamfer.value
        sleeve_thickness = build_ele.SleeveThickness.value

        if found_length == 0  or  found_width == 0  or found_height == 0:
            return None


        #------------- Slab foundation

        sleeve_found = AllplanGeo.Polyhedron3D.CreateCuboid(found_length, found_width, found_height)

        self.sleeve_pnt_bot = AllplanGeo.Point3D((found_length - sleeve_out_length) / 2.,
                                                 (found_width  - sleeve_out_width) / 2.,
                                                 found_height)


        #----------------- Sleeve outside volume

        sleeve_out = AllplanGeo.Polyhedron3D.CreateCuboid(
            self.sleeve_pnt_bot,
            self.sleeve_pnt_bot + AllplanGeo.Point3D(sleeve_out_length,
                                                     sleeve_out_width,
                                                     sleeve_height))

        err, sleeve_found = AllplanGeo.MakeUnion(sleeve_found, sleeve_out)

        if not GeometryValidate.polyhedron(err):
            return None


        #----------------- Sleeve volume

        sleeve_length = sleeve_out_length - 2. * sleeve_thickness
        sleeve_width = sleeve_out_width  - 2. * sleeve_thickness


        err, sleeve = AllplanGeo.CreateFrustumOfPyramid(
            sleeve_length,
            sleeve_width,
            -sleeve_height,
            -sleeve_chamfer,
            AllplanGeo.Plane3D(AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Vector3D(0, 0, 1000)))

        if not GeometryValidate.polyhedron(err):
            return None

        err, sleeve_found = AllplanGeo.MakeSubtraction(
            sleeve_found,
            AllplanGeo.Move(
                sleeve,
                AllplanGeo.Vector3D(self.sleeve_pnt_bot + AllplanGeo.Point3D(sleeve_thickness,
                                                                             sleeve_thickness,
                                                                             sleeve_height))))

        if not GeometryValidate.polyhedron(err):
            return None

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        geometry_element = AllplanBasisElements.ModelElement3D(com_prop, sleeve_found)


        #------------- Create the handles

        self.handle_list = [HandleProperties("FoundationLengthHandle",
                                             AllplanGeo.Point3D(found_length, found_width / 2, 0),
                                             AllplanGeo.Point3D(0           , found_width / 2, 0),
                                             [("FoundationLength", HandleDirection.point_dir)],
                                             HandleDirection.point_dir),
                            HandleProperties("FoundationWidthHandle",
                                             AllplanGeo.Point3D(found_length / 2, found_width, 0),
                                             AllplanGeo.Point3D(found_length / 2, 0          , 0),
                                             [("FoundationWidth", HandleDirection.point_dir)],
                                             HandleDirection.point_dir),
                            HandleProperties("FoundationHeightHandle",
                                             AllplanGeo.Point3D(found_length, found_width, found_height),
                                             AllplanGeo.Point3D(found_length, found_width, 0),
                                             [("FoundationHeight", HandleDirection.point_dir)],
                                             HandleDirection.point_dir)
                           ]

        return geometry_element


    def create_reinforcement(self, build_ele):
        """
        Create the reinforcement elements

        Args:
            build_ele:  the building element.
        """

        found_length = build_ele.FoundationLength.value
        found_width = build_ele.FoundationWidth.value
        found_height = build_ele.FoundationHeight.value
        sleeve_out_length = build_ele.SleeveOutLength.value
        sleeve_out_width = build_ele.SleeveOutWidth.value
        sleeve_height = build_ele.SleeveHeight.value
        sleeve_thickness = build_ele.SleeveThickness.value

        reinforcement = [] # will be filled with reinforcement

        diameter2 = 10
        diameter_found_x = 10
        diameter_found_y = 20

        found_concrete_cover = 25.

        bar_dist_found_x = 200.
        bar_dist_found_y = 150.

        steel_grade = 4
        bending_roller = 4

        stirrup_top_distance = 50.

        mesh_type = build_ele.FoundMeshType.value

        if mesh_type != "":
            mesh_data = AllplanReinf.ReinforcementShapeBuilder.GetMeshData(mesh_type)

            diameter_found_y = mesh_data.DiameterLongitudinal
            diameter_found_x = mesh_data.DiameterCross

        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        start_bar_pos  = AllplanReinf.ReinforcementUtil.GetNextBarPositionNumber(self.document) - 1
        start_mesh_pos = AllplanReinf.ReinforcementUtil.GetNextMeshPositionNumber(self.document) - 1


        #------------- Vertical shape in the sleeve wall and foundation

        shape_props = ReinforcementShapeProperties.rebar(build_ele.SleeveUShapeDiameter.value, bending_roller,
                                                         steel_grade, -1, AllplanReinf.BendingShapeType.Freeform)

        shape = SleeveFoundReinfBuilder.    \
            create_vertial_sleeve_foundation_shape(found_length, found_height,
                                                   self.sleeve_pnt_bot.X,
                                                   sleeve_out_length,
                                                   sleeve_height, sleeve_thickness,
                                                   RotationAngles(90, 0, 0),
                                                   shape_props,
                                                   found_concrete_cover + diameter_found_x + diameter_found_y,
                                                   found_concrete_cover,
                                                   found_concrete_cover + diameter2, found_concrete_cover + diameter2)

        if shape.IsValid() is True:
            shape1 = AllplanReinf.BendingShape(shape)  # clone the shape

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_count(
                    start_bar_pos + 1,
                    shape,
                    AllplanGeo.Point3D(0, self.sleeve_pnt_bot.Y, 0),
                    AllplanGeo.Point3D(0, self.sleeve_pnt_bot.Y + sleeve_thickness, 0),
                    found_concrete_cover,
                    found_concrete_cover,
                    3))

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_count(
                    start_bar_pos + 2,
                    shape1,
                    AllplanGeo.Point3D(0,
                                       self.sleeve_pnt_bot.Y + sleeve_out_width - sleeve_thickness,
                                       0),
                    AllplanGeo.Point3D(0,
                                       self.sleeve_pnt_bot.Y + sleeve_out_width,
                                       0),
                    found_concrete_cover,
                    found_concrete_cover,
                    3))


        #------------- Create the horizontal reinforcement inside the vertical(X/Y) sleeve walls

        shape_props = ReinforcementShapeProperties.rebar(diameter2, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape = SleeveFoundReinfBuilder.create_sleeve_wall_shape(sleeve_out_width,
                                                                 sleeve_thickness,
                                                                 RotationAngles(0, 0, 90),
                                                                 shape_props,
                                                                 found_concrete_cover)

        if shape.IsValid() is True:
            shape1 = AllplanReinf.BendingShape(shape)  # clone the shape

            ref_pnt_bot = self.sleeve_pnt_bot + AllplanGeo.Point3D(sleeve_thickness, 0, 0)

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(
                    start_bar_pos + 3,
                    shape,
                    ref_pnt_bot + AllplanGeo.Point3D(0, 0, sleeve_height),
                    ref_pnt_bot,
                    found_concrete_cover,
                    stirrup_top_distance,
                    3))

            ref_pnt_bot = self.sleeve_pnt_bot + AllplanGeo.Point3D(sleeve_out_length, 0, 0)

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(
                    start_bar_pos + 4,
                    shape1,
                    ref_pnt_bot + AllplanGeo.Point3D(0, 0, sleeve_height),
                    ref_pnt_bot,
                    found_concrete_cover,
                    stirrup_top_distance,
                    3))



        #------------- Create the horizontal reinforcement inside the horizontal(X/Y) sleeve walls

        shape_props = ReinforcementShapeProperties.rebar(diameter2, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape = SleeveFoundReinfBuilder.create_sleeve_wall_shape(sleeve_out_length, sleeve_thickness,
                                                                 RotationAngles(0, 0, 0),
                                                                 shape_props, found_concrete_cover)

        if shape.IsValid() is True:
            shape1 = AllplanReinf.BendingShape(shape)  # clone the shape

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(
                    start_bar_pos + 5,
                    shape,
                    self.sleeve_pnt_bot + AllplanGeo.Point3D(0, 0, sleeve_height - diameter2),
                    self.sleeve_pnt_bot,
                    found_concrete_cover,
                    stirrup_top_distance,
                    3))

            ref_pnt_bot = self.sleeve_pnt_bot + AllplanGeo.Point3D(
                0, sleeve_out_width - sleeve_thickness, 0)

            reinforcement.append(
                LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(
                    start_bar_pos + 6,
                    shape1,
                    ref_pnt_bot + AllplanGeo.Point3D(0, 0, sleeve_height - diameter2),
                    ref_pnt_bot,
                    found_concrete_cover,
                    stirrup_top_distance,
                    3))


        #----------------- Foundation reinforcement -----------------------------------------------


        if mesh_type == "":

            #------------- Create the reinforcement inside the foundation for the Y direction

            shape_props = ReinforcementShapeProperties.rebar(diameter_found_y, bending_roller, steel_grade, -1,
                                                             AllplanReinf.BendingShapeType.LongitudinalBar)

            concrete_cover_props = ConcreteCoverProperties.all(found_concrete_cover)

            shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(found_length,
                                                                             RotationAngles(90, 0, 0),
                                                                             shape_props, concrete_cover_props)

            if shape.IsValid() is True:
                cover_left_right_x = BarUtil.get_placement_start_from_bending_roller(
                    shape,
                    1,
                    bending_roller,
                    AllplanGeo.Line2D(AllplanGeo.Point2D(), AllplanGeo.Point2D(found_length, 0)),
                    diameter_found_x,
                    RotationAngles(-90, 0, 0))

                reinforcement.append(
                    LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                        start_bar_pos + 7,
                        shape,
                        AllplanGeo.Point3D(),
                        AllplanGeo.Point3D(0, found_width, 0),
                        found_concrete_cover,
                        found_concrete_cover,
                        bar_dist_found_y))


            #------------- Create the reinforcement inside the foundation for the X direction

            shape_props = ReinforcementShapeProperties.rebar(diameter_found_x, bending_roller, steel_grade, -1,
                                                             AllplanReinf.BendingShapeType.LongitudinalBar)

            concrete_cover_props = ConcreteCoverProperties.left_right_bottom(found_concrete_cover,
                                                                             found_concrete_cover,
                                                                             found_concrete_cover + diameter_found_y)

            shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(found_width,
                                                                             RotationAngles(90, 0, 90),
                                                                             shape_props, concrete_cover_props)

            if shape.IsValid() is True:
                reinforcement.append(
                    LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                        start_bar_pos + 8,
                        shape,
                        AllplanGeo.Point3D(),
                        AllplanGeo.Point3D(found_length, 0, 0),
                        cover_left_right_x,
                        cover_left_right_x,
                        bar_dist_found_x))

        else:
            shape_props = ReinforcementShapeProperties.mesh(mesh_type, mesh_bending_dir, -1, bending_roller,
                                                            AllplanReinf.BendingShapeType.LongitudinalBar)

            concrete_cover_props = ConcreteCoverProperties.all(found_concrete_cover)

            shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(found_length,
                                                                             RotationAngles(90, 0, 0),
                                                                             shape_props,
                                                                             concrete_cover_props)

            if shape.IsValid() is True:
                MeshPlacementBuilder.create_mesh_placement_by_points([(shape, 0)],
                                                                     AllplanGeo.Point3D(),
                                                                     AllplanGeo.Point3D(0, found_width, 0),
                                                                     start_mesh_pos,
                                                                     found_concrete_cover,
                                                                     found_concrete_cover,
                                                                     reinforcement)

        return reinforcement
