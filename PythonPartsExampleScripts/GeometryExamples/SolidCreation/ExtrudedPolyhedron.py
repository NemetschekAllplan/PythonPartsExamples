"""An example script of creating a solid by extruding a flat polygonal 3D profile
along a 3D vector
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

from TypeCollections.ModelEleList import ModelEleList


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


def create_element(build_ele: BuildingElement,
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of extruded polyhedron.

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result with the extruded polyhedron
    """

    # get common properties and construct list of model elements

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create profile to extrude

    polygon = AllplanGeo.Polygon3D(build_ele.ProfilePoints.value)
    polygon += polygon.Points[0]    # close the polygon

    if not polygon.IsValid():
        print("Profile polygon is not valid")
        return CreateElementResult()


    # rotate the profile

    err, profile_plane = polygon.GetPlane()
    profile_normal_vector = profile_plane.Vector if err is AllplanGeo.eOK else AllplanGeo.Vector3D(0,0,1)

    rotation_matrix = AllplanGeo.Matrix3D()
    rotation_matrix.SetRotation(profile_normal_vector,
                                build_ele.ProfileNormalVector.value)
    polygon *= rotation_matrix

    area = AllplanGeo.PolygonalArea3D()
    area += polygon


    # create polyhedron by extruding the profile

    extruded_solid = AllplanGeo.ExtrudedAreaSolid3D()
    extruded_solid.SetDirection(build_ele.ExtrusionDirection.value)
    extruded_solid.SetRefPoint(polygon.StartPoint)
    extruded_solid.SetExtrudedArea(area)

    error_code, polyhedron = AllplanGeo.CreatePolyhedron(extruded_solid)


    # create list of model elements, if extruding was successful

    if error_code is AllplanGeo.eOK:
        model_elements.append_geometry_3d(polyhedron)
    else:
        print("Extrusion failed")

    return CreateElementResult(model_elements)
