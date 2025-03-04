""" An example script showing creation of a PythonPart with attributes.
The purpose of this PythonPart is to show, how to save values
calculated inside the script inside an attribute.

Other purpose is to show, how attribute values modified outside the
PythonPart, using native Attribute functions of Allplan, can be read
back into the script to use the in geometry calculation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from PythonPart import PythonPart
from PythonPartUtil import PythonPartUtil
from TypeCollections.ModelEleList import ModelEleList

from Utilities.AttributeIdEnums import AttributeIdEnums

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartWithAttributesBuildingElement import \
        PythonPartWithAttributesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

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

    return PythonPartWithAttributes(build_ele, script_object_data)


class PythonPartWithAttributes(BaseScriptObject):
    """ Definition of class PythonPartWithAttributes
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


    def create_library_preview(self) -> CreateElementResult:
        """ create the library preview

        Returns:
            created elements for the preview
        """

        return self.execute()


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        python_part = self.create_pythonpart()

        return CreateElementResult(python_part.create(), multi_placement = True)


    def create_pythonpart(self) -> PythonPart:
        """ Create a PythonPart containing cube geometry and some attributes

        Returns:
            PythonPart object
        """

        build_ele = self.build_ele

        python_part_util = PythonPartUtil(build_ele.CommonProp.value)

        python_part_util.add_pythonpart_view_2d3d(self.create_bottom_cuboid() + self.create_top_cuboid())

        if build_ele.AppendGeometryAttributes.value:
            geometry_attributes = BuildingElementAttributeList()
            geometry_attributes.add_attribute_by_unit(AttributeIdEnums.LENGTH, build_ele.Dimensions.value.X)
            geometry_attributes.add_attribute_by_unit(AttributeIdEnums.THICKNESS, build_ele.Dimensions.value.Y)
            geometry_attributes.add_attribute_by_unit(AttributeIdEnums.HEIGHT, build_ele.Dimensions.value.Z)

            python_part_util.add_attribute_list(geometry_attributes)

        return python_part_util.get_pythonpart(build_ele,
                                               type_uuid = "23b28875-bc0e-4e8b-b0df-e36d0d1c432c",
                                               type_display_name = "PythonPart with attributes")


    def create_top_cuboid(self) -> ModelEleList:
        """ Creates a model element list containing one cuboid with dimensions specified
        by the user in the property palette

        Returns:
            Model element list with one element representing a cuboid
        """

        build_ele = self.build_ele

        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(0, 0, build_ele.LayerThickness.value),
                                                          AllplanGeo.Point3D() + build_ele.Dimensions.value)

        common_props       = AllplanBaseEle.CommonProperties()
        common_props.Color = 6

        model_ele_list = ModelEleList(common_props)
        model_ele_list.append_geometry_3d(cuboid_geo)

        return model_ele_list


    def create_bottom_cuboid(self) -> ModelEleList:
        """ Creates a model element list containing one cuboid with dimensions specified
        by the user in the property palette

        Returns:
            Model element list with one element representing a cuboid
        """

        build_ele = self.build_ele

        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(),
                                                          AllplanGeo.Point3D(build_ele.Dimensions.value.X,
                                                                             build_ele.Dimensions.value.Y,
                                                                             build_ele.LayerThickness.value))

        common_props       = AllplanBaseEle.CommonProperties()
        common_props.Color = 7

        model_ele_list = ModelEleList(common_props)
        model_ele_list.append_geometry_3d(cuboid_geo)

        return model_ele_list
