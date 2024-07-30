""" Script for SelectObjectsByAttributeID
"""

from __future__ import annotations

from typing import Any, List, TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SelectObjectsByAttributeIDBuildingElement import SelectObjectsByAttributeIDBuildingElement
else:
    SelectObjectsByAttributeIDBuildingElement = BuildingElement

print('Load SelectObjectsByAttributeID.py')


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
                               r"Examples\PythonParts\ModelObjectExamples\SelectionExamples\SelectObjectsByAttributeID.png"))

def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : List[BuildingElementControlProperties],
                      _modify_uuid_list        : list) -> object:
    """ Create the interactor

    Args:
        coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            list with the building elements
        build_ele_composite:       building element composite with the building element constraints
        control_props_list:        control properties list
        _modify_uuid_list:         list with the UUIDs of the modified elements

    Returns:
          Created interactor object
    """

    return SelectObjectsByAttributeID(coord_input, build_ele_list, build_ele_composite, control_props_list)


class SelectObjectsByAttributeID(BaseInteractor):
    """ Definition of class SelectObjectsByAttributeID
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:         API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list:      list with the building elements
            build_ele_composite: building element composite with the building element constraints
            control_props_list:  control properties list
        """

        self.coord_input    = coord_input
        self.build_ele_list = build_ele_list
        self.build_ele      = cast(SelectObjectsByAttributeIDBuildingElement, build_ele_list[0])

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)


        #----------------- set the filter and start the selection

        self.post_element_selection = None

        self.start_element_selection()

    def start_element_selection(self):
        """ start the element selection
        """

        build_ele = self.build_ele

        class Object3DFilter():
            """ implementation of the 3D object filter """

            def __call__(self, element: AllplanEleAdapter.BaseElementAdapter) -> bool:
                """ execute the filtering

                Args:
                    element: element to filter

                Returns:
                    element fulfills the filter: True/False
                """

                for attribute in element.GetAttributes(AllplanBaseEle.eAttibuteReadState.ReadAllAndComputable):
                    if attribute[0] in build_ele.AttributeIDFilter.value:
                        return True

                return False

        sel_query   = AllplanIFW.SelectionQuery([Object3DFilter()])
        sel_setting = AllplanIFW.ElementSelectFilterSetting(sel_query, True)

        self.post_element_selection = AllplanIFW.PostElementSelection()

        AllplanIFW.InputFunctionStarter.StartElementSelect("Select elements",
                                                            sel_setting, self.post_element_selection, True)

        self.interactor_input_mode = self.InteractorInputMode.ELEMENT_SELECTION

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: str):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

    def on_control_event(self,
                         event_id: int):
        """ Handles on control event

        Args:
            event_id: event id of the clicked button control
        """

    def on_cancel_function(self) -> bool:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True

    def on_preview_draw(self):
        """ Handles the preview draw event
        """

    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """
        self.on_preview_draw()

    def on_value_input_control_enter(self) -> bool:
        """ Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Process the mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        AllplanIFW.HighlightService.CancelAllHighlightedElements(self.coord_input.GetInputViewDocumentID())


        #----------------- get the selected elements

        if self.post_element_selection:
            sel_elements = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())

            self.post_element_selection = None

            if not (elements := [str(ele) for ele in sel_elements]):
                return True

            self.build_ele.SelectedElements.value = elements

            AllplanIFW.HighlightService.HighlightElements(sel_elements)

            self.palette_service.update_palette(-1, True)


        #----------------- restart the selection

        self.start_element_selection()

        return True


    def __del__(self):
        """ save the default favorite data
        """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
