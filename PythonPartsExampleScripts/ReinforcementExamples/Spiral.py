"""
Example Script for Spiral
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

print('Loading script: Spiral.py')


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
    element = Spiral(doc)

    return element.create(build_ele)


class Spiral():
    """
    Definition of class Spiral
    """

    def __init__(self, doc):
        """
        Initialisation of class Spiral

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc

        #----------------- format parameter values
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()

    def read_values(self, build_ele):
        """
        Read palette parameter values

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette geoemetry parameter values
        self.height                     = build_ele.Height.value
        self.radius                     = build_ele.Radius.value

        #----------------- Extract reinforcement parameter values
        self.layer                  = build_ele.Layer.value
        self.pen_by_layer           = build_ele.PenByLayer.value
        self.stroke_by_layer        = build_ele.StrokeByLayer.value
        self.color_by_layer         = build_ele.ColorByLayer.value
        self.concrete_grade         = build_ele.ConcreteGrade.value
        self.concrete_cover         = build_ele.ConcreteCover.value
        self.place_per_linear_meter = build_ele.PlacePerLinearMeter.value
        self.diameter               = build_ele.Diameter.value
        self.steel_grade            = build_ele.SteelGrade.value
        self.pitch                  = build_ele.Pitch.value
        self.start_hook             = build_ele.StartHook.value
        self.start_hook_length      = build_ele.StartHookLength.value
        self.start_hook_angle       = build_ele.StartHookAngle.value
        self.end_hook               = build_ele.EndHook.value
        self.end_hook_length        = build_ele.EndHookLength.value
        self.end_hook_angle         = build_ele.EndHookAngle.value


    def create_reinf_common_prop(self):
        """
        Create the reinforcement common properties
        """

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        if self.layer == "Standard":
            com_prop.Layer = 3700

        elif self.layer == "RU_ALL":
            com_prop.Layer = 3864

        elif self.layer == "RU_R":
            com_prop.Layer = 3829

        com_prop.PenByLayer    = self.pen_by_layer
        com_prop.StrokeByLayer = self.stroke_by_layer
        com_prop.ColorByLayer  = self.color_by_layer

        return com_prop


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.read_values(build_ele)

        cylinder = self.create_geometry()
        spiral   = self.create_reinforcement(build_ele)

        self.model_ele_list = [AllplanBasisElements.ModelElement3D(self.com_prop, cylinder), spiral]


        #----------------- create the PythonPart

        if build_ele.IsPythonPart.value:
            views = [View2D3D ([self.model_ele_list[0]])]

            pythonpart = PythonPart ("SpiralElement",
                                     parameter_list   = build_ele.get_params_list(),
                                     hash_value       = build_ele.get_hash(),
                                     python_file      = build_ele.pyp_file_name,
                                     views            = views,
                                     reinforcement    = [spiral])

            self.model_ele_list = pythonpart.create()

        self.create_handles()

        return (self.model_ele_list, self.handle_list)

    def create_geometry(self):
        """
        Create the geometry
        Returns: created cylinder
        """
        return AllplanGeo.Cylinder3D(self.radius, self.radius, AllplanGeo.Point3D(0, 0, self.height))

    def create_reinforcement(self, build_ele):
        """
        Create the stirrup placement
        Returns: created stirrup reinforcement
        """

        start_hook_length = self.start_hook_length if self.start_hook and not self.place_per_linear_meter else 0
        end_hook_length   = self.end_hook_length   if self.end_hook   and not self.place_per_linear_meter else 0

        rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0, 0, 0),
                                          AllplanGeo.Point3D(0, 0, self.height))

        contour = AllplanGeo.Polyline3D()
        contour += AllplanGeo.Point3D(self.radius, 0, 0)
        contour += AllplanGeo.Point3D(self.radius, 0, self.height)

        spiral = AllplanReinf.SpiralElement(1, self.diameter, self.steel_grade, self.concrete_grade,
                                            rotation_axis, contour, self.pitch, start_hook_length,
                                            self.start_hook_angle, end_hook_length, self.end_hook_angle,
                                            self.concrete_cover, self.concrete_cover,  self.concrete_cover)

        spiral.SetPlacePerLinearMeter(self.place_per_linear_meter)
        spiral.SetLengthFactor(build_ele.LengthFactor.value)
        spiral.SetNumberLoopsStart(build_ele.LoopsStart.value)
        spiral.SetNumberLoopsEnd(build_ele.LoopsEnd.value)
        spiral.SetPitchSections(build_ele.Pitch1.value, build_ele.Length1.value,
                                build_ele.Pitch2.value, build_ele.Length2.value,
                                build_ele.Pitch3.value, build_ele.Length3.value,
                                build_ele.Pitch4.value, build_ele.Length4.value)

        spiral.SetCommonProperties(self.create_reinf_common_prop())

        return spiral


    def create_handles(self):
        """
        Create handles

        Args:
            build_ele:  the building element.
        """
        # Handle for Height
        self.handle_list.append(
            HandleProperties("Height",
                              AllplanGeo.Point3D(0, 0, self.height),
                              AllplanGeo.Point3D(0, 0, 0),
                              [("Height", HandleDirection.z_dir)],
                              HandleDirection.z_dir,
                              True))

        # Handle for radius
        self.handle_list.append(
            HandleProperties("Radius",
                             AllplanGeo.Point3D(0, self.radius, 0),
                             AllplanGeo.Point3D(0, 0, 0),
                             [("Radius", HandleDirection.x_dir)],
                             HandleDirection.x_dir,
                             True))
