""" Script for DrawingFile_LayoutFileService
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.DrawingFile_LayoutFileServiceBuildingElement import DrawingFile_LayoutFileServiceBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load DrawingFile_LayoutFileService.py')

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

    return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{_build_ele.pyp_file_path}\{_build_ele.pyp_name}.png"))


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

    if event_id == 1001:

        result = AllplanBaseElements.DrawingFileService.GetDrawingFileName(build_ele.DrawingFileNumber.value)
        
        build_ele.DrawingFileName.value = result[1]
        
        return True

    if event_id == 1002:
       
        result = AllplanBaseElements.DrawingFileService.RenameDrawingFile(build_ele.DrawingFileNumber.value, build_ele.DrawingFileName.value)
        
        return True
    
    if event_id == 1003:  
       
        result = AllplanBaseElements.LayoutFileService.GetLayoutFileName(build_ele.LayoutFileNumber.value)
        
        build_ele.LayoutFileName.value = result[1]
        
        return True
    
    if event_id == 1004:
        
       
        result = AllplanBaseElements.LayoutFileService.RenameLayoutFile(build_ele.LayoutFileNumber.value, build_ele.LayoutFileName.value)
        
        return True