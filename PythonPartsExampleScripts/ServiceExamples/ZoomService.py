""" Example script showing the possibilities of zooming to specific object(s)
inside the viewport using Python API calls
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ZoomServiceBuildingElement import ZoomServiceBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ZoomService.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ZoomToElementInteractor(build_ele, script_object_data)


class ZoomToElementInteractor(BaseScriptObject):
    """Implementation of the examples PythonPart to show the possibilities of ZoomService

    This PythonPart allows to zoom to object(s) or to a min-max-box.
    When zooming to object(s), user must select them first. After that, he sets up the parameters
    such as "zoom factor" in the property palette and hits the "zoom" button.
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

        self.build_ele                 = build_ele
        self.build_ele.InputMode.value = self.build_ele.ZOOM

        # create empty containers for the selection results and initialize the zoom service
        self.single_ele_selection_result = SingleElementSelectResult()
        self.multi_ele_selection_result  = MultiElementSelectInteractorResult()
        self.zoom_service                = AllplanBaseEle.ZoomService()

    def execute(self) -> CreateElementResult:
        """Execute the element creation

        Because this interactor does not create any elements, just zooms to existing ones,
        there is nothing to create here.

        Returns:
            empty creation result
        """
        return CreateElementResult()

    def modify_element_property(self, name: str, value: Any) -> bool:
        """Handles the event of modifying a property in the property palette

        Args:
            name:   name of the modified property
            value:  new value of the modified property

        Returns:
            Always False, since no palette update is necessary
        """

        if value == "ZoomToElement":
            self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT
            self.script_object_interactor = SingleElementSelectInteractor(self.single_ele_selection_result,
                                                                          prompt_msg="Select an element to zoom into")
            self.script_object_interactor.start_input(self.coord_input)

        elif value == "ZoomToElements":
            self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT
            self.script_object_interactor = MultiElementSelectInteractor(self.multi_ele_selection_result,
                                                                         prompt_msg="Select elements to zoom into")
            self.script_object_interactor.start_input(self.coord_input)

        elif name == "ZoomTo":
            self.build_ele.InputMode.value = self.build_ele.ZOOM
            self.script_object_interactor = None

        return False

    def start_next_input(self):
        """Handles the event of successful element selection

        After successful selection, the selection interactor is terminated. PythonPart switches to
        zooming mode, where the user can set up the parameter in the palette and perform the zoom
        to selected object by pressing a button.
        """
        self.build_ele.InputMode.value = self.build_ele.ZOOM
        self.script_object_interactor = None

    def on_control_event(self, _event_id: int):
        """Handles the event of hitting a button

        Since there is only one button with an event id of 1001 on the property palette, it handles only this event.

        Args:
            _event_id: triggered event id
        """
        match self.build_ele.ZoomTo.value:

            case "ZoomToElement":
                if self.build_ele.ZoomBy.value == "ZoomByFactor":
                    self.zoom_service.ZoomToElementWithFactor(self.single_ele_selection_result.sel_element,
                                                              self.coord_input.GetViewWorldProjection(),
                                                              self.build_ele.ZoomFactor.value,
                                                              self.build_ele.ZoomInAllViews.value)

                else:
                    self.zoom_service.ZoomToElement(self.single_ele_selection_result.sel_element,
                                                    self.coord_input.GetViewWorldProjection(),
                                                    self.build_ele.InflateValue.value,
                                                    self.build_ele.ZoomInAllViews.value)

            case "ZoomToElements":
                if self.build_ele.ZoomBy.value == "ZoomByFactor":
                    self.zoom_service.ZoomToElementsWithFactor(self.multi_ele_selection_result.sel_elements,
                                                               self.coord_input.GetViewWorldProjection(),
                                                               self.build_ele.ZoomFactor.value,
                                                               self.build_ele.ZoomInAllViews.value)

                else:
                    self.zoom_service.ZoomToElements(self.multi_ele_selection_result.sel_elements,
                                                     self.coord_input.GetViewWorldProjection(),
                                                     self.build_ele.InflateValue.value,
                                                     self.build_ele.ZoomInAllViews.value)

            case "ZoomToMinMaxBox":
                min_max_box = AllplanGeometry.MinMax3D(self.build_ele.MinPoint.value,
                                                       self.build_ele.MaxPoint.value)

                if self.build_ele.ZoomBy.value == "ZoomByFactor":
                    self.zoom_service.ZoomToMinMaxBoxWithFactor(min_max_box,
                                                                self.coord_input.GetViewWorldProjection(),
                                                                self.build_ele.ZoomFactor.value,
                                                                self.build_ele.ZoomInAllViews.value)

                else:
                    self.zoom_service.ZoomToMinMaxBox(min_max_box,
                                                      self.coord_input.GetViewWorldProjection(),
                                                      self.build_ele.InflateValue.value,
                                                      self.build_ele.ZoomInAllViews.value)
