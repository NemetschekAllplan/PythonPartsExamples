""" Example Script for get flush pier data
"""

from __future__ import annotations
from pathlib    import Path

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HideElementsService import HideElementsService

from ArchitectureExamples.ModifyObjects.ModifyOpeningBase import ModifyOpeningBase

from Utils.General.AttributeUtil import AttributeUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GetFlushPierDataBuildingElement import GetFlushPierDataBuildingElement
else:
    GetFlushPierDataBuildingElement = BuildingElement

print('Load GetFlushPierData.py')

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
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
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

    return GetFlushPierData(build_ele, script_object_data)


class GetFlushPierData(ModifyOpeningBase):
    """ Definition of class GetFlushPierData
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(build_ele, script_object_data)

        self.flush_pier_sel_result = SingleElementSelectResult()

        self.build_ele = cast(GetFlushPierDataBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.placement_pnt        = AllplanGeo.Point3D()
        self.shape_polygon        = AllplanGeo.Polygon2D()
        self.shape_geo_param_util = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())
        self.hide_ele_service     = HideElementsService()
        self.flush_pier_ele       = AllplanArchEle.FlushPierElement()

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.flush_pier_sel_result,
                                                                      [AllplanEleAdapter.FlushPier_TypeUUID,
                                                                       AllplanEleAdapter.FlushPierTier_TypeUUID],
                                                                      "Select the flush pier")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        last_input_mode = build_ele.InputMode.value

        build_ele.InputMode.value = build_ele.JOINT_INPUT

        self.script_object_interactor = None

        if last_input_mode == build_ele.JOINT_PLACEMENT:
            return

        #----------------- get the flush pier element
        self.flush_pier_ele = cast(AllplanArchEle.FlushPierElement, AllplanBaseEle.GetElement(self.flush_pier_sel_result.sel_element))

        #----------------- get the properties

        flush_pier_properties = self.flush_pier_ele.Properties
        
        build_ele.PlaneReferences.value       = flush_pier_properties.PlaneReferences
        build_ele.Width.value                 = flush_pier_properties.Width
        build_ele.StartPoint.value            = self.flush_pier_ele.GetStartPoint()
        build_ele.EndPoint.value              = self.flush_pier_ele.GetEndPoint()
        
        build_ele.SurfaceElemProp.value       = flush_pier_properties.SurfaceElementProperties
        build_ele.IsSurface.value             = flush_pier_properties.Surface.strip() != ""
        build_ele.SurfaceName.value           = flush_pier_properties.Surface
        build_ele.Trade.value                 = flush_pier_properties.Trade
        build_ele.Priority.value              = flush_pier_properties.Priority
        build_ele.CalculationMode.value       = AttributeUtil.get_enum_value_string_from_id(build_ele.CalculationMode,
                                                                                      flush_pier_properties.CalculationMode)

        build_ele.Material.value              = flush_pier_properties.Material

        #----------------- start the joint modification

        self.placement_ele = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(self.flush_pier_sel_result.sel_element)

    def modify_opening_element(self) -> list[ModelEleList]:

        """ modify the flush pier element


        Returns:
            list with the elements
        """
        return []

    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        return[]