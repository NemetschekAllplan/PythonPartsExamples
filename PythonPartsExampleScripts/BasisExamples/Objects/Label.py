""" Example Script for Label
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisEle

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from ParameterUtils.TextPropertiesParameterUtil import TextPropertiesParameterUtil

from Utils.LabelTextUtil import LabelTextUtil, LabelTextDimensionUnit, LabelTextFormat, LabelTextFrame

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelBuildingElement import LabelBuildingElement as BuildingElement  # type: ignore
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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Label(build_ele, script_object_data)


class Label(BaseScriptObject):
    """ Definition of class Label
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialize

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """  execute the script

        Returns:
            created result
        """

        #------------------ Define the cube polyhedron

        build_ele = self.build_ele

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value,
                                                       build_ele.Width.value,
                                                       build_ele.Height.value)

        model_ele_list.append_geometry_3d(polyhed)


        #----------------- create the label for the dimension

        label_util = LabelTextUtil()

        label_util.set_text_frame(cast(LabelTextFrame, build_ele.Frame.value))
        label_util.set_pre_text(build_ele.ParameterName.value + "=")
        label_util.set_format(LabelTextFormat.FLOAT, 10, 2)
        label_util.set_dimension_unit(LabelTextDimensionUnit.M)


        #----------------- use the value from the PythonPart parameter attribute

        build_ele_attr_list = BuildingElementAttributeList()

        if build_ele.CreatePythonPart.value:
            label_util.add_parameter(build_ele, build_ele.ParameterName.value)


        #----------------- create and use an attribute

        else:
            geo_attr_dict = {"Length": 220, "Width": 758, "Height": 222}

            attribute_id    = geo_attr_dict[build_ele.ParameterName.value]
            attribute_value = build_ele.get_existing_property(build_ele.ParameterName.value).value

            build_ele_attr_list.add_attribute(attribute_id, attribute_value / 1000)

            label_util.add_attribute(self.document, attribute_id, attribute_value)

        text_prop = TextPropertiesParameterUtil.create_text_properties(build_ele, "")

        text_prop.Alignment = AllplanBasisEle.TextAlignment.eMiddleTop
        text_prop.Type      = AllplanBasisEle.TextType.eVariableText

        label_text = AllplanBasisEle.TextElement(build_ele.CommonProp.value, text_prop,
                                                      label_util.create_label_text() +
                                                      label_util.create_label_default_text(),
                                                      AllplanGeo.Point2D(build_ele.Length.value / 2, -300))

        labels = [AllplanBasisEle.LabelElement(label_text, AllplanBasisEle.LabelType.eLabelVariableText)]


        #----------------- create the attribute label

        y_label = build_ele.Width.value + 300

        label_text_ele = AllplanBasisEle.TextElementList()

        for attribute in build_ele.AttributeList.value:
            if not attribute.attribute_id:
                break

            text_prop.Alignment = AllplanBasisEle.TextAlignment.eMiddleBottom

            label_util = LabelTextUtil()

            label_util.set_text_frame(cast(LabelTextFrame, build_ele.Frame.value))
            label_util.add_attribute(self.document, attribute.attribute_id, attribute.value)

            label_text = AllplanBasisEle.TextElement(build_ele.CommonProp.value, text_prop,
                                                          label_util.create_label_text() +
                                                          label_util.create_label_default_text(),
                                                          AllplanGeo.Point2D(build_ele.Length.value / 2, y_label))

            label_text_ele.append(label_text)

            build_ele_attr_list.add_attribute(attribute.attribute_id, attribute.value)

            y_label += label_text.GetDimensions(self.document).Y * 2

        if label_text_ele:
            labels.append(AllplanBasisEle.LabelElement(label_text_ele, AllplanBasisEle.LabelType.eLabelVariableText))


        #----------------- create the PythonPart

        if build_ele.CreatePythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(model_ele_list)

            pyp_util.add_label_elements(labels)

            return CreateElementResult(pyp_util.create_pythonpart(build_ele))


        #----------------- create a model element

        model_ele_list.set_element_attributes(-1, build_ele_attr_list.get_attribute_list())

        model_ele_list += labels

        return CreateElementResult(model_ele_list)
