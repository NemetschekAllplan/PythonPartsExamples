""" Script for ModifyPythonPartParameter
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor, BaseInteractorData
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult

from Utils import LibraryBitmapPreview

from Utils.ElementFilter.PythonPartFilter import PythonPartFilter
from Utils.ElementFilter.PythonPartByNameFilter import PythonPartByNameFilter

from Utils.PythonPart.ModifyPythonPartUtil import ModifyPythonPartUtil
from Utils.PythonPart.ModifyPythonPartParameterUtil import ModifyPythonPartParameterUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyPythonPartParameterBuildingElement \
        import ModifyPythonPartParameterBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ModifyPythonPartParameter.py')


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
                               r"Examples\PythonParts\BasisExamples\PythonParts\ModifyPythonPartParameter.png"))

def create_interactor(interactor_data: BaseInteractorData) -> object:
    """ Create the interactor

    Args:
        interactor_data: interactor data

    Returns:
        Created interactor object
    """

    return ModifyPythonPartParameter(interactor_data)


class ModifyPythonPartParameter(BaseInteractor):
    """ Definition of class ModifyPythonPartParameter
    """

    def __init__(self,
                 interactor_data: BaseInteractorData):
        """ Create the interactor

        Args:
            interactor_data: interactor data
        """

        self.coord_input     = interactor_data.coord_input
        self.build_ele       = cast(BuildingElement, interactor_data.build_ele_list[0])
        self.interactor_data = interactor_data


        self.pyp_parameter = []
        self.ref_pyp_ele   = AllplanEleAdapter.BaseElementAdapter()
        self.undo_service  = None

        self.palette_service: BuildingElementPaletteService

        self.sel_ref_ele_result = SingleElementSelectResult()
        self.sel_mod_ele_result = MultiElementSelectInteractorResult()

        self.start_pyp_selection()


    def show_palette(self):
        """ show the palette
        """

        interactor_data = self.interactor_data

        self.palette_service = BuildingElementPaletteService(interactor_data.build_ele_list, interactor_data.build_ele_composite,
                                                             self.build_ele.script_name,
                                                             interactor_data.control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)


    def start_pyp_selection(self):
        """ start the PythonPart selection
        """

        #----------------- start the selection interactor

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_ref_ele_result, PythonPartFilter(),
                                                                      "Select the reference PythonPart")

        self.script_object_interactor.start_input(self.coord_input)

        self.build_ele.InputMode.value = self.build_ele.REF_PYP_SELECT

        self.show_palette()


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.palette_service.close_palette()


        #----------------- start the parameter input

        if build_ele.InputMode.value == build_ele.REF_PYP_SELECT:
            self.ref_pyp_ele = self.sel_ref_ele_result.sel_element

            self.script_object_interactor = ModifyPythonPartUtil(self.ref_pyp_ele)

            self.script_object_interactor.start_input(self.coord_input)

            self.build_ele.InputMode.value = self.build_ele.PARAMETER_INPUT

            _, _, self.pyp_parameter = AllplanBaseEle.PythonPartService.GetParameter(self.ref_pyp_ele)

            return


        #----------------- modify the PythonParts

        self.modify_parameter()

        self.start_pyp_selection()


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

        build_ele = self.build_ele

        self.palette_service.close_palette()

        if build_ele.InputMode.value == build_ele.PARAMETER_INPUT:
            self.start_mod_pyp_selection()

            return False

        if self.build_ele.InputMode.value in (build_ele.REF_PYP_SELECT,
                                              build_ele.PYP_SELECTION) or not self.script_object_interactor:
            if self.undo_service:
                self.undo_service.CreateUndoStep()

            return True

        return False


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


    def start_mod_pyp_selection(self):
        """ start the selection of the PythonParts to modify
        """

        #----------------- close the ref PyP modification

        if self.script_object_interactor is not None:
            self.undo_service = AllplanIFW.UndoRedoService(self.coord_input.GetInputViewDocument())

            self.script_object_interactor.on_cancel_function()


        #----------------- start the selection

        self.script_object_interactor = MultiElementSelectInteractor(self.sel_mod_ele_result, PythonPartByNameFilter(self.ref_pyp_ele),
                                                                     "Select the PythonParts to modify")

        self.script_object_interactor.start_input(self.coord_input)

        self.build_ele.InputMode.value = self.build_ele.PYP_SELECTION

        self.show_palette()


    def modify_parameter(self):
        """ modify the parameter
        """

        AllplanSettings.PythonPartsSettings.GetInstance().UpdateIdenticalPythonParts = \
            AllplanSettings.UpdateIdenticalPythonPartsState.eDoNotUpdateIdentical


        #----------------- get the modified parameter

        if self.build_ele.ExecuteModification.value == self.build_ele.MODIFY_ALL:                       # pylint: disable=consider-ternary-expression
            mod_param_data = ModifyPythonPartParameterUtil.get_overtake_parameters(self.ref_pyp_ele,
                                                                                   self.build_ele.get_string_tables()[1],
                                                                                   self.build_ele.get_material_string_table())
        else:
            mod_param_data = ModifyPythonPartParameterUtil.get_modified_parameters(self.pyp_parameter, self.ref_pyp_ele,
                                                                                   self.build_ele.get_string_tables()[1],
                                                                                   self.build_ele.get_material_string_table())

        if not mod_param_data:
            return


        #----------------- modify all PythonParts with the same name

        ref_guid = self.ref_pyp_ele.GetModelElementUUID()

        for ele in self.sel_mod_ele_result.sel_elements:
            if ele.GetModelElementUUID() != ref_guid:
                ModifyPythonPartParameterUtil.execute(ele, self.coord_input, mod_param_data)


        #----------------- create the undo step

        AllplanSettings.PythonPartsSettings.GetInstance().UpdateIdenticalPythonParts = \
            AllplanSettings.UpdateIdenticalPythonPartsState.eUndefinded

        if self.undo_service:
            self.undo_service.CreateUndoStep()

        self.undo_service = None
