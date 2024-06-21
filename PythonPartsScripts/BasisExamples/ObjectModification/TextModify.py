""" Example Script for Text
"""

from __future__ import annotations

from typing import TYPE_CHECKING,cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from ParameterUtils.TextPropertiesParameterUtil import TextPropertiesParameterUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.TextModifyBuildingElement import TextModifyBuildingElement as BuildingElement  # type: ignore
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


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\ObjectModification\TextModify.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return TextModify(build_ele, coord_input)


class TextModify(BaseScriptObject):
    """ Definition of class TextModify
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.build_ele = build_ele

        self.placement_pnt  = AllplanGeo.Point2D()

        self.sel_text = SingleElementSelectResult()
        self.text_ele = AllplanBasisEle.TextElement()

        build_ele.InputMode.value = build_ele.TEXT_SELECT


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_text,
                                                                [AllplanEleAdapter.TextBlock_TypeUUID,
                                                                 AllplanEleAdapter.ArchitectureTextBlock_TypeUUID])

        self.build_ele.InputMode.value = self.build_ele.TEXT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele


        #----------------- get the text element and start the modification

        ele_list = AllplanEleAdapter.BaseElementAdapterList([self.sel_text.sel_element])

        self.text_ele = cast(AllplanBasisEle.TextElement, AllplanBaseEle.GetElements(ele_list).pop())

        TextPropertiesParameterUtil.set_parameter_values(build_ele, self.text_ele.GetTextProperties(), "")

        build_ele.Text.value       = self.text_ele.GetText()
        build_ele.CommonProp.value = self.text_ele.GetCommonProperties()

        self.placement_pnt = self.text_ele.GetGeometryObject()


        #----------------- change to text modification

        self.set_text_for_palette_modification("Modify the text")

        AllplanIFW.VisibleService.ShowElements(ele_list, False)

        build_ele.InputMode.value = build_ele.TEXT_MODIFY

        self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        text_prop = TextPropertiesParameterUtil.create_text_properties(build_ele, "")

        self.text_ele.SetCommonProperties(build_ele.CommonProp.value)
        self.text_ele.SetTextProperties(text_prop)
        self.text_ele.SetText(build_ele.Text.value)

        model_ele_list = ModelEleList()

        model_ele_list.append(self.text_ele)

        return CreateElementResult(model_ele_list, multi_placement = True)
