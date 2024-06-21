"""
Example Script for StructuredContainer
"""

import math
import uuid

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil

print('Load StructuredContainer.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        Object with the result data of the element creation
    """

    element = StructuredContainerExample(doc)

    return element.create(build_ele)


def move_handle(build_ele  : BuildingElement,
                handle_prop: HandleProperties,
                input_pnt  : AllplanGeo.Point3D,
                doc        : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document

    Returns:
        Object with the result data of the element creation
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class StructuredContainerExample():
    """
    Definition of class StructuredContainerExample
    """

    obj1_uuid = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e01}')
    obj2_uuid = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e02}')

    def __init__(self, doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class StructuredContainerExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = []
        self.document       = doc


    def create(self, build_ele: BuildingElement) -> CreateElementResult:
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            Object with the result data of the element creation
        """

        self.create_geometry(build_ele)

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d(self.model_ele_list)

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(self.model_ele_list, self.handle_list)


    def create_table(self, com_prop, width, count):
        """
        Create table
        """
        
        length = float(count * 600)
        
        # define line 2D elements
        line_list = []
        point1 = AllplanGeo.Point2D(0, 0)
        point2 = AllplanGeo.Point2D(0, width)
        point3 = AllplanGeo.Point2D(length, width)
        point4 = AllplanGeo.Point2D(length, 0)
        
        line = AllplanGeo.Line2D(point1,point2)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        line_list.append(ele)
        line = AllplanGeo.Line2D(point2,point3)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        line_list.append(ele)
        line = AllplanGeo.Line2D(point3,point4)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        line_list.append(ele)
        line = AllplanGeo.Line2D(point4,point1)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        line_list.append(ele)
        
        ele = AllplanBasisElements.ElementNodeElement(com_prop, StructuredContainerExample.obj1_uuid, line_list)
        self.model_ele_list.append(ele)


    def create_chair(self, com_prop, deltaX, deltaY, length, ele_list):
        """
        Create a pair of chairs
        """
        
        length = 400
        
        # define line 2D elements
        point1 = AllplanGeo.Point2D(deltaX, deltaY)
        point2 = AllplanGeo.Point2D(deltaX, deltaY + length)
        point3 = AllplanGeo.Point2D(deltaX + length, deltaY + length)
        point4 = AllplanGeo.Point2D(deltaX + length, deltaY)
        
        line = AllplanGeo.Line2D(point1,point2)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        ele_list.append(ele)
        line = AllplanGeo.Line2D(point2,point3)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        ele_list.append(ele)
        line = AllplanGeo.Line2D(point3,point4)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        ele_list.append(ele)
        line = AllplanGeo.Line2D(point4,point1)
        ele = AllplanBasisElements.ModelElement2D(com_prop, line)
        ele_list.append(ele)


    def create_chair_pair(self, com_prop, width, delta, ele_list):
        """
        Create a pair of chairs
        """
        
        length = 400
        
        # define line 2D elements
        self.create_chair(com_prop, delta, -200 - length, length, ele_list)
        self.create_chair(com_prop, delta, width + 200, length, ele_list)

    def create_chairs(self, com_prop, width, count):
        """
        Create chairs
        """
            
        
        ele_list = []
        
        for ind in range (0, count):
            # define chair pairs
            self.create_chair_pair(com_prop, width, float((ind * 600) + 100), ele_list);
            
        ele = AllplanBasisElements.ElementNodeElement(com_prop, StructuredContainerExample.obj2_uuid, ele_list)
        #ele.SetParentID(StructuredContainerExample.obj1_uuid)      

        self.model_ele_list.append(ele)


    def create_geometry(self, build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """
        
        #------------------ Define common properties, take global Allplan settings
        
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #----------------- Extract palette parameter values

        width = float(build_ele.TableWidth.value * 10)
        count = int(build_ele.NrChairs.value)
        
        self.create_table(com_prop, width, count)
        self.create_chairs(com_prop, width, count)
