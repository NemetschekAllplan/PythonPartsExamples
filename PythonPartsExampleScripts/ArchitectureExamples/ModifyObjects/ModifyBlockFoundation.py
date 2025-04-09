""" Example Script for the Block foundation modification
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
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

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService
from Utils.General.AttributeUtil import AttributeUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyBlockFoundationBuildingElement import ModifyBlockFoundationBuildingElement
else:
    ModifyBlockFoundationBuildingElement = BuildingElement

print('Load ModifyBlockFoundation.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\ModifyObjects\ModifyBlockFoundation.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifyBlockFoundation(build_ele, script_object_data)


class ModifyBlockFoundation(BaseScriptObject):
    """ Definition of class ModifyBlockFoundation
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

        self.blockfound_sel_result  = SingleElementSelectResult()

        self.build_ele = cast(ModifyBlockFoundationBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.placement_pnt        = AllplanGeo.Point3D()
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())
        self.hide_ele_service     = HideElementsService()
        self.blockfound_ele       = AllplanArchEle.BlockFoundationElement()
        self.shape_polygon        = AllplanGeo.Polygon2D()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.blockfound_sel_result,
                                                                      [AllplanEleAdapter.IndividualFoundation_TypeUUID],
                                                                      "Select the block foundation")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        build_ele.InputMode.value = build_ele.BLOCKFOUNDATION_INPUT

        self.script_object_interactor = None


        #----------------- get the block foundation element

        self.blockfound_ele = cast(AllplanArchEle.BlockFoundationElement, AllplanBaseEle.GetElement(self.blockfound_sel_result.sel_element))

        self.placement_pnt = self.blockfound_ele.GetPlacementPoint().To3D

        #----------------- get the properties

        blockfound_properties = self.blockfound_ele.Properties

        build_ele.WallPlaneRef.value    = blockfound_properties.PlaneReferences
        build_ele.CommonProp.value      = blockfound_properties.CommonProperties
        build_ele.SurfaceElemProp.value = blockfound_properties.SurfaceElementProperties
        build_ele.IsSurface.value       = blockfound_properties.Surface.strip() != ""
        build_ele.SurfaceName.value     = blockfound_properties.Surface
        build_ele.Trade.value           = blockfound_properties.Trade
        build_ele.Priority.value        = blockfound_properties.Priority
        build_ele.Factor.value          = blockfound_properties.Factor

        build_ele.CalculationMode.value = AttributeUtil.get_enum_value_string_from_id(build_ele.CalculationMode,
                                                                                      blockfound_properties.CalculationMode)

        #--------- Define properties specific to a block foundation
        if blockfound_properties.ShapeType == AllplanArchEle.ShapeType.eRectangular:
            build_ele.ShapeType.value        = "eRectangular"
            build_ele.Width.value            = blockfound_properties.Width
            build_ele.Depth.value            = blockfound_properties.Depth
        if blockfound_properties.ShapeType == AllplanArchEle.ShapeType.eUnknown: #has to be rectangular
            build_ele.ShapeType.value        = "eRectangular"
            build_ele.Width.value            = blockfound_properties.Width
            build_ele.Depth.value            = blockfound_properties.Width
        if blockfound_properties.ShapeType == AllplanArchEle.ShapeType.eCircular:
            build_ele.ShapeType.value        = "eCircular"
            build_ele.Width.value            = blockfound_properties.Width
        if blockfound_properties.ShapeType == AllplanArchEle.ShapeType.eConical:
            build_ele.ShapeType.value        = "eConical"
            build_ele.VouteBack.value        = blockfound_properties.VouteBack
            build_ele.VouteFront.value       = blockfound_properties.VouteFront
            build_ele.VouteLeft.value        = blockfound_properties.VouteLeft
            build_ele.VouteRight.value       = blockfound_properties.VouteRight
            build_ele.Width.value            = blockfound_properties.Width
            build_ele.Depth.value            = blockfound_properties.Depth
        if blockfound_properties.ShapeType == AllplanArchEle.ShapeType.ePolygonal:
            build_ele.ShapeType.value        = "ePolygonal"
            build_ele.ProfilePoints.value    = blockfound_properties.ShapePolygon.Points

        self.hide_ele_service.hide_element(self.blockfound_sel_result.sel_element)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_blockfound_element(), self.create_handles(),
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D())


    def create_blockfound_element(self) -> ModelEleList:
        """ create the block foundation element


        Returns:
            list with the elements
        """

        build_ele =  self.build_ele

        #----------------- create the properties

        blockfound_properties = AllplanArchEle.BlockFoundationProperties()

        blockfound_properties.VouteBack       = build_ele.VouteBack.value
        blockfound_properties.VouteFront      = build_ele.VouteFront.value
        blockfound_properties.VouteLeft       = build_ele.VouteLeft.value
        blockfound_properties.VouteRight      = build_ele.VouteRight.value
        blockfound_properties.PlaneReferences = build_ele.WallPlaneRef.value
        blockfound_properties.Width           = build_ele.Width.value
        blockfound_properties.Depth           = build_ele.Depth.value
        blockfound_properties.CircleDivision  = 50

        #--------- Define properties specific to a block foundation
        if build_ele.ShapeType.value == "eRectangular": # pylint:disable=magic-value-comparison
            blockfound_properties.ShapeType = AllplanArchEle.ShapeType.eRectangular
        if build_ele.ShapeType.value == "eCircular": # pylint:disable=magic-value-comparison
            blockfound_properties.ShapeType = AllplanArchEle.ShapeType.eCircular
        if build_ele.ShapeType.value == "ePolygonal": # pylint:disable=magic-value-comparison
            blockfound_properties.ShapeType = AllplanArchEle.ShapeType.ePolygonal
        if build_ele.ShapeType.value == "eConical": # pylint:disable=magic-value-comparison
            blockfound_properties.ShapeType = AllplanArchEle.ShapeType.eConical

        blockfound_properties.CommonProperties         = build_ele.CommonProp.value
        blockfound_properties.SurfaceElementProperties = build_ele.SurfaceElemProp.value
        blockfound_properties.Trade                    = build_ele.Trade.value
        blockfound_properties.Priority                 = build_ele.Priority.value
        blockfound_properties.Factor                   = build_ele.Factor.value
        blockfound_properties.CalculationMode          = AttributeUtil.get_enum_id_from_value_string(build_ele.CalculationMode)
        profile_points                                  = self.build_ele.ProfilePoints.value

        blockfound_properties.SetShapePolygon(AllplanGeo.Polygon2D(profile_points))

        if build_ele.IsSurface.value:
            blockfound_properties.Surface = build_ele.SurfaceName.value

        self.blockfound_ele.Properties = blockfound_properties

        #----------------- add the placement point and create the element
        if blockfound_properties.ShapeType == AllplanArchEle.ShapeType.ePolygonal:
            self.blockfound_ele.PlacementPoint = blockfound_properties.GetShapePolygon().GetStartPoint()
        else:
            self.blockfound_ele.PlacementPoint = self.placement_pnt.To2D

        model_ele_list = ModelEleList()

        model_ele_list.append(self.blockfound_ele)

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
                    input_pnt  : AllplanGeo.Point3D):
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


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        self.hide_ele_service.show_elements()

        AllplanBaseEle.ModifyElements(self.document, self.create_blockfound_element())

        AllplanIFW.HandleService().RemoveHandles()

        return OnCancelFunctionResult.RESTART
