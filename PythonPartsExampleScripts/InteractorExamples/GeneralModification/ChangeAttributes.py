""" Example showing how to change the element attributes by accessing the BaseElementAdapter
using ElementsAttributeService"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pathlib import Path

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ChangeAttributesBuildingElement import \
        ChangeAttributesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ChangeAttributes.py')


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


def create_preview(build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele:  building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """
    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return AttributesModificator(build_ele, script_object_data)


class AttributesModificator(BaseScriptObject):
    """Implementation of an interactor, where the user has define attributes with their values
    in the property palette and subsequently has to select an element. The attributes are then
    assigned to this element.

    Terminating the interactor happens by pressing ESC.
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Default constructor

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """
        super().__init__(script_object_data)

        # set initial values
        self.build_ele          = build_ele
        self.interaction_result = MultiElementSelectInteractorResult()

    def execute(self) -> CreateElementResult:
        """Execute the element creation

        Returns:
            created element
        """
        return CreateElementResult()   # this PythonPart just modifies elements, nothing to create

    def start_input(self):
        """Start the element selection"""

        prompt = "Define attributes and their values in the property palette and select elements to assign them"
        self.script_object_interactor = MultiElementSelectInteractor(self.interaction_result,
                                                                     prompt_msg = prompt)

    def start_next_input(self):
        """Change the attributes of selected element and restart the input"""
        self.change_element_attributes(self.interaction_result.sel_elements)

        self.start_input()

    def change_element_attributes(self, elements: AllplanEleAdapter.BaseElementAdapterList):
        """Change the attributes of the element.

        The pairs (attribute ID, attribute value) are taken from the building element, which
        contains the parameter values from the property palette.

        Args:
            elements:   selected elements
        """

        # get the attributes from the building element
        attributes = BuildingElementAttributeList()
        attributes.add_attributes_from_parameters(self.build_ele)

        # assign the attributes to the selected elements
        AllplanBaseEle.ElementsAttributeService.ChangeAttributes(attributes.get_attributes_list_as_tuples(), elements)

    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handle the cancel function event.

        This event is triggered by hitting ESC during the runtime of a PythonPart.
        In this case, the selection is terminated as well as the PythonPart itself

        Returns:
            Always cancel the input and terminate PythonPart
        """

        self.script_object_interactor = None

        return OnCancelFunctionResult.CANCEL_INPUT
