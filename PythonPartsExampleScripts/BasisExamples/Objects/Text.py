""" Script for Text
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from ParameterUtils.TextPropertiesParameterUtil import TextPropertiesParameterUtil

from Utils import LibraryBitmapPreview

from TypeCollections import ModelEleList


if TYPE_CHECKING:
    from __BuildingElementStubFiles.TextBuildingElement import TextBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Text.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Text(build_ele, script_object_data)


class Text(BaseScriptObject):
    """ Definition of class Text
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

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

        build_ele = self.build_ele

        text_prop = TextPropertiesParameterUtil.create_text_properties(build_ele, "")

        model_ele_list = ModelEleList()

        model_ele_list.append(AllplanBasisEle.TextElement(build_ele.CommonProp.value, text_prop,
                                                          build_ele.Text.value, AllplanGeo.Point2D()))

        return CreateElementResult(model_ele_list)
