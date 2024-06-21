""" Script for LabelElement
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult

from ParameterUtils.TextPropertiesParameterUtil import TextPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from Utils import LibraryBitmapPreview
from Utils.LabelTextUtil import LabelTextUtil, LabelTextFrame

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelElementBuildingElement import LabelElementBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load LabelElement.py')


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
                               r"Examples\PythonParts\BasisExamples\ObjectCreation\LabelElement.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return LabelElement(build_ele, coord_input)


class LabelElement(BaseScriptObject):
    """ Definition of class LabelElement
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

        self.sel_res     = SingleElementSelectResult()
        self.labeled_ele = AllplanEleAdapter.BaseElementAdapter()

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_res)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.labeled_ele = self.sel_res.sel_element

        if not (ele_attributes := self.labeled_ele.GetAttributes(AllplanBaseEle.eAttibuteReadState.ReadAll)):
            AllplanUtil.ShowMessageBox("Selected element has no attributes", AllplanUtil.MB_OK)
            return


        #----------------- sort the attributes by the group IDs

        group_names = []
        attributes  = []

        for group_name, group_attribute_ids in AllplanBaseEle.AttributeService.GetGroupAttributeIDs(self.labeled_ele, ele_attributes,
                                                                                                    True):
            group_names += [group_name] * len(group_attribute_ids)

            for group_attribute_id in group_attribute_ids:
                attributes.append(next((attribute_id, value) for attribute_id, value in ele_attributes \
                                        if attribute_id == group_attribute_id))


        #----------------- assign the attribute data

        prop = build_ele.Attributes

        build_ele.GroupNames.value    = group_names
        build_ele.AttributeName.value = [AllplanBaseEle.AttributeService.GetAttributeName(self.document, attribute_id) \
                                         for attribute_id, _ in attributes]
        prop.value                    = [value for _, value in attributes]
        prop.attribute_id_str         = str([attribute_id for attribute_id, _ in attributes])

        build_ele.AttributeLabel.value = [False] * len(prop.value)

        self.set_text_for_palette_modification("Select the attribute(s)")

        build_ele.InputMode.value = build_ele.ELEMENT_LABEL

        self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        text_prop = TextPropertiesParameterUtil.create_text_properties(build_ele, "")

        text_prop.Type = AllplanBasisEle.TextType.eVariableText

        label_text_ele = AllplanBasisEle.TextElementList()

        ref_pnt = AllplanGeo.Point2D()

        for state, attribute_id, attribute_value in zip(build_ele.AttributeLabel.value,
                                                        cast(list, build_ele.Attributes.attribute_id),
                                                        build_ele.Attributes.value):
            if not state:
                continue

            label_util = LabelTextUtil()
            label_util.set_text_frame(cast(LabelTextFrame, build_ele.Frame.value))

            label_util.add_attribute(self.document, attribute_id, attribute_value)

            text_ele = AllplanBasisEle.TextElement(build_ele.TextCommonProp.value, text_prop,
                                                   label_util.create_label_text() + label_util.create_label_default_text(),
                                                   ref_pnt)

            ref_pnt -= AllplanGeo.Point2D(0, text_ele.GetDimensions(self.document).Y * 2)

            label_text_ele.append(text_ele)

        label = AllplanBasisEle.LabelElement(label_text_ele, AllplanBasisEle.LabelType.eLabelVariableText)

        label.SetLabeledElement(self.labeled_ele)

        return CreateElementResult([label], multi_placement = True)
