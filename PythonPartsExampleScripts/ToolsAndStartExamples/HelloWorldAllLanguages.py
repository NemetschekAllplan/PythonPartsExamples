"""
Hello world template
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements


# Print some information
print('Load HelloWorld.py')


# Method for checking the supported versions
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


# Method for element creation
def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
            tuple  with created elements, handles and (otional) reinforcement.
    """

    # Delete unused arguments
    #del build_ele
    del doc

    # Define common style properties
    common_props = AllplanBaseElements.CommonProperties()
    common_props.GetGlobalProperties()

    # Define text properties
    text_prop = AllplanBasisElements.TextProperties()

    # Create text with all languages
    text = ""
    text += build_ele.bg.value + "\n"
    text += build_ele.fi.value + "\n"
    text += build_ele.fr.value + "\n"
    text += build_ele.el.value + "\n"
    text += build_ele.nl.value + "\n"
    text += build_ele.it.value + "\n"
    text += build_ele.pl.value + "\n"
    text += build_ele.es.value + "\n"
    text += build_ele.sl.value + "\n"
    text += build_ele.cs.value + "\n"
    text += build_ele.hu.value + "\n"
    text += build_ele.da.value + "\n"
    text += build_ele.pt.value + "\n"
    text += build_ele.lt.value + "\n"
    text += build_ele.lv.value + "\n"
    text += build_ele.et.value + "\n"
    text += build_ele.de.value + "\n"
    text += build_ele.en.value + "\n"
    text += build_ele.zh.value + "\n"
    text += build_ele.ja.value + "\n"
    text += build_ele.ru.value + "\n"
    text += build_ele.uk.value + "\n"
    text += build_ele.tr.value + "\n"
    text += build_ele.sk.value + "\n"
    text += build_ele.ko.value + "\n"
    text += build_ele.no.value + "\n"
    text += build_ele.sv.value + "\n"
    text += build_ele.ro.value + "\n"
    text += build_ele.SteelConstruction.value + "\n"
    text += build_ele.GermanChinese.value + "\n"

    # Create a Text element instance and add it to elements list
    model_elem_list = [AllplanBasisElements.TextElement(common_props, text_prop, text, AllplanGeo.Point2D(0, 0))]

    # Define the handles list
    handle_list = []
    # Return a tuple with elements list and handles list
    return (model_elem_list, handle_list)
