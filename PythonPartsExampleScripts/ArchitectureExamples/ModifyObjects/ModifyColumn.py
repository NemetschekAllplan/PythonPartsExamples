""" Example Script for the column modification
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyColumnBuildingElement import ModifyColumnBuildingElement
else:
    ModifyColumnBuildingElement = BuildingElement

print('Load ModifyColumn.py')

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


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\ArchitectureExamples\ModifyObjects\ModifyColumn.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifyColumn(build_ele, script_object_data)


class ModifyColumn(BaseScriptObject):
    """ Definition of class ModifyColumn
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

        self.column_sel_result = SingleElementSelectResult()
        self.polygon_result    = PolygonInteractorResult()

        self.build_ele = cast(ModifyColumnBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.placement_pnt        = AllplanGeo.Point3D()
        self.shape_polygon        = AllplanGeo.Polygon2D()
        self.shape_geo_param_util = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())
        self.hide_ele_service     = HideElementsService()
        self.column_ele           = AllplanArchEle.ColumnElement()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.column_sel_result,
                                                                      [AllplanEleAdapter.Column_TypeUUID],
                                                                      "Select the column")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        last_input_mode = build_ele.InputMode.value

        build_ele.InputMode.value = build_ele.COLUMN_INPUT

        self.script_object_interactor = None

        if last_input_mode == build_ele.COLUMN_PLACEMENT:
            return

        #----------------- get the column element

        self.column_ele = cast(AllplanArchEle.ColumnElement, AllplanBaseEle.GetElement(self.column_sel_result.sel_element))

        self.placement_pnt = self.column_ele.GetPlacementPoint().To3D

        #----------------- get the properties

        column_properties = self.column_ele.Properties

        self.shape_geo_param_util.set_parameter_values(build_ele, column_properties, "", self.shape_polygon)

        build_ele.PlaneReferences.value = column_properties.PlaneReferences
        build_ele.CommonProp.value      = column_properties.CommonProperties
        build_ele.SurfaceElemProp.value = column_properties.SurfaceElementProperties
        build_ele.IsSurface.value       = column_properties.Surface.strip() != ""
        build_ele.SurfaceName.value     = column_properties.Surface
        build_ele.Material.value        = column_properties.Material
        build_ele.Name.value            = column_properties.Name
        build_ele.Trade.value           = column_properties.Trade
        build_ele.Priority.value        = column_properties.Priority
        build_ele.Factor.value          = column_properties.Factor

        build_ele.Status.value          = AllplanBaseEle.AttributeService.GetEnumValueStringFromID(build_ele.Status.attribute_id, column_properties.Status)
        build_ele.CalculationMode.value = AllplanBaseEle.AttributeService.GetEnumValueStringFromID(build_ele.CalculationMode.attribute_id, column_properties.CalculationMode)

        #----------------- start the column modification

        self.hide_ele_service.hide_element(self.column_sel_result.sel_element)

    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_column_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def create_column_element(self) -> ModelEleList:
        """ create the column element


        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        #----------------- create the properties

        column_properties = AllplanArchEle.ColumnProperties()

        self.shape_geo_param_util.create_shape_geo_properties(build_ele, column_properties, self.shape_polygon)

        column_properties.PlaneReferences          = build_ele.PlaneReferences.value
        column_properties.CommonProperties         = build_ele.CommonProp.value
        column_properties.SurfaceElementProperties = build_ele.SurfaceElemProp.value
        column_properties.Material                 = build_ele.Material.value
        column_properties.Name                     = build_ele.Name.value
        column_properties.Trade                    = build_ele.Trade.value
        column_properties.Priority                 = build_ele.Priority.value
        column_properties.Factor                   = build_ele.Factor.value

        column_properties.Status          = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(build_ele.Status.attribute_id, build_ele.Status.value)
        column_properties.CalculationMode = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(build_ele.CalculationMode.attribute_id, build_ele.CalculationMode.value)

        if build_ele.IsSurface.value:
            column_properties.Surface = build_ele.SurfaceName.value

        self.column_ele.Properties = column_properties

        #----------------- add the placement point and create the element

        self.column_ele.PlacementPoint = self.placement_pnt.To2D - self.shape_geo_param_util.get_reference_point(build_ele)

        model_ele_list = ModelEleList()

        model_ele_list.append(self.column_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            handles
        """

        handle_list = []

        HandleCreator.move(handle_list, "PlacementPoint", self.placement_pnt)

        return handle_list


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

        match handle_prop.handle_id:
            case "PlacementPoint":
                self.placement_pnt = input_pnt

        return self.execute()


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        if build_ele.InputMode.value == build_ele.COLUMN_PLACEMENT:
            if self.script_object_interactor is not None and build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                self.script_object_interactor.on_cancel_function()

                self.shape_polygon = AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1]

                return OnCancelFunctionResult.CONTINUE_INPUT

            return OnCancelFunctionResult.RESTART

        self.hide_ele_service.show_elements()

        AllplanBaseEle.ModifyElements(self.document, self.create_column_element())

        return OnCancelFunctionResult.RESTART

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

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return False

        match name:
            case "Shape":
                if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                    self.script_object_interactor = PolygonInteractor(self.polygon_result, self.column_ele.CommonProperties,
                                                                      False, False)

                    self.script_object_interactor.start_input(self.coord_input)

                    build_ele.InputMode.value = build_ele.COLUMN_PLACEMENT

        return False
