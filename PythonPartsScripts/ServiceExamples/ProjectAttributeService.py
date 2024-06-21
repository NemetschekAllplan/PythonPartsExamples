""" Script for ProjectAttributeService
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil

from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ProjectAttributeServiceBuildingElement \
        import ProjectAttributeServiceBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ProjectAttributeService.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_libary_bitmap_preview( \
                                    AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                                    r"Examples\PythonParts\ServiceExamples\ProjectAttributeService.png"))


def create_element(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult()


def on_control_event(build_ele: BuildingElement,
                     event_id : int,
                     doc      : AllplanElementAdapter.DocumentAdapter):
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        event_id:  event id of the clicked button control
        doc:       document of the Allplan drawing files
    """


    #--------------------- change the attribute

    if event_id == 1003:
        print("Set project attribute:")

        attr_list = [(attribute.attribute_id, attribute.value) for attribute in build_ele.ProjectAttributes.value if attribute.attribute_id]

        AllplanBaseElements.ProjectAttributeService.ChangeAttributesFromCurrentProject(attr_list, doc)

        return


    #----------------- get the attributes

    print("")
    print("---------------------------------------------------------------------------")

    if event_id == 1001:
        print("Attributes of the current project:")

        attributes = AllplanBaseElements.ProjectAttributeService.GetAttributesFromCurrentProject()

        for attribute in attributes:
            print(attribute[0], AllplanBaseElements.AttributeService.GetAttributeName(doc, attribute[0]), " = ", attribute[1])

    elif event_id == 1002:
        print("Attributes of all projects:")

        all_attributes = AllplanBaseElements.ProjectAttributeService.GetAttributesFromAllProjects()

        last_id = 0

        for attribute in all_attributes:
            if attribute[0] < last_id:
                print("")
                print("======================")
                print("")

            print(attribute[0], AllplanBaseElements.AttributeService.GetAttributeName(doc, attribute[0]), " = ", attribute[1])

            last_id = attribute[0]

    AllplanUtil.ShowMessageBox("The attribute log is shown in the Trace window", AllplanUtil.MB_OK)
