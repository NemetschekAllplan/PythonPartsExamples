"""
Example Script for scalable PythonPart adapted from MacroColumnExample
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from GeometryExamples.GeometryElements import GeometryElements

from PythonPart import View2D3D, PythonPart

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
        self._wall_thickness = 100.
        self._create_3d_body = True
        self._hash_value = ""
        self._python_file = ""

    def create_geo(self, AxisPlacement3D, width, depth, height, wall_thickness):
        cuboid_out = AllplanGeo.BRep3D.CreateCuboid(AxisPlacement3D, width, depth, height)
        cuboid_inner = AllplanGeo.BRep3D.CreateCuboid(AxisPlacement3D, width - 2 * wall_thickness.value, depth - 2 * wall_thickness.value, height)
        transvec = AllplanGeo.Vector3D(wall_thickness.value, wall_thickness.value, 0)
        cuboid_inner = AllplanGeo.Move(cuboid_inner, transvec)
        
        err, diff = AllplanGeo.MakeSubtraction(cuboid_out, cuboid_inner)
        print(err)
         
        if err:
            print("invalid substraction in create_geo")
            return cuboid_out
         
        return diff
    
    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        #------------------ Extract property values
        self._height = build_ele.Ref_z.value
        self._width = build_ele.Ref_x.value
        self._depth = build_ele.Ref_y.value
        self._wall_thickness =  build_ele.Wall_thickness
        self._hash_value = build_ele.get_hash()
        self._python_file = build_ele.pyp_file_name

        self.create_column(build_ele)
        self.create_handles()



        return (self.model_ele_list, self.handle_list)

    def create_column(self, build_ele):
        """
        Create the column
        """
        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define 3D slide, holding the 3D cuboid of the column
        cuboid_geo = self.create_geo(AllplanGeo.AxisPlacement3D(),
                                  self._width, self._depth, self._height, self._wall_thickness)                                                           
                                                    
                                                    
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)

        #------------------ Define macro definition
        views = [View2D3D ([cuboid])]

        pythonpart = PythonPart ("MacroColumnScalable", build_ele.get_params_list(),
                                 self._hash_value, self._python_file, views)
                                 
        pythonpart.distortion_state(True)
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
                                   [("Ref_x", HandleDirection.x_dir),
                                    ("Ref_y", HandleDirection.y_dir)],
                                   HandleDirection.xy_dir,
                                   True)
        self.handle_list.append(handle1)

        handle2 = HandleProperties("Height",
                                   uppercorner,
                                   origin,
                                   [("Ref_z", HandleDirection.z_dir)],
                                   HandleDirection.z_dir,
                                   True)
        self.handle_list.append(handle2)

