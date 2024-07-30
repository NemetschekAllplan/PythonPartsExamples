"""
Example Script for Symbol3DCloud
"""
import os

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load Symbol3DCloud.py')
print('DGM data taken from http://vermessung.bayern.de/service/download/testdaten/dgm.html')

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
    element = Symbol3DCloudExample(doc)
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


class Symbol3DCloudExample():
    """
    Definition of class Symbol3DCloudExample
    """

    def __init__(self, doc):
        """
        Initialisation of class Symbol3DCloudExample

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


    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define Symbol3D properties
        height = build_ele.Height.value
        width  = build_ele.Width.value

        symbol_prop = AllplanBasisElements.Symbol3DProperties()
        symbol_prop.SymbolID                = build_ele.SymbolId.value
        symbol_prop.Height                  = height
        symbol_prop.Width                   = width
        symbol_prop.IsScaleDependent        = False

        rotation_angle                      = AllplanGeo.Angle ()
        rotation_angle.Deg                  = build_ele.RotationAngle.value
        symbol_prop.RotationAngle           = rotation_angle

        #------------------ Read DGM and create 3D symbols
        dgm_file = self.dgm_type_converter (build_ele.DgmType.value)
        filename = os.path.dirname(os.path.abspath(__file__)) + '\\' + dgm_file
        print("Filename: ", filename)

        first_point_extracted = False
        first_point_movement = None

        with open(filename,'r') as file:
            for line in file:
                xval, yval, zval = line.split()
                if not first_point_extracted:
                    first_point_extracted = True
                    first_point_movement = AllplanGeo.Point3D(float(xval), float(yval), float(zval))

                location = AllplanGeo.Point3D(
                    float(xval) - first_point_movement.X,
                    float(yval) - first_point_movement.Y,
                    float(zval)-first_point_movement.Z)
                self.model_ele_list.append(AllplanBasisElements.Symbol3DElement(com_prop, symbol_prop, location))


    def dgm_type_converter(self, argument):
        """
        Converter for DGM type
        """
        switcher = {
            'Small DGM (~1600 symbols)' : 'Symbol3DCloud50Meter.txt',
            'Medium DGM (~6400 symbols)': 'Symbol3DCloud25Meter.txt',
            'Large DGM (~40000 symbols)': 'Symbol3DCloud10Meter.txt',
            }
        return switcher.get(argument, 1)
