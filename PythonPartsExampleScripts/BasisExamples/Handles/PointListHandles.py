""" Script for PointListHandles
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from string import Template

import math

import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils.Geometry.TransformationStack import TransformationStack, LengthUnit, AngleUnit
from Utils.HandleCreator.HandleCreator import HandleCreator
from Utils.HandleCreator.PointListHandlesCreator import PointListHandlesCreator

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PointListHandlesBuildingElement import \
        PointListHandlesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PointListHandles.py')


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

    return PointListHandles(build_ele, script_object_data)


class PointListHandles(BaseScriptObject):
    """ Definition of class PointListHandles
    """

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

        trans_stack = TransformationStack(LengthUnit.MM, AngleUnit.DEGREE)

        model_ele_list = ModelEleList(trans_stack = trans_stack)
        handle_list    = HandleList(trans_stack)


        #----------------- create the transformation

        trans_stack.rotate_z(build_ele.RotAngleZ.value, rot_pnt_z := build_ele.RotationPoint.value)
        trans_stack.rotate_y(build_ele.RotAngleY.value, rot_pnt_y := build_ele.RotationPoint.value + AllplanGeo.Vector3D(0, 500, 0))


        #----------------- create the lines

        ref_pnt = AllplanGeo.Point3D(0, 4000, 0)

        start_pnt = ref_pnt

        self.add_line(start_pnt, model_ele_list)

        for dist in build_ele.DistanceList.value:
            start_pnt = start_pnt + AllplanGeo.Point3D(dist, 0, 0)

            self.add_line(start_pnt, model_ele_list)


        #----------------- create the arcs

        for pnt in build_ele.PointList.value:
            self.add_arc(pnt, model_ele_list)


        #----------------- distance handles

        start_pnt = ref_pnt

        for index, dist in enumerate(build_ele.DistanceList.value):
            HandleCreator.point_distance(handle_list, "DistanceList", start_pnt + AllplanGeo.Point3D(dist, 0, 0),
                                         AllplanGeo.Point3D(start_pnt), True, False,
                                         list_index              = index,
                                         info_text               = f"Index={index}",
                                         show_input_field_always = True)

            start_pnt += AllplanGeo.Point3D(dist, 0, 0)


        #----------------- point list handles

        plane = AllplanGeo.Plane3D(AllplanGeo.Point3D(), AllplanGeo.Vector3D(0, 0, 1000))

        PointListHandlesCreator.point_list(handle_list, "PointList", build_ele.PointList.value,
                                           info_text_template = Template("Shift + click = delete point\nIndex=$index"),
                                           delete_point       = True,
                                           plane              = plane)

        PointListHandlesCreator.point_list_segment_center(handle_list, "PointList", build_ele.PointList.value,
                                                          info_text_template = Template("Split segment $index"),
                                                          index_offset       = 1,
                                                          plane              = plane)


        #----------------- rotation handles

        HandleCreator.angle(handle_list, "RotAngleZ", rot_pnt_z, rot_pnt_z + AllplanGeo.Vector3D(1000, 0, 0),
                            AllplanGeo.AxisPlacement3D(rot_pnt_z, AllplanGeo.Vector3D(1000, 0, 0),
                                                       AllplanGeo.Vector3D(0, 0, 1000)),
                            info_text = "Z rotation handle")

        HandleCreator.angle(handle_list, "RotAngleY", rot_pnt_y, rot_pnt_y + AllplanGeo.Vector3D(0, 1000, 0),
                            AllplanGeo.AxisPlacement3D(rot_pnt_y, AllplanGeo.Vector3D(1000, 0, 0),
                                                       AllplanGeo.Vector3D(0, 1000, 0)),
                            info_text = "Y rotation handle")

        return CreateElementResult(model_ele_list, handle_list, multi_placement = True)


    @staticmethod
    def add_line(start_pnt     : AllplanGeo.Point3D,
                 model_ele_list: ModelEleList):
        """ add a line to the model element list

        Args:
            start_pnt:      start point
            model_ele_list: model element list
        """

        line = AllplanGeo.Line3D(start_pnt, start_pnt + AllplanGeo.Point3D(0, 2000, 0))

        model_ele_list.append_geometry_3d(line)


    @staticmethod
    def add_arc(start_pnt     : AllplanGeo.Point3D,
                model_ele_list: ModelEleList):
        """ add an arc to the model element list

        Args:
            start_pnt:      start point
            model_ele_list: model element list
        """

        arc = AllplanGeo.Arc3D(start_pnt, 300, 300, 0, math.pi * 2)

        model_ele_list.append_geometry_3d(arc)
