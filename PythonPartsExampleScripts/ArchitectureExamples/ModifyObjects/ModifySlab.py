""" Example Script for slab modification
"""

from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, cast

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService


if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifySlabBuildingElement import ModifySlabBuildingElement
else:
    ModifySlabBuildingElement = BuildingElement

print('Load ModifySlab.py')

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

    script_path = Path(_build_ele.pyp_file_path) / Path(_build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")
    preview = LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path))

    return CreateElementResult(preview)

def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifySlab(build_ele, script_object_data)

class ModifySlab(BaseScriptObject):
    """ Definition of class ModifySlab
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

        self.slab_sel_result          = SingleElementSelectResult()
        self.build_ele                = cast(ModifySlabBuildingElement, build_ele)
        self.hide_ele_service         = HideElementsService()
        self.slab_element             = AllplanArchEle.SlabElement()
        self.reverse_offset_direction = False
        self.polygon                  = AllplanGeo.Polygon2D()

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.slab_sel_result,
                                                                      [AllplanEleAdapter.Slab_TypeUUID],
                                                                      "Select the slab")

    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.SLAB_SELECTED

        #----------------- get the slab element

        self.slab_element = cast(AllplanArchEle.SlabElement, AllplanBaseEle.GetElement(self.slab_sel_result.sel_element))

        self.polygon       = self.slab_element.GetGeometryObject()

        #----------------- get the properties
        slab_props = self.slab_element.Properties


        build_ele.TierCount.value       = slab_props.TierCount
        build_ele.PlaneReferences.value = slab_props.PlaneReferences
        build_ele.VariableTier.value    = slab_props.VariableTier

        calc_modes = ["m³","m²","m","Pcs","kg"]

        #----------------- loop through tiers and assign new list
        build_ele.CommonProp.value      = [slab_props.GetSlabTierProperties(iCnt).CommonProperties for iCnt in range(slab_props.TierCount)]
        build_ele.SurfaceElemProp.value = [slab_props.GetSlabTierProperties(iCnt).SurfaceElementProperties for iCnt in range(slab_props.TierCount)]    # pylint:disable=line-too-long
        build_ele.Thickness.value       = [slab_props.GetSlabTierProperties(iCnt).Thickness for iCnt in range(slab_props.TierCount)]
        build_ele.Trade.value           = [slab_props.GetSlabTierProperties(iCnt).Trade for iCnt in range(slab_props.TierCount)]
        build_ele.Priority.value        = [slab_props.GetSlabTierProperties(iCnt).Priority for iCnt in range(slab_props.TierCount)]
        build_ele.CalculationMode.value = [calc_modes[slab_props.GetSlabTierProperties(iCnt).CalculationMode] for iCnt in range(slab_props.TierCount)]     # pylint:disable=line-too-long
        build_ele.Factor.value          = [slab_props.GetSlabTierProperties(iCnt).Factor for iCnt in range(slab_props.TierCount)]
        build_ele.IsSurface.value       = [slab_props.GetSlabTierProperties(iCnt).Surface.strip() != "" for iCnt in range(slab_props.TierCount)]     # pylint:disable=line-too-long
        build_ele.SurfaceName.value     = [slab_props.GetSlabTierProperties(iCnt).Surface for iCnt in range(slab_props.TierCount)]

        parent_elem = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(self.slab_sel_result.sel_element)

        self.hide_ele_service.hide_element(parent_elem)

    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_slab_element(),self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())

    def create_slab_element(self) -> ModelEleList:
        """ create the slab element


        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        #----------------- create the properties
        slab_props                          = AllplanArchEle.SlabProperties()
        slab_props.TierCount                = build_ele.TierCount.value
        slab_props.PlaneReferences          = build_ele.PlaneReferences.value
        slab_props.VariableTier             = build_ele.VariableTier.value
       

        calc_modes = ["m³","m²","m","Pcs","kg"]

        #----------------- loop through tiers
        for tier in range(slab_props.TierCount):
            slab_props.GetSlabTierProperties(tier).CommonProperties         = build_ele.CommonProp.value[tier]
            slab_props.GetSlabTierProperties(tier).SurfaceElementProperties = build_ele.SurfaceElemProp.value[tier]
            slab_props.GetSlabTierProperties(tier).Thickness                = build_ele.Thickness.value[tier]
            slab_props.GetSlabTierProperties(tier).Trade                    = build_ele.Trade.value[tier]
            slab_props.GetSlabTierProperties(tier).Priority                 = build_ele.Priority.value[tier]
            slab_props.GetSlabTierProperties(tier).CalculationMode          = calc_modes.index(self.build_ele.CalculationMode.value[tier])
            slab_props.GetSlabTierProperties(tier).Factor                   = build_ele.Factor.value[tier]

        self.slab_element.Properties = slab_props

        #----------------- create the element

        model_ele_list = ModelEleList()

        model_ele_list.append(self.slab_element)

        return model_ele_list

    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            handles
        """

        handle_list = []

        HandleCreator.move(handle_list, "PlacementPointStart", (self.polygon.StartPoint.To3D))
        #HandleCreator.move(handle_list, "PlacementPointEnd", (self.axis.EndPoint.To3D))

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
            case "PlacementPointStart":
                self.polygon.StartPoint = input_pnt.To2D
                self.polygon.EndPoint = input_pnt.To2D



        return self.execute()

    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        self.hide_ele_service.show_elements()

        if self.slab_sel_result != SingleElementSelectResult():
            AllplanBaseEle.ModifyElements(self.document, self.create_slab_element())

        return OnCancelFunctionResult.CANCEL_INPUT

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
        match name:
            case "TierCount":

                slab_props = AllplanArchEle.SlabProperties()
                slab_props.PlaneReferences = self.build_ele.PlaneReferences.value

                height = 0.0

                for tier in range(value):
                    height = height + self.build_ele.Thickness.value[tier]

                plane_ref = slab_props.GetPlaneReferences()
                plane_ref.SetHeight(height)

                self.build_ele.PlaneReferences.value = plane_ref

                return True
            
            case "VariableTier":

                old_variable_tier = self.slab_element.GetProperties().GetVariableTier() -1
                old_thickness    = self.build_ele.Thickness.value[value-1]

                self.build_ele.Thickness.value[value-1] = self.build_ele.Thickness.value[old_variable_tier]
                self.build_ele.Thickness.value[old_variable_tier] = old_thickness
                return True
              
            case "PlaneReferences.Height":

                height = 0.0
                variable_tier = self.build_ele.VariableTier.value
                tier_count = self.build_ele.TierCount.value

                for tier in range(tier_count):
                    if tier != variable_tier:
                        height = height + self.build_ele.Thickness.value[tier]
                        
                self.build_ele.Thickness.value[variable_tier-1] = value - height

                return True

            case s if s.startswith('Thickness'):

                height = 0.0

                slab_props = AllplanArchEle.SlabProperties()
                slab_props.PlaneReferences = self.build_ele.PlaneReferences.value

                tier_count = self.build_ele.TierCount.value

                for tier in range(tier_count):
                    height = height + self.build_ele.Thickness.value[tier]

                plane_ref = slab_props.GetPlaneReferences()
                plane_ref.SetHeight(height)

                self.build_ele.PlaneReferences.value = plane_ref

        return False
