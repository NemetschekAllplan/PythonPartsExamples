""" implementation of the Grasshopper Python host handler
"""

# pylint: disable=bare-except

from __future__ import annotations

import json
from typing import cast, Any
import json
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
                 coord_input : AllplanIFW.CoordinateInput,
                 build_ele: Any):
        """ Create the handler

        Args:
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        self.coord_input = coord_input

        self.node_script_mananager = NodeScriptManager()

        self.model_ele_list   = ModelEleList()
        self.preview_ele_list = ModelEleList()
        self.build_ele        = build_ele


    def handle_create_elements(self, request : dict):
        """ Handles request to create a cuboid object on default coordinates

        Args:
            request: request parameters
        """

        self.model_ele_list.clear()
        self.preview_ele_list.clear()

        for element in request.values():
            if isinstance(element, list):
                for sub_element in element:
                    if sub_element is None:
                        continue
                    self.create_model_element(sub_element)
            else:
                self.create_model_element(element)

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(), AllplanGeo.Matrix3D(),
                                               self.preview_ele_list, True, None)


    def create_model_element(self,
                             element_prop: dict[str, Any]):
        """ create a model element from the element properties


        Args:
            element_prop: element properties
        """

        if isinstance( element_prop, str):
            element_prop = json.loads(element_prop)
        node_name = element_prop["Name"]


        build_ele, control_props, script = self.node_script_mananager.get_node(f"Node{node_name}.pypsub")

        build_ele.get_existing_property("CreateModelObjects").value = True


        if element_prop.get("Bake"):
            build_ele.Format.value.reload = True
        else:
            build_ele.Format.value.reload = False
    
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


        if element_prop.get("PreviewState", False):
            self.preview_ele_list += build_ele.node_architecture_elements

        # Commented out for Testing purposed to show user preview being turned on and off
        if element_prop.get("Bake", False):
            self.model_ele_list   += build_ele.node_architecture_elements

    def get_plane_reference(self)-> str:
        """ Get Plane reference from ALLPLAN Palette.

        Returns:
            str: Plance reference in string form.
        """

        self.build_ele.HidePlaneReference.value = 0
        return self.build_ele.PlaneReferences.value_type.to_string(self.build_ele.PlaneReferences.value)
