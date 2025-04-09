""" Example Script for the general opening
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor, ArchPointInteractorResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PolygonalGeneralOpeningBuildingElement \
        import PolygonalGeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PolygonalGeneralOpening.py')

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
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(
                               fr"{build_ele.pyp_file_path}\PolygonalGeneralOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PolygonalGeneralOpening(build_ele, script_object_data)


class PolygonalGeneralOpening(BaseScriptObject):
    """ Definition of class PolygonalGeneralOpening
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

        self.build_ele = build_ele

        self.polygon_result  = PolygonInteractorResult()
        self.arch_pnt_result = ArchPointInteractorResult()

        build_ele.InputMode.value = build_ele.POLYGON_INPUT

        self.placement_ele = AllplanEleAdapter.BaseElementAdapter()
        self.hide_ele      = HideElementsService()

        self.opening_polygon = AllplanGeo.Polygon2D()
        self.shape_pol       = AllplanGeo.Polygon2D()
        self.profile_name    = ""

        self.read_profile()


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        if build_ele.Shape.value == AllplanArchEle.ShapeType.ePolygonal:
            self.script_object_interactor = PolygonInteractor(self.polygon_result,
                                                              z_coord_input       = False,
                                                              multi_polygon_input = False)
        else:
            self.script_object_interactor = ArchPointInteractor(self.arch_pnt_result,
                                                                ArchitectureElementsQueryUtil.create_arch_general_opening_elements_query(),
                                                                "Placement point", self.draw_placement_preview)

        build_ele.InputMode.value = self.build_ele.POLYGON_INPUT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        if build_ele.Shape.value == AllplanArchEle.ShapeType.eProfile:
            self.placement_ele = self.arch_pnt_result.sel_model_ele

            self.script_object_interactor = None

            return


        #----------------- select the wall

        self.opening_polygon = AllplanGeo.ConvertTo2D(self.polygon_result.input_polygon)[1]

        if not self.opening_polygon.IsValid():
            return

        arch_ele = AllplanIFW.SelectElementsService.SelectByPolygon(
                    self.document, self.opening_polygon,
                    self.coord_input.GetViewWorldProjection(),
                    AllplanIFW.SelectElementsService.eSelectCondition.SELECT_ALL,
                    ArchitectureElementsQueryUtil.create_arch_general_opening_elements_query(), True)

        if not arch_ele:
            AllplanUtil.ShowMessageBox("Opening is outside the wall", AllplanUtil.MB_OK)

            return


        #----------------- in case of selected tier get the parent element

        if (parent_ele := AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(arch_ele[0])) and parent_ele.IsNull():
            self.placement_ele = arch_ele[0]
        else:
            self.placement_ele = parent_ele

        self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.hide_general_element()

        handle_placement_geo = self.hide_ele.get_hidden_geo_elements
        handle_placement_geo.append(self.opening_polygon)

        return CreateElementResult(self.create_opening_element(), self.create_handles(),
                                   multi_placement      = True,
                                   placement_point      = AllplanGeo.Point3D(),
                                   handle_placement_geo = handle_placement_geo)


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if self.script_object_interactor is not None:
            return self.script_object_interactor.on_cancel_function()

        self.hide_ele.show_elements()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def hide_general_element(self):
        """ hide the general element
        """

        build_ele = self.build_ele

        if not build_ele.HasIndependent2DInteraction.value and not self.hide_ele.hidden_elements:
            self.hide_ele.hide_arch_ground_view_elements(self.placement_ele)

        elif build_ele.HasIndependent2DInteraction.value and self.hide_ele.hidden_elements:
            ele_list = AllplanEleAdapter.BaseElementAdapterList([self.placement_ele])

            AllplanIFW.VisibleService.ShowElements(ele_list, True)

            self.hide_ele.clear()


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

        OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())


        #----------------- create the opening

        opening_ele = AllplanArchEle.GeneralOpeningElement(opening_prop, self.placement_ele, self.opening_polygon, False)

        model_ele_list = ModelEleList()

        model_ele_list.append(opening_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        handle_list = list[HandleProperties]()

        HandleCreator.point_list_2d(handle_list, "OpeningPolygon", self.opening_polygon.Points[:-1])

        return handle_list


    def draw_placement_preview(self):
        """ draw the placement preview
        """

        if self.arch_pnt_result.sel_model_ele.IsNull() or self.arch_pnt_result.sel_geo_ele is None:
            return

        geo_ele = self.arch_pnt_result.sel_geo_ele
        pnt     = self.arch_pnt_result.input_point

        angle = AllplanGeo.Vector2D(geo_ele.StartPoint, geo_ele.EndPoint).GetAngle()

        shape_pol = AllplanGeo.Rotate(self.shape_pol, angle)
        shape_pol = AllplanGeo.Move(shape_pol, AllplanGeo.Vector2D(pnt.To2D))

        self.opening_polygon = AllplanGeo.Polygon2D(shape_pol.Points)

        model_ele_list = ModelEleList()
        model_ele_list.append_geometry_2d(self.opening_polygon)

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(),
                                          model_ele_list, True, None)


    def read_profile(self):
        """ read the profile
        """

        build_ele = self.build_ele

        if self.profile_name == build_ele.Profile.value:
            return

        ref_pnt           = AllplanArchEle.ProfileCatalogService.GetProfilePlacementPoint(build_ele.Profile.value)
        shape_pol         = AllplanArchEle.ProfileCatalogService.GetProfileBoundaryPolyline(build_ele.Profile.value)
        self.profile_name = build_ele.Profile.value

        self.shape_pol = AllplanGeo.Move(shape_pol, AllplanGeo.Vector2D(ref_pnt.To2D, AllplanGeo.Point2D()))


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D):
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point
        """

        index = cast(int, handle_prop.parameter_data[0].list_index)

        self.opening_polygon.SetPoint(input_pnt.To2D, index)

        end_index = self.opening_polygon.Count() - 1

        if index == 0:
            self.opening_polygon.SetPoint(input_pnt.To2D, end_index)

        elif index == end_index:
            self.opening_polygon.SetPoint(input_pnt.To2D, 0)


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

        if name == "Shape":
            self.start_input()

            if self.script_object_interactor:
                self.script_object_interactor.start_input(self.coord_input)

            self.hide_ele.show_elements()

            AllplanIFW.HandleService().RemoveHandles()

        return False
