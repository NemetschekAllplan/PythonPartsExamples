"""
Example Script for Open Stirrup
"""

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

print('Loading script: Open Stirrup.py')


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

def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = OpenStirrupWithArc(doc)

    return element.create(build_ele)


class OpenStirrupWithArc():
    """
    Definition of class OpenStirrupWithArc
    """

    def __init__(self, doc):
        """
        Initialisation of class OpenStirrupWithArc

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc

        #----------------- geoemetry parameter values
        self.width                 = 2000
        self.placement_length      = 3000
        self.height                = 1000

        #----------------- reinforcement parameter values
        self.horizontal_placement  = None
        self.concrete_grade        = None
        self.concrete_cover        = None
        self.diameter              = None
        self.bending_roller        = None
        self.steel_grade           = None
        self.distance              = None
        self.mesh_type             = None
        self.start_hook            = None
        self.end_hook              = None

        #----------------- format parameter values
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.texturedef = None

    def read_values(self, build_ele):
        """
        Read palette parameter values

        Args:
            build_ele:  the building element.
        """
        #----------------- Extract palette geoemetry parameter values
        self.width                      = build_ele.Width.value
        self.placement_length           = build_ele.PlacementLength.value
        self.height                     = build_ele.Height.value

        #----------------- Extract reinforcement parameter values
        self.horizontal_placement       = build_ele.HorizontalPlacement.value
        self.concrete_grade             = build_ele.ConcreteGrade.value
        self.concrete_cover             = build_ele.ConcreteCover.value
        self.diameter                   = build_ele.Diameter.value
        self.bending_roller             = build_ele.BendingRoller.value
        self.steel_grade                = build_ele.SteelGrade.value
        self.distance                   = build_ele.Distance.value
        self.start_hook                 = build_ele.StartHook.value
        self.start_hook_angle           = build_ele.StartHookAngle.value
        self.end_hook                   = build_ele.EndHook.value
        self.end_hook_angle             = build_ele.EndHookAngle.value

        #----------------- Extract palette format parameter values
        self.texturedef                 = AllplanBasisElements.TextureDefinition(build_ele.Surface.value)
        self.com_prop.Color             = build_ele.Color.value
        self.com_prop.Pen               = build_ele.Pen.value
        self.com_prop.Stroke            = build_ele.Stroke.value
        self.com_prop.Layer             = build_ele.Layer.value
        self.com_prop.HelpConstruction  = build_ele.UseConstructionLineMode.value

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.read_values(build_ele)
        self.create_stirrup(build_ele)
        self.create_handles()
        return (self.model_ele_list, self.handle_list)

    def create_stirrup(self, build_ele):
        """
        Create the geometry

        Args:
            build_ele:  the building element.
        """
        polyhedron = self.create_geometry()
        reinforcement = self.create_reinforcement()

        #----------------- Create PythonPart view
        views = [View2D3D ([AllplanBasisElements.ModelElement3D(self.com_prop, self.texturedef, polyhedron)])]

        #----------------- Create PythonPart
        pythonpart = PythonPart ("Stirrup",
                                 parameter_list = build_ele.get_params_list(),
                                 hash_value     = build_ele.get_hash(),
                                 python_file    = build_ele.pyp_file_name,
                                 views          = views,
                                 reinforcement  = reinforcement,
                                 common_props = self.com_prop)

        self.model_ele_list = pythonpart.create()

    def create_geometry(self):
        """
        Create the geometry
        Returns: created poylhedron
        """
        corner1 = AllplanGeo.Point3D(0, 0, 0)
        corner2 = AllplanGeo.Point3D(self.width, self.placement_length, self.height)
        if not self.horizontal_placement:
            corner2 = AllplanGeo.Point3D(self.width, self.height, self.placement_length)
        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(corner1, corner2)
        return polyhed

    def create_reinforcement(self):
        """
        Create the stirrup placement
        Returns: created stirrup reinforcement
        """
        concrete_cover_props = ConcreteCoverProperties(self.concrete_cover, self.concrete_cover,
                                                       self.concrete_cover, self.concrete_cover)

        shape_props = ReinforcementShapeProperties.rebar(self.diameter, self.bending_roller,
                                                         self.steel_grade, self.concrete_grade,
                                                         AllplanReinf.BendingShapeType.BarWithArc)

        placement_start_point = AllplanGeo.Point3D(0, 0, 0)
        placement_end_point   = AllplanGeo.Point3D(0, self.placement_length, 0)
        rotation_angles       = RotationAngles(90, 0 , 0)

        if not self.horizontal_placement:
            rotation_angles     = RotationAngles(0, 0 , 0)
            placement_end_point = AllplanGeo.Point3D(0, 0, self.placement_length)


        #----------------- create the shape

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        line1  = AllplanGeo.Line2D(self.width, self.height, self.width, 0)
        line2  = AllplanGeo.Line2D(0, 0, 0, self.height)
        radius = self.width / 2

        arc  = AllplanGeo.Arc2D(AllplanGeo.Point2D(radius, radius), radius, radius, 0, math.pi, 2 * math.pi, False)

        shape_builder.AddSides([(self.concrete_cover),
                                (line1, -self.concrete_cover),
                                (arc, -self.concrete_cover),
                                (line2, -self.concrete_cover),
                                (self.concrete_cover)])

        if self.start_hook:
            shape_builder.SetHookStart(0, -self.start_hook_angle, AllplanReinf.HookType.eStirrup)

        if self.end_hook:
            shape_builder.SetHookEnd(0, -self.end_hook_angle, AllplanReinf.HookType.eStirrup)

        shape = shape_builder.CreateShape(shape_props)

        shape.Transform(rotation_angles.get_rotation_matrix())

        reinforcement = []

        if shape.IsValid():
            reinforcement.append (LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                1, shape,
                placement_start_point,
                placement_end_point,
                self.concrete_cover,
                self.concrete_cover,
                self.distance))
        return reinforcement

    def create_handles(self):
        """
        Create handles

        Args:
            build_ele:  the building element.
        """
        if self.horizontal_placement:
            # Handle for Height
            self.handle_list.append(
                HandleProperties("Height",
                                 AllplanGeo.Point3D(0, 0, self.height),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("Height", HandleDirection.z_dir)],
                                 HandleDirection.z_dir,
                                 True))

            # Handle for Bottom XY dimension
            self.handle_list.append(
                HandleProperties("PlacementLength",
                                 AllplanGeo.Point3D(0, self.placement_length, 0),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("PlacementLength", HandleDirection.y_dir)],
                                 HandleDirection.y_dir,
                                 True))
        else:
            # Handle for Height
            self.handle_list.append(
                HandleProperties("PlacementLength",
                                 AllplanGeo.Point3D(0, 0, self.placement_length),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("PlacementLength", HandleDirection.z_dir)],
                                 HandleDirection.z_dir,
                                 True))

            # Handle for Bottom XY dimension
            self.handle_list.append(
                HandleProperties("Height",
                                 AllplanGeo.Point3D(0, self.height, 0),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("Height", HandleDirection.y_dir)],
                                 HandleDirection.y_dir,
                                 True))

        # Handle for Bottom XY dimension
        self.handle_list.append(
            HandleProperties("Width",
                             AllplanGeo.Point3D(self.width, 0, 0),
                             AllplanGeo.Point3D(0, 0, 0),
                             [("Width", HandleDirection.x_dir)],
                             HandleDirection.x_dir,
                             True))
