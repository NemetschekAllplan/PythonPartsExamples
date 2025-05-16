""" Example Script for Picture sizes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PictureBuildingElement import PictureBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PictureSizes.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
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
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{_build_ele.pyp_file_path}\{_build_ele.pyp_name}.png"))

def create_element(_build_ele: BuildingElement,
                   _doc: AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of element

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        Object with the result data of the element creation
    """

    return CreateElementResult()
