""" Script for ValueIndexName
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

print('Load ValueIndexName.py')


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
                               r"Examples\PythonParts\PaletteExamples\OptionalTags\ValueIndexName.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = ValueIndexName(doc)

    return element.create(build_ele)


class ValueIndexName():
    """ Definition of class ValueIndexName
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class ValueIndexName

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(_build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            _build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        return CreateElementResult()
