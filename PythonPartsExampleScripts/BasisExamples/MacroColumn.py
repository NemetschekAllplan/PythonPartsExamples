"""
Example Script for Macro and MacroPlacement, One slide is visible in 2D the other in 3D
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

from PythonPart import View2D, View3D, PythonPart

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
    element = MacroColumnExample(doc)

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

class MacroColumnExample():
    """
    Definition of class MacroColumnExample
    """

    def __init__(self, doc):
        """
        Initialisation of class MacroColumnExample

        Args:
            doc: input document
        """
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc
        self._height = 1000.
        self._width = 1000.
        self._depth = 1000.
        self._create_3d_body = True
        self._hash_value = ""
        self._python_file = ""

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        #------------------ Extract property values
        self._height = build_ele.Height.value
        self._width = build_ele.Width.value
        self._depth = build_ele.Depth.value
        self._create_3d_body = build_ele.Create3DBody.value
        self._hash_value = build_ele.get_hash()
        self._python_file = build_ele.pyp_file_name

        self.create_column(build_ele)
        self.create_handles()

        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(),
                                             build_ele.RotationAngleX.value,
                                             build_ele.RotationAngleY.value,
                                             build_ele.RotationAngleZ.value,
                                             self.model_ele_list)

        return (self.model_ele_list, self.handle_list)

    def create_column(self, build_ele):
        """
        Create the column
        """
        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define 2D slide, holding polygon, hatch and text

        # define a border polygon for the 2D hatch
        poly_geo = self.create_rectangle2d(AllplanGeo.Point2D(0, 0),
                                                                      self._width, self._depth)
        polygon = AllplanBasisElements.ModelElement2D(com_prop, poly_geo)

        # define the 2D hatch
        hatch_props = AllplanBasisElements.HatchingProperties()
        hatch_props.HatchID = 301
        hatch = AllplanBasisElements.HatchingElement(com_prop, hatch_props, poly_geo)

        # define the 2D filling
        color = AllplanBasisElements.ARGB (255, 128, 0, 0)
        filling_props = AllplanBasisElements.FillingProperties()
        filling_props.FirstColor = color
        filling = AllplanBasisElements.FillingElement(com_prop, filling_props, poly_geo)

        # define description text
        text = "H = " + str(round(self._height, 3)) + "\n"
        text += "W = " + str(round(self._width, 3)) + "\n"
        text += "D = " + str(round(self._depth, 3))

        text_prop = AllplanBasisElements.TextProperties()
        text_prop.Height = 0.2
        text_prop.Width  = 0.2
        text_prop.IsScaleDependent = False

        text = AllplanBasisElements.TextElement(com_prop, text_prop, text,
                                                AllplanGeo.Point2D(self._width + 10, self._depth - 20))

        #------------------ Define 3D slide, holding the 3D cuboid of the column
        cuboid_geo = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(),
                                                    self._width, self._depth, self._height)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)

        ##------------------ Define macro definition
        borderview = View2D ([polygon])
        textview = View2D ([text]) # Text only visible if LayerC is enabled in Allplan global settings
        textview.visibility_layer_a = False
        textview.visibility_layer_b = False
        views = [View2D ([filling], 0, 49), View2D ([hatch], 49, 9999), borderview, textview]
        if self._create_3d_body:
            views.append(View3D ([cuboid]))

        pythonpart = PythonPart ("MacroColumnExample", build_ele.get_params_list(),
                                 self._hash_value, self._python_file, views)
        self.model_ele_list = pythonpart.create()

    def create_handles(self):
        """
        Create the column handles
        """

        #------------------ Define handles
        origin = AllplanGeo.Point3D(0, 0, 0)
        corner = AllplanGeo.Point3D(self._width, self._depth, 0.0)
        uppercorner = AllplanGeo.Point3D(0, 0, self._height)

        handle1 = HandleProperties("UpperRightCorner",
                                   corner,
                                   origin,
                                   [("Width", HandleDirection.x_dir),
                                    ("Depth", HandleDirection.y_dir)],
                                   HandleDirection.xy_dir,
                                   True)
        self.handle_list.append(handle1)

        handle2 = HandleProperties("Height",
                                   uppercorner,
                                   origin,
                                   [("Height", HandleDirection.z_dir)],
                                   HandleDirection.z_dir,
                                   True)
        self.handle_list.append(handle2)


    @staticmethod
    def create_rectangle2d(location, sizex, sizey):
        """
        Create the 2D rectangle

        Args:
            location:  Rectangle global location
            sizex:     Size in X direction
            sizey:     Size in Y direction

        Returns:
            Created AllplanGeo.Polygon2D (no model element !!!)
        """

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(location.X,location.Y)
        polygon += AllplanGeo.Point2D(location.X+sizex,location.Y)
        polygon += AllplanGeo.Point2D(location.X+sizex,location.Y+sizey)
        polygon += AllplanGeo.Point2D(location.X,location.Y+sizey)
        polygon += AllplanGeo.Point2D(location.X,location.Y)
        return polygon
