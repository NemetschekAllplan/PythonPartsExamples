""" implementation of the example PythonPart showing how to associate the PythonPart with
another element in order for the PythonPart to be updated when the associated element changes
"""

from __future__ import annotations

import hashlib

from pathlib import Path
from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from PythonPartTransaction import ConnectToElements
from PythonPartUtil import PythonPartUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.ElementFilter.CurvedGeometryElementFilter import CurvedGeometryElementFilter
from Utils.ElementFilter.FilterCollection import FilterCollection
from Utils.Geometry.ExtrudeByVectorUtil import ExtrudeByVectorUtil

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


def create_preview(build_ele: BuildingElement,
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


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

        self.build_ele  = build_ele
        self.connection = ConnectToElements()
        self.geo_ele    = None
        self.sel_result = SingleElementSelectResult()

        #----------------- check for modification

        if self.execution_event == AllplanSettings.ExecutionEvent.eCreation:
            return

        # use associative framework to get associated elements
        pythonpart_uuid  = self.modification_ele_list.get_base_element_adapter(self.document).GetModelElementUUID()
        observed_elements = AllplanBaseElements.AssociationService.GetObservedElements(self.document, pythonpart_uuid)

        if len(observed_elements) == 0:
            return

        self.geo_ele = observed_elements[0].GetGeometry()

        # save hash of the associated element`s geometry to trigger the update only on geometry change
        build_ele.SourceElementHash.value = hashlib.sha224(repr(self.geo_ele).encode()).hexdigest()
        build_ele.InputMode.value         = build_ele.PARAMETER_MODIFICATION


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        if self.execution_event != AllplanSettings.ExecutionEvent.eCreation:
            return

        # set up selection filter
        element_filter = FilterCollection(True)
        element_filter.append(CurvedGeometryElementFilter(True, True))      # allow only curves (2D and 3D)
        element_filter.append(lambda ele: ele.IsInActiveLayer())            # allow only elements on current drawing file on active layers

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_result, element_filter, "Select the curve element")

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        self.geo_ele = self.sel_result.sel_element.GetGeometry()

        build_ele.SourceElementHash.value = hashlib.sha224(repr(self.geo_ele).encode()).hexdigest()
        build_ele.InputMode.value         = self.build_ele.PARAMETER_MODIFICATION

        self.connection = ConnectToElements([str(self.sel_result.sel_element.GetModelElementUUID())])


    def execute(self) -> CreateElementResult:
        """  execute the script

        Returns:
            created result
        """
        if self.geo_ele is None:
            return CreateElementResult()

        build_ele = self.build_ele

        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.extrude_geometry())


        #----------------- create the handle

        if isinstance(start_pnt := self.geo_ele.StartPoint, AllplanGeo.Point2D):
            start_pnt = start_pnt.To3D

        handle_list = [HandleProperties("ExtrusionVector", start_pnt + build_ele.ExtrusionVector.value, start_pnt,
                                        [HandleParameterData("ExtrusionVector.X", HandleParameterType.X_DISTANCE, True),
                                         HandleParameterData("ExtrusionVector.Y", HandleParameterType.Y_DISTANCE, True),
                                         HandleParameterData("ExtrusionVector.Z", HandleParameterType.Z_DISTANCE, True)],
                                         HandleDirection.XYZ_DIR, False)]

        return CreateElementResult(pyp_util.create_pythonpart(build_ele), handle_list,
                                   placement_point     = AllplanGeo.Point3D(),
                                   multi_placement     = True,
                                   connect_to_ele      = self.connection)


    def extrude_geometry(self) -> ModelEleList:
        """ extrude the geometry

        Returns:
            created model elements
        """

        model_ele_list = ModelEleList()

        # if the curve is a closed polyline, convert it to a polygon
        if isinstance(self.geo_ele, AllplanGeo.Polyline2D) and self.geo_ele.Points[0] == self.geo_ele.Points[-1]:
            self.geo_ele = AllplanGeo.Polygon2D(self.geo_ele.Points)

        if (extruded_ele := ExtrudeByVectorUtil.extrude([self.geo_ele],
                                                         self.build_ele.ExtrusionVector.value, False, True)) is not None:
            model_ele_list.append_geometry_3d(extruded_ele)

        return model_ele_list
