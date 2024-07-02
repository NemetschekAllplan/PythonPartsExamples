"""An example script of creating a brep by rail sweeping of three profiles: square,
another square (rotated) and a circle, all arranged in XY plane in a defined distance
to each other
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult

from TypeCollections.ModelEleList import ModelEleList
from TypeCollections.Curve3DList import Curve3DList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.RailSweptBRepBuildingElement import RailSweptBRepBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties

    Returns:
        True
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the rail swept solid

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result with rail swept brep and optionally curves representing
        swept profiles and/or rails
    """

    # get common properties and construct list of model elements

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create profiles and rails

    profiles, rails = create_profiles_and_rails(bottom_square_side=     build_ele.BottomSquareSide.value,
                                                middle_square_side=     build_ele.MiddleSquareSide.value,
                                                middle_square_rotation= AllplanGeo.Angle.FromDeg(build_ele.MiddleSquareRotation.value),
                                                top_circle_radius=      build_ele.TopCircleRadius.value,
                                                distance=               build_ele.Distance.value)


    # create curves representing profiles and/or rails if corresponding option is selected

    if build_ele.CreateProfileCurves.value:
        for curve in profiles:
            model_elements.append_geometry_3d(curve)

    if build_ele.CreateRailCurves.value:
        for curve in rails:
            model_elements.append_geometry_3d(curve)


    # create rail swept brep

    error_code, rail_swept_brep = AllplanGeo.CreateRailSweptBRep3D(profiles=       profiles,
                                                                   rails=          rails,
                                                                   closecaps=      build_ele.CloseCaps.value,
                                                                   uniformScaling= build_ele.UniformScaling.value,
                                                                   railrotation=   build_ele.RailRotation.value)


    # create list of model elements, if sweeping was successful

    if error_code is AllplanGeo.eOK:
        model_elements.append_geometry_3d(rail_swept_brep)
    return CreateElementResult(model_elements)


def create_profiles_and_rails(bottom_square_side: float,
                              middle_square_side: float,
                              middle_square_rotation: AllplanGeo.Angle,
                              top_circle_radius: float,
                              distance: float) -> tuple[Curve3DList, Curve3DList]:
    """Create two lists. One with profiles containing: square at the bottom, square in the middle rotated
    by 45° and a circle at the top. All the profiles arranged above each other, separated with the same distance.
    Second list contains rails connecting all three profiles to be used later for rail sweep.

    Args:
        bottom_square_side:     size of the bottom square
        middle_square_side:     size of the middle, rotated square
        middle_square_rotation: rotation of the middle square around the Z axis
        top_circle_radius:      radius of the circle at the top
        distance:               distance between the profiles

    Returns:
        list with the three profiles
        list with four rails connecting the profiles
    """

    profiles = Curve3DList()


    # create bottom square

    bottom_square_2d = AllplanGeo.Polygon2D.CreateRectangle(leftBottom= AllplanGeo.Point2D(-bottom_square_side/2,-bottom_square_side/2),
                                                            rightTop=   AllplanGeo.Point2D( bottom_square_side/2, bottom_square_side/2))

    bottom_square = AllplanGeo.Polyline3D([AllplanGeo.Point3D(point) for point in bottom_square_2d.Points])

    profiles.append(bottom_square)


    # create middle square

    middle_square_2d = AllplanGeo.Polygon2D.CreateRectangle(leftBottom= AllplanGeo.Point2D(-middle_square_side/2,-middle_square_side/2),
                                                            rightTop=   AllplanGeo.Point2D( middle_square_side/2, middle_square_side/2))

    middle_square = AllplanGeo.Polyline3D([AllplanGeo.Point3D(point) for point in middle_square_2d.Points])


    # create transformation matrix to describe rotation and translation in positive Z direction

    transformation_matrix = AllplanGeo.Matrix3D()
    transformation_matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(),
                                                     AllplanGeo.Point3D(0,0,1)),
                                   middle_square_rotation)
    transformation_matrix.Translate(AllplanGeo.Vector3D(0, 0, distance))

    middle_square = middle_square * transformation_matrix

    profiles.append(middle_square)


    # create top circle

    top_circle = AllplanGeo.Arc3D(center=        AllplanGeo.Point3D(0, 0, distance * 2),
                                  xDir=          AllplanGeo.Vector3D(1,0,0),
                                  normVector=    AllplanGeo.Vector3D(0,0,1),
                                  minor=         top_circle_radius,
                                  major=         top_circle_radius,
                                  startAngle=    0,
                                  deltaAngle=    2 * math.pi)

    profiles.append(top_circle)


    # create rails

    rails = Curve3DList()

    angle_list = [AllplanGeo.Angle.FromDeg(angle) for angle in (0, 90, 180, 270)]

    points_on_arc = [top_circle.GetPoint(angle) for angle in angle_list]


    # each rail begins in the edge of the bottom square, goes through the corresponding
    # edge of the middle square and ends up on the quarter point of the top circle

    for i, point_on_arc in enumerate(points_on_arc):
        rail = AllplanGeo.Spline3D([bottom_square.Points[i],
                                    middle_square.Points[i],
                                    point_on_arc])
        rails.append(rail)

    return profiles, rails
