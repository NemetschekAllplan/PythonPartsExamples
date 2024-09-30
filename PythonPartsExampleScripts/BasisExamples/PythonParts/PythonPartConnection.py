""" Script for PythonPartConnection
"""

from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementXML import BuildingElementXML
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

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


def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties],
                      modification_ele_list   : ModificationElementList) -> PythonPartConnection:
    """ Create the interactor

    Args:
        coord_input:              API object for the coordinate input, element selection, ... in the Allplan view
        pyp_path:                 path of the pyp file
        global_str_table_service: global string table service
        build_ele_list:           list with the building elements
        build_ele_composite:      building element composite with the building element constraints
        control_props_list:       control properties list
        modification_ele_list:    list with the modification elements in modification mode

    Returns:
        Created interactor object
    """

    return PythonPartConnection(coord_input, pyp_path, global_str_table_service,
                                build_ele_list, build_ele_composite, control_props_list, modification_ele_list)


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

    del_elements = AllplanEleAdapter.BaseElementAdapterList()

    for connection in build_ele.__HoleConnection__.value:
        if not connection.element.IsNull():
            del_elements.append(connection.element)

    AllplanBaseEle.DeleteElements(doc, del_elements)


class PythonPartConnection():
    """ Definition of class PythonPartConnection
    """

    def __init__(self,
                 coord_input             : AllplanIFW.CoordinateInput,
                 pyp_path                : str,
                 global_str_table_service: StringTableService,
                 build_ele_list          : list[BuildingElement],
                 build_ele_composite     : BuildingElementComposite,
                 control_props_list      : list[BuildingElementControlProperties],
                 modification_ele_list   : ModificationElementList):
        """ initialize and start the input

        Args:
            coord_input:              API object for the coordinate input, element selection, ... in the Allplan view
            pyp_path:                 path of the pyp file
            global_str_table_service: global string table service
            build_ele_list:           list with the building elements
            build_ele_composite:      building element composite with the building element constraints
            control_props_list:       control properties list
            modification_ele_list:    list with the modification elements in modification mode
        """

        self.coord_input           = coord_input
        self.pyp_path              = pyp_path
        self.str_table_service     = global_str_table_service
        self.build_ele_list        = build_ele_list
        self.build_ele_composite   = build_ele_composite
        self.control_props_list    = control_props_list
        self.modification_ele_list = modification_ele_list
        self.model_ele_list        = []
        self.object                = None
        self.modification_mode     = modification_ele_list.is_modification_element()

        self.build_ele = cast(PythonPartConnectionBuildingElement, self.build_ele_list[0])


        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             "PythonPartsFramework\\InteractorExamples\\PythonPartConnection")

        if self.modification_mode:
            self.create_sub_element(False)

        else:
            self.read_sub_element(False)


    def read_sub_element(self,
                         is_refresh_palette: bool):
        """ read the sub element

        Args:
            is_refresh_palette: palette refresh state
        """

        file_name = self.pyp_path + "\\" + ("PythonPartConnectionPlate.pypsub" if self.build_ele.ObjectType.value == 1 else \
                                            "PythonPartConnectionHole.pypsub")

        self.build_ele.__AddPypSubFile__.value = file_name

        xml_ele = BuildingElementXML()

        build_ele, control_props, _ = xml_ele.read_element_parameter(file_name,
                                                                     self.str_table_service.str_table,
                                                                     self.str_table_service.material_str_table)

        if len(self.build_ele_list) == 2:
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
            self.object = PythonPartConnectionPlate(self.coord_input, self.palette_service,
                                                    self.build_ele_list, self.modification_ele_list)

        else:
            self.object = PythonPartConnectionHole(self.coord_input, self.palette_service,
                                                   self.build_ele_list, self.modification_ele_list)

        if is_refresh_palette:
            self.palette_service.refresh_palette(self.build_ele_list, self.control_props_list)
        else:
            self.palette_service.show_palette(self.build_ele.script_name)


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
            if self.modification_mode:
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

        if name == "ObjectType":
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
