""" Script for a PythonPart, that prints the entire hierarchy of the selected element in the console.
"""

from __future__ import annotations

import importlib
import os

from pathlib import Path
from typing import TYPE_CHECKING

import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ShowHierarchyBuildingElement import ShowHierarchyBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

try:
    from anytree import AnyNode, RenderTree
except ImportError:
    AnyNode = None
    RenderTree = None

print('Load ShowHierarchy.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check, whether the anytree module is installed

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True if the anytree module is installed, False otherwise
    """
    try:
        importlib.import_module('anytree')
    except ImportError:
        AllplanUtil.ShowMessageBox(
            "The 'anytree' module is required to run this script. " + \
            "Please install it using the tool 'Install Python Package'. " + \
            "You may need to restart ALLPLAN after the installation.",
            AllplanUtil.MB_OK)
        return False

    return True


def create_preview(build_ele : BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele:  building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """
    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """
    os.system("color")
    return ObjectHierarchyScript(build_ele, script_object_data)


class ObjectHierarchyScript(BaseScriptObject):
    """Implementation of a script object, showing the hierarchy of the selected model element

    Workflow: The user selects an element in the model and the entire hierarchy is printed in the console.
    This means all the parent elements up until the root and all child elements of the root are printed
    as a tree structure. The selected element is marked with a different color.
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Default constructor

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """
        super().__init__(script_object_data)

        self.build_ele        = build_ele
        self.selection_result = SingleElementSelectResult()

    def execute(self) -> CreateElementResult:
        """Execute the element creation

        Returns:
            created element
        """
        return CreateElementResult()   # this interactor class just prints hierarchy, nothing to create

    def start_input(self):
        """Start the element selection"""

        self.script_object_interactor = SingleElementSelectInteractor(self.selection_result)

    def start_next_input(self):
        """Print the information about selected element and restarts the input"""

        tree = BaseElementAdapterTree(self.selection_result.sel_element,
                                      self.build_ele.MaxTreeDepth.value,
                                      self.build_ele.PrintHiddenElements.value)
        tree.print()


class BaseElementAdapterTree:
    """Class to build a tree of the BaseElementAdapter hierarchy"""

    def __init__(self,
                 selected_element: AllplanEleAdapter.BaseElementAdapter,
                 max_tree_depth: int = 20,
                 include_hidden_elements: bool = False):
        """Default constructor

        Args:
            selected_element:        selected element to build the tree from
            max_tree_depth:          maximum depth of the tree (from root element to the leaf elements)
            include_hidden_elements: whether to include hidden elements in the tree
        """
        self.selected_element = selected_element
        self.doc              = selected_element.GetDocument()
        self.max_tree_depth   = max_tree_depth

        # build the tree
        root_element = BaseElementAdapterTree._get_root_element_adapter(self.selected_element)

        self.root = AnyNode(id       = str(root_element.GetModelElementUUID()),               # type: ignore
                            type     = root_element.GetElementAdapterType().GetTypeName() ,
                            geo_type = type(root_element.GetGeometry()).__name__ ,
                            selected = root_element == self.selected_element)

        self._add_children(self.root, include_hidden_elements= include_hidden_elements)

    @staticmethod
    def _get_root_element_adapter(element: AllplanEleAdapter.BaseElementAdapter) -> AllplanEleAdapter.BaseElementAdapter:
        """Recursively go up the hierarchy until the root element adapter is reached

        Args:
            element: element to get the root element adapter from

        Returns:
            root element adapter
        """
        parent = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(element)

        return BaseElementAdapterTree._get_root_element_adapter(parent) if not parent.IsNull() else element

    def _add_children(self, parent: AnyNode, depth: int = 0, include_hidden_elements: bool = False) -> None:
        """Recursively add the child elements to the tree

        Args:
            parent: parent node to add the children to
            depth:  current depth in the tree
        """
        parent_guid     = AllplanEleAdapter.GUID.FromString(parent.id)
        parent_adapter  = AllplanEleAdapter.BaseElementAdapter.FromGUID(parent_guid, self.doc)
        children        = AllplanEleAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(parent_adapter, include_hidden_elements)

        if len(children) == 0:
            return

        for child_adapter in children:
            child = AnyNode(parent   = parent,                                              # type: ignore
                            id       = str(child_adapter.GetModelElementUUID()),
                            type     = child_adapter.GetElementAdapterType().GetTypeName(),
                            geo_type = type(child_adapter.GetGeometry()).__name__,
                            selected = child_adapter == self.selected_element)

            if depth <= self.max_tree_depth:
                self._add_children(child, depth + 1, include_hidden_elements)

    def print(self) -> None:
        """Print the tree in the console"""

        print(f"\n\n{'=' * 60} Object hierarchy {'=' * 60}\n")
        print(f"{'Tree':<80}{'|  Geometry type'}")
        print(f'{"-" * 80}|{"-" * 30}')

        for pre, _, node in RenderTree(self.root):                                          # type: ignore
            mark = "\033[33m" if node.selected else "\033[00m"
            print(f"{pre + mark + node.type:<85}|  {node.geo_type}\033[0m")

        print()
        AllplanUtil.ShowMessageBox("Object hierarchy printed in the console. " + \
            "The selected element is printed in yellow.",
            AllplanUtil.MB_OK)
