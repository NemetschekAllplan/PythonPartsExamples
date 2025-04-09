""" Example Script for the window opening
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

from ParameterUtils.OpeningSymbolsPropertiesParameterUtil import OpeningSymbolsPropertiesParameterUtil
from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifySlabOpeningBuildingElement import ModifySlabOpeningBuildingElement
else:
    ModifySlabOpeningBuildingElement = BuildingElement

print('Load ModifySlabOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\ModifyObjects\ModifySlabOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifySlabOpening(build_ele, script_object_data)


class ModifySlabOpening(BaseScriptObject):
    """ Definition of class ModifySlabOpening
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

        self.slab_opening_sel_result = SingleElementSelectResult()
        self.polygon_result          = PolygonInteractorResult()

        self.build_ele = cast(ModifySlabOpeningBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.slab_adapter_ele     = AllplanEleAdapter.BaseElementAdapter()
        self.placement_pnt        = AllplanGeo.Point3D()
        self.common_prop          = AllplanBaseEle.CommonProperties()
        self.shape_type           = self.build_ele.Shape.value
        self.shape_polygon        = AllplanGeo.Polygon2D()
        self.shape_geo_param_util = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())
        self.hide_ele_service     = HideElementsService()
        self.opening_ele          = AllplanArchEle.SlabOpeningElement()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.slab_opening_sel_result,
                                                                      [AllplanEleAdapter.SlabOpening_TypeUUID,
                                                                       AllplanEleAdapter.SlabRecess_TypeUUID],
                                                                      "Select the slab opening/recess")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        last_input_mode = build_ele.InputMode.value

        build_ele.InputMode.value = build_ele.OPENING_INPUT

        self.script_object_interactor = None

        if last_input_mode == build_ele.OPENING_PLACEMENT:
            return


        #----------------- get the opening element

        self.opening_ele = cast(AllplanArchEle. SlabOpeningElement, AllplanBaseEle.GetElement(self.slab_opening_sel_result.sel_element))

        self.placement_pnt = self.opening_ele.GetPlacementPoint().To3D

        self.slab_adapter_ele = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(
                                    self.slab_opening_sel_result.sel_element)

        slab_ele = cast(AllplanArchEle.SlabElement, AllplanBaseEle.GetElement(self.slab_adapter_ele))

        self.slab_plane_ref = slab_ele.Properties.PlaneReferences

        self.common_prop = self.slab_adapter_ele.GetCommonProperties()


        #----------------- get the properties

        opening_props = self.opening_ele.Properties

        self.shape_geo_param_util.set_parameter_values(build_ele, opening_props, "", self.shape_polygon)

        build_ele.HeightSettings.value              = self.opening_ele.Properties.PlaneReferences
        build_ele.HasIndependent2DInteraction.value = opening_props.Independent2DInteraction

        build_ele.OpeningType.value = "Opening" if opening_props.GetOpeningType() == AllplanArchEle.SlabOpeningType.eOpening else "Recess"

        OpeningSymbolsPropertiesParameterUtil.set_parameter_values(build_ele, opening_props.GetOpeningSymbolsProperties(), "")


        #----------------- start the opening modification

        self.hide_ele_service.hide_element(self.slab_opening_sel_result.sel_element)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_opening_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele =  self.build_ele


        #----------------- create the properties

        opening_type = AllplanArchEle.SlabOpeningType.eOpening if build_ele.OpeningType.value == "Opening" else \
                       AllplanArchEle.SlabOpeningType.eRecess

        opening_props = AllplanArchEle.SlabOpeningProperties(opening_type)

        self.shape_geo_param_util.create_shape_geo_properties(build_ele, opening_props, self.shape_polygon)

        opening_props.PlaneReferences  = build_ele.HeightSettings.value
        opening_props.CommonProperties = self.common_prop

        opening_props.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value

        OpeningSymbolsPropertiesParameterUtil.create_opening_symbols_properties(build_ele, "", opening_props.GetOpeningSymbolsProperties())

        self.opening_ele.Properties     = opening_props
        self.opening_ele.PlacementPoint = self.placement_pnt.To2D - self.shape_geo_param_util.get_reference_point(build_ele)


        #----------------- create the element

        model_ele_list = ModelEleList()

        model_ele_list.append(self.opening_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            handles
        """

        build_ele = self.build_ele

        handle_list = []

        if build_ele.Shape.value != AllplanArchEle.ShapeType.ePolygonal:
            HandleCreator.move(handle_list, "PlacementPoint", self.placement_pnt)

        return handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        match handle_prop.handle_id:
            case "PlacementPoint":
                self.placement_pnt = input_pnt


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        if build_ele.InputMode.value == build_ele.OPENING_PLACEMENT:
            if self.script_object_interactor is not None and build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                self.script_object_interactor.on_cancel_function()

                self.shape_polygon = AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1]

                return OnCancelFunctionResult.CONTINUE_INPUT

            return OnCancelFunctionResult.RESTART

        self.hide_ele_service.show_elements()

        AllplanBaseEle.ModifyElements(self.document, self.create_opening_element())

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
                    self.script_object_interactor = PolygonInteractor(self.polygon_result, self.common_prop,
                                                                      False, False)

                    self.script_object_interactor.start_input(self.coord_input)

                    build_ele.InputMode.value = build_ele.OPENING_PLACEMENT

                self.shape_type = build_ele.Shape.value

            case "HeightSettings" | "HeightSettings.Height":
                build_ele.UseBottomLevelOfSlab.value = self.slab_plane_ref.GetAbsBottomElevation() == \
                                                       build_ele.HeightSettings.value.GetAbsBottomElevation()

                build_ele.UseTopLevelOfSlab.value = self.slab_plane_ref.GetAbsTopElevation() == \
                                                    build_ele.HeightSettings.value.GetAbsTopElevation()

                return True

            case "UseBottomLevelOfSlab":
                if value:
                    build_ele.HeightSettings.value.SetAbsBottomElevation(self.slab_plane_ref.GetAbsBottomElevation())
                else:
                    build_ele.UseBottomLevelOfSlab.value = self.slab_plane_ref.GetAbsBottomElevation() == \
                                                        build_ele.HeightSettings.value.GetAbsBottomElevation()

                return True

            case "UseTopLevelOfSlab":
                if value:
                    build_ele.HeightSettings.value.SetAbsTopElevation(self.slab_plane_ref.GetAbsTopElevation())
                else:
                    build_ele.UseTopLevelOfSlab.value = self.slab_plane_ref.GetAbsTopElevation() == \
                                                        build_ele.HeightSettings.value.GetAbsTopElevation()


                return True

            case "OpeningType":
                build_ele.HeightSettings.value = AllplanArchEle.PlaneReferences(self.slab_plane_ref)

                return True

        return False
