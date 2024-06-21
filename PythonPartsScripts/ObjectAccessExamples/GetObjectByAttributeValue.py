"""
Get objects by an attribute value example
"""

# pylint: disable=global-statement

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BuildingElement import BuildingElement
from ControlPropertiesUtil import ControlPropertiesUtil
from CreateElementResult import CreateElementResult

print('Load GetObjectByAttributeValue.py')

CURRENT_ATTRIBUTE_ID    = 0
CURRENT_ATTRIBUTE_VALUE = ""


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
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


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    if not build_ele.AttributeID.value:
        return CreateElementResult()

    global CURRENT_ATTRIBUTE_ID, CURRENT_ATTRIBUTE_VALUE

    if CURRENT_ATTRIBUTE_ID == build_ele.AttributeID.value and CURRENT_ATTRIBUTE_VALUE == build_ele.AttributeValue.value:
        return CreateElementResult()


    #--------------------- get the elements for the attribute ID

    if CURRENT_ATTRIBUTE_ID != build_ele.AttributeID.value:
        AllplanBaseElements.ElementsByAttributeService.GetInstance().Init(build_ele.AttributeID.value, doc)

    CURRENT_ATTRIBUTE_ID    = build_ele.AttributeID.value
    CURRENT_ATTRIBUTE_VALUE = build_ele.AttributeValue.value

    elements = AllplanBaseElements.ElementsByAttributeService.GetInstance().GetElements(build_ele.AttributeValue.value)

    AllplanIFW.HighlightService.CancelAllHighlightedElements(doc.GetDocumentID())

    AllplanIFW.HighlightService.HighlightElements(elements)

    AllplanBaseElements.DrawingService.RedrawAll(doc)

    return CreateElementResult()
