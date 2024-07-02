""" Script for AttributeService
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from Utils import LibraryBitmapPreview

from CreateElementResult import CreateElementResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.AttributeServiceBuildingElement \
        import AttributeServiceBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load AttributeService.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_libary_bitmap_preview( \
                                    AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                                    r"Examples\PythonParts\ServiceExamples\AttributeService.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    attr_service = AllplanBaseEle.AttributeService

    build_ele.AttributeNameByID.value         = attr_service.GetAttributeName(doc, build_ele.AttributeIDIn.value)
    build_ele.AttributeTypeByID.value         = str(attr_service.GetAttributeType(doc, build_ele.AttributeIDIn.value))
    build_ele.AttributeDefaultValueByID.value = str(attr_service.GetDefaultValue(doc, build_ele.AttributeIDIn.value))
    build_ele.AttributeControlTypeByID.value  = str(attr_service.GetAttributeControlType(doc, build_ele.AttributeIDIn.value))

    if build_ele.AttributeTypeByID.value == "Enum":
        build_ele.AttributeInputListByID.value = attr_service.GetEnumValues(doc, build_ele.AttributeIDIn.value)
    else:
        build_ele.AttributeInputListByID.value = attr_service.GetInputListValues(doc, build_ele.AttributeIDIn.value)

    build_ele.AttributeIDByName.value           = attr_service.GetAttributeID(doc, build_ele.AttributeNameIn.value)
    build_ele.AttributeTypeByName.value         = str(attr_service.GetAttributeType(doc, build_ele.AttributeIDByName.value))
    build_ele.AttributeDefaultValueByName.value = str(attr_service.GetDefaultValue(doc, build_ele.AttributeIDByName.value))

    build_ele.AttributeIDByDlg.value   = build_ele.AttributeByDlg.value
    build_ele.AttributeNameByDlg.value = str(attr_service.GetAttributeName(doc, build_ele.AttributeByDlg.value))

    return CreateElementResult()


def on_control_event(build_ele: BuildingElement,
                     _event_id: int,
                     doc      : AllplanEleAdapter.DocumentAdapter) -> bool:
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        _event_id: event id of the clicked button control
        doc:       document of the Allplan drawing files

    Returns:
        update the palette state
    """

    attr_service = AllplanBaseEle.AttributeService


    #--------------------- check for an existing attribute

    if attr_service.GetAttributeID(doc, build_ele.UserAttributeName.value) != -1:
        AllplanUtil.ShowMessageBox("An attribute with this names exists", AllplanUtil.MB_OK)

        return False


    #--------------------- create the attribute list

    list_values = AllplanUtil.VecStringList()

    if build_ele.UserAttributeControlType.value in ["ComboBox", "ComboBoxFixed"]:
        list_values[:] = build_ele.UserAttributeListValues.value


    #--------------------- create the attribute

    build_ele.UserAttributeID.value = attr_service.AddUserAttribute(
                                        doc,
                                        attr_service.AttributeType.names[build_ele.UserAttributeType.value],
                                        build_ele.UserAttributeName.value,
                                        build_ele.UserAttributeDefaultValue.value,
                                        build_ele.UserAttributeMinValue.value,
                                        build_ele.UserAttributeMaxValue.value,
                                        build_ele.UserAttributeDim.value,
                                        attr_service.AttributeControlType.names[build_ele.UserAttributeControlType.value],
                                        list_values)

    if build_ele.UserAttributeID.value == -1:
        AllplanUtil.ShowMessageBox("Not possible to create the attribute", AllplanUtil.MB_OK)

        return False


    #--------------------- initialize the user attribute input

    if build_ele.UserAttributeType.value in ["String", "Date"]:
        build_ele.UserAttribute.value = build_ele.UserAttributeDefaultValue.value

    elif build_ele.UserAttributeType.value == "Double":
        build_ele.UserAttribute.value = float(build_ele.UserAttributeDefaultValue.value)

    else:
        build_ele.UserAttribute.value = int(build_ele.UserAttributeDefaultValue.value)

    build_ele.UserAttribute.attribute_id_str = str(build_ele.UserAttributeID.value)

    return True
