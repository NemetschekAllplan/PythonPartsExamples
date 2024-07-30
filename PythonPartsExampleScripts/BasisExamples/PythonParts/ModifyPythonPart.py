""" Script for ModifyPythonPart
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

from ScriptObjectInteractors.BaseFilterObject import BaseFilterObject
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from Utils import LibraryBitmapPreview

from Utils.PythonPart.ModifyPythonPartUtil import ModifyPythonPartUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyPythonPartBuildingElement \
        import ModifyPythonPartBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ModifyPythonPart.py')


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
                               r"Examples\PythonParts\BasisExamples\PythonParts\ModifyPythonPart.png"))

def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : list[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : list[BuildingElementControlProperties],
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

    return ModifyPythonPart(coord_input, build_ele_list, build_ele_composite, control_props_list)


class ModifyPythonPart(BaseInteractor):
    """ Definition of class ModifyPythonPart
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : list[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : list[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:         API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list:      list with the building elements
            build_ele_composite: building element composite with the building element constraints
            control_props_list:  control properties list
        """

        self.coord_input         = coord_input
        self.build_ele_list      = build_ele_list
        self.build_ele           = build_ele_list[0]
        self.control_props_list  = control_props_list
        self.build_ele_composite = build_ele_composite

        self.palette_service: BuildingElementPaletteService

        self.sel_result = SingleElementSelectResult()

        self.start_pyp_selection()


    def show_palette(self):
        """ show the palette
        """

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite, # type: ignore
                                                             self.build_ele.script_name,
                                                             self.control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)


    def start_pyp_selection(self):
        """ start the PythonPart selection
        """

        class PythonPartFilter(BaseFilterObject):
            """ implementation of the PythonPart filter
            """

            def __call__(self, element: AllplanEleAdapter.BaseElementAdapter) -> bool:
                """ execute the filtering

                Args:
                    element: element to filter

                Returns:
                    element fulfills the filter: True/False
                """

                return AllplanBaseEle.PythonPartService.IsPythonPartElement(element)


        #----------------- start the selection interactor

        self.show_palette()

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_result, PythonPartFilter(),
                                                                      "Select the PythonPart")

        self.script_object_interactor.start_input(self.coord_input)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        self.palette_service.close_palette()

        self.script_object_interactor = ModifyPythonPartUtil(self.sel_result.sel_element)

        self.script_object_interactor.start_input(self.coord_input)

        self.build_ele.InputMode.value = self.build_ele.PARAMETER_MODIFICATION


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

        if self.script_object_interactor:
            self.script_object_interactor.on_cancel_function()

        if self.build_ele.InputMode.value == self.build_ele.PARAMETER_MODIFICATION:
            self.start_pyp_selection()

            return False

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

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        return True
