"""Example script of creating a polyhedron by sweeping a flat, polygonal
profile along a polygonal path
"""

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
    """Creation of the polyhedron

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

    profile = AllplanGeo.Polyline3D(build_ele.ProfilePoints.value)
    profile += profile.Points[0]

    if not AllplanGeo.IsCoplanar(profile.Points)[0]:
        print("Profile points are not coplanar")

    profiles = AllplanGeo.Polyline3DList()
    profiles.append(profile)


    # create path

    path = AllplanGeo.Polyline3D(build_ele.PathPoints.value)

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


    # sweep polyhedron

    error_code, swept_polyhedron = AllplanGeo.CreateSweptPolyhedron3D( profiles=      profiles,
                                                                       path=          path,
                                                                       closecaps=     build_ele.CloseCaps.value,
                                                                       railrotation=  build_ele.RailRotation.value,
                                                                       rotAxis=       build_ele.RotationAxis.value)

    if error_code == AllplanGeo.eOK:
        model_elements.append_geometry_3d(swept_polyhedron)
    else:
        print("Sweeping failed")

    return CreateElementResult(elements=        model_elements,
                               preview_symbols= preview_symbols)
