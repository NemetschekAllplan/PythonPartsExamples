""" Example Script for the column modification
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService

from ParameterUtils.Architecture.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

from TypeCollections.ElementModificationDataList import ElementModificationDataList
from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator.HandleCreator import HandleCreator
from Utils.HandleCreator.CurveHandlesCreator import CurveHandlesCreator
from Utils.HandleCreator.ShapeHandleCreator import ShapeHandleCreator
from Utils.HideElementsService import HideElementsService
from Utils.General.AttributeUtil import AttributeUtil
from Utils.HandleModify.RectangleHandleModification import RectangleHandleModification

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

        self.column_sel_result = MultiElementSelectInteractorResult()
        self.polygon_result    = PolygonInteractorResult()

        self.build_ele = cast(ModifyColumnBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.shape_geo_param_util = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())
        self.hide_ele_service     = HideElementsService()

        self.columns = ElementModificationDataList[AllplanArchEle.ColumnElement, AllplanGeo.Polygon2D]()


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

        self.script_object_interactor = MultiElementSelectInteractor(self.column_sel_result,
                                                                      [AllplanEleAdapter.Column_TypeUUID],
                                                                      "Select the column")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        last_input_mode = build_ele.InputMode.value

        build_ele.reset()

        build_ele.InputMode.value = build_ele.COLUMN_INPUT

        self.script_object_interactor = None

        if last_input_mode == build_ele.COLUMN_PLACEMENT:
            return

        #----------------- get the column elements data

        self.columns.clear()

        for column in self.column_sel_result.sel_elements:
            column_ele = cast(AllplanArchEle.ColumnElement, AllplanBaseEle.GetElement(column))

            self.columns.add_elements(column, column_ele, column_ele.Properties.ShapePolygon)


            #----------------- get the properties

            column_properties = column_ele.Properties

            self.shape_geo_param_util.set_parameter_values(column_properties, "", column_properties.ShapePolygon)

            build_ele.PlaneReferences.varied_value = column_properties.PlaneReferences
            build_ele.CommonProp.varied_value      = column_properties.CommonProperties
            build_ele.SurfaceElemProp.varied_value = column_properties.SurfaceElementProperties
            build_ele.IsSurface.varied_value       = column_properties.Surface.strip() != ""
            build_ele.SurfaceName.varied_value     = column_properties.Surface
            build_ele.Material.varied_value        = column_properties.Material
            build_ele.Name.varied_value            = column_properties.Name
            build_ele.Trade.varied_value           = column_properties.Trade
            build_ele.Priority.varied_value        = column_properties.Priority
            build_ele.Factor.varied_value          = column_properties.Factor

            build_ele.Status.varied_value          = AttributeUtil.get_enum_value_string_from_id(build_ele.Status, column_properties.Status)
            build_ele.CalculationMode.varied_value = AttributeUtil.get_enum_value_string_from_id(build_ele.CalculationMode,
                                                                                          column_properties.CalculationMode)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        preview_ele = self.create_column_elements() if self.columns.is_modified else ModelEleList()

        return CreateElementResult(ModelEleList(), self.create_handles(), preview_ele,
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def create_column_elements(self) -> ModelEleList:
        """ create the column elements

        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        model_ele_list = ModelEleList()

        for column_data in self.columns:
            column_ele = column_data.element

            column_prop = column_ele.Properties

            if not self.columns.is_handle_modified or column_data.is_handle_modification:
                self.shape_geo_param_util.modify_shape_geo_properties(column_prop, column_data.additional_data)

            column_prop.PlaneReferences          = build_ele.PlaneReferences.get_unique_value(column_prop.PlaneReferences)
            column_prop.CommonProperties         = build_ele.CommonProp.get_unique_value(column_prop.CommonProperties)
            column_prop.SurfaceElementProperties = build_ele.SurfaceElemProp.get_unique_value(column_prop.SurfaceElementProperties)
            column_prop.Material                 = build_ele.Material.get_unique_value(column_prop.Material)
            column_prop.Name                     = build_ele.Name.get_unique_value(column_prop.Name)
            column_prop.Trade                    = build_ele.Trade.get_unique_value(column_prop.Trade)
            column_prop.Priority                 = build_ele.Priority.get_unique_value((column_prop.Priority))
            column_prop.Factor                   = build_ele.Factor.get_unique_value(column_prop.Factor)

            column_prop.Status = AttributeUtil.get_enum_id_from_string(cast(int, build_ele.Status.attribute_id),
                                                                       build_ele.Status.get_unique_value(column_prop.Status))
            column_prop.CalculationMode = \
                AttributeUtil.get_enum_id_from_string(cast(int, build_ele.CalculationMode.attribute_id),
                                                      build_ele.CalculationMode.get_unique_value(column_prop.CalculationMode))

            if build_ele.IsSurface.get_unique_value(column_prop.Surface.strip() != ""):
                column_prop.Surface = build_ele.SurfaceName.get_unique_value(column_prop.Surface)

            column_ele.Properties = column_prop


            #----------------- add the placement point and create the element

            if column_prop.ShapeType == AllplanArchEle.ShapeType.ePolygonal:
                column_ele.PlacementPoint = column_prop.ShapePolygon.GetStartPoint()

            model_ele_list.append(column_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            handles
        """

        handle_list = HandleList()

        for column_data in self.columns:
            column_ele  = column_data.element
            column_prop = column_ele.Properties

            match column_prop.ShapeType:
                case AllplanArchEle.ShapeType.eRectangular:
                    ShapeHandleCreator.rect_by_center(handle_list, column_ele.GetPlacementPoint().To3D,
                                                      column_prop.Angle, column_prop.Width, column_prop.Depth,
                                                      "Width", "Depth", column_data.adapter_element)

                case AllplanArchEle.ShapeType.eCircular |   \
                     AllplanArchEle.ShapeType.eRegularPolygonInscribed |    \
                     AllplanArchEle.ShapeType.eRegularPolygonCircumscribed:
                    HandleCreator.point_distance(handle_list, "Radius",
                                                 column_ele.GetPlacementPoint().To3D + AllplanGeo.Vector3D(column_prop.Radius, 0, 1),
                                                 column_ele.GetPlacementPoint().To3D,
                                                 owner_element = column_data.adapter_element)

                case AllplanArchEle.ShapeType.ePolygonal:
                    CurveHandlesCreator.poly_curve(handle_list, "", column_data.additional_data, True,
                                                  delete_point  = True,
                                                  owner_element = column_data.adapter_element)


        return handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        build_ele = self.build_ele

        if not self.columns.is_modified:
            self.hide_ele_service.hide_elements(self.columns.adapter_elements)

        column = self.columns.get_element(handle_prop.owner_element)

        column_prop = column.Properties

        if RectangleHandleModification.is_rect_handle(handle_prop):
            column.PlacementPoint, build_ele.Width.value, build_ele.Depth.value = \
                RectangleHandleModification.get_center_and_sizes(handle_prop, input_pnt.To2D, column.PlacementPoint,
                                                                column_prop.Angle, column_prop.Width, column_prop.Depth)
        else:
            HandlePropertiesService.update_property_value(build_ele, handle_prop, input_pnt)

        self.columns.set_handle_modification(handle_prop.owner_element)


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

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return False

        if not self.columns.is_modified:
            self.hide_ele_service.hide_elements(self.columns.adapter_elements)

        self.columns.set_property_modification()


        #----------------- start a polygon input

        if name == "Shape" and build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
            AllplanIFW.HandleService().RemoveHandles()
            AllplanIFW.BuildingElementInputControls().CloseControls()

            self.script_object_interactor = PolygonInteractor(self.polygon_result, build_ele.CommonProp.value,
                                                              False, False)

            self.script_object_interactor.start_input(self.coord_input)

            build_ele.InputMode.value = build_ele.COLUMN_PLACEMENT

        return False


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT


        #----------------- cancel the polygon or placement input

        if build_ele.InputMode.value == build_ele.COLUMN_PLACEMENT:
            if self.script_object_interactor is not None and build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                self.script_object_interactor.on_cancel_function()

                for column_data in self.columns:
                    column_data.additional_data = AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1]

                return OnCancelFunctionResult.CONTINUE_INPUT

            return OnCancelFunctionResult.RESTART

        #----------------- modify the elements

        if self.columns.is_modified:
            self.create_column_elements()

            AllplanBaseEle.ModifyElements(self.document, self.columns.get_modified_elements())

        self.hide_ele_service.show_elements()

        AllplanIFW.HandleService().RemoveHandles()
        AllplanIFW.BuildingElementInputControls().CloseControls()

        return OnCancelFunctionResult.RESTART
