""" Script for CurveHandles
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils.HandleCreator.CurveHandlesCreator import CurveHandlesCreator
from Utils.HandleCreator.PolyPointsDistanceType import PolyPointsDistanceType
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CurveHandlesBuildingElement import CurveHandlesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load CurveHandles.py')


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

    return CurveHandles(build_ele, script_object_data)


class CurveHandles(BaseScriptObject):
    """ Definition of class CurveHandles
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

        model_ele_list.append_geometry_3d(build_ele.Polygon.value)
        model_ele_list.append_geometry_2d(build_ele.Line.value)

        handle_list = HandleList()

        CurveHandlesCreator.poly_curve(handle_list, "Polygon", build_ele.Polygon.value, True,
                                      input_field_above          = False,
                                      poly_point_distance_fields = PolyPointsDistanceType.LENGTH)

        CurveHandlesCreator.line(handle_list, "Line", build_ele.Line.value)

        return CreateElementResult(model_ele_list, handle_list, multi_placement = True)
