"""Example script showing the creation of a PythonPartSwitcher
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartSwitcherBuildingElement import PythonPartSwitcherBuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PythonPartSwitcher.py')

def check_allplan_version(_build_ele: PythonPartSwitcherBuildingElement,
                          _version: float) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_script_object(build_ele         : PythonPartSwitcherBuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PythonPartSwitcherExample(build_ele, script_object_data)


class PythonPartSwitcherExample(BaseScriptObject):
    """ Definition of class PythonPartSwitcherExample
    """

    def __init__(self,
                 build_ele         : PythonPartSwitcherBuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def create_library_preview(self) -> CreateElementResult:
        """ create the library preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult()


    def modify_element_property(self,
                                name : str,
                                value: str) -> bool:
        """ modify the element property

        Args:
            name:  name
            value: value

        Returns:
            update palette state
        """

        if name == "PythonPartSelect" and self.exec_switch_pythonpart and value != "None":          # pylint: disable=magic-value-comparison
            self.exec_switch_pythonpart(value + ".pyp", self.build_ele.AddCurrentToStack.value)

        return False
