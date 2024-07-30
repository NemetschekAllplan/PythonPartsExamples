"""Example script of creating a simple cylinder as brep or as polyhedron
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from ControlPropertiesUtil import ControlPropertiesUtil
from BuildingElement import BuildingElement

from TypeCollections.ModelEleList import ModelEleList

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def modify_control_properties(build_ele     : BuildingElement,
                              _ctrl_prop_util: ControlPropertiesUtil,
                              value_name    : str,
                              _event_id      : int,
                              _doc           : AllplanEleAdapter.DocumentAdapter) -> bool:
    """Called after each change within the property palette

    Args:
        build_ele:      building element
        _ctrl_prop_util: control properties utility
        value_name:     name(s) of the modified value (multiple names are separated by ,)
        _event_id:       event ID
        _doc:            document

    Returns:
        True if an update of the property palette is necessary, False otherwise
    """

    # when major and minor radiuses differs, creating the cylinder is possible only as polyhedron

    if value_name in ["MajorRadius", "MinorRadius"] and not build_ele.MinorRadius.value == build_ele.MajorRadius.value:
        build_ele.CreateAs.value = 1
        return True

    # when the cylinder is oblique (apex not on Z axis), creating the cylinder is possible only as polyhedron

    elif value_name in ["Apex.X", "Apex.Y"] and (build_ele.Apex.value.X != 0 or build_ele.Apex.value.Y != 0) :
        build_ele.CreateAs.value = 1
        return True
    return False


def create_element(build_ele: BuildingElement,
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of cylinder

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    #------ get common properties

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    #------ create a cylinder

    cylinder = AllplanGeo.Cylinder3D(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(),
                                                                build_ele.LocalXVector.value,
                                                                build_ele.LocalZVector.value),
                                     build_ele.MajorRadius.value,
                                     build_ele.MinorRadius.value,
                                     build_ele.Apex.value)

    #if the cylinder should be a BRep, we can just append it to the list of model elements

    if build_ele.CreateAs.value == 0:
        model_elements.append_geometry_3d(cylinder)

    #if the cylinder should be created as a polyhedron, the tessellation must be performed

    elif build_ele.CreateAs.value == 1:
        error_code, polyhedron = AllplanGeo.CreatePolyhedron(cylinder, build_ele.CountOfSegments.value)

        if error_code == AllplanGeo.eOK:
            model_elements.append_geometry_3d(polyhedron)
        else:
            print("Tessellation failed")

    return CreateElementResult(model_elements)
