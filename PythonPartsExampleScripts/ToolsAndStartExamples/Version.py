"""
Example script for Script Version
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load Version.py')


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

    # Check version >= 2016.1
    versions = version.split('.')
    print(versions)

    try:
        return float(versions[0]) > 2016 or float(versions[0]) == 2016 and float(versions[1]) >= 1

    except (ValueError, IndexError):
        return False


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = AllplanVersionExample(doc)

    return element.create(build_ele)


def move_handle(build_ele, handle, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    del handle

    build_ele.change_property(handle_prop, input_pnt)

    element = AllplanVersionExample(doc)

    return element.create(build_ele)


class AllplanVersionExample():
    """
    Definition of class AllplanVersionExample
    """

    def __init__(self, doc):
        """
        Initialisation of class AllplanVersionExample

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
        if not hasattr(build_ele, 'init_version'):
            # do evaluation of version only once
            build_ele.init_version = True
            self.evaluate_version(build_ele)

        self.create_geometry(build_ele)

        return (self.model_ele_list, self.handle_list)

    def evaluate_version(self, build_ele):
        """
        fills the defined string with the values from build_ele

        Args:
            build_ele:  the building element.

        Returns:

        """
        build_ele.Version_pyp.value = build_ele.version
        d_version = float(build_ele.version)
        build_ele.d_version = d_version

        if d_version == 1.0:
            print('version 1')

        if d_version >= 2.0:
            print(' >= version 1')
        return



    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette parameter values

        length = build_ele.Length.value

        if build_ele.d_version >= 2.0:
            width = build_ele.Width.value
        else:
            # build_ele.Width is missing in .pyp file
            width = 1000 # set as default value

        #------------------ Define the cube polyhedron

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(length, width, length)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Append for creation as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed1))

        polyhed1 = AllplanGeo.Move(polyhed1, AllplanGeo.Vector3D(length * 1.5, 0, 0))


        #------------------ No handles

        self.handle_list = []
