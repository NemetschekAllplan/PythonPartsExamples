""" Example Script for the sloped general opening
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult

from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil
from Utils.Architecture.GeneralOpeningSlopedBRepUtil import GeneralOpeningSlopedBRepUtil
from Utils.Architecture.GeneralOpeningSlopedPolyhedronUtil import GeneralOpeningSlopedPolyhedronUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SlopedGeneralOpeningBuildingElement \
        import SlopedGeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load SlopedGeneralOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\SlopedGeneralOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return SlopedGeneralOpening(build_ele, script_object_data)


class SlopedGeneralOpening(BaseScriptObject):
    """ Definition of class SlopedGeneralOpening
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

        self.axis_pnt_result = PointInteractorResult()
        self.axis_start_pnt  = AllplanGeo.Point3D()
        self.axis_end_pnt    = AllplanGeo.Point3D()

        self.arch_ele        = AllplanEleAdapter.BaseElementAdapterList()
        self.parent_arch_ele = AllplanEleAdapter.BaseElementAdapterList()
        self.hide_ele        = False
        self.undo_service    = None

        self.sel_query = ArchitectureElementsQueryUtil.create_arch_general_opening_elements_query()

        self.opening_bottom_plane_surfaces : list[(AllplanGeo.Polyhedron3D | AllplanGeo.BRep3D)] = []
        self.opening_top_plane_surfaces    : list[(AllplanGeo.Polyhedron3D | AllplanGeo.BRep3D)] = []
        self.opening_polygons              : list[AllplanGeo.Polygon2D]                          = []


    def start_input(self):
        """ start the input
        """

        if self.undo_service:
            self.undo_service.CreateUndoStep()
            self.undo_service = None

        build_ele = self.build_ele

        self.script_object_interactor = PointInteractor(self.axis_pnt_result, True,
                                                        "Start point of the axis of the opening volume")

        build_ele.InputMode.value = self.build_ele.START_AXIS_INPUT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value == build_ele.START_AXIS_INPUT:
            self.axis_start_pnt = self.axis_pnt_result.input_point

            self.script_object_interactor = PointInteractor(self.axis_pnt_result, False,
                                                            "End point of the axis of the opening volume",
                                                            self.draw_axis_preview)

            build_ele.InputMode.value = self.build_ele.END_AXIS_INPUT

            return


        #----------------- create the opening points

        self.axis_end_pnt = self.axis_pnt_result.input_point

        for arch_ele in self.arch_ele:
            self.parent_arch_ele.append(AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(arch_ele))

        self.calculate_opening_polygons_and_planes()

        if not self.opening_polygons:
            self.start_input()

            return

        build_ele.InputMode.value = build_ele.OPENING_INPUT

        self.script_object_interactor = None


    def draw_axis_preview(self):
        """ draw the axis preview
        """

        build_ele = self.build_ele

        AllplanIFW.HighlightService.CancelAllHighlightedElements(self.document.GetDocumentID())

        if self.axis_start_pnt == self.axis_pnt_result.input_point:
            return

        model_ele_list = ModelEleList()

        match build_ele.Shape.value:
            case AllplanArchEle.VerticalOpeningShapeType.eRectangle:
                if (opening_cut_geo := self.create_rectangular_subtraction_body()) is None:
                    return

            case _:
                if (opening_cut_geo := self.create_circular_subtraction_body()) is None:
                    return

        model_ele_list.append_geometry_3d(opening_cut_geo)

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(), model_ele_list, False, None)


        #----------------- select the walls

        view_proj = self.coord_input.GetViewWorldProjection()

        path = AllplanGeo.Polygon2D()
        path += view_proj.WorldToView(self.axis_start_pnt)
        path += view_proj.WorldToView(self.axis_pnt_result.input_point)
        path += view_proj.WorldToView(self.axis_start_pnt)

        self.arch_ele = AllplanIFW.SelectElementsService.SelectByPolygon(
                            self.document, path, view_proj,
                            AllplanIFW.SelectElementsService.eSelectCondition.SELECT_INTERSECTED,
                            self.sel_query)

        AllplanIFW.HighlightService.HighlightElements(self.arch_ele)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.hide_general_element()

        return CreateElementResult(self.create_opening_element(), [],
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D(),
                                   as_static_preview = True)


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList()

        for opening_polygon, parent_ele, bottom_surface, top_surface in zip(self.opening_polygons, self.parent_arch_ele,
                                                                            self.opening_bottom_plane_surfaces,
                                                                            self.opening_top_plane_surfaces):

            #----------------- create the properties

            opening_prop = AllplanArchEle.GeneralOpeningProperties(AllplanArchEle.OpeningType.eNiche)

            opening_prop.VisibleInViewSection3D   = True
            opening_prop.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value


            #--------------- set the surface planes

            plane_ref = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())

            plane_ref.SetBottomPlaneSurface(bottom_surface)
            plane_ref.SetTopPlaneSurface(top_surface)

            opening_prop.PlaneReferences = plane_ref


            #----------------- set the geometry properties

            geometry_prop = opening_prop.GetGeometryProperties()

            geometry_prop.Shape = AllplanArchEle.VerticalOpeningShapeType.eRectangle
            geometry_prop.Width = AllplanGeo.Vector2D(opening_polygon.GetStartPoint(),
                                                      opening_polygon.GetPoint(opening_polygon.Count() - 2)).GetLength()
            geometry_prop.Depth = AllplanEleAdapter.AxisElementAdapter(parent_ele).GetThickness()

            OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())


            #----------------- create the opening

            opening_ele = AllplanArchEle.GeneralOpeningElement(opening_prop, parent_ele, opening_polygon, False)

            model_ele_list.append(opening_ele)

        return model_ele_list


    def calculate_opening_polygons_and_planes(self):
        """ calculate the opening polygons and planes
        """

        build_ele = self.build_ele

        self.opening_polygons.clear()
        self.opening_bottom_plane_surfaces.clear()
        self.opening_top_plane_surfaces.clear()


        #----------------- get the start and end point of the openings

        for parent_ele in self.parent_arch_ele:
            if build_ele.Shape.value == AllplanArchEle.ShapeType.eRectangular:
                if (subtraction_body := self.create_rectangular_subtraction_body()) is None:
                    continue

                created, bottom_plane_surface, top_plane_surface, opening_polygon = \
                    GeneralOpeningSlopedPolyhedronUtil.create_opening_polygon_and_plane_surfaces(parent_ele, subtraction_body)
            else:
                if (subtraction_body := self.create_circular_subtraction_body()) is None:
                    continue

                created, bottom_plane_surface, top_plane_surface, opening_polygon = \
                    GeneralOpeningSlopedBRepUtil.create_opening_polygons_and_plane_surfaces(parent_ele, subtraction_body)

            if not created:
                continue

            self.opening_bottom_plane_surfaces.append(bottom_plane_surface)
            self.opening_top_plane_surfaces.append(top_plane_surface)
            self.opening_polygons.append(opening_polygon)


    def hide_general_element(self):
        """ hide the general element
        """

        build_ele = self.build_ele

        if not build_ele.HasIndependent2DInteraction.value and not self.hide_ele:
            AllplanIFW.VisibleService.ShowElements(self.parent_arch_ele, False)

            self.hide_ele = True

        elif build_ele.HasIndependent2DInteraction.value and self.hide_ele:
            ele_list = AllplanEleAdapter.BaseElementAdapterList(self.parent_arch_ele)

            AllplanIFW.VisibleService.ShowElements(ele_list, True)

            self.hide_ele = False


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value != build_ele.OPENING_INPUT:
            return OnCancelFunctionResult.CANCEL_INPUT

        if self.hide_ele:
            AllplanIFW.VisibleService.ShowElements(self.parent_arch_ele, True)

            self.hide_ele = False

        self.parent_arch_ele = AllplanEleAdapter.BaseElementAdapterList()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def create_rectangular_subtraction_body(self) -> (AllplanGeo.Polyhedron3D | None):
        """ create the rectangular subtraction body

        Returns:
            created subtraction body
        """

        build_ele = self.build_ele

        norm_vec = AllplanGeo.Vector3D(self.axis_start_pnt, self.axis_pnt_result.input_point)

        plane = AllplanGeo.Plane3D(self.axis_start_pnt, norm_vec)

        trans_mat = plane.GetTransformationMatrix()

        width_halve  = build_ele.CuboidWidth.value / 2
        height_halve = build_ele.CuboidHeight.value / 2

        ele = AllplanGeo.Polyline3D()

        ele += AllplanGeo.Point3D(width_halve, height_halve, 0)
        ele += AllplanGeo.Point3D(-width_halve, height_halve, 0)
        ele += AllplanGeo.Point3D(-width_halve, -height_halve, 0)
        ele += AllplanGeo.Point3D(width_halve, -height_halve, 0)
        ele += AllplanGeo.Point3D(width_halve, height_halve, 0)

        ele = AllplanGeo.Transform(ele, trans_mat)

        path = AllplanGeo.Polyline3D()
        path += ele.StartPoint
        path += ele.StartPoint + norm_vec

        err, surface = AllplanGeo.CreateSweptPolyhedron3D(AllplanGeo.Polyline3DList([ele]), path, False, True,
                                                          AllplanGeo.Vector3D(0, 0, 0))

        return None if err else surface


    def create_circular_subtraction_body(self) -> (AllplanGeo.BRep3D | None):
        """ create the circular subtraction body

        Returns:
            created subtraction body
        """

        build_ele = self.build_ele

        norm_vec = AllplanGeo.Vector3D(self.axis_start_pnt, self.axis_pnt_result.input_point)

        radius = build_ele.PipeRadius.value

        arc = AllplanGeo.Arc3D(self.axis_start_pnt,
                            AllplanGeo.Plane3D(AllplanGeo.Point3D(), norm_vec).CalcPlaneVectors()[0],
                            norm_vec, radius, radius, 0, math.pi * 2)

        path = AllplanGeo.Polyline3D()
        path += arc.StartPoint
        path += arc.StartPoint + norm_vec

        err, surface = AllplanGeo.CreateSweptBRep3D([arc], path, False, False, None, 0)

        return None if err else surface
