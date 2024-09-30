""" Example Script for the general opening
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil
from ParameterUtils.OpeningSymbolsPropertiesParameterUtil import OpeningSymbolsPropertiesParameterUtil

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil

from .OpeningBase import OpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeneralOpeningBuildingElement import GeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load GeneralOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\GeneralOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return GeneralOpening(build_ele, script_object_data)


class GeneralOpening(OpeningBase):
    """ Definition of class GeneralOpening
    """

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = ArchPointInteractor(self.arch_pnt_result,
                                                            ArchitectureElementsQueryUtil.create_arch_general_opening_elements_query(),
                                                            "Set properties or click a component line",
                                                            self.draw_placement_preview)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = self.build_ele


        #----------------- create the properties

        opening_prop = AllplanArchEle.GeneralOpeningProperties(
            AllplanArchEle.OpeningType.eNiche if build_ele.NicheType.value == "Niche" else \
            AllplanArchEle.OpeningType.eRecess)

        opening_prop.VisibleInViewSection3D   = build_ele.IsVisibleInViewSection3D.value
        opening_prop.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value
        opening_prop.PlaneReferences          = build_ele.HeightSettings.value

        self.opening_geo_param_util.create_opening_geo_properties(build_ele, opening_prop.GetGeometryProperties())

        OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())

        OpeningSymbolsPropertiesParameterUtil.create_opening_symbols_properties(build_ele, "", opening_prop.GetOpeningSymbolsProperties())


        #----------------- create the opening

        if not AllplanEleAdapter.AxisElementAdapter(self.general_ele).IsNull():
            self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_axis_element(self.opening_start_pnt.To2D,
                                                                                                build_ele.Width.value,
                                                                                                self.general_ele_axis,
                                                                                                self.general_ele_geo,
                                                                                                self.placement_line).To3D
        else:
            self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_shaped_element(self.opening_start_pnt.To2D,
                                                                                                 build_ele.Width.value,
                                                                                                 self.placement_line).To3D

        opening_ele = AllplanArchEle.GeneralOpeningElement(opening_prop, self.general_ele,
                                                           self.opening_start_pnt.To2D,
                                                           self.opening_end_pnt.To2D,
                                                           build_ele.InputMode.value == build_ele.ELEMENT_SELECT)

        model_ele_list = ModelEleList()

        model_ele_list.append(opening_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        build_ele = self.build_ele

        bottom_pnt = AllplanGeo.Point3D(0, 0,
                                        build_ele.HeightSettings.value.AbsBottomElevation - build_ele.HeightSettings.value.BottomElevation)

        opening_start_pnt = self.opening_start_pnt + bottom_pnt
        opening_end_pnt   = self.opening_end_pnt + bottom_pnt

        handle_list : list[HandleProperties] = []


        #----------------- width input controls

        HandleCreator.point_distance(handle_list, "Width", opening_end_pnt, opening_start_pnt,
                                     show_handles = False, input_field_above = False)

        depth = build_ele.Depth.value or build_ele.ElementThickness.value


        #----------------- create the depth handle

        if isinstance(self.general_ele_axis, AllplanGeo.Line2D):
            x_start = AllplanGeo.TransformCoord.PointLocal(self.placement_line, opening_start_pnt).X

            depth_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_line, AllplanGeo.Point2D(x_start, depth))

            HandleCreator.point_distance(handle_list, "Depth", depth_pnt + bottom_pnt, opening_start_pnt)

        elif isinstance(self.general_ele_axis, AllplanGeo.Arc2D):
            x_start = AllplanGeo.TransformCoord.PointLocal(self.placement_arc, opening_start_pnt).X

            depth_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_arc, AllplanGeo.Point2D(x_start, depth))

            depth_ref_pnt = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_arc, opening_start_pnt)[1]

            HandleCreator.point_distance(handle_list, "Depth", depth_pnt + bottom_pnt, bottom_pnt + depth_ref_pnt)

        else:
            _, segment_line = AllplanGeo.Polyline2DUtil.GetPolyline2DSegment(AllplanGeo.Polyline2D(self.general_ele_geo.Points),
                                                                             opening_start_pnt.To2D)

            x_start = AllplanGeo.TransformCoord.PointLocal(segment_line, opening_start_pnt).X

            depth_pnt = AllplanGeo.TransformCoord.PointGlobal(segment_line, AllplanGeo.Point2D(x_start, depth))

            HandleCreator.point_distance(handle_list, "Depth", depth_pnt + bottom_pnt, opening_start_pnt)

        self.create_opening_handles(handle_list)

        return handle_list
