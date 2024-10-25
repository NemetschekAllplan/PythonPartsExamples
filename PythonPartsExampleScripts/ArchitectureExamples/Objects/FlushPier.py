""" Example Script for the Flush Pier
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil
from Utils.Architecture.OpeningHandlesUtil import OpeningHandlesUtil
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

from .OpeningBase import OpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.FlushPierBuildingElement import FlushPierBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load FlushPier.py')

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
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ArchitectureExamples\Objects\FlushPier.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return FlushPier(build_ele, script_object_data) # type: ignore


class FlushPier(OpeningBase):
    """ Definition of class FlushPier
    """

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = ArchPointInteractor(self.arch_pnt_result,
                                                            ArchitectureElementsQueryUtil.create_arch_door_window_opening_elements_query(),
                                                            "Set properties or click a component line",
                                                            self.draw_placement_preview)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = cast(BuildingElement, self.build_ele)

        #----------------- create the properties

        self.set_flush_pier_properties()

        #----------------- create the Flush Pier

        self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_axis_element(self.opening_start_pnt.To2D,
                                                                                            build_ele.Width.value,
                                                                                            self.placement_ele_axis,
                                                                                            self.placement_ele_geo,
                                                                                            self.placement_line).To3D

        flush_pier_ele = AllplanArchEle.FlushPierElement(self.flush_pier_prop, self.placement_ele,
                                                           self.opening_start_pnt.To2D,
                                                           self.opening_end_pnt.To2D,
                                                           build_ele.InputMode.value == build_ele.ELEMENT_SELECT)


        if build_ele.SetFormatProperties.value:
            flush_pier_ele.CommonProperties = build_ele.CommonProp.value

        model_ele_list = ModelEleList()
        model_ele_list.append(flush_pier_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        build_ele = self.build_ele

        bottom_pnt = AllplanGeo.Point3D(0, 0,
                                        build_ele.HeightSettings.value.AbsBottomElevation - build_ele.HeightSettings.value.BottomElevation)

        handle_list : list[HandleProperties] = []

        OpeningHandlesUtil.create_opening_handles(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                                                  self.offset_start_pnt, self.offset_end_pnt,
                                                  self.placement_ele_axis, self.placement_arc, self.input_field_above, bottom_pnt,
                                                  handle_list)

        return handle_list


    def set_flush_pier_properties(self):
        """ set the wall properties """

        build_ele = cast(BuildingElement, self.build_ele)

        flush_pier_prop = AllplanArchEle.FlushPierProperties()

        flush_pier_prop.Width = build_ele.Width.value
        flush_pier_prop.PlaneReferences = build_ele.HeightSettings.value

        flush_pier_prop.Trade = build_ele.Trade.value
        flush_pier_prop.Priority = build_ele.Priority.value

        calculation_mode_id = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(build_ele.CalculationMode.attribute_id,
                                                                                       build_ele.CalculationMode.value)
        flush_pier_prop.CalculationMode = calculation_mode_id

        flush_pier_prop.Material = build_ele.Material.value

        status_id = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(build_ele.Status.attribute_id, build_ele.Status.value)
        flush_pier_prop.Status = status_id

        flush_pier_prop.SurfaceElementProperties = build_ele.SurfaceElemProp.value

        if build_ele.IsSurface.value:
            flush_pier_prop.Surface = build_ele.SurfaceName.value

        self.flush_pier_prop = flush_pier_prop
