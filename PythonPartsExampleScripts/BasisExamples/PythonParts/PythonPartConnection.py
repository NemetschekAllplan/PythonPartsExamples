""" Script for PythonPartConnection
"""

from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

import pathlib

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseInteractor import BaseInteractor, BaseInteractorData
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementXML import BuildingElementXML
from CreateElementResult import CreateElementResult

from TypeCollections.ModificationElementList import ModificationElementList

from .PythonPartConnectionPlate import PythonPartConnectionPlate
from .PythonPartConnectionHole import PythonPartConnectionHole

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartConnectionBuildingElement import PythonPartConnectionBuildingElement
    from __BuildingElementStubFiles.PythonPartConnectionPlateBuildingElement import PythonPartConnectionPlateBuildingElement
else:
    PythonPartConnectionBuildingElement      = BuildingElement
    PythonPartConnectionPlateBuildingElement = BuildingElement

print('Load PythonPartConnection.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
            version is supported state
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult()


def create_interactor(interactor_data: BaseInteractorData) -> PythonPartConnection:
    """ Create the interactor

    Args:
        interactor_data: interactor data

    Returns:
        Created interactor object
    """

    return PythonPartConnection(interactor_data)


def execute_pre_element_delete(doc                   : AllplanEleAdapter.DocumentAdapter,
                               build_ele_list        : list[BuildingElement],
                               _modification_ele_list: ModificationElementList):
    """ execute the pre element delete

    Args:
        doc:                    document of the Allplan drawing files
        build_ele_list:         list with the building elements
        _modification_ele_list: list with the modification elements in modification mode
    """

    build_ele = cast(PythonPartConnectionBuildingElement, build_ele_list[0])

    if build_ele.ObjectType.value != 1:
        return


    #--------------------- delete the connected holes

    build_ele = cast(PythonPartConnectionPlateBuildingElement, build_ele_list[1])

    del_elements = AllplanEleAdapter.BaseElementAdapterList([connection.element for connection in build_ele.__HoleConnection__.value \
                                                             if not connection.element.IsNull()])

    AllplanBaseEle.DeleteElements(doc, del_elements)


class PythonPartConnection(BaseInteractor):
    """ Definition of class PythonPartConnection
    """

    BUILD_ELE_LIST_COUNT = 2

    def __init__(self,
                 interactor_data: BaseInteractorData):
        """ initialize and start the input

        Args:
            interactor_data: interactor data
        """

        self.interactor_data       = interactor_data
        self.coord_input           = interactor_data.coord_input
        self.pyp_path              = interactor_data.pyp_path
        self.str_table_service     = interactor_data.global_str_table_service
        self.build_ele_list        = interactor_data.build_ele_list
        self.build_ele_composite   = interactor_data.build_ele_composite
        self.control_props_list    = interactor_data.control_props_list
        self.modification_ele_list = interactor_data.modification_ele_list
        self.model_ele_list        = []
        self.object                = None

        self.build_ele = cast(PythonPartConnectionBuildingElement, self.build_ele_list[0])


        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             "PythonPartsFramework\\InteractorExamples\\PythonPartConnection")

        if interactor_data.execution_event != AllplanSettings.ExecutionEvent.eCreation:
            self.create_sub_element(False)

        else:
            self.read_sub_element(False)


    def read_sub_element(self,
                         is_refresh_palette: bool):
        """ read the sub element

        Args:
            is_refresh_palette: palette refresh state
        """

        #----------------- use the local path for the sub element

        local_pyp_file_path = pathlib.Path(self.build_ele.pyp_file_name).parent

        file_name = f"{local_pyp_file_path}\\{("PythonPartConnectionPlate.pypsub" if self.build_ele.ObjectType.value == 1 else  \
                                               "PythonPartConnectionHole.pypsub")}"

        self.build_ele.__AddPypSubFile__.value = file_name


        #----------------- read the sub element

        xml_ele = BuildingElementXML()

        file_name = f"{self.pyp_path}\\{("PythonPartConnectionPlate.pypsub" if self.build_ele.ObjectType.value == 1 else  \
                                         "PythonPartConnectionHole.pypsub")}"

        build_ele, control_props, _ = xml_ele.read_element_parameter(file_name,
                                                                     self.str_table_service.str_table,
                                                                     self.str_table_service.material_str_table)

        if len(self.build_ele_list) == self.BUILD_ELE_LIST_COUNT:
            self.build_ele_list    [1] = build_ele
            self.control_props_list[1] = control_props
        else:
            self.build_ele_list.append(build_ele)
            self.control_props_list.append(control_props)

        self.create_sub_element(is_refresh_palette)


    def create_sub_element(self,
                           is_refresh_palette: bool):
        """ create the sub element

        Args:
            is_refresh_palette: is palette refresh state
        """

        if self.build_ele.ObjectType.value == 1:
            build_ele = cast(PythonPartConnectionPlateBuildingElement, self.build_ele_list[1])


            #------------- reset the hole visibility in case of copy

            if self.interactor_data.execution_event == AllplanSettings.ExecutionEvent.eCopy:
                build_ele.HoleVisibility.value = []


            #------------- set the hole visibility

            build_ele.HoleVisibility.value += [True] * (len(build_ele.__HoleConnection__.value) - len(build_ele.HoleVisibility.value))

            build_ele.HoleVisibility.value = build_ele.HoleVisibility.value[:len(build_ele.__HoleConnection__.value)]

            self.object = PythonPartConnectionPlate(self.coord_input, self.palette_service,
                                                    self.build_ele_list, self.modification_ele_list)

        else:
            self.object = PythonPartConnectionHole(self.coord_input, self.palette_service,
                                                   self.build_ele_list, self.modification_ele_list)

        if is_refresh_palette:
            self.palette_service.refresh_palette(self.build_ele_list, self.control_props_list)
        else:
            self.palette_service.show_palette(self.build_ele.script_name)


    def set_copied_hole_visibility(self,
                                   build_ele: BuildingElement):
        """ set the visibility of the copied holes (hidden holes are not copied)

        Args:
            build_ele: building element with the parameter properties
        """

        build_ele = cast(PythonPartConnectionPlateBuildingElement, build_ele)

        hole_visibility = list[bool]()

        for connection, visible in zip(build_ele.__HoleConnection__.value, build_ele.HoleVisibility.value):
            connection_ele_uuid_str = str(connection.element.GetModelElementUUID())

            if self.interactor_data.org_and_copy_ele_guids.get(connection_ele_uuid_str, None) is not None:
                hole_visibility.append(visible)

        build_ele.HoleVisibility.value = hole_visibility


    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        if self.object:
            self.object.draw_preview()


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        if self.object:
            self.object.on_mouse_leave()


    def on_cancel_function(self) -> bool:
        """ Check for input function cancel in case of ESC

        Returns:
            cancel the function state
        """

        if self.object:
            if self.interactor_data.execution_event != AllplanSettings.ExecutionEvent.eCreation:
                self.object.create_python_part()
            else:
                self.object.on_cancel_function()

        self.palette_service.close_palette()

        return True


    def on_control_event(self,
                         _event_id: int) -> bool:
        """ Handle the control event

        Args:
            _event_id: event ID

        Returns:
            event was processed state
        """

        if self.object:
            self.object.create_python_part()

        return True


    def on_value_input_control_enter(self) -> bool:
        """ Handles the value input control enter event.

        This event is triggered, when enter key is hit during the input inside the input control
        located in the dialog line.

        Returns:
            True/False for success.
        """

        return False


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        if name == self.build_ele.ObjectType.name:
            self.build_ele.ObjectType.value = value

            self.read_sub_element(True)

            if self.object:
                self.object.draw_preview()

            return

        if self.object:
            self.object.modify_element_property(page, name, value)


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """ Handles the process mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        if self.object is None:
            return False

        return self.object.process_mouse_msg(mouse_msg, pnt, msg_info)


    def update_after_favorite_read(self):
        """ execute the necessary update after a favorite read
        """

        self.palette_service.update_palette(-1, True)

        self.on_preview_draw()


    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
