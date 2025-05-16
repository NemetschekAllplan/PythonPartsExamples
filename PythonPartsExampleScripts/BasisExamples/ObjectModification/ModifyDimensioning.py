"""
Example Script for Modify Dimensioning
"""
from __future__ import annotations

from typing import TYPE_CHECKING, cast


import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisElements

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult

from TypeCollections.ModelEleList import ModelEleList

import NemAll_Python_IFW_Input as AllplanIFW

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyDimensioningBuildingElement import ModifyDimensioningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Modify Dimensioning.py')

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
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

    return ModifyDimLine(build_ele, script_object_data)

class ModifyDimLine(BaseScriptObject):
    """ Definition of class Modify DImensioning
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

        self.dim_sel_result                = SingleElementSelectResult()
        self.dim_ele                       = AllplanBasisElements.DimensionLineElement()
        self.build_ele                     = build_ele

        build_ele.InputMode.value = build_ele.DIMENSIONING_SELECT


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.dim_sel_result,
                                                                      [AllplanEleAdapter.ElevationDimension_TypeUUID,
                                                                       AllplanEleAdapter.LinearDimension_TypeUUID],
                                                                      "Select the dimension")

        self.build_ele.InputMode.value = self.build_ele.DIMENSIONING_SELECT

    def start_next_input(self):
    #     """ start the next input
    #     """

        build_ele = self.build_ele

        self.dim_ele = cast(AllplanBasisElements.DimensionLineElement, AllplanBaseEle.GetElement(self.dim_sel_result.sel_element))

        props = self.dim_ele.GetProperties()
        seg_props = self.dim_ele.GetSegmentProperties()

        self.build_ele.FirstElementIsUnderlined.value   = seg_props[0].DimensionNumberIsUnderline
        self.build_ele.ColorDimLine.value               = props.LineColorIDDimLine
        self.build_ele.SizeDimText.value                = props.TextHeightDimensionNumber
        self.build_ele.ShowDimLine.value                = props.DimensionLineIsVisible
        self.build_ele.SizeArrowHead.value              = props.PointSymbolSize
        self.build_ele.TextOffset.value                 = props.TextOffset


        ele_list = AllplanEleAdapter.BaseElementAdapterList([self.dim_sel_result.sel_element])

        AllplanIFW.VisibleService.ShowElements(ele_list, False)

        self.script_object_interactor = None

        build_ele.InputMode.value = build_ele.DIMENSIONING_MODIFY


    def create_dimension(self) -> ModelEleList:

        model_ele_list = ModelEleList()

        props = self.dim_ele.GetProperties()
        seg_props = self.dim_ele.GetSegmentProperties()

        seg_props[0].DimensionNumberIsUnderline         = self.build_ele.FirstElementIsUnderlined.value
        props.LineColorIDDimLine                        = self.build_ele.ColorDimLine.value
        props.TextHeightDimensionNumber                 = self.build_ele.SizeDimText.value
        props.DimensionLineIsVisible                    = self.build_ele.ShowDimLine.value
        props.PointSymbolSize                           = self.build_ele.SizeArrowHead.value
        props.TextOffset                                = self.build_ele.TextOffset.value

        self.dim_ele.SetProperties(props)
        self.dim_ele.SetSegmentProperties(seg_props)

        model_ele_list.append(self.dim_ele)

        return model_ele_list

    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_dimension(), multi_placement = True)

    def on_cancel_function(self) -> OnCancelFunctionResult:

        if self.dim_sel_result != SingleElementSelectResult():
            AllplanBaseEle.ModifyElements(self.document, self.create_dimension())

        return OnCancelFunctionResult.CANCEL_INPUT

