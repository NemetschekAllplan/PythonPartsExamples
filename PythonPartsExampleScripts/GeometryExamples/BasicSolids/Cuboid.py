"""Example script of creating a simple cuboid as brep or as polyhedron
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

from TypeCollections.ModelEleList import ModelEleList


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   str) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True

def create_element(build_ele:   BuildingElement,
                   _doc:        AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of the cuboid

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    # get common properties

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create cuboid as BRep

    if build_ele.CreateAs.value == 0:
        cuboid = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(),
                                                                           build_ele.LocalXVector.value,
                                                                           build_ele.LocalZVector.value),
                                                build_ele.CuboidLength.value,
                                                build_ele.CuboidWidth.value,
                                                build_ele.CuboidHeight.value)


    # create cuboid as polyhedron

    else:
        cuboid = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(),
                                                                                 build_ele.LocalXVector.value,
                                                                                 build_ele.LocalZVector.value),
                                                      build_ele.CuboidLength.value,
                                                      build_ele.CuboidWidth.value,
                                                      build_ele.CuboidHeight.value)


    model_elements.append_geometry_3d(cuboid)

    return CreateElementResult(model_elements)

