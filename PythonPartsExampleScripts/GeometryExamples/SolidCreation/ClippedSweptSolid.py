"""Example script of creating a solid as a result of vertical extrusion
of a 2D polygonal profile, bounded from the bottom and the top by a 3D plane
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo

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


def create_element(build_ele, _) -> CreateElementResult:
    """Create a polyhedron by sweeping a two-dimensional polygonal profile vertically and clipping it from
    the bottom and from the top by planes
    """

    # get common properties and create a model element list

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create profile

    polygon = AllplanGeo.Polygon2D(build_ele.ProfilePoints.value)
    polygon += polygon.Points[0]    # close the polygon

    if not polygon.IsValid():
        print("Profile polygon is not valid")
        return CreateElementResult()

    area = AllplanGeo.PolygonalArea2D()
    area += polygon


    # define clipping top and bottom planes

    top_plane = AllplanGeo.Plane3D(build_ele.TopPlaneReferencePoint.value,
                                   build_ele.TopPlaneDirectionVector.value)

    bottom_plane = AllplanGeo.Plane3D(build_ele.BottomPlaneReferencePoint.value,
                                      build_ele.BottomPlaneDirectionVector.value)


    # create the clipped swept solid

    swept_solid = AllplanGeo.ClippedSweptSolid3D(area,
                                                 bottom_plane,
                                                 top_plane)

    error_code, polyhedron = AllplanGeo.CreatePolyhedron(swept_solid)

    if error_code is AllplanGeo.eOK:
        model_elements.append_geometry_3d(polyhedron)

    else:
        print("Solid creation failed")

    return CreateElementResult(model_elements)
