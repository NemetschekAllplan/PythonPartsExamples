"""
Example Script for Picture
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil

print('Load Picture.py')


def check_allplan_version(build_ele: BuildingElement,
                          version:   float):
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


def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = PictureExample(doc)

    return element.create(build_ele)


def move_handle(build_ele: BuildingElement,
                handle_prop: HandleProperties,
                input_pnt: AllplanGeo.Point3D,
                doc: AllplanElementAdapter.DocumentAdapter):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    element = PictureExample(doc)

    return element.create(build_ele)


class PictureExample():
    """
    Definition of class PictureExample
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class PictureExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = None
        self.document       = doc


    def create(self,
               build_ele: BuildingElement):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        print('Create the Quaders')

        self.create_geometry(build_ele)

        return (self.model_ele_list, self.handle_list)


    def create_geometry(self,
                        build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette parameter values

        width  = build_ele.Width.value
        length = build_ele.Length.value
        height = build_ele.Height.value


        #------------------ Define the cube polyhedron

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(width, length, height)


        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


        #------------------ Append cubes as new Allplan elements

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)


        #------------------ No handles

        self.handle_list = []
