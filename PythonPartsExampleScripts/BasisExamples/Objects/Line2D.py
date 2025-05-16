""" Script for Line2D
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from BuildingElementListService import BuildingElementListService

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult

from TypeCollections import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.Line2DBuildingElement import Line2DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Line2D.py')


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

    return Line2D(build_ele, script_object_data)


class Line2D(BaseScriptObject):
    """ Definition of class Line2D
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

        self.build_ele             = build_ele
        self.pnt_interactor_result = PointInteractorResult()
        self.model_ele_list        = ModelEleList()
        self.from_point            = AllplanGeo.Point3D()


    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        self.script_object_interactor = PointInteractor(self.pnt_interactor_result, True, "From point", self.draw_preview,
                                                        z_coord_input = False)

        build_ele.InputMode.value = build_ele.FROM_POINT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value == build_ele.TO_POINT:
            AllplanBaseEle.CreateElements(self.document, AllplanGeo.Matrix3D(), self.model_ele_list, [], None)

        self.from_point = self.pnt_interactor_result.input_point

        build_ele.InputMode.value = build_ele.TO_POINT

        self.script_object_interactor = PointInteractor(self.pnt_interactor_result, True, "To point", self.draw_preview,
                                                        z_coord_input = False, start_point = self.from_point)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult()


    def draw_preview(self):
        """ draw the preview
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value == build_ele.FROM_POINT:
            return

        self.model_ele_list = ModelEleList(build_ele.CommonProp.value)

        self.model_ele_list.append_geometry_2d(AllplanGeo.Line2D(self.from_point.To2D,
                                                                 self.pnt_interactor_result.input_point.To2D))

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(),
                                          self.model_ele_list, False, None)


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        return OnCancelFunctionResult.CANCEL_INPUT if build_ele.InputMode.value == build_ele.FROM_POINT else OnCancelFunctionResult.RESTART
