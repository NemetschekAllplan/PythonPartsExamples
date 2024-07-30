"""An example script of creating a brep by lofting through a set of circular and square profiles
"""

import typing

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

from TypeCollections.Curve3DList import Curve3DList
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
                   _doc     : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a polyhedron by sweeping a two-dimensional polygonal profile vertically and clipping it from
    the bottom and from the top by planes

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result with lofted breps and optionally the profile curves
    """

    # get common properties and construct list of model elements

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create curves of the profiles to loft

    profiles = create_profiles(radius=      build_ele.Radius.value,
                               square_side= build_ele.SquareSide.value)


    # if the option is selected, create model elements representing the curves

    if build_ele.CreateProfileCurves.value:
        for profile in profiles:
            model_elements.append_geometry_3d(profile)

    #------ create lofted BRep

    error_code, lofted_brep = AllplanGeo.CreateLoftedBRep3D(profiles,
                                                            Curve3DList(),
                                                            build_ele.CloseCaps.value,
                                                            build_ele.CreateProfileEdges.value,
                                                            build_ele.Linear.value,
                                                            build_ele.Periodic.value)

    if error_code is AllplanGeo.eOK:
        model_elements.append_geometry_3d(lofted_brep)
    else:
        print("Lofting failed")

    return CreateElementResult(model_elements)



def create_profiles(radius: float, square_side: float) -> Curve3DList:
    """Create a profile list containing 8 profiles: four squares and four circles. All profiles
    are perpendicular to the XY plane and arranged alternately 45° from each other by copying
    and rotating around the origin of the coordinate system.

    Args:
        radius:      radius of the circular profile
        square_side: side of the square profile

    Returns:
        list with the profile curves
    """

    y_axis = AllplanGeo.Line3D(point1=  AllplanGeo.Point3D(),
                               point2=  AllplanGeo.Point3D(0,1,0))
    z_axis = AllplanGeo.Line3D(point1=  AllplanGeo.Point3D(),
                               point2=  AllplanGeo.Point3D(0,0,1))


    # create square profile

    rectangle_2d = AllplanGeo.Polygon2D.CreateRectangle(AllplanGeo.Point2D(-square_side/2,-square_side/2),
                                                        AllplanGeo.Point2D( square_side/2, square_side/2))

    rectangle_3d = AllplanGeo.Polyline3D([AllplanGeo.Point3D(point) for point in rectangle_2d.Points])

    transformation_matrix = AllplanGeo.Matrix3D()
    transformation_matrix.Rotation(z_axis, AllplanGeo.Angle.FromDeg(90))
    transformation_matrix.Rotation(y_axis, AllplanGeo.Angle.FromDeg(90))
    transformation_matrix.Translate(AllplanGeo.Vector3D(0,2000,0))
    transformation_matrix.Rotation(z_axis, AllplanGeo.Angle.FromDeg(45))

    rectangle_3d *= transformation_matrix


    # create circular profile

    circle_3d = AllplanGeo.Arc3D(center=    AllplanGeo.Point3D(),
                                 major=     radius,
                                 minor=     radius,
                                 startAngle=0,
                                 deltaAngle=float(AllplanGeo.Angle.FromDeg(360)))

    transformation_matrix.SetIdentity()
    transformation_matrix.Rotation(z_axis, AllplanGeo.Angle.FromDeg(-45))
    transformation_matrix.Rotation(y_axis, AllplanGeo.Angle.FromDeg(90))
    transformation_matrix.Translate(AllplanGeo.Vector3D(0,2000,0))

    circle_3d = AllplanGeo.Transform(circle_3d, transformation_matrix)


    # copy and rotate both square and circle  around center point by 90° four times
    # to get 8 curves in total

    profiles = []

    transformation_matrix.SetIdentity()
    transformation_matrix.SetRotation(z_axis, AllplanGeo.Angle.FromDeg(-90))

    for _ in range(0,4):
        profiles.append(AllplanGeo.Polyline3D(rectangle_3d))
        rectangle_3d = AllplanGeo.Transform(rectangle_3d, transformation_matrix)

        profiles.append(AllplanGeo.Arc3D(circle_3d))
        circle_3d = AllplanGeo.Transform(circle_3d, transformation_matrix)

    return profiles
