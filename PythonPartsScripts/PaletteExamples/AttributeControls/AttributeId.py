""" Script for AttributeId control example
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.AttributeIdBuildingElement import AttributeIdBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load AttributeId.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
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

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\PaletteExamples\AttributeControls\AttributeId.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = AttributeId(doc)

    return element.create(build_ele)


class AttributeId():
    """ Definition of class AttributeId
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class AttributeId

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        build_ele.AttributeInfo.value     = build_ele.AttributeID.value
        build_ele.AttributeInfoList.value = build_ele.AttributeIDList.value

        return CreateElementResult()
