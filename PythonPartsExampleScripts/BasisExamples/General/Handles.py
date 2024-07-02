""" Example Script for Handles
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_BasisElements as AllplanBasisEle

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService
from Utils import RotationUtil

from TypeCollections import ModelEleList

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


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return Handles(build_ele, coord_input)


class Handles(BaseScriptObject):
    """ Definition of class self
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ Create the elements

        Returns:
            created element result
        """

        model_ele_list1, handle_list1 = self.create_cuboid()
        model_ele_list2, handle_list2 = self.create_arc()
        model_ele_list3, handle_list3 = self.create_polygon()
        model_ele_list4, handle_list4 = self.create_lines()

        return CreateElementResult(model_ele_list1 + model_ele_list2 + model_ele_list3 + model_ele_list4,
                                   handle_list1 + handle_list2 + handle_list3 + handle_list4)


    def create_cuboid(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a cuboid

        Returns:
            model element
        """

        build_ele = self.build_ele

        point1 = AllplanGeo.Point3D()
        point3 = AllplanGeo.Point3D(-build_ele.Length.value if build_ele.MirrorCuboid.value else build_ele.Length.value,
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
        point2   = AllplanGeo.Point3D(-build_ele.Length.value if build_ele.MirrorCuboid.value else build_ele.Length.value, 0, 0)
        point5   = AllplanGeo.Point3D(0, build_ele.Thickness.value / 2, 0)

        point1 = AllplanGeo.Transform(point1, rot_mat)
        point3 = AllplanGeo.Transform(point3, rot_mat)
        point2 = AllplanGeo.Transform(point2, rot_mat)
        point5 = AllplanGeo.Transform(point5, rot_mat)

        point4_bottom = AllplanGeo.Point3D(0, build_ele.Thickness.value, build_ele.Height.value)
        point4_top    = AllplanGeo.Point3D(0, build_ele.Thickness.value, build_ele.Height.value)
        point4_bottom = AllplanGeo.Transform(point4_bottom, rot_mat)
        point4_top    = AllplanGeo.Transform(point4_top, rot_mat)


        #-----------------  mirror handle

        mirror_handle = HandleProperties("MirrorCuboid", point5, AllplanGeo.Point3D(),
                                         [],
                                         HandleDirection.CLICK)

        mirror_handle.handle_type  = AllplanIFW.ElementHandleType.HANDLE_ARROW
        mirror_handle.info_text    = "Mirror the cuboid"
        mirror_handle.handle_angle = rot_angle

        handle_list = [mirror_handle]


        #----------------- checkbox handle for input controls

        show_input_handle = HandleProperties("ShowInputControlsHandle", point1 + AllplanGeo.Point3D(0, -500, 0), AllplanGeo.Point3D(),
                                             [HandleParameterData("ShowInputControls", HandleParameterType.CHECK_BOX,
                                                                   check_box_state = build_ele.ShowInputControls.value)],
                                             HandleDirection.CLICK)

        show_input_handle.info_text = "Hide input controls" if build_ele.ShowInputControls.value else "Show input controls"

        handle_list.append(show_input_handle)


        #----------------- checkbox handle for show handles

        show_handles = HandleProperties("ShowHandles", point1 + AllplanGeo.Point3D(0, -800, 0), AllplanGeo.Point3D(),
                                        [HandleParameterData("ShowHandles", HandleParameterType.CHECK_BOX,
                                                             check_box_state = build_ele.ShowHandles.value)],
                                         HandleDirection.CLICK)

        show_handles.info_text = "Hide handles" if build_ele.ShowHandles.value else "Show handles"

        handle_list.append(show_handles)


        #----------------- increment and decrement handle

        increment_handle = HandleProperties("IncrementHandle",
                                             point2 + AllplanGeo.Point3D(200, 100, 0), AllplanGeo.Point3D(),
                                             [HandleParameterData("Thickness", HandleParameterType.INCREMENT_BUTTON,
                                                                  in_decrement_value = 100.)],
                                             HandleDirection.CLICK)

        increment_handle.info_text = "Increment thickness by 0.1m"

        handle_list.append(increment_handle)

        decrement_handle = HandleProperties("DecrementHandle",
                                             point2 + AllplanGeo.Point3D(200, -100, 0), AllplanGeo.Point3D(),
                                             [HandleParameterData("Thickness", HandleParameterType.DECREMENT_BUTTON,
                                                                  in_decrement_value = 100.)],
                                             HandleDirection.CLICK)

        decrement_handle.info_text = "Decrement thickness by 0.1m"
        decrement_handle.handle_angle = AllplanGeo.Angle(math.pi)

        handle_list.append(decrement_handle)


        #-----------------  offset point handle

        offset_handle = HandleProperties("Offset", build_ele.OffsetPoint.value, AllplanGeo.Point3D(),
                                         [HandleParameterData("OffsetPoint", HandleParameterType.POINT, False)],
                                         HandleDirection.XYZ_DIR)

        offset_handle.handle_type  = AllplanIFW.ElementHandleType.HANDLE_SQUARE_RED
        offset_handle.info_text    = "Offset the cuboid"

        handle_list.append(offset_handle)


        #----------------- slope handle

        show_input_controls = build_ele.ShowInputControls.value
        show_handles        = build_ele.ShowHandles.value

        handle_slope = HandleProperties("Slope",
                                        point1 + AllplanGeo.Point3D(build_ele.SlopeX.value, build_ele.SlopeY.value, 0),
                                        point1,
                                        [HandleParameterData("SlopeX", HandleParameterType.X_DISTANCE, show_input_controls),
                                         HandleParameterData("SlopeY", HandleParameterType.Y_DISTANCE, show_input_controls)],
                                        HandleDirection.XYZ_DIR, False,
                                        show_handles = show_handles)

        handle_slope.info_text = "Slope handle"

        handle_list.append(handle_slope)


        #----------------- dimension handles

        handle_length = HandleProperties("Length", point2, point1,
                                         [HandleParameterData("Length", HandleParameterType.POINT_DISTANCE, show_input_controls)],
                                         HandleDirection.XYZ_DIR,
                                         show_handles = show_handles)

        handle_length.info_text = "Length handle"

        handle_list.append(handle_length)

        handle_thickness = HandleProperties("HandleThickness", point3, point2,
                                            [HandleParameterData("Thickness", HandleParameterType.POINT_DISTANCE, show_input_controls)],
                                            HandleDirection.XYZ_DIR,
                                            show_handles = show_handles)

        handle_thickness.info_text = "Thickness handle"

        handle_list.append(handle_thickness)

        handle_height = HandleProperties("HandleHeight", point4_bottom, point4_top,
                                         [HandleParameterData("Height", HandleParameterType.POINT_DISTANCE, show_input_controls)],
                                         HandleDirection.XYZ_DIR,
                                         show_handles = show_handles)

        handle_height.info_text = "Height handle"

        handle_list.append(handle_height)

        return model_ele_list, handle_list


    def create_arc(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a cuboid

        Returns:
            model element
        """

        build_ele      = self.build_ele
        model_ele_list = ModelEleList()
        handle_list    = []
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

        handle_placement = HandleProperties("ArcPlacement", center_pnt + handle_pnt, center_pnt,
                                            [HandleParameterData("XPlacement", HandleParameterType.VECTOR_DISTANCE, False,
                                                                 dir_vector = AllplanGeo.Vector3D(1000, 0, 0)),
                                             HandleParameterData("YPlacement", HandleParameterType.VECTOR_DISTANCE, False,
                                                                 dir_vector = AllplanGeo.Vector3D(0, 1000, 0))],
                                            HandleDirection.VECTOR_DIR)

        handle_placement.info_text = "Placement handle"

        handle_list.append(handle_placement)

        handle_opening = HandleProperties("DeltaAngle", center_pnt + opening_handle_pnt, center_pnt,
                                          [HandleParameterData("DeltaAngle", HandleParameterType.ANGLE, False)],
                                          HandleDirection.ANGLE, angle_placement = angle_placement)

        handle_opening.info_text = "Opening handle"

        handle_list.append(handle_opening)

        return model_ele_list, handle_list



    def create_polygon(self) -> tuple[ModelEleList, list[HandleProperties]]:
        """ create a polygon

        Returns:
            model element
        """

        #----------------- create a polygon

        build_ele = self.build_ele

        poly_points = build_ele.PolyPoints.value

        poly = AllplanGeo.Polygon3D()

        for pnt in poly_points:
            poly += pnt

        poly += poly.StartPoint

        rot_pnt_y = (poly_points[0] + poly_points[1]) / 2
        rot_pnt_z = (poly_points[1] + poly_points[2]) / 2

        poly = AllplanGeo.Transform(poly, RotationUtil(0, 0, build_ele.RotAngleZ.value).get_rotation_matrix(rot_pnt_z))
        poly = AllplanGeo.Transform(poly, RotationUtil(0, -build_ele.RotAngleY.value, 0).get_rotation_matrix(rot_pnt_y))

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(poly)


        #----------------- point list handles

        poly_points = poly.Points
        ref_pnt     = poly_points[0]
        handle_list = []

        for index, pnt in enumerate(poly_points[:-1]):
            handle_list.append(HandleProperties("PolyPoints", pnt, ref_pnt,
                                                [HandleParameterData("PolyPoints", HandleParameterType.POINT, False,
                                                                     list_index = index)],
                                                 HandleDirection.XYZ_DIR))
            handle_list[-1].info_text = "Index=" + str(index)


        #----------------- rotation handles

        rot_pnt_y = (poly_points[0] + poly_points[1]) / 2
        rot_pnt_z = (poly_points[1] + poly_points[2]) / 2

        handle_z_rot = HandleProperties("Z_Rotation",
                                        rot_pnt_z, rot_pnt_z,
                                        [HandleParameterData("RotAngleZ", HandleParameterType.ANGLE)],
                                        HandleDirection.ANGLE, False)

        handle_z_rot.info_text = "Z rotation handle"

        handle_list.append(handle_z_rot)

        handle_y_rot = HandleProperties("Y_Rotation",
                                        rot_pnt_y, rot_pnt_y,
                                        [HandleParameterData("RotAngleY", HandleParameterType.ANGLE)],
                                        HandleDirection.ANGLE, False,
                                        angle_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(),
                                                                                     AllplanGeo.Vector3D(1000, 0, 0),
                                                                                     AllplanGeo.Vector3D(0, -1000, 0)))

        handle_y_rot.info_text = "Y rotation handle"

        handle_list.append(handle_y_rot)

        return model_ele_list, handle_list


    def create_lines(self) -> tuple[list[AllplanBasisEle.ModelElement3D], list[HandleProperties]]:
        """ create lines by distance

        Returns:
            model element
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

        handle_list = []
        start_pnt   = ref_pnt

        for index, dist in enumerate(build_ele.DistanceList.value):
            handle_list.append(HandleProperties("DistanceList", start_pnt + AllplanGeo.Point3D(dist, 0, 0), AllplanGeo.Point3D(start_pnt),
                                                [HandleParameterData("DistanceList", HandleParameterType.X_DISTANCE, True,
                                                                     list_index = index)],
                                                 HandleDirection.X_DIR))
            handle_list[-1].info_text = "Index=" + str(index)

            start_pnt += AllplanGeo.Point3D(dist, 0, 0)

        return model_ele_list, handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D) -> CreateElementResult:
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point

        Returns:
            created element result
        """

        build_ele = self.build_ele

        if handle_prop.handle_id == build_ele.MirrorCuboid.name:
            build_ele.MirrorCuboid.value = not build_ele.MirrorCuboid.value

        else:
            HandlePropertiesService.update_property_value(build_ele, handle_prop, input_pnt)

        return self.execute()
