"""
Script for starting the error log window
"""

from ErrorLogWindow import *


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


def create_preview(build_ele_list, build_ele_composite, doc):
    del build_ele_list
    del build_ele_composite
    del doc

    return


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    # Delete unused arguments
    del build_ele
    del doc

    create_error_log_window()

    return None
