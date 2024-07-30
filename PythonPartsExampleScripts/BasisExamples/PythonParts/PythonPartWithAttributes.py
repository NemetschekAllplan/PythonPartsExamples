""" An example script showing creation of a PythonPart with attributes.
The purpose of this PythonPart is to show, how to save values
calculated inside the script inside an attribute.

Other purpose is to show, how attribute values modified outside the
PythonPart, using native Attribute functions of Allplan, can be read
back into the script to use the in geometry calculation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from PythonPart import PythonPart
from PythonPartUtil import PythonPartUtil
from TypeCollections.ModelEleList import ModelEleList

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


def create_element(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Function for the element creation

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        created element result
    """
    python_part = create_pythonpart(build_ele)

    return CreateElementResult(python_part.create())

def create_pythonpart(build_ele: BuildingElement) -> PythonPart:
    """Create a PythonPart containing cube geometry and some attributes

    Args:
        build_ele: BuildingElement object containing parameter values

    Returns:
        PythonPart object
    """
    python_part_util = PythonPartUtil(build_ele.CommonProp.value)

    python_part_util.add_pythonpart_view_2d3d(create_bottom_cuboid(build_ele) + create_top_cuboid(build_ele))

    if build_ele.AppendGeometryAttributes.value:
        geometry_attributes = BuildingElementAttributeList()
        geometry_attributes.add_attribute(220, build_ele.Dimensions.value.X / 1000)
        geometry_attributes.add_attribute(221, build_ele.Dimensions.value.Y / 1000)
        geometry_attributes.add_attribute(222, build_ele.Dimensions.value.Z / 1000)

        python_part_util.add_attribute_list(geometry_attributes)

    return python_part_util.get_pythonpart(build_ele,
                                           type_uuid = "23b28875-bc0e-4e8b-b0df-e36d0d1c432c",
                                           type_display_name = "PythonPart with attributes")


def create_top_cuboid(build_ele: BuildingElement) -> ModelEleList:
    """Creates a model element list containing one cuboid with dimensions specified
    by the user in the property palette

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        Model element list with one element representing a cuboid
    """
    cuboid_geo     = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(0, 0, build_ele.LayerThickness.value),
                                                          AllplanGeo.Point3D() + build_ele.Dimensions.value)

    common_props       = AllplanBaseElements.CommonProperties()
    common_props.Color = 6

    model_ele_list = ModelEleList(common_props)
    model_ele_list.append_geometry_3d(cuboid_geo)

    return model_ele_list

def create_bottom_cuboid(build_ele: BuildingElement) -> ModelEleList:
    """Creates a model element list containing one cuboid with dimensions specified
    by the user in the property palette

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        Model element list with one element representing a cuboid
    """
    cuboid_geo     = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(),
                                                          AllplanGeo.Point3D(build_ele.Dimensions.value.X,
                                                                             build_ele.Dimensions.value.Y,
                                                                             build_ele.LayerThickness.value))

    common_props       = AllplanBaseElements.CommonProperties()
    common_props.Color = 7

    model_ele_list = ModelEleList(common_props)
    model_ele_list.append_geometry_3d(cuboid_geo)

    return model_ele_list
