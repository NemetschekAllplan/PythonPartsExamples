""" Example showing how to change the format properties of an element by accessing the
BaseElementAdapter"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pathlib import Path

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyFormatPropertiesBuildingElement import \
        ModifyFormatPropertiesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load ModifyFormatProperties.py')


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


def create_preview(build_ele : BuildingElement,
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


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return FormatPropertiesModify(build_ele, coord_input)


class FormatPropertiesModify(BaseScriptObject):
    """Implementation of an interactor, where the user has define format properties (like layer)
    in the property palette and subsequently has to select an element. The properties are then
    assigned to this element.

    Terminating the interactor happens by pressing ESC.
    """

    def __init__(self,
                 build_ele: BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """Default constructor

        Args:
            build_ele:      building element with parameter values from the property palette
            coord_input:    object representing the coordinate input inside the viewport
        """
        super().__init__(coord_input)

        # set initial values
        self.build_ele          = build_ele
        self.interaction_result = MultiElementSelectInteractorResult()

    def execute(self) -> CreateElementResult:
        """Execute the element creation

        Returns:
            created element
        """
        return CreateElementResult()   # this interactor class just modifies elements, nothing to create

    def start_input(self):
        """Start the element selection"""

        prompt = "Set format properties in the palette and select elements to apply them to"
        self.script_object_interactor = MultiElementSelectInteractor(self.interaction_result,
                                                                     prompt_msg = prompt)


    def start_next_input(self):
        """Modify the format properties of the selected element and restart the input"""
        self.modify_format_properties(self.interaction_result.sel_elements)

        self.start_input()


    def modify_format_properties(self, elements: AllplanEleAdapter.BaseElementAdapterList):
        """Modify the format properties of the elements

        The format properties are taken from the parameter values set by the user in the property palette

        Args:
            elements:   elements to apply the properties to
        """

        layer_name = AllplanBaseEle.LayerService.GetShortNameByID(self.build_ele.LayerID.value,
                                                                  self.coord_input.GetInputViewDocumentID())

        AllplanBaseEle.ElementsLayerService.ChangeLayer(elements, layer_name)

    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handle the cancel function event.

        This event is triggered by hitting ESC during the runtime of a PythonPart.
        In this case, the selection is terminated as well as the PythonPart itself

        Returns:
            Always cancel the input and terminate PythonPart
        """

        self.script_object_interactor = None

        return OnCancelFunctionResult.CANCEL_INPUT
