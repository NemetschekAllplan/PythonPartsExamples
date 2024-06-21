"""
Example Script for Closed Stirrup Spiral Freeform
"""

import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

print('Loading script: Closed Stirrup Spiral Freeform.py')


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
    element = ClosedStirrupSpiralFreeform(doc)

    return element.create(build_ele)


class ClosedStirrupSpiralFreeform():
    """
    Definition of class ClosedStirrupSpiralFreeform
    """

    def __init__(self, doc):
        """
        Initialisation of class ClosedStirrupSpiralFreeform

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc

        #----------------- geoemetry parameter values
        self.height                = 1000
        self.width                 = 1000
        self.placement_length      = 3000

        #----------------- reinforcement parameter values
        self.horizontal_placement  = None
        self.concrete_grade        = None
        self.concrete_cover        = None
        self.diameter              = None
        self.bending_roller        = None
        self.steel_grade           = None
        self.distance              = None
        self.mesh_type             = None

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
        self.height                     = build_ele.Height.value
        self.width                      = build_ele.Width.value
        self.placement_length           = build_ele.PlacementLength.value

        #----------------- Extract reinforcement parameter values
        self.horizontal_placement       = build_ele.HorizontalPlacement.value
        self.concrete_grade             = build_ele.ConcreteGrade.value
        self.concrete_cover             = build_ele.ConcreteCover.value
        self.diameter                   = build_ele.Diameter.value
        self.bending_roller             = build_ele.BendingRoller.value
        self.steel_grade                = build_ele.SteelGrade.value
        self.distance                   = build_ele.Distance.value

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
                                 common_props   = self.com_prop)

        self.model_ele_list = pythonpart.create()

    def create_spiral(self):
        """
        Create the profile of sweep solid
        Returns: created profile polyline
        """
        profile = AllplanGeo.Polyline3D()
        bendling_roller_list = AllplanUtil.VecDoubleList()

        # spiral segement count
        spiral_count = int((self.placement_length - 2 * self.concrete_cover) / self.distance)
        # stirrup holds 4 points for one spiral segement
        spiral_delta = self.distance / 4
        # stirrup concrete coverage
        spiral_coverage = self.concrete_cover + self.diameter/2

        # define the spiral points
        spiral_point_offset = self.concrete_cover
        for _ in range(1, spiral_count + 1):
            profile += AllplanGeo.Point3D(0 + spiral_coverage,
                                          spiral_point_offset,
                                          0 + spiral_coverage)
            spiral_point_offset += spiral_delta

            profile += AllplanGeo.Point3D(self.width - spiral_coverage,
                                          spiral_point_offset,
                                          0 + spiral_coverage)
            spiral_point_offset += spiral_delta

            profile += AllplanGeo.Point3D(self.width - spiral_coverage,
                                          spiral_point_offset,
                                          self.height - spiral_coverage)
            spiral_point_offset += spiral_delta

            profile += AllplanGeo.Point3D(0 + spiral_coverage,
                                          spiral_point_offset,
                                          self.height - spiral_coverage)
            spiral_point_offset += spiral_delta

        profile += AllplanGeo.Point3D(0 + spiral_coverage,
                                      spiral_point_offset,
                                      0 + spiral_coverage)

        # profile must be rotated for vertical placement and moved back into 3D body
        if not self.horizontal_placement:
            rot_mat = AllplanGeo.Matrix3D()
            rot_angle = AllplanGeo.Angle()
            rot_angle.SetDeg(90)
            rot_mat.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(), AllplanGeo.Point3D(1000, 0, 0)), rot_angle)
            rot_mat.Translate(AllplanGeo.Vector3D(0, self.height, 0))
            profile = AllplanGeo.Transform (profile, rot_mat)

        # define bending roller values for every point of spiral
        for _ in range(profile.Count()):
            bendling_roller_list.append(self.bending_roller)

        return (profile, bendling_roller_list)

    def create_geometry(self):
        """
        Create the geometry
        Returns: created poylhedron
        """
        corner1 = AllplanGeo.Point3D(0, 0, 0)
        corner2 = AllplanGeo.Point3D(self.width, self.placement_length, self.height)
        if not self.horizontal_placement:
            corner2 = AllplanGeo.Point3D(self.width, self.height, self.placement_length)
        geometry = AllplanGeo.Polyhedron3D.CreateCuboid(corner1, corner2)
        return geometry

    def create_reinforcement(self):
        """
        Create the stirrup placement
        Returns: created stirrup reinforcement
        """
        # get the profile
        profile, bendling_roller_list = self.create_spiral()

        # define shape
        shape = AllplanReinf.BendingShape(profile, bendling_roller_list, self.diameter, self.steel_grade,
                                          self.concrete_grade, AllplanReinf.BendingShapeType.Freeform)

        reinforcement = []
        if shape.IsValid():
            reinforcement.append(AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(), AllplanGeo.Point3D(),
                                                           AllplanGeo.Point3D(), shape))
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
                HandleProperties("Height",
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

