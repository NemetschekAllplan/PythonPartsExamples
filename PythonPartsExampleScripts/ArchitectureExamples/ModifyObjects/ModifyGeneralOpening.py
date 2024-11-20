""" Example Script for the general opening
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

from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil
from ParameterUtils.OpeningSymbolsPropertiesParameterUtil import OpeningSymbolsPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil
from Utils.Architecture.OpeningHandlesUtil import OpeningHandlesUtil

from .ModifyOpeningBase import ModifyOpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyGeneralOpeningBuildingElement \
        import ModifyGeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ModifyGeneralOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\ModifyObjects\ModifyGeneralOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifyGeneralOpening(build_ele, script_object_data)


class ModifyGeneralOpening(ModifyOpeningBase):
    """ Definition of class ModifyGeneralOpening
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

        self.general_opening_ele = AllplanArchEle.GeneralOpeningElement()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.opening_sel_res,
                                                                      [AllplanEleAdapter.NicheTier_TypeUUID,
                                                                       AllplanEleAdapter.RecessTier_TypeUUID],
                                                                      "Select the niche/recess")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        if self.placement_line is None:
            return

        build_ele = self.build_ele


        #----------------- get the data of the opening

        self.general_opening_ele = cast(AllplanArchEle.GeneralOpeningElement, AllplanBaseEle.GetElement(self.opening_sel_res.sel_element))

        opening_prop = self.general_opening_ele.Properties

        self.opening_geo_param_util.set_parameter_values(build_ele, opening_prop.GetGeometryProperties(), opening_prop.PlaneReferences)

        OpeningSillPropertiesParameterUtil.set_parameter_values(build_ele, opening_prop.GetSillProperties(), "")
        OpeningSymbolsPropertiesParameterUtil.set_parameter_values(build_ele, opening_prop.GetOpeningSymbolsProperties(), "")

        self.opening_start_pnt = self.general_opening_ele.StartPoint.To3D
        self.opening_end_pnt   = self.general_opening_ele.EndPoint.To3D

        super().start_next_input()


    def modify_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = self.build_ele


        #----------------- create the properties

        opening_prop = self.general_opening_ele.Properties

        opening_prop.VisibleInViewSection3D   = build_ele.IsVisibleInViewSection3D.value
        opening_prop.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value
        opening_prop.PlaneReferences          = build_ele.HeightSettings.value

        self.opening_geo_param_util.create_opening_geo_properties(build_ele, opening_prop.GetGeometryProperties())

        OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())

        OpeningSymbolsPropertiesParameterUtil.create_opening_symbols_properties(build_ele, "", opening_prop.GetOpeningSymbolsProperties())


        #----------------- create the opening

        if not AllplanEleAdapter.AxisElementAdapter(self.placement_ele).IsNull():
            self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_axis_element(self.opening_start_pnt.To2D,
                                                                                               build_ele.Width.value,
                                                                                               self.placement_ele_axis,
                                                                                               self.placement_ele_geo,
                                                                                               self.placement_line).To3D
        else:
            self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_shaped_element(self.opening_start_pnt.To2D,
                                                                                                 build_ele.Width.value,
                                                                                                 self.placement_line).To3D

        self.general_opening_ele.Properties = opening_prop
        self.general_opening_ele.StartPoint = self.opening_start_pnt.To2D
        self.general_opening_ele.EndPoint   = self.opening_end_pnt.To2D

        model_ele_list = ModelEleList()

        model_ele_list.append(self.general_opening_ele)

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

        depth = build_ele.Depth.value or build_ele.ElementThickness.value

        OpeningHandlesUtil.create_opening_depth_handle(self.opening_start_pnt.To2D, self.placement_ele_axis, self.placement_ele_geo,
                                                       self.placement_line, self.placement_arc, bottom_pnt, depth, handle_list)

        OpeningHandlesUtil.create_opening_handles(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                                                  self.offset_start_pnt, self.offset_end_pnt,
                                                  self.placement_ele_axis, self.placement_arc, self.input_field_above, bottom_pnt,
                                                  handle_list)

        if (prop := build_ele.get_property("SmartSymbolGroup")) is not None and prop.value:
            self.opening_tier_center, self.opening_tier_ref_pnt = \
                OpeningHandlesUtil.create_opening_symbol_handles(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                                                                 build_ele.Width.value,
                                                                 build_ele.Depth.value, self.placement_ele, 1, False,
                                                                 build_ele.OpeningSymbolRefPntIndex.value,
                                                                 bottom_pnt, handle_list)

        return handle_list
