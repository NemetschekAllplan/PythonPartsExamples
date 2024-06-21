""" Script for LabelPythonPart
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from AnyValueByType import AnyValueByType
from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult

from ParameterUtils.TextPropertiesParameterUtil import TextPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ParameterValueList import ParameterValueList

from Utils import LibraryBitmapPreview
from Utils.PythonPart.PythonPartParameterUtil import PythonPartParameterUtil
from Utils.LabelTextUtil import LabelTextUtil, LabelTextFrame, LabelTextDimensionUnit

from ValueTypes.ParameterPropertyValueTypes import ParameterPropertyValueTypes

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelPythonPartBuildingElement import LabelPythonPartBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load LabelPythonPart.py')


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
                               r"Examples\PythonParts\BasisExamples\ObjectCreation\LabelPythonPart.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return LabelPythonPart(build_ele, coord_input)


class LabelPythonPart(BaseScriptObject):
    """ Definition of class LabelPythonPart
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

        self.placement_pnt = AllplanGeo.Point2D()
        self.param_values  = ParameterValueList()

        self.sel_res                = SingleElementSelectResult()
        self.labeled_ele            = AllplanEleAdapter.BaseElementAdapter()
        self.labeled_build_ele_list = []

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_res,
                                                                      [AllplanEleAdapter.PythonPart_TypeUUID,
                                                                       AllplanEleAdapter.PythonPartGroup_TypeUUID,
                                                                       AllplanEleAdapter.SubPythonPart_TypeUUID])

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.labeled_ele = self.sel_res.sel_element


        #----------------- get the parameter

        param_util =PythonPartParameterUtil(self.labeled_ele, build_ele.get_string_tables()[1],
                                            build_ele.get_material_string_table())

        self.param_values, self.labeled_build_ele_list = param_util.get_label_data(self.coord_input.GetInputViewDocument())

        param_label = self.build_ele.ParameterLabel.value
        param_text  = self.build_ele.ParameterText.value
        parameters  = self.build_ele.Parameters.value

        for param_value in self.param_values:
            param_text.append(param_value.text)
            param_label.append(False)

            parameters.append(AnyValueByType(param_value.value_type, "", param_value.value))


        #----------------- select the parameter

        self.set_text_for_palette_modification("Select the parameter(s)")

        build_ele.InputMode.value = build_ele.ELEMENT_LABEL

        self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """ create the label

        Returns:
            created element result
        """

        build_ele = self.build_ele

        if True not in build_ele.ParameterLabel.value:
            return CreateElementResult()


        #----------------- create the elements

        text_prop = TextPropertiesParameterUtil.create_text_properties(build_ele, "")

        text_prop.Type = AllplanBasisEle.TextType.eVariableText

        label_text_ele = AllplanBasisEle.TextElementList()

        ref_pnt = AllplanGeo.Point2D()

        doc = self.coord_input.GetInputViewDocument()


        #----------------- create the labels

        for state, data in zip(build_ele.ParameterLabel.value, self.param_values):
            if not state:
                continue

            label_util = LabelTextUtil()
            label_util.set_text_frame(cast(LabelTextFrame, build_ele.Frame.value))

            if build_ele.AddParameterText.value:
                label_util.set_pre_text(f"{data.text}=")


            #------------- add attribute or parameter label

            if data.attribute_id:
                label_util.add_attribute(doc, data.attribute_id, data.value)

            else:
                if data.value_type == ParameterPropertyValueTypes.ANGLE:
                    label_util.set_dimension_unit(LabelTextDimensionUnit.DEG)
                else:
                    label_util.set_dimension_unit_by_value_type(data.value_type)

                label_util.set_format_by_value_type(data.value_type)
                label_util.add_parameter(self.labeled_build_ele_list, data.name, data.value)


            #------------- create the text

            text_ele = AllplanBasisEle.TextElement(build_ele.TextCommonProp.value, text_prop,
                                                   label_util.create_label_text() + label_util.create_label_default_text(), ref_pnt)

            ref_pnt -= AllplanGeo.Point2D(0, text_ele.GetDimensions(doc).Y * 2)

            label_text_ele.append(text_ele)


        #----------------- create the label

        label = AllplanBasisEle.LabelElement(label_text_ele, AllplanBasisEle.LabelType.eLabelVariableText)

        label.SetLabeledElement(self.labeled_ele)

        return CreateElementResult([label])
