"""Example script showing the creation of a column"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from Utils import LibraryBitmapPreview

from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_ArchElements as AllplanArchEle

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


def create_preview(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a simplified column representation for library preview

    Args:
        build_ele:   building element with the parameter properties
        _doc:        input document

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

        if self.build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
            self.script_object_interactor = PolygonInteractor(self.polygon_result, self.build_ele.CommonProp.value, False, False)
        else:
            self.script_object_interactor = PointInteractor(self.pnt_result, True, "Place the element", self.draw_preview)


    def start_next_input(self):
        """Terminate the input after successful input of start point"""

        if self.pnt_result != PointInteractorResult() or  self.polygon_result  != PolygonInteractorResult():
            self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        return CreateElementResult([self.column_element()], placement_point = AllplanGeometry.Point2D())


    def draw_preview(self):
        """ draw the preview
        """

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeometry.Matrix3D(),
                                          [self.column_element()], False, None)


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        if self.script_object_interactor:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def create_column_properties(self) -> AllplanArchElements.ColumnProperties:
        """Properties of the column element, based on the values from the property palette

        Returns:
            column properties
        """

        column_prop = AllplanArchElements.ColumnProperties()

        #--------- Define properties specific to a column

        column_prop.PlaneReferences = self.build_ele.PlaneReferences.value
        self.shape_geo_param_util.create_shape_geo_properties(self.build_ele, column_prop,
                                                              AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1])

        #--------- Define standard architecture attributes

        column_prop.CalculationMode = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(120, self.build_ele.CalculationMode.value)
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


    def column_element(self) -> AllplanArchElements.ColumnElement:
        """Creates a ColumnElement based on axis (2d line)

        Returns:
            Column element
        """

        return AllplanArchElements.ColumnElement(self.create_column_properties(), self.pnt_result.input_point)

    def modify_element_property(self,
                                name : str,
                                value: Any) -> bool:
        """ modify the element property

        Args:
            name:  name
            value: value

        Returns:
            update palette state
        """

        build_ele = self.build_ele

        match name:
            case "Shape":
                if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                   self.script_object_interactor = PolygonInteractor(self.polygon_result, build_ele.CommonProp.value, False, False)
                else:
                    self.script_object_interactor = PointInteractor(self.pnt_result, True, "Place the element", self.draw_preview)

                if self.script_object_interactor:
                    self.script_object_interactor.start_input(self.coord_input)

                return True

        return False



