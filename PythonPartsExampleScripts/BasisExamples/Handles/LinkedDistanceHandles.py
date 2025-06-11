""" Script for LinkedDistanceHandles
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils.HandleCreator.HandleCreator import HandleCreator

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LinkedDistanceHandlesBuildingElement \
        import LinkedDistanceHandlesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load LinkedDistanceHandles.py')


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

    return LinkedDistanceHandles(build_ele, script_object_data)


class LinkedDistanceHandles(BaseScriptObject):
    """ Definition of class LinkedDistanceHandles
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

        model_ele_list = ModelEleList()
        handle_list    = HandleList()

        reft_pnt = AllplanGeo.Point2D()

        line_length = build_ele.RectLength.value - build_ele.RectThickness.value / 2

        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(reft_pnt, reft_pnt + AllplanGeo.Vector2D(line_length, 0)))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(reft_pnt, reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value)))
        model_ele_list.append_geometry_2d(AllplanGeo.Line2D(reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value),
                                                            reft_pnt + AllplanGeo.Vector2D(line_length, build_ele.RectThickness.value)))
        model_ele_list.append_geometry_2d(AllplanGeo.Arc2D(reft_pnt + AllplanGeo.Vector2D(line_length, build_ele.RectThickness.value / 2),
                                                           build_ele.RectThickness.value / 2,
                                                           build_ele.RectThickness.value / 2, 0, math.pi * 1.5,  math.pi * 2.5))

        HandleCreator.x_distance(handle_list, "RectLength",
                                 (reft_pnt + AllplanGeo.Vector2D(build_ele.RectLength.value, build_ele.RectThickness.value / 2)).To3D,
                                 (reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value / 2)).To3D, True, False,
                                 info_text = "Length handle")

        HandleCreator.y_distance(handle_list, "RectThickness", (reft_pnt + AllplanGeo.Vector2D(0, build_ele.RectThickness.value)).To3D,
                                 reft_pnt.To3D, True, True, info_text = "Thickness handle")

        return CreateElementResult(model_ele_list, handle_list, multi_placement = True)
