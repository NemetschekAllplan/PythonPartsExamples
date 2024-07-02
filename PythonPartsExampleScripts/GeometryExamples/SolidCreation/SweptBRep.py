"""Example script of creating a brep by sweeping a flat profile along path
"""
import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from PreviewSymbols import PreviewSymbols
from Utils import TextReferencePointPosition

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
    """ Creation of the brep

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    # get common properties and construct list of model elements

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)
    preview_symbols = PreviewSymbols()


    # create profile

    profile = AllplanGeo.Arc3D(center=      AllplanGeo.Point3D(),
                               minor=       build_ele.MinorRadius.value,
                               major=       build_ele.MajorRadius.value,
                               startAngle=  0,
                               deltaAngle=  2 * math.pi)


    # create the profile 3D circle in the model if the option is selected

    if build_ele.CreateProfileCurve.value:
        model_elements.append_geometry_3d(profile)


    # create path

    path = AllplanGeo.Spline3D(build_ele.PathPoints.value)


    # show helping preview symbols for the path points: a cross and a point index

    for i, point in enumerate(path.Points):
        preview_symbols.add_text(text=              str(i),
                                 reference_point=   point + AllplanGeo.Point3D(80,0,0),
                                 ref_pnt_pos=       TextReferencePointPosition.TOP_LEFT,
                                 height=            25.0,
                                 color=             6,
                                 rotation_angle=    AllplanGeo.Angle())

        preview_symbols.add_cross(reference_point=  point,
                                  width=            25,
                                  color=            6)


    # create the path spline in the model if the option is selected

    if build_ele.CreatePathCurve.value:
        model_elements.append_geometry_3d(path)


    # create swept BRep

    error_code, swept_brep = AllplanGeo.CreateSweptBRep3D([profile],
                                                          path,
                                                          build_ele.CloseCaps.value,
                                                          AllplanGeo.SweepRotationType.names[build_ele.RailRotationType.value])


    #-------- create list of model elements, if sweeping was successful

    if error_code is AllplanGeo.eOK:
        model_elements.append_geometry_3d(swept_brep)
    else:
        print("Sweeping failed")

    return CreateElementResult(elements=        model_elements,
                               preview_symbols= preview_symbols)
