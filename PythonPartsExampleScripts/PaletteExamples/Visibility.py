"""
Example script for Visibility
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from ControlPropertiesUtil import ControlPropertiesUtil
from PythonPartUtil import PythonPartUtil

print('Load Visibility.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def initialize_control_properties(build_ele     : BuildingElement,
                                  ctrl_prop_util: ControlPropertiesUtil,
                                  _doc          : AllplanElementAdapter.DocumentAdapter) -> None:
    """ initialize the control properties

    Args:
        build_ele     : building element
        ctrl_prop_util: control properties utility
        _doc          : document
    """

    #--------------------- use the enable function

    def pen_enable() -> bool:
        return build_ele.CheckBox1.value

    ctrl_prop_util.set_enable_function("Pen", pen_enable)


    #--------------------- use the visible function

    def cylinder_visible() -> bool:
        return build_ele.CheckBox4.value and build_ele.GeometryType.value == 2

    ctrl_prop_util.set_visible_function("Row2", cylinder_visible)


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        result of the created element
    """

    element = Visibility(doc)

    return element.create(build_ele)


class Visibility():
    """
    Definition of class Visibility
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class Visibility

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.document       = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            result of the created element
        """

        self.create_geometry(build_ele)

        return CreateElementResult(self.model_ele_list)


    def create_geometry(self,
                        build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #------------------ Define the cube polyhedron

        if build_ele.GeometryType.value == 1:
            geo_ele = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value,
                                                           build_ele.Width.value,
                                                           build_ele.Height.value)
        else:
            axis_place = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D())
            geo_ele    = AllplanGeo.BRep3D.CreateCylinder(axis_place, build_ele.CylinderRadius.value,
                                                          build_ele.CylinderHeight.value)


        #------------------ Define common properties, take global Allplan settings plus specified color

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        if build_ele.CheckBox1.value:
            com_prop.Pen = build_ele.Pen.value

            if build_ele.CheckBox2.value:
                com_prop.Stroke = build_ele.Stroke.value
                com_prop.Color = build_ele.Color.value


        #------------------ create PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, geo_ele))

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)
