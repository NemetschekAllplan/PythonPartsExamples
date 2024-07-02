"""Example script of creating a simple cone as brep or as polyhedron
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
    """ Creation of cone

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    # get common properties

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # create a cone

    cone = AllplanGeo.Cone3D(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(),
                                                        build_ele.LocalXVector.value,
                                                        build_ele.LocalZVector.value),
                             build_ele.MajorRadius.value,
                             build_ele.MinorRadius.value,
                             build_ele.Apex.value)

    cone_as_brep = AllplanGeo.BRep3D.CreateCone(cone,
                                                build_ele.Closed.value)


    # if the cone is to be a BRep, it can be appended to model element list at this point

    if build_ele.CreateAs.value == 0:
        model_elements.append_geometry_3d(cone_as_brep)


    # if the cone is to be a polyhedron, a tesselation needs to be introduced

    elif build_ele.CreateAs.value == 1:
        tesselation_settings = AllplanGeo.ApproximationSettings(AllplanGeo.eApproximationSettingsType.ASET_BREP_TESSELATION)

        tesselation_settings.SetBRepTesselation(build_ele.TessellationDensity.value,
                                                AllplanGeo.Angle.FromDeg(build_ele.TessellationMaxAngle.value),
                                                build_ele.TessellationMinLength.value,
                                                build_ele.TessellationMaxLength.value)

        error_code , cone_as_polyhedron = AllplanGeo.CreatePolyhedron(cone_as_brep, tesselation_settings)

        if error_code is AllplanGeo.eOK:
            model_elements.append_geometry_3d(cone_as_polyhedron)
        else:
            print("Tessellation failed")

    return CreateElementResult(model_elements)
