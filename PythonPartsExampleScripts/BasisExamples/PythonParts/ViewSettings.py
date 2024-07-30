""" An example script showing creation of a PythonPart with two views. The purpose
of this example is to show possible view settings and how they influence the display
behavior of the PythonPart in different viewports and scales.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from PythonPartViewData import PythonPartViewData

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ViewSettingsBuildingElement import ViewSettingsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement



def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_element(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Function for the element creation

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        created element result
    """

    python_part_util = PythonPartUtil(build_ele.CommonProp.value)

    scale_dict= {"Vx": 1,
                 "Vy": 2,
                 "Vz": 3,
                 }

    # ----------- add the view with cube

    cube_model_ele = create_cuboid(build_ele)

    cube_view_data = PythonPartViewData()

    cube_view_data.start_scale        = build_ele.CubeStartScale.value
    cube_view_data.end_scale          = build_ele.CubeEndScale.value
    cube_view_data.visibility_layer_a = build_ele.CubeVisibilityLayerA.value
    cube_view_data.visibility_layer_b = build_ele.CubeVisibilityLayerB.value
    cube_view_data.visibility_layer_c = build_ele.CubeVisibilityLayerC.value

    # ------------ these visibility settings cannot be controlled yet -------------
    # cube_view_data.ref_pnt1_x         = build_ele.CubeRefPoint1.value.X
    # cube_view_data.ref_pnt1_y         = build_ele.CubeRefPoint1.value.Y
    # cube_view_data.ref_pnt1_z         = build_ele.CubeRefPoint1.value.Z
    # cube_view_data.ref_pnt2_x         = build_ele.CubeRefPoint2.value.X
    # cube_view_data.ref_pnt2_y         = build_ele.CubeRefPoint2.value.Y
    # cube_view_data.ref_pnt2_z         = build_ele.CubeRefPoint2.value.Z
    # cube_view_data.scale_x            = scale_dict.get(build_ele.CubeScaleX.value)
    # cube_view_data.scale_y            = scale_dict.get(build_ele.CubeScaleY.value)
    # cube_view_data.scale_z            = scale_dict.get(build_ele.CubeScaleZ.value)
    # -----------------------------------------------------------------------------

    if build_ele.CubeVisibleIn2D.value and build_ele.CubeVisibleIn3D.value:
        python_part_util.add_pythonpart_view_2d3d(cube_model_ele, cube_view_data) #
    elif build_ele.CubeVisibleIn2D.value:
        python_part_util.add_pythonpart_view_2d(cube_model_ele, cube_view_data)
    elif build_ele.CubeVisibleIn3D.value:
        python_part_util.add_pythonpart_view_3d(cube_model_ele, cube_view_data)


    # ----------- add the view with sphere

    sphere_model_ele = create_sphere(build_ele)

    sphere_view_data = PythonPartViewData()

    sphere_view_data.start_scale        = build_ele.SphereStartScale.value
    sphere_view_data.end_scale          = build_ele.SphereEndScale.value
    sphere_view_data.visibility_layer_a = build_ele.SphereVisibilityLayerA.value
    sphere_view_data.visibility_layer_b = build_ele.SphereVisibilityLayerB.value
    sphere_view_data.visibility_layer_c = build_ele.SphereVisibilityLayerC.value

    # ------------ these visibility settings cannot be controlled yet -------------
    # cube_view_data.ref_pnt1_x         = build_ele.SphereRefPoint1.value.X
    # cube_view_data.ref_pnt1_y         = build_ele.SphereRefPoint1.value.Y
    # cube_view_data.ref_pnt1_z         = build_ele.SphereRefPoint1.value.Z
    # cube_view_data.ref_pnt2_x         = build_ele.SphereRefPoint2.value.X
    # cube_view_data.ref_pnt2_y         = build_ele.SphereRefPoint2.value.Y
    # cube_view_data.ref_pnt2_z         = build_ele.SphereRefPoint2.value.Z
    # cube_view_data.scale_x            = scale_dict.get(build_ele.SphereScaleX.value)
    # cube_view_data.scale_y            = scale_dict.get(build_ele.SphereScaleY.value)
    # cube_view_data.scale_z            = scale_dict.get(build_ele.SphereScaleZ.value)
    # -----------------------------------------------------------------------------

    if build_ele.SphereVisibleIn2D.value and build_ele.SphereVisibleIn3D.value:
        python_part_util.add_pythonpart_view_2d3d(sphere_model_ele, sphere_view_data)
    elif build_ele.SphereVisibleIn2D.value:
        python_part_util.add_pythonpart_view_2d(sphere_model_ele, sphere_view_data)
    elif build_ele.SphereVisibleIn3D.value:
        python_part_util.add_pythonpart_view_3d(sphere_model_ele, sphere_view_data)

    return CreateElementResult(python_part_util.create_pythonpart(build_ele))


def create_cuboid(build_ele: BuildingElement) -> AllplanBasisElements.ModelElement3D:
    """Creates a model element representing a cube with equal x,y,z dimensions specified
    by the user in the property palette

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        Model element representing a cuboid
    """
    cube_geometry  = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(),
                                                          AllplanGeo.Point3D(x= build_ele.Length.value,
                                                                             y= build_ele.Length.value,
                                                                             z= build_ele.Length.value))
    common_props   = AllplanBaseElements.CommonProperties()

    return AllplanBasisElements.ModelElement3D(common_props, cube_geometry)

def create_sphere(build_ele: BuildingElement) -> AllplanBasisElements.ModelElement3D:
    """Creates a model element representing a sphere with radius specified
    by the user in the property palette

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        Model element representing a sphere
    """
    center = AllplanGeo.Point3D(x= build_ele.Length.value / 2,
                                y= build_ele.Length.value / 2,
                                z= build_ele.Length.value / 2)
    sphere_geometry = AllplanGeo.BRep3D.CreateSphere(placement=  AllplanGeo.AxisPlacement3D(center),
                                                     radius=     500)
    common_props   = AllplanBaseElements.CommonProperties()

    return AllplanBasisElements.ModelElement3D(common_props, sphere_geometry)
