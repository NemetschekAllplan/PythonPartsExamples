"""Example script of creating a brep by revolving a flat profile
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
    """Creation of the revolved brep

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result containing revolved brep
    """

    # get common properties and construct list of model elements

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create profile

    profile = Curve3DList()

    spline = AllplanGeo.Spline3D()

    spline.Points = build_ele.ProfilePoints.value

    profile.append(spline)

    profile.append(AllplanGeo.Line3D(spline.EndPoint, spline.StartPoint))


    # if the option is selected, create model elements representing the profile curves

    if build_ele.CreateProfileCurves.value:
        model_elements.append_geometry_3d(profile)


    # create revolve axis

    y_axis = AllplanGeo.Axis3D(AllplanGeo.Point3D(),
                               AllplanGeo.Vector3D(0,1,0))


    # create revolved BRep

    error_code, revolved_brep = AllplanGeo.CreateRevolvedBRep3D(profiles=           profile,
                                                                axis=               y_axis,
                                                                rotationAngle=      AllplanGeo.Angle.FromDeg(build_ele.RevolveAngle.value),
                                                                closecaps=          build_ele.CloseCaps.value,
                                                                numprofiles=        build_ele.NumProfiles.value)


    if error_code == AllplanGeo.eOK:
        model_elements.append_geometry_3d(revolved_brep)
    else:
        print("Revolving failed")

    return CreateElementResult(model_elements)
