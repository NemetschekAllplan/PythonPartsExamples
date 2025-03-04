""" implementation of the Grasshopper Python host handler
"""

# pylint: disable=bare-except

from __future__ import annotations

from typing import cast, Any


import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_BaseElements as AllplanBaseElements

from NodeUtil.NodeInitData import NodeInitData
from NodeUtil.NodeBase import NodeBase

from TypeCollections.ModelEleList import ModelEleList

from .NodeScriptManager import NodeScriptManager


class GrasshopperPythonHostHandler:
    """ implementation of the Grasshopper Python host handler
    """

    def __init__(self,
                 coord_input : AllplanIFW.CoordinateInput):
        """ Create the handler

        Args:
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        self.coord_input = coord_input

        self.node_script_mananager = NodeScriptManager()

        self.model_ele_list = ModelEleList()

    def handle_create_elements(self, request : dict):
        """ Handles request to create a cuboid object on default coordinates

        Args:
            request: request parameters
        """
        for element in request.values():
            if isinstance(element, list):
                for sub_element in element:
                    self.create_model_element(sub_element)
            else:
                self.create_model_element(element)


        #----------------- draw the preview

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(), AllplanGeo.Matrix3D(),
                                               self.model_ele_list, True, None)


    def create_model_element(self,
                             element_prop: dict[str, Any]):
        """ create a model element from the element properties

        Args:
            element_prop: element properties
        """
        node_name = element_prop["Name"]

        build_ele, control_props, script = self.node_script_mananager.get_node(f"Node{node_name}.pypsub")

        build_ele.get_existing_property("CreateModelObjects").value = True


        node_init_data = NodeInitData(self.coord_input, build_ele, control_props, None, None, AllplanGeo.Matrix3D(), None)

        node = cast(NodeBase, script.create_node(node_init_data))


        for prop in build_ele.get_properties():
            if (value := element_prop.get(prop.name, None)) is None:
                continue

            if isinstance(value, dict):
                for item_name, item_value in value.items():
                    node.modify_element_property(0, f"{prop.name}.{item_name}",  item_value)

            else:
                node._modify_element_property_no_execute(0, prop.name, value)

        node.create_objects()

        self.model_ele_list += build_ele.node_architecture_elements
