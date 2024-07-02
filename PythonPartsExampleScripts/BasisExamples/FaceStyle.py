"""
Example Script for FaceStyle
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

print('Load FaceStyle.py')


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
    element = FaceStyleExample(doc)
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


class FaceStyleExample():
    """
    Definition of class FaceStyleExample
    """

    def __init__(self, doc):
        """
        Initialisation of class FaceStyleExample

        Args:
            doc: input document
        """
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.create_geometry(build_ele)
        return (self.model_ele_list, self.handle_list)

    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette parameter values

        length = build_ele.Length.value
        width = build_ele.Width.value

        #------------------ Define the polygon

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(0,0)
        polygon += AllplanGeo.Point2D(length,0)
        polygon += AllplanGeo.Point2D(length,width)
        polygon += AllplanGeo.Point2D(0,width)
        polygon += AllplanGeo.Point2D(0,0)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define face style properties

        facestyle_prop = AllplanBasisElements.FaceStyleProperties()
        facestyle_prop.FaceStyleID              = build_ele.FaceStyleID.value
        rotation_angle                          = AllplanGeo.Angle ()
        rotation_angle.Deg                      = build_ele.RotationAngle.value
        facestyle_prop.RotationAngle            = rotation_angle

        facestyle_prop.UseDirectionToReferenceLine = build_ele.UseDirectionToReferenceLine.value
        if build_ele.DirectionToReferenceLine.value:
            facestyle_prop.DirectionToReferenceLine = build_ele.DirectionToReferenceLine.value


        facestyle_prop.UseReferencePoint        = build_ele.DefineReferencePoint.value
        facestyle_prop.ReferencePoint           = AllplanGeo.Point2D (build_ele.ReferencePointX.value,
                                                                      build_ele.ReferencePointY.value)

        #------------------ Append for creation as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.FaceStyleElement(com_prop, facestyle_prop, polygon))

        #------------------ Handles
        origin = AllplanGeo.Point3D(0, 0, 0)
        corner = AllplanGeo.Point3D(length, width, 0)

        handle1 = HandleProperties("UpperRightCorner",
                                   corner,
                                   origin,
                                   [("Length", HandleDirection.x_dir),
                                    ("Width", HandleDirection.y_dir)],
                                   HandleDirection.xy_dir,
                                   True)
        self.handle_list.append(handle1)
