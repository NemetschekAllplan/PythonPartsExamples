"""
Example Script for Symbol2D
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load Symbol2D.py')

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
    element = Symbol2DExample(doc)
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


class Symbol2DExample():
    """
    Definition of class Symbol2DExample
    """

    def __init__(self, doc):
        """
        Initialisation of class Symbol2DExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = None
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

    def create_default(self, location, scaledependency):
        """
        Create symbol element

        Args:
            location:           the Point2D location in global coordinates of base polygon
            scaledependency:    the boolean flag for scale dependency

        Returns:
            Created symbol element
        """
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        props = AllplanBasisElements.Symbol2DProperties()
        props.IsScaleDependent = scaledependency

        elem = AllplanBasisElements.Symbol2DElement(com_prop, props, location)
        return elem


    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #------------------ Define the location

        # Dummy location, mouse move interactor reset the location
        location = AllplanGeo.Point2D(0, 0)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define Symbol2D properties

        symbol_prop = AllplanBasisElements.Symbol2DProperties()
        symbol_prop.SymbolID                = build_ele.SymbolId.value
        symbol_prop.Height                  = build_ele.Height.value
        symbol_prop.Width                   = build_ele.Width.value
        symbol_prop.IsScaleDependent        = build_ele.IsScaleDependent.value
        symbol_prop.PrimaryPointNumber      = build_ele.PrimaryPointNumber.value
        symbol_prop.SecondaryPointNumber    = build_ele.SecondaryPointNumber.value

        rotation_angle                      = AllplanGeo.Angle ()
        rotation_angle.Deg                  = build_ele.RotationAngle.value
        symbol_prop.RotationAngle           = rotation_angle

        #------------------ Append for creation as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.Symbol2DElement(com_prop, symbol_prop, location))


