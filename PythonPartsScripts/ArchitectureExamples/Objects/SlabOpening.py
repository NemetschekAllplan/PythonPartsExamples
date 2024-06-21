""" Example Script for the window opening
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.OpeningSymbolsPropertiesParameterUtil import OpeningSymbolsPropertiesParameterUtil
from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SlabOpeningBuildingElement import SlabOpeningBuildingElement
else:
    SlabOpeningBuildingElement = BuildingElement

print('Load SlabOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\SlabOpening.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return SlabOpening(build_ele, coord_input)


class SlabOpening(BaseScriptObject):
    """ Definition of class SlabOpening
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.slab_sel_result          = SingleElementSelectResult()
        self.opening_placement_result = PointInteractorResult()
        self.polygon_result           = PolygonInteractorResult()

        self.build_ele = cast(SlabOpeningBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.slab_adapter_ele     = AllplanEleAdapter.BaseElementAdapter()
        self.placement_pnt        = AllplanGeo.Point3D()
        self.common_prop          = AllplanBaseEle.CommonProperties()
        self.shape_type           = self.build_ele.Shape.value
        self.shape_geo_param_util = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value == build_ele.OPENING_INPUT:
            self.start_next_input()

            return

        self.script_object_interactor = SingleElementSelectInteractor(self.slab_sel_result,
                                                                      [AllplanEleAdapter.Slab_TypeUUID],
                                                                      "Select the slab")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele


        #----------------- start the opening placement

        if build_ele.InputMode.value in (build_ele.ELEMENT_SELECT, build_ele.OPENING_INPUT):
            self.slab_adapter_ele = self.slab_sel_result.sel_element

            if self.slab_adapter_ele is None:
                return

            build_ele.InputMode.value = build_ele.OPENING_PLACEMENT

            slab_ele = cast(AllplanArchEle.SlabElement, AllplanBaseEle.GetElement(self.slab_adapter_ele))

            self.slab_plane_ref = slab_ele.Properties.PlaneReferences

            self.build_ele.HeightSettings.value = AllplanArchEle.PlaneReferences(self.slab_plane_ref)
            self.common_prop                    = slab_ele.Properties.CommonProperties

            if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                self.script_object_interactor = PolygonInteractor(self.polygon_result, self.common_prop,
                                                                  False, False)
            else:
                self.script_object_interactor = PointInteractor(self.opening_placement_result, True,
                                                                "Placement point", self.draw_opening_preview)

            return


        #----------------- start the opening modification

        build_ele.InputMode.value = build_ele.OPENING_INPUT

        self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_opening_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def draw_opening_preview(self):
        """ draw the opening preview
        """

        self.placement_pnt = self.opening_placement_result.input_point

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(),
                                          self.create_opening_element(), False, None)


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

        self.shape_geo_param_util.create_shape_geo_properties(build_ele, opening_props,
                                                              AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1])

        opening_props.PlaneReferences = build_ele.HeightSettings.value

        opening_props.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value

        OpeningSymbolsPropertiesParameterUtil.create_opening_symbols_properties(build_ele, "", opening_props.GetOpeningSymbolsProperties())


        #----------------- create the element

        opening_props.CommonProperties = self.common_prop

        opening_ele = AllplanArchEle.SlabOpeningElement(opening_props,
                                                        self.placement_pnt.To2D - self.shape_geo_param_util.get_reference_point(build_ele),
                                                        self.slab_adapter_ele.GetModelElementUUID())

        model_ele_list = ModelEleList()

        model_ele_list.append(opening_ele)

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

        if build_ele.InputMode.value == build_ele.OPENING_PLACEMENT:
            if self.script_object_interactor is not None and build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                self.script_object_interactor.on_cancel_function()

                return OnCancelFunctionResult.CONTINUE_INPUT

            return OnCancelFunctionResult.RESTART

        return OnCancelFunctionResult.CREATE_ELEMENTS


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
                build_ele.InputMode.value = build_ele.OPENING_PLACEMENT

                if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
                    self.script_object_interactor = PolygonInteractor(self.polygon_result, self.coord_input, self.common_prop,
                                                                    False, False)
                elif self.shape_type == AllplanArchEle.ShapeType.ePolygonal:
                    self.script_object_interactor = PointInteractor(self.opening_placement_result, True,
                                                                    "Placement point", self.draw_opening_preview)

                if self.script_object_interactor:
                    self.script_object_interactor.start_input(self.coord_input)

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
