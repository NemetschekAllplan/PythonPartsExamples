""" Implementation of the node script manager"""

from typing import Any
from dataclasses import dataclass
import pathlib

import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElement import BuildingElement
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementMaterialStringTable import BuildingElementMaterialStringTable
from BuildingElementService import BuildingElementService
from BuildingElementStringTable import BuildingElementStringTable
from BuildingElementUtil import BuildingElementUtil
from BuildingElementXML import BuildingElementXML


@dataclass
class NodeData:
    """Data class representing Node data"""

    build_ele           : BuildingElement
    build_ele_ctrl_prop : BuildingElementControlProperties
    script              : Any



class NodeScriptManager():
    """ implementation of the node script manager
    """

    def __init__(self):
        """ Intialize NodeScript Instance
        """

        self.nodes : map[str, NodeData] = {}


    def get_node(self,
                 node_name: str) -> tuple[BuildingElement, BuildingElementControlProperties, Any]:
        """ get the node

        Args:
            name: node name
        Returns:
            BuildingElement                  : An instance of Building Element
            BuildingElementControlProperties : An instance of BuildingElementControlProperties
            Any                              : A script instance of Type Any

        """

        if (node_data := self.nodes.get(node_name, None)) is not None:
            return node_data.build_ele, node_data.build_ele_ctrl_prop, node_data.script

        #------------------- read the data and import the script

        library_path = pathlib.Path(fr"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}\VisualScripts\NodeLib")
        file_name = None

        for file in library_path.rglob(node_name):
            file_name = str(file)
            break

        if file_name is None:
            return

        xml_ele = BuildingElementXML()

        build_ele, control_props, _ = xml_ele.read_element_parameter(file_name, BuildingElementStringTable("", False, ""),
                                                                     BuildingElementMaterialStringTable("", False, ""))


        script = BuildingElementUtil.import_building_element_script(build_ele, True)

        self.nodes[node_name] = NodeData(build_ele, control_props, script)

        return build_ele, control_props, script