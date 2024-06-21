""" Script for DWGExportByFileList
"""

# pylint: disable=consider-using-with

from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, cast

import os
import sys


import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Utility as AllplanUtil

sys.path.append(f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}\\PythonParts-site-packages")

import yaml
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService
from PythonPartActionBarUtil.YamlUtil.yaml_models import AppConfig
from PythonPartActionBarUtil.YamlUtil.copy_files import CopyFiles



def check_allplan_version(_build_ele: BuildingElement,
                          _version  : type) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version  : the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_element(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element (only necessary for the library preview)

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult()


def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      build_ele_ctrl_props_list: List[BuildingElementControlProperties],
                      _modify_uuid_list        : List[str]) -> object:
    """ Create the interactor

    Args:
        coord_input              : API object for the coordinate input, element selection, ... in the Allplan view
        _pyp_path                : path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list           : list with the building elements
        build_ele_composite      : building element composite with the building element constraints
        build_ele_ctrl_props_list: list with the building element control properties
        _modify_uuid_list        : list with the UUIDs of the modified elements

    Returns:
        created interactor
    """

    return TestConfigYML(coord_input, build_ele_list, build_ele_composite,  build_ele_ctrl_props_list)


class TestConfigYML():
    """ Definition of class TestConfigYML
    """

    def __init__(self,
                 coord_input              : AllplanIFW.CoordinateInput,
                 build_ele_list           : List[BuildingElement],
                 build_ele_composite      : BuildingElementComposite,
                 build_ele_ctrl_props_list: List[BuildingElementControlProperties]):
        """ Initialization of class TestConfigYML

        Args:
            coord_input              : API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list           : list with the building elements
            build_ele_composite      : building element composite with the building element constraints
            build_ele_ctrl_props_list: list with the building element control properties
        """

        self.coord_input               = coord_input
        self.build_ele_list            = build_ele_list
        self.build_ele_composite       = build_ele_composite
        self.build_ele_ctrl_props_list = build_ele_ctrl_props_list
        self.build_ele                 = cast(BuildingElement, build_ele_list[0])

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             "TestConfigYML",
                                                             self.build_ele_ctrl_props_list, "")


        self.palette_service.show_palette("")


        #----------------- get the properties and start the input

        if not sys.argv or sys.argv == ['']:
            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Execute by button click"))

            return

        AllplanBaseElements.ProjectService.CloseAllplan()

    def read_config(self, file_path: str) -> AppConfig:

        with open(file_path, "rt", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
            return AppConfig.model_validate(config_data)

    def modify_element_property(self, page: int, name: str, value: Any):
        """ Modify property of element

        Args:
            page : page index of the modified property
            name : name of the modified property
            value: new value
        """

        self.palette_service.modify_element_property(page, name, value)



    def on_cancel_function(self) -> bool:
        """ Check for input function cancel in case of ESC

        Returns:
            True
        """

        self.palette_service.close_palette()

        return True


    def on_preview_draw(self):
        """ Handles the preview draw event
        """


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """


    def on_control_event(self,
                         _event_id: int):
        """ On control event

        Args:
            _event_id: event id of the clicked button control
        """
        
        if _event_id == 1003:
            config = self.read_config(self.build_ele.ConfigFile.value)
            config.installation.install_pypackages(self.build_ele.reqFile.value)
        if _event_id == 1002:
            config = self.read_config(self.build_ele.ConfigFile.value)
            config.write_npd_file()
        if _event_id == 1004:
            file_mover = CopyFiles.create(self.build_ele.allep.value)
            file_mover.move_files(self.build_ele.allep.value)


    def process_mouse_msg(self,
                          _mouse_msg: int,
                          _pnt      : AllplanGeo.Point2D,
                          _msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """ Process the mouse message event

        Args:
            _mouse_msg: mouse message ID
            _pnt:       input point in Allplan view coordinates
            _msg_info:  additional mouse message info

        Returns:
            True
        """

        return True


    def check_structure_settings(self,
                                 host_name   : str,
                                 project_name: str):
        """ create the file with the structure settings

        Args:
            host_name:    host name
            project_name: project name
        """

        error, path = AllplanBaseElements.ProjectService.GetProjectPath(host_name, project_name)

        if error:
            return

        path += "\\BIM\\" + AllplanBaseElements.ProjectService.GetCurrentUserAsBwsPath() + "\\settings"

        settings_file = path + "\\Structure_settings.xml"

        if os.path.exists(settings_file):
            return

        if not os.path.exists(path):
            os.makedirs(path)

        with open(settings_file, "w", encoding = "UTF-8") as file:
            file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
                       "<NemetschekBIMStructureSettings Activated=\"1\">\n"
                       "<Files>\n"
                       "    <File ID=\"0001\" State=\"3\" Activated=\"1\" />\n"
                       "</Files>\n"
                       "</NemetschekBIMStructureSettings>")
