""" Example script for PictureComboBox
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PictureComboBoxBuildingElement \
        import PictureComboBoxBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PictureComboBox.py')


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
ö
    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\PaletteExamples\BasicControls\PictureComboBox.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PictureComboBox(build_ele, script_object_data)


class PictureComboBox(BaseScriptObject):
    """ Definition of class PictureComboBox
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        com_prop = build_ele.CommonProp.value

        text_prop = AllplanBasisEle.TextProperties()

        y_dist = -(text_prop.Height * 2 * self.document.GetScalingFactor())

        texts = [AllplanBasisEle.TextElement(com_prop, text_prop,
                                             f"Integer value list: {build_ele.IntegerValueList.value}",  AllplanGeo.Point2D(0, 0)),
                 AllplanBasisEle.TextElement(com_prop, text_prop,
                                             f"Constant value list: {build_ele.UpDown.value}",  AllplanGeo.Point2D(0, y_dist))]


        #----------------- add the types from the list

        y_text = y_dist * 4

        for index, sel_index in enumerate(build_ele.Indexes.value):
            texts.append(AllplanBasisEle.TextElement(com_prop, text_prop,
                                                     f"Indexes[{index}]: {sel_index}", AllplanGeo.Point2D(0, y_text)))

            y_text += y_dist


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(texts)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
