""" Example Script for LabelModify
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from ParameterUtils.TextPropertiesParameterUtil import TextPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelModifyBuildingElement import LabelModifyBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Label.py')


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
                               r"Examples\PythonParts\BasisExamples\ObjectModification\LabelModify.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return LabelModify(build_ele, script_object_data)


class LabelModify(BaseScriptObject):
    """ Definition of class LabelModify
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

        self.placement_pnt  = AllplanGeo.Point2D()

        self.sel_label     = SingleElementSelectResult()
        self.label_ele     = AllplanBasisEle.LabelElement()
        self.text_elements = AllplanBasisEle.TextElementList()

        build_ele.InputMode.value = build_ele.LABEL_SELECT


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_label,
                                                                [AllplanEleAdapter.GeneralVariableText_TypeUUID,
                                                                 AllplanEleAdapter.GeneralVariableTextBlock_TypeUUID,
                                                                 AllplanEleAdapter.ArchitectureVariableText_TypeUUID,
                                                                 AllplanEleAdapter.ArchitectureVariableTextBlock_TypeUUID])

        self.build_ele.InputMode.value = self.build_ele.LABEL_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele


        #----------------- get the text element and start the modification

        ele_list = AllplanEleAdapter.BaseElementAdapterList([self.sel_label.sel_element])

        self.label_ele = cast(AllplanBasisEle.LabelElement, AllplanBaseEle.GetElements(ele_list).pop())

        self.text_elements = self.label_ele.TextElements

        text_ele = self.text_elements[0]

        TextPropertiesParameterUtil.set_parameter_values(build_ele, text_ele.GetTextProperties(), "")

        build_ele.Texts.value      = [text_ele.GetText() for text_ele in self.text_elements]
        build_ele.CommonProp.value = text_ele.GetCommonProperties()


        #----------------- change to text modification

        self.set_text_for_palette_modification("Modify the text")

        AllplanIFW.VisibleService.ShowElements(ele_list, False)

        build_ele.InputMode.value = build_ele.LABEL_MODIFY

        self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        text_prop = TextPropertiesParameterUtil.create_text_properties(build_ele, "")

        for text_ele in self.text_elements:
            text_ele.SetCommonProperties(build_ele.CommonProp.value)
            text_ele.SetTextProperties(text_prop)

        self.label_ele.TextElements = self.text_elements

        model_ele_list = ModelEleList()

        model_ele_list.append(self.label_ele)

        return CreateElementResult(model_ele_list, multi_placement = True)
