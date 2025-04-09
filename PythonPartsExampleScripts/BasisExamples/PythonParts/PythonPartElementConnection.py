""" implementation of the example PythonPart showing how to associate the PythonPart with
another element in order for the PythonPart to be updated when the associated element changes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil

from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.ElementFilter.CurvedGeometryElementFilter import CurvedGeometryElementFilter
from Utils.ElementFilter.FilterCollection import FilterCollection
from Utils.Geometry.ExtrudeByVectorUtil import ExtrudeByVectorUtil
from Utils.HandleCreator.CurveHandleCreator import CurveHandleCreator

from ValueTypes.Data.ElementGeometryConnection import ElementGeometryConnection, GeometryType

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartElementConnectionBuildingElement \
        import PythonPartElementConnectionBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load PythonPartElementConnection.py')

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

    return PythonPartElementConnection(build_ele, script_object_data)


class PythonPartElementConnection(BaseScriptObject):
    """ Definition of class PythonPartElementConnection
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)


        #----------------- set initial values

        self.build_ele    = build_ele
        self.sel_result   = MultiElementSelectInteractorResult()

        self.script_object_interactor : (MultiElementSelectInteractor | None) = None


        #----------------- check for modification

        if self.execution_event == AllplanSettings.ExecutionEvent.eCreation:
            return

        build_ele.InputMode.value = build_ele.PARAMETER_MODIFICATION


    def create_library_preview(self) -> CreateElementResult:
        """ create the library preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        if self.execution_event != AllplanSettings.ExecutionEvent.eCreation:
            return


        #----------------- set up selection filter

        element_filter = FilterCollection(True)

        element_filter.append(CurvedGeometryElementFilter(True, True))      # allow only curves (2D and 3D)

        self.script_object_interactor = MultiElementSelectInteractor(self.sel_result, element_filter, "Select the curve element(s)")

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        build_ele.InputMode.value = self.build_ele.PARAMETER_MODIFICATION

        build_ele.ElementGeoConnection.value = \
            [ElementGeometryConnection(sel_element, GeometryType.BASE_GEOMETRY) for sel_element in self.sel_result.sel_elements]


    def execute(self) -> CreateElementResult:
        """  execute the script

        Returns:
            created result
        """

        build_ele = self.build_ele


        #----------------- check for empty elements

        if not build_ele.ElementGeoConnection.value:
            if self.execution_event == AllplanSettings.ExecutionEvent.eCreation:
                return CreateElementResult()

            elements_to_delete = \
                AllplanEleAdapter.BaseElementAdapterList([self.modification_ele_list.get_base_element_adapter(self.document)])

            return CreateElementResult(ModelEleList(), [], elements_to_delete = elements_to_delete)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.extrude_geometry())

        handle_list  = list[HandleProperties]()

        CurveHandleCreator.vector(handle_list, self.build_ele.ElementGeoConnection.value[0].geometry.StartPoint,
                                  build_ele.ExtrusionVector.value, "ExtrusionVector")

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),  handle_list,
                                   placement_point     = AllplanGeo.Point3D(),
                                   multi_placement     = True)


    def extrude_geometry(self) -> ModelEleList:
        """ extrude the geometry

        Returns:
            created model elements
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList()

        for connection in build_ele.ElementGeoConnection.value:
            geo_ele = connection.geometry

            if isinstance(geo_ele, AllplanGeo.Polyline2D) and geo_ele.Points[0] == geo_ele.Points[-1]:
                geo_ele = AllplanGeo.Polygon2D(geo_ele.Points)                                          # pylint: disable=redefined-loop-name

            if (extruded_ele := ExtrudeByVectorUtil.extrude([geo_ele],
                                                            self.build_ele.ExtrusionVector.value, False, True)) is not None:
                model_ele_list.append_geometry_3d(extruded_ele)

        return model_ele_list


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting ESC during the input

        Cancels the input, when ESC is hit during the start point input. Otherwise restarts the start point input.

        Returns:
            False during the start point input, True otherwise
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            if self.script_object_interactor:
                self.script_object_interactor.close_selection()

            return OnCancelFunctionResult.CANCEL_INPUT

        return OnCancelFunctionResult.CREATE_ELEMENTS
