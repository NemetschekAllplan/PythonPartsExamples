"""
Example Script for AttributeValueControlByRuntime
"""

import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from ControlPropertiesUtil import ControlPropertiesUtil
from CreateElementResult import CreateElementResult

print('Load AttributeValueControlByRuntime.py')


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


def modify_control_properties(build_ele      : BuildingElement,
                              _ctrl_prop_util: ControlPropertiesUtil,
                              value_name     : str,
                              _event_id      : int,
                              _doc           : AllplanElementAdapter.DocumentAdapter) -> bool:
    """ modify the control properties

    Args:
        build_ele      : building element
        _ctrl_prop_util: control properties utility
        value_name     : name of the modified value
        _event_id      : event ID
        _doc           : document

    Returns:
        update the property palette is necessary: True/False
    """

    if value_name != "AttributeID":
        return False

    build_ele.AttributeValue.attribute_id = build_ele.AttributeID.value

    return True


def create_element(_build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Execute the element creation

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    return CreateElementResult()
