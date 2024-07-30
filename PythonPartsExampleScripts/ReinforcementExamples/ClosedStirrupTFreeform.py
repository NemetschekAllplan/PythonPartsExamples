"""
Example Script for Closed Stirrup Freeform
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

import StdReinfShapeBuilder.ProfileReinfShapeBuilder as ProfileShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

from TypeCollections import Curve3DList

print('Loading script: Closed Stirrup Freeform.py')


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
    element = ClosedStirrupFreeform(doc)

    return element.create(build_ele)


class ClosedStirrupFreeform():
    """
    Definition of class ClosedStirrupFreeform
    """

    def __init__(self, doc):
        """
        Initialisation of class ClosedStirrupFreeform

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc

        #----------------- geoemetry parameter values
        self.bottomheight          = 1000
        self.topheight             = 1000
        self.bottomwidth           = 1000
        self.topwidth              = 2000
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
        self.placement_length           = build_ele.PlacementLength.value
        self.bottomheight               = build_ele.BottomHeight.value
        self.bottomwidth                = build_ele.BottomWidth.value
        self.topwidth                   = build_ele.TopWidth.value
        self.topheight                  = build_ele.TopHeight.value

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

    def create_profile(self):
        """
        Create the profile of sweep solid
        Returns: created profile polyline
        """
        # topwidth evenly distributed
        delta = (self.topwidth - self.bottomwidth) / 2
        height = self.bottomheight + self.topheight

        #----------------- Create profile
        profile = AllplanGeo.Polyline3D()
        profile += AllplanGeo.Point3D(0, 0, 0)
        profile += AllplanGeo.Point3D(self.bottomwidth, 0, 0)
        if self.horizontal_placement:
            profile += AllplanGeo.Point3D(self.bottomwidth, 0, self.bottomheight)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, 0, self.bottomheight)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, 0, height)
            profile += AllplanGeo.Point3D(- delta, 0, height)
            profile += AllplanGeo.Point3D(- delta, 0, self.bottomheight)
            profile += AllplanGeo.Point3D(0, 0, self.bottomheight)
        else:
            profile += AllplanGeo.Point3D(self.bottomwidth, self.bottomheight, 0)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, self.bottomheight, 0)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, height, 0)
            profile += AllplanGeo.Point3D(- delta, height, 0)
            profile += AllplanGeo.Point3D(- delta, self.bottomheight, 0)
            profile += AllplanGeo.Point3D(0, self.bottomheight, 0)
        profile += AllplanGeo.Point3D(0, 0, 0)
        return profile

    def create_bar_polyline(self):
        """
        Create the reinforcement bar polyline
        Returns: created profile polyline
        """
        # topwidth evenly distributed
        delta = (self.topwidth - self.bottomwidth) / 2
        height = self.bottomheight + self.topheight

        #----------------- Create profile
        profile = AllplanGeo.Polyline3D()
        if self.horizontal_placement:
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, 0, self.bottomheight)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, 0, height)
            profile += AllplanGeo.Point3D(0, 0, height)
            profile += AllplanGeo.Point3D(0, self.diameter, 0) # use self.diameter so the bar doesn't intersect themself
            profile += AllplanGeo.Point3D(self.bottomwidth, self.diameter, 0)
            profile += AllplanGeo.Point3D(self.bottomwidth, self.diameter, height)
            profile += AllplanGeo.Point3D(- delta, self.diameter, height)
            profile += AllplanGeo.Point3D(- delta, self.diameter, self.bottomheight)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, self.diameter, self.bottomheight)
        else:
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, self.bottomheight, 0)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, height, 0)
            profile += AllplanGeo.Point3D(0, height, 0)
            profile += AllplanGeo.Point3D(0, self.diameter, 0) # use self.diameter so the bar doesn't intersect themself
            profile += AllplanGeo.Point3D(self.bottomwidth, self.diameter, 0)
            profile += AllplanGeo.Point3D(self.bottomwidth, self.diameter + height, 0)
            profile += AllplanGeo.Point3D(- delta, self.diameter + height, 0)
            profile += AllplanGeo.Point3D(- delta, self.diameter + self.bottomheight, 0)
            profile += AllplanGeo.Point3D(self.bottomwidth + delta, self.diameter + self.bottomheight, 0)

        return profile

    def create_geometry(self):
        """
        Create the geometry
        Returns: created poylhedron
        """
        #----------------- Create front profile
        frontprofile = self.create_profile()
        frontprofilepath = AllplanGeo.Path3D()
        frontprofilepath += frontprofile

        #----------------- Create back profile
        backprofile = self.create_profile()
        if self.horizontal_placement:
            backprofile = AllplanGeo.Move(backprofile, AllplanGeo.Vector3D(0, self.placement_length, 0))
        else:
            backprofile = AllplanGeo.Move(backprofile, AllplanGeo.Vector3D(0, 0, self.placement_length))
        backprofilepath = AllplanGeo.Path3D()
        backprofilepath += backprofile

        #----------------- Create connecting rail from bottom to top profile
        rails = Curve3DList([AllplanGeo.Line3D(frontprofile.GetStartPoint(), backprofile.GetStartPoint())])
        profiles = Curve3DList([frontprofilepath, backprofilepath])

        _, brep = AllplanGeo.CreateRailSweptBRep3D(profiles, rails, True, True, False)
        return brep

    def create_reinforcement(self):
        """
        Create the stirrup placement
        Returns: created stirrup reinforcement
        """
        # get the profile
        profile = self.create_bar_polyline()

        # define shape properties
        shape_props = ReinforcementShapeProperties.rebar(self.diameter, self.bending_roller, self.steel_grade,
                                                         self.concrete_grade, AllplanReinf.BendingShapeType.Freeform)

        placement_start_point = AllplanGeo.Point3D(0, 0, 0)
        placement_end_point = AllplanGeo.Point3D(0, self.placement_length, 0)
        rotation_matrix = ProfileShapeBuilder.get_rotation_matrix_from_xz_to_xy()
        if not self.horizontal_placement:
            rotation_matrix = AllplanGeo.Matrix3D()
            placement_end_point = AllplanGeo.Point3D(0, 0, self.placement_length)

        # define shape
        shape = ProfileShapeBuilder.create_profile_stirrup(profile,
                                                           rotation_matrix,
                                                           shape_props,
                                                           self.concrete_cover,
                                                           AllplanReinf.StirrupType.Column)

        reinforcement = []
        if shape.IsValid():
            reinforcement.append (LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                1, shape, placement_start_point, placement_end_point,
                self.concrete_cover, self.concrete_cover, self.distance))
        return reinforcement

    def create_handles(self):
        """
        Create handles

        Args:
            build_ele:  the building element.
        """
        delta = (self.topwidth - self.bottomwidth) / 2

        # Handle for Height dimensions
        if self.horizontal_placement:

            self.handle_list.append(
                HandleProperties("BottomHeight",
                                 AllplanGeo.Point3D(0, 0, self.bottomheight),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("BottomHeight", HandleDirection.z_dir)],
                                 HandleDirection.z_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("TopHeight",
                                 AllplanGeo.Point3D(-delta, 0, self.bottomheight + self.topheight),
                                 AllplanGeo.Point3D(-delta, 0, self.bottomheight),
                                 [("TopHeight", HandleDirection.z_dir)],
                                 HandleDirection.z_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("BottomWidth",
                                 AllplanGeo.Point3D(self.bottomwidth, 0, 0),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("BottomWidth", HandleDirection.x_dir)],
                                 HandleDirection.x_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("TopWidth",
                                 AllplanGeo.Point3D(self.bottomwidth + delta, self.placement_length, self.bottomheight + self.topheight),
                                 AllplanGeo.Point3D(-delta, self.placement_length, self.bottomheight + self.topheight),
                                 [("TopWidth", HandleDirection.x_dir)],
                                 HandleDirection.x_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("PlacementLength",
                                 AllplanGeo.Point3D(0, self.placement_length, 0),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("PlacementLength", HandleDirection.y_dir)],
                                 HandleDirection.y_dir,
                                 True))

        else:
            self.handle_list.append(
                HandleProperties("BottomHeight",
                                 AllplanGeo.Point3D(0, self.bottomheight, 0),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("BottomHeight", HandleDirection.y_dir)],
                                 HandleDirection.y_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("TopHeight",
                                 AllplanGeo.Point3D(-delta, self.bottomheight + self.topheight, 0),
                                 AllplanGeo.Point3D(-delta, self.bottomheight, 0),
                                 [("TopHeight", HandleDirection.y_dir)],
                                 HandleDirection.y_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("BottomWidth",
                                 AllplanGeo.Point3D(self.bottomwidth, 0, 0),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("BottomWidth", HandleDirection.x_dir)],
                                 HandleDirection.x_dir,
                                 True))

            self.handle_list.append(
                HandleProperties("TopWidth",
                                 AllplanGeo.Point3D(self.bottomwidth + delta, self.bottomheight + self.topheight, self.placement_length),
                                 AllplanGeo.Point3D(-delta, self.bottomheight + self.topheight, self.placement_length),
                                 [("TopWidth", HandleDirection.x_dir)],
                                 HandleDirection.x_dir,
                                 True))

            # Handle for PlacementLength dimension
            self.handle_list.append(
                HandleProperties("PlacementLength",
                                 AllplanGeo.Point3D(0, 0, self.placement_length),
                                 AllplanGeo.Point3D(0, 0, 0),
                                 [("PlacementLength", HandleDirection.z_dir)],
                                 HandleDirection.z_dir,
                                 True))

