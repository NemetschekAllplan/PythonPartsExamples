"""
Hello world template
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement


# Print some information
print('Load HelloWorld.py')


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
                   _doc     : AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
            tuple  with created elements, handles and (optional) reinforcement.
    """

    #--------------------- Access the parameter property from *.pyp file

    length = build_ele.Length.value


    #--------------------- Create a 2d line

    line = AllplanGeo.Line2D(0, 0, length, 0)


    #--------------------- Define common style properties

    common_props = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


    #--------------------- Create a 2D ModelElement instance and add it to elements list

    model_elem_list = [AllplanBasisElements.ModelElement2D(common_props, line)]


    #--------------------- Define the handles list

    handle_list = []


    #--------------------- Return a tuple with elements list and handles list

    return (model_elem_list, handle_list)
