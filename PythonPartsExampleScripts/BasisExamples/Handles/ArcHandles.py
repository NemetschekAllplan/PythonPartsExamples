""" Script for ArcHandles
"""

from __future__ import annotations

import math

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils.Geometry.TransformationStack import TransformationStack
from Utils.HandleCreator.CurveHandlesCreator import CurveHandlesCreator
from Utils.HandleCreator.HandleCreator import HandleCreator

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ArcHandlesBuildingElement import ArcHandlesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ArcHandles.py')


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

    return ArcHandles(build_ele, script_object_data)


class ArcHandles(BaseScriptObject):
    """ Definition of class ArcHandles
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

        trans_stack = TransformationStack()

        model_ele_list = ModelEleList(trans_stack = trans_stack)
        handle_list    = HandleList(trans_stack)


        #----------------- get the transformation

        trans_stack.scale_xy(build_ele.XPlacement.value, build_ele.YPlacement.value)

        radius     = build_ele.Arc.value.MajorRadius
        end_angle  = build_ele.Arc.value.EndAngle
        center_pnt = build_ele.Arc.value.Center

        opening_handle_pnt = AllplanGeo.Point2D(radius * math.cos(end_angle), radius * math.sin(end_angle))

        model_ele_list.append_geometry_2d(build_ele.Arc.value)
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(center_pnt, center_pnt + opening_handle_pnt))


        #----------------- create the handles

        handle_pnt  = opening_handle_pnt.To3D / 2 * trans_stack.trans_matrix
        center_pnt  = center_pnt.To3D * trans_stack.trans_matrix

        HandleCreator.vector_distances(handle_list, ["XPlacement", "YPlacement"], center_pnt + handle_pnt, center_pnt,
                                       [AllplanGeo.Vector3D(1000, 0, 0), AllplanGeo.Vector3D(0, 1000, 0)],
                                       [False, False], [False, False],
                                       info_text         = "Placement handle",
                                       disable_transform = True)

        CurveHandlesCreator.arc_2d(handle_list, "Arc", build_ele.Arc.value, info_text = "Arc handles")

        return CreateElementResult(model_ele_list, handle_list, multi_placement = True)
