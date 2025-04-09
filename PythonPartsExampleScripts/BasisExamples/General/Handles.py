""" Example Script for Handles
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from string import Template

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService

from TypeCollections import ModelEleList

from Utils import RotationUtil
from Utils.HandleCreator import HandleCreator

if TYPE_CHECKING:
    from __BuildingElementStubFiles.HandlesBuildingElement import HandlesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Handles.py')

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

    return Handles(build_ele, script_object_data)


class Handles(BaseScriptObject):
    """ Definition of class self
    """

    MIRROR_CUBOID_KEY = "MirrorCuboid"

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele     = build_ele
        self.mirror_cuboid = False


    def execute(self) -> CreateElementResult:
        """ Create the elements

        Returns:
            created element result
        """

        model_ele_list1, handle_list1 = self.create_cuboid()
        model_ele_list2, handle_list2 = self.create_arc()
        model_ele_list3, handle_list3 = self.create_polygon()
        model_ele_list4, handle_list4 = self.create_lines()
        model_ele_list5, handle_list5 = self.create_rounded_rect()

        return CreateElementResult(model_ele_list1 + model_ele_list2 + model_ele_list3 + model_ele_list4 + model_ele_list5,
                                   handle_list1 + handle_list2 + handle_list3 + handle_list4 + handle_list5)


    def create_cuboid(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a cuboid

        Returns:
            model element
        """

        build_ele = self.build_ele

        point1 = AllplanGeo.Point3D()
        point3 = AllplanGeo.Point3D(-build_ele.Length.value if self.mirror_cuboid else build_ele.Length.value,
                                    build_ele.Thickness.value,
                                    build_ele.Height.value)

        cube = AllplanGeo.Polyhedron3D.CreateCuboid(point1, point3)

        rot_angle = AllplanGeo.Vector2D(build_ele.SlopeX.value, build_ele.SlopeY.value).GetAngle()

        rot_mat = AllplanGeo.Matrix3D()
        rot_mat.SetRotation(AllplanGeo.Line3D(0, 0, 0, 0, 0, 1000), rot_angle)
        rot_mat.Translate(AllplanGeo.Vector3D(build_ele.OffsetPoint.value))

        cube = AllplanGeo.Transform(cube, rot_mat)

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(cube)


        #----------------- create the handles

        point3.Z = 0
        point2   = AllplanGeo.Point3D(-build_ele.Length.value if self.mirror_cuboid else build_ele.Length.value, 0, 0)
        point5   = AllplanGeo.Point3D(0, build_ele.Thickness.value / 2, 0)

        point1 = AllplanGeo.Transform(point1, rot_mat)
        point3 = AllplanGeo.Transform(point3, rot_mat)
        point2 = AllplanGeo.Transform(point2, rot_mat)
        point5 = AllplanGeo.Transform(point5, rot_mat)

        point4_bottom = AllplanGeo.Point3D(0, build_ele.Thickness.value, 0)
        point4_top    = AllplanGeo.Point3D(0, build_ele.Thickness.value, build_ele.Height.value)
        point4_bottom = AllplanGeo.Transform(point4_bottom, rot_mat)
        point4_top    = AllplanGeo.Transform(point4_top, rot_mat)


        #-----------------  mirror handle

        handle_list = list[HandleProperties]()

        HandleCreator.click(handle_list, self.MIRROR_CUBOID_KEY, point5, AllplanIFW.ElementHandleType.HANDLE_ARROW,
                            "Mirror the cuboid", rot_angle)


        #----------------- checkbox handle for input controls

        HandleCreator.checkbox(handle_list, "ShowInputControls", point1 + AllplanGeo.Point3D(0, -500, 0),
                               build_ele.ShowInputControls.value, "Hide input controls", "Show input controls")


        #----------------- checkbox handle for show handles

        HandleCreator.checkbox(handle_list, "ShowHandles", point1 + AllplanGeo.Point3D(0, -800, 0),
                               build_ele.ShowHandles.value, "Hide handles", "Show handles")


        #----------------- increment and decrement handle

        HandleCreator.increment(handle_list, "Thickness", point3 + AllplanGeo.Point3D(0, 200, 0), 100,
                                "Increment thickness by 0.1m")

        HandleCreator.decrement(handle_list, "Thickness", point3 + AllplanGeo.Point3D(0, -200, 0), 100,
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

        HandleCreator.point_distance(handle_list, "Thickness", point3, point2, show_input_controls, True, show_handles,
                                     info_text = "Thickness handle")

        HandleCreator.point_distance(handle_list, "Height", point4_top, point4_bottom, show_input_controls, True, show_handles,
                                     info_text="Height handle")

        return model_ele_list, handle_list


    def create_arc(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a cuboid

        Returns:
            model elements, handles
        """

        build_ele      = self.build_ele
        model_ele_list = ModelEleList()
        handle_list    = list[HandleProperties]()
        delta_angle    = AllplanGeo.Angle.DegToRad(build_ele.DeltaAngle.value)
        center_pnt     = AllplanGeo.Point3D(1000, build_ele.Length.value, 0)

        angle_placement = AllplanGeo.AxisPlacement3D(center_pnt, AllplanGeo.Vector3D(1000, 0, 0),
                                                     AllplanGeo.Vector3D(0, 0, 1000))


        #----------------- get the arc angles

        if build_ele.XPlacement.value == 1 and build_ele.YPlacement.value == 1:
            angle_start  = 0
            angle_end    = angle_start + delta_angle
            handle_angle = angle_end

        elif build_ele.XPlacement.value == -1 and build_ele.YPlacement.value == 1:
            angle_start  = math.pi - delta_angle
            angle_end    = math.pi
            handle_angle = angle_start

            angle_placement = AllplanGeo.AxisPlacement3D(center_pnt, AllplanGeo.Vector3D(-1000, 0, 0),
                                                         AllplanGeo.Vector3D(0, 0, -1000))

        elif build_ele.XPlacement.value == -1 and build_ele.YPlacement.value == -1:
            angle_start  = math.pi
            angle_end    = angle_start + delta_angle
            handle_angle = angle_end

            angle_placement = AllplanGeo.AxisPlacement3D(center_pnt, AllplanGeo.Vector3D(-1000, 0, 0),
                                                         AllplanGeo.Vector3D(0, 0, 1000))

        else:
            angle_start  = math.pi * 2 - delta_angle
            angle_end    = math.pi * 2
            handle_angle = angle_start

            angle_placement = AllplanGeo.AxisPlacement3D(center_pnt, AllplanGeo.Vector3D(1000, 0, 0),
                                                         AllplanGeo.Vector3D(0, 0, -1000))

        radius = 1000

        opening_handle_pnt = AllplanGeo.Point3D(radius * math.cos(handle_angle), radius * math.sin(handle_angle), 0)

        model_ele_list.append_geometry_3d(AllplanGeo.Arc3D(center_pnt, radius, radius, angle_start, angle_end - angle_start))
        model_ele_list.append_geometry_3d(AllplanGeo.Line3D(center_pnt, center_pnt + opening_handle_pnt))


        #----------------- create the handles

        handle_pnt = opening_handle_pnt / 2

        HandleCreator.vector_distances(handle_list, ["XPlacement", "YPlacement"], center_pnt + handle_pnt, center_pnt,
                                       [AllplanGeo.Vector3D(1000, 0, 0), AllplanGeo.Vector3D(0, 1000, 0)],
                                       [False, False], [False, False],
                                       info_text = "Placement handle")

        HandleCreator.angle(handle_list, "DeltaAngle", center_pnt + opening_handle_pnt, center_pnt,
                            angle_placement, center_pnt, info_text = "Delta angle handle")

        return model_ele_list, handle_list


    def create_polygon(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a polygon

        Returns:
            model elements, handles
       """

        #----------------- create a polygon

        build_ele = self.build_ele

        poly_points = build_ele.PolyPoints.value

        poly = AllplanGeo.Polygon3D(poly_points)

        poly += poly.StartPoint

        _, rot_pnt_z = AllplanGeo.CenterCalculus.Calculate(poly, True, 0)
        rot_pnt_y    = rot_pnt_z + AllplanGeo.Vector3D(0, -500, 0)

        poly = AllplanGeo.Transform(poly, RotationUtil(0, 0, build_ele.RotAngleZ.value).get_rotation_matrix(rot_pnt_z))
        poly = AllplanGeo.Transform(poly, RotationUtil(0, -build_ele.RotAngleY.value, 0).get_rotation_matrix(rot_pnt_y))

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(poly)


        #----------------- point list handles

        poly_points = poly.Points
        handle_list = list[HandleProperties]()

        HandleCreator.point_list(handle_list, "PolyPoints", poly_points[:-1],
                                 info_text_template = Template("Shift + click = delete point\nIndex=$index"),
                                 delete_point = True)
        HandleCreator.point_list_segment_center(handle_list, "PolyPoints", poly_points,
                                                info_text_template = Template("Split segment $index"), index_offset = 1)

        if not poly.IsValid():
            return model_ele_list, handle_list


        #----------------- rotation handles

        HandleCreator.angle(handle_list, "RotAngleZ", rot_pnt_z, rot_pnt_z + AllplanGeo.Vector3D(1000, 0, 0),
                            AllplanGeo.AxisPlacement3D(AllplanGeo.Axis3D(rot_pnt_z, poly.GetPlane()[1].GetVector()),
                                                       rot_pnt_z + AllplanGeo.Vector3D(1000, 0, 0)),
                            info_text = "Z rotation handle")

        HandleCreator.angle(handle_list, "RotAngleY", rot_pnt_y, rot_pnt_y + AllplanGeo.Vector3D(0, 1000, 0),
                            AllplanGeo.AxisPlacement3D(rot_pnt_y, AllplanGeo.Vector3D(1000, 0, 0),
                                                       AllplanGeo.Vector3D(0, -1000, 0)),
                            info_text = "Y rotation handle")

        return model_ele_list, handle_list


    def create_lines(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create lines by distance

        Returns:
            model elements, handles
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList()

        ref_pnt = AllplanGeo.Point3D(build_ele.Length.value * 1.2, 0, 0)

        def add_line(start_pnt: AllplanGeo.Point3D):
            """ add a line to the model element list

            Args:
                start_pnt: start point
            """

            line = AllplanGeo.Line3D(start_pnt, start_pnt + AllplanGeo.Point3D(0, 2000, 0))

            model_ele_list.append_geometry_3d(line)

        add_line(ref_pnt)

        start_pnt = ref_pnt

        for dist in build_ele.DistanceList.value:
            start_pnt = start_pnt + AllplanGeo.Point3D(dist, 0, 0)

            add_line(start_pnt)


        #----------------- create the handles

        handle_list = list[HandleProperties]()
        start_pnt   = ref_pnt

        for index, dist in enumerate(build_ele.DistanceList.value):
            HandleCreator.x_distance(handle_list, "DistanceList", start_pnt + AllplanGeo.Point3D(dist, 0, 0),
                                     AllplanGeo.Point3D(start_pnt), True, False,
                                     list_index = index, info_text = f"Index={index}",
                                     show_input_field_always = True)

            start_pnt += AllplanGeo.Point3D(dist, 0, 0)

        return model_ele_list, handle_list


    def create_rounded_rect(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a rounded rectangle

        Returns:
            model elements, handles
        """

        build_ele = self.build_ele

        reft_pnt = AllplanGeo.Point2D(4000, build_ele.Length.value)

        line_length = build_ele.RectLength.value - build_ele.RectThickness.value / 2

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(reft_pnt, reft_pnt + AllplanGeo.Vector2D(line_length, 0)))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(reft_pnt, reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value)))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value),
                                                            reft_pnt + AllplanGeo.Vector2D(line_length, build_ele.RectThickness.value)))
        model_ele_list.append_geometry_2d(AllplanGeo.Arc2D(reft_pnt + AllplanGeo.Vector2D(line_length, build_ele.RectThickness.value / 2),
                                                           build_ele.RectThickness.value / 2,
                                                           build_ele.RectThickness.value / 2, 0, math.pi * 1.5,  math.pi * 2.5))

        handle_list = list[HandleProperties]()

        HandleCreator.x_distance(handle_list, "RectLength",
                                 (reft_pnt + AllplanGeo.Vector2D(build_ele.RectLength.value, build_ele.RectThickness.value / 2)).To3D,
                                 (reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value / 2)).To3D, True, False,
                                 info_text = "Thickness handle")

        HandleCreator.y_distance(handle_list, "RectThickness", (reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value)).To3D,
                                 reft_pnt.To3D, True, False, info_text = "Thickness handle")

        return model_ele_list, handle_list


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
