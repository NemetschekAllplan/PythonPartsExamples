""" Script for the use of global handles. The handles are defined by global coordinates,
    which needs to transform local coordinates before the handle creation.

    The source code can be simplified by using local handles with a transformation matrix.
    This solution is shown in the example LocalHandles.py.
"""

from __future__ import annotations

import math

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService

from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils.HandleCreator import HandleCreator
from Utils.Geometry.ExtrudeByVectorUtil import ExtrudeByVectorUtil

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GlobalHandlesBuildingElement import GlobalHandlesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load GlobalHandles.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return GlobalHandles(build_ele, script_object_data)


class GlobalHandles(BaseScriptObject):
    """ Definition of class GlobalHandles
    """

    MIRROR_CUBOID_KEY = "MirrorCuboid"

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele

        self.mirror_cuboid = False


    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele


        #---------------- create the polyhedron by local coordinates

        point1     = AllplanGeo.Point3D()
        point2     = AllplanGeo.Point3D(build_ele.Length.value, 0, 0)
        point3     = AllplanGeo.Point3D(build_ele.Length.value + build_ele.Offset.value, build_ele.Thickness.value, 0)
        point3_top = AllplanGeo.Point3D(build_ele.Length.value + build_ele.Offset.value, build_ele.Thickness.value, build_ele.Height.value)
        point4     = AllplanGeo.Point3D(0, build_ele.Thickness.value, 0)
        point5     = AllplanGeo.Point3D(0, build_ele.Thickness.value / 2, 0)

        base_poly = AllplanGeo.Polyline3D([point1, point2, point3, point4, point1])

        if (polyhed := ExtrudeByVectorUtil.extrude([base_poly], AllplanGeo.Vector3D(0, 0, build_ele.Height.value), False, True)) is None:
            return CreateElementResult()


        #----------------- create the transformation matrix

        rot_angle = AllplanGeo.Vector2D(build_ele.SlopeX.value, build_ele.SlopeY.value).GetAngle()

        rot_mat = AllplanGeo.Matrix3D()

        if self.mirror_cuboid:
            rot_mat.Scaling(-1, 1, 1)

        rot_mat.Rotation(AllplanGeo.Line3D(0, 0, 0, 0, 0, 1000), rot_angle)
        rot_mat.Translate(AllplanGeo.Vector3D(build_ele.OffsetPoint.value))


        #----------------- transform the polyhedron and add it to the model element list

        cube = AllplanGeo.Transform(polyhed, rot_mat)

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(cube)


        #----------------- create the handles

        point1     = point1 * rot_mat
        point2     = point2 * rot_mat
        point3     = point3 * rot_mat
        point4     = point4 * rot_mat
        point5     = point5 * rot_mat
        point3_top = point3_top * rot_mat


        #-----------------  mirror handle

        handle_list = HandleList()

        HandleCreator.click(handle_list, self.MIRROR_CUBOID_KEY, point5, AllplanIFW.ElementHandleType.HANDLE_ARROW,
                            "Mirror the cuboid", rot_angle)


        #----------------- checkbox handle for input controls

        HandleCreator.checkbox(handle_list, "ShowInputControls", point1 + AllplanGeo.Point3D(0, -500, 0),
                               build_ele.ShowInputControls.value, "Hide input controls", "Show input controls")


        #----------------- checkbox handle for show handles

        HandleCreator.checkbox(handle_list, "ShowHandles", point1 + AllplanGeo.Point3D(0, -800, 0),
                               build_ele.ShowHandles.value, "Hide handles", "Show handles")


        #----------------- increment and decrement handle

        HandleCreator.increment(handle_list, "Thickness", point3 + AllplanGeo.Point3D(0, 500, 0) * rot_mat, 100,
                                "Increment thickness by 0.1m")

        HandleCreator.decrement(handle_list, "Thickness", point3 + AllplanGeo.Point3D(0, -500, 0) * rot_mat, 100,
                                "Decrement thickness by 0.1m")

        handle_list[-1].handle_angle = AllplanGeo.Angle(math.pi)


        #-----------------  offset point handle

        HandleCreator.move(handle_list, "OffsetPoint", build_ele.OffsetPoint.value, "Offset the cuboid")


        #----------------- slope handle


        show_input_controls = build_ele.ShowInputControls.value
        show_handles        = build_ele.ShowHandles.value

        HandleCreator.xy_distance(handle_list, "SlopeX", "SlopeY",
                                  point1 + AllplanGeo.Point3D(build_ele.SlopeX.value, build_ele.SlopeY.value, 0), point1,
                                  show_input_controls, show_handles = show_handles)

        handle_list[-1].info_text = "Slope handle"


        #----------------- dimension handles

        HandleCreator.point_distance(handle_list, "Length", point2, point1, show_input_controls, False, show_handles,
                                     info_text = "Length handle")

        HandleCreator.point_distance(handle_list, "Thickness", point4, point1, show_input_controls, True, show_handles,
                                     info_text = "Thickness handle")

        HandleCreator.point_distance(handle_list, "Height", point3_top, point3, show_input_controls, True, show_handles,
                                     info_text="Height handle")

        HandleCreator.vector_distance(handle_list, "Offset", point3, point2, AllplanGeo.Vector3D(point1, point2),
                                      show_input_controls, False, show_handles,
                                      info_text="Offset handle")

        return CreateElementResult(model_ele_list, handle_list)


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        build_ele = self.build_ele

        if handle_prop.handle_id == self.MIRROR_CUBOID_KEY:
            self.mirror_cuboid = not self.mirror_cuboid

        else:
            HandlePropertiesService.update_property_value(build_ele, handle_prop, input_pnt)
