"""Example script showing the creation of a column"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.DockingPointInteractor import DockingPointInteractor
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

from Utils import LibraryBitmapPreview
from Utils.General.AttributeUtil import AttributeUtil

from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ColumnBuildingElement import ColumnBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Create a simplified column representation for library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        Preview elements
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ArchitectureExamples\Objects\Column.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ColumnScript(build_ele, script_object_data)


class ColumnScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural upstand/downstand column

    This script objects prompts the user to input a 2D-Line by specifying
    start and end point and subsequently creates a column
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialize the column script object

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.pnt_result               = PointInteractorResult()
        self.build_ele                = build_ele
        self.shape_geo_param_util     = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.polygon_result           = PolygonInteractorResult()


    def start_input(self):
        """Starts the column axis input at the beginning of the script runtime"""

        build_ele = self.build_ele

        build_ele.__PlacementPointConnection__.value.reset()

        if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
            self.script_object_interactor = PolygonInteractor(self.polygon_result, build_ele.CommonProp.value, False, False)

        elif build_ele.PlaceAtDockingPoint.value:
            self.script_object_interactor = DockingPointInteractor(build_ele.__PlacementPointConnection__, self.draw_preview)

        else:
            self.script_object_interactor = PointInteractor(self.pnt_result, True, "Place the element", self.draw_preview)


    def start_next_input(self):
        """Terminate the input after successful input of start point"""

        if self.pnt_result     != PointInteractorResult() or \
           self.polygon_result != PolygonInteractorResult() or \
           self.build_ele.__PlacementPointConnection__.value.is_valid():
            self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        return CreateElementResult([self.create_column_element()], placement_point = AllplanGeo.Point3D(),  multi_placement = True)


    def draw_preview(self):
        """ draw the preview
        """

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(),
                                          [self.create_column_element()], False, None)


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        if self.script_object_interactor:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def create_column_properties(self) -> AllplanArchEle.ColumnProperties:
        """Properties of the column element, based on the values from the property palette

        Returns:
            column properties
        """

        column_prop = AllplanArchEle.ColumnProperties()

        #--------- Define properties specific to a column

        column_prop.PlaneReferences = self.build_ele.PlaneReferences.value

        self.shape_geo_param_util.create_shape_geo_properties(self.build_ele, column_prop,
                                                              AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1])

        #--------- Define standard architecture attributes

        column_prop.CalculationMode = AttributeUtil.get_enum_id_from_value_string(self.build_ele.CalculationMode)
        column_prop.Trade           = self.build_ele.Trade.value
        column_prop.Priority        = self.build_ele.Priority.value
        column_prop.Factor          = self.build_ele.Factor.value

        #--------- Define surface elements

        column_prop.SurfaceElementProperties = self.build_ele.SurfaceElemProp.value

        #--------- Define format and texture properties

        column_prop.CommonProperties = self.build_ele.CommonProp.value

        if self.build_ele.IsSurface.value:
            column_prop.Surface = self.build_ele.SurfaceName.value

        return column_prop


    def create_column_element(self) -> AllplanArchEle.ColumnElement:
        """Creates a ColumnElement based on placement point

        Returns:
            Column element
        """

        build_ele = self.build_ele

        input_point = AllplanGeo.Point3D(self.pnt_result.input_point)

        if build_ele.PlaceAtDockingPoint.value == False:
            input_point.X = input_point.X - self.shape_geo_param_util.get_reference_point(build_ele).X
            input_point.Y = input_point.Y - self.shape_geo_param_util.get_reference_point(build_ele).Y

        return AllplanArchEle.ColumnElement(self.create_column_properties(),
                                            input_point if not build_ele.__PlacementPointConnection__.value.is_valid() \
                                            else build_ele.__PlacementPointConnection__.value.point)

    def modify_element_property(self,
                                name  : str,
                                _value: Any) -> bool:
        """ modify the element property

        Args:
            name:   name
            _value: value

        Returns:
            update palette state
        """

        build_ele = self.build_ele

        match name:
            case "PlaceAtDockingPoint":
                self.start_input()

                if self.script_object_interactor:
                    self.script_object_interactor.start_input(self.coord_input)

            case "Shape":
                if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                    self.script_object_interactor = PolygonInteractor(self.polygon_result, build_ele.CommonProp.value, False, False)
                else:
                    self.script_object_interactor = PointInteractor(self.pnt_result, True, "Place the element", self.draw_preview)

                if self.script_object_interactor:
                    self.script_object_interactor.start_input(self.coord_input)

                return True

        return False
