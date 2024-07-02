"""
Example Script for Filling
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

print('Load Filling.py')


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
    element = FillingExample(doc)
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

def modify_element_property(build_ele, name, value):
    """
        Modify property of element

        Args:
            build_ele:  the building element.
            name:       the name of the property.
            value:      new value for property.

        Returns:
            True/False if palette refresh is necessary
    """

    print ("Filling.py (modify_element_property called, property name: ", name, ", property value: ", value, ")")

    if (name == "FirstColorRed") or (name == "FirstColorBlue") or (name == "FirstColorGreen"):
        used_color = AllplanBasisElements.ARGB (build_ele.FirstColorRed.value,
                                                           build_ele.FirstColorGreen.value,
                                                           build_ele.FirstColorBlue.value,
                                                           build_ele.SecondColorAlpha.value)

        color_number = AllplanBaseElements.GetIdByColor(used_color)
        build_ele.AllplanColor.value = color_number
        return True

    return False


class FillingExample():
    """
    Definition of class FillingExample
    """

    def __init__(self, doc):
        """
        Initialisation of class FillingExample

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

    def create_properties(self, build_ele):
        """
        Create the filling properties

        Args:
            build_ele:  the building element.
        """

        props = AllplanBasisElements.FillingProperties()
        rotation_angle                    = AllplanGeo.Angle ()
        rotation_angle.Deg                = build_ele.RotationAngle.value
        props.RotationAngle               = rotation_angle
        props.FirstColor                  = AllplanBasisElements.ARGB (build_ele.FirstColorRed.value,
                                                                       build_ele.FirstColorGreen.value,
                                                                       build_ele.FirstColorBlue.value,
                                                                       build_ele.FirstColorAlpha.value)
        props.SecondColor                 = AllplanBasisElements.ARGB (build_ele.SecondColorAlpha.value,
                                                                       build_ele.SecondColorAlpha.value,
                                                                       build_ele.SecondColorAlpha.value,
                                                                       build_ele.SecondColorAlpha.value)

        props.UseGradientFilling          = build_ele.DefineGradientFilling.value
        props.TranslationType             = self.transition_type_converter(build_ele.TransitionType.value)
        props.ShadingType                 = self.shading_type_converter(build_ele.ShadingType.value)
        props.VariantType                 = self.variant_type_converter(build_ele.VariantType.value)

        props.UseDirectionToReferenceLine = build_ele.UseDirectionToReferenceLine.value
        if build_ele.DirectionToReferenceLine.value:
            props.DirectionToReferenceLine = build_ele.DirectionToReferenceLine.value

        if build_ele.TransitionType.value == 0:
            # No Transition - SecondColor must be identical to FirstColor, Alpha value is important
            props.SecondColor = AllplanBasisElements.ARGB (build_ele.FirstColorRed.value,
                                                           build_ele.FirstColorGreen.value,
                                                           build_ele.FirstColorBlue.value,
                                                           build_ele.SecondColorAlpha.value)

        elif build_ele.TransitionType.value == 1:
            # One color transition - Transition must be stored in SecondColor - Alpha value is important
            props.SecondColor = AllplanBasisElements.ARGB (build_ele.Transition.value,
                                                           build_ele.Transition.value,
                                                           build_ele.Transition.value,
                                                           build_ele.SecondColorAlpha.value)

        elif build_ele.TransitionType.value == 2:
            # Two color transition
            props.SecondColor = AllplanBasisElements.ARGB (build_ele.SecondColorRed.value,
                                                           build_ele.SecondColorGreen.value,
                                                           build_ele.SecondColorBlue.value,
                                                           build_ele.SecondColorAlpha.value)

        color_val = build_ele.AllplanColor.value

        return props


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

        props = self.create_properties(build_ele)

        #------------------ Append for creation as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.FillingElement(com_prop, props, polygon))

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

    def transition_type_converter(self, argument):
        """
        Converter for transition type
        """
        switcher = {
            0: AllplanBasisElements.TransitionType.eNoTransition,
            1: AllplanBasisElements.TransitionType.eOneColorTransition,
            2: AllplanBasisElements.TransitionType.eTwoColorTransition,
            }
        return switcher.get(argument, 1)

    def shading_type_converter(self, argument):
        """
        Converter for shading type
        """
        switcher = {
            0: AllplanBasisElements.ShadingType.eLinear,
            1: AllplanBasisElements.ShadingType.eFromCorner,
            2: AllplanBasisElements.ShadingType.eFromCenter,
            3: AllplanBasisElements.ShadingType.eRound,
            }
        return switcher.get(argument, 1)

    def variant_type_converter(self, argument):
        """
        Converter for variant type
        """
        switcher = {
            0: AllplanBasisElements.VariantType.eVariant1,
            1: AllplanBasisElements.VariantType.eVariant2,
            2: AllplanBasisElements.VariantType.eVariant3,
            3: AllplanBasisElements.VariantType.eVariant4,
            }
        return switcher.get(argument, 1)
