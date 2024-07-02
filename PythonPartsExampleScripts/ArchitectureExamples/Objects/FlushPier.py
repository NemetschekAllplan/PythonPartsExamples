""" Example Script for the Flush Pier
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator

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


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return FlushPier(build_ele, coord_input) # type: ignore


class FlushPier(OpeningBase):
    """ Definition of class FlushPier
    """

    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = cast(BuildingElement, self.build_ele)

        #----------------- create the properties

        self.set_flush_pier_properties()

        #----------------- create the Flush Pier

        self.create_opening_points()

        flush_pier_ele = AllplanArchEle.FlushPierElement(self.flush_pier_prop, self.general_ele,
                                                           self.opening_start_pnt.To2D,
                                                           self.opening_end_pnt.To2D,
                                                           build_ele.InputMode.value == build_ele.ELEMENT_SELECT)

        model_ele_list = ModelEleList()
        model_ele_list.append(flush_pier_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        opening_start_pnt = self.opening_start_pnt
        opening_end_pnt   = self.opening_end_pnt

        handle_list : list[HandleProperties] = []

        #----------------- width input controls

        HandleCreator.point_distance(handle_list, "Width", opening_end_pnt, opening_start_pnt,
                                     show_handles = False, input_field_above = False)

        self.create_opening_handles(handle_list)

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
         #--flush_pier_prop.Status = build_ele.Status.value

        status_id = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(build_ele.Status.attribute_id, build_ele.Status.value)
        flush_pier_prop.Status = status_id

        flush_pier_prop.SetShowAreaElementInGroundView(build_ele.ShowAreaElementInGroundView.value)
        flush_pier_prop.SetHatch(0)
        flush_pier_prop.SetPattern(0)
        flush_pier_prop.SetFaceStyle(0)

        use_background_color_instead_of_filling = False

        if build_ele.IsHatch.value:
            flush_pier_prop.Hatch = build_ele.HatchId.value
            use_background_color_instead_of_filling = True

        elif build_ele.IsPattern.value:
            flush_pier_prop.SetPattern(build_ele.PatternId.value)
            use_background_color_instead_of_filling = True

        elif build_ele.IsFaceStyle.value:
            flush_pier_prop.SetFaceStyle(build_ele.FaceStyleId.value)
            use_background_color_instead_of_filling = True

        elif build_ele.IsBitmap.value:
            flush_pier_prop.BitmapName = build_ele.BitmapName.value

        if build_ele.IsFilling.value:
            if use_background_color_instead_of_filling:
                flush_pier_prop.SetBackgroundColor(build_ele.FillingId.value)
            else:
                flush_pier_prop.SetFilling(build_ele.FillingId.value)

        if build_ele.IsSurface.value:
            flush_pier_prop.Surface = build_ele.SurfaceName.value

        self.flush_pier_prop = flush_pier_prop
