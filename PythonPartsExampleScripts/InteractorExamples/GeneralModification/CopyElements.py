""" Script for CopyElements
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import Any, List, cast, TYPE_CHECKING

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
    from __BuildingElementStubFiles.CopyElementsBuildingElement import CopyElementsBuildingElement
else:
    CopyElementsBuildingElement = BuildingElement

print('Load CopyElements.py')


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
                               r"Examples\PythonParts\InteractorExamples\GeneralModification\CopyElements.png"))

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

    return CopyElements(coord_input, build_ele_list, build_ele_composite, control_props_list)


class CopyElements(BaseInteractor):
    """ Definition of class CopyElements
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
        self.build_ele      = cast(CopyElementsBuildingElement, build_ele_list[0])

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)

        self.start_element_selection()

    def start_element_selection(self):
        """ start the element selection
        """

        sel_setting = AllplanIFW.ElementSelectFilterSetting()

        self.post_element_selection = AllplanIFW.PostElementSelection()

        AllplanIFW.InputFunctionStarter.StartElementSelect("Select elements",
                                                        sel_setting, self.post_element_selection, True)

        self.interactor_input_mode = self.InteractorInputMode.ELEMENT_SELECTION

        self.build_ele.IsInSelection.value = True

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

        if self.interactor_input_mode == self.InteractorInputMode.ELEMENT_SELECTION and self.post_element_selection:
            self.selected_elements = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())

            self.post_element_selection = None

            self.interactor_input_mode = self.InteractorInputMode.COORDINATE_INPUT

            self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("From point"))

            self.build_ele.IsInSelection.value = False

            self.palette_service.update_palette(-1, True)

            return True


        #----------------- reference point input

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        if self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- copy the elements

        build_ele = self.build_ele

        AllplanBaseEle.CopyElements(self.coord_input.GetInputViewDocument(), self.selected_elements,
                                    input_pnt, build_ele.DistanceVector.value, build_ele.RotationVector.value,
                                    AllplanGeo.Angle.DegToRad(build_ele.RotationAngle.value),
                                    build_ele.NumberOfCopies.value, self.coord_input.GetViewWorldProjection())


        self.start_element_selection()

        self.palette_service.update_palette(-1, True)

        return True


    def reset_param_values(self, _build_ele_list):
        """ reset the parameter values
        """

        BuildingElementListService.reset_param_values(self.build_ele_list)

        self.palette_service.update_palette(-1, True)


    def execute_save_favorite(self,
                              file_name: str):
        """ save the favorite data

        Args:
            file_name: file name of the favorite file
        """

        BuildingElementListService.write_to_file(file_name, self.build_ele_list)


    def execute_load_favorite(self,
                              file_name: str):
        """ load the favorite data

        Args:
            file_name: file name of the favorite file
        """

        BuildingElementListService.read_from_file(file_name, self.build_ele_list)

        self.palette_service.update_palette(-1, True)

    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
