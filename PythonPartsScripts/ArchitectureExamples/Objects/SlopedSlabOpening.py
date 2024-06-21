""" Example Script for the sloped general opening
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, Any

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.Architecture.SlabOpeningSlopedBRepUtil import SlabOpeningSlopedBRepUtil
from Utils.Architecture.SlabOpeningSlopedPolyhedronUtil import SlabOpeningSlopedPolyhedronUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SlopedSlabOpeningBuildingElement \
        import SlopedSlabOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load SlopedSlabOpening.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\SlopedSlabOpening.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return SlopedSlabOpening(build_ele, coord_input)


class SlopedSlabOpening(BaseScriptObject):
    """ Definition of class SlopedSlabOpening
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

        self.build_ele = build_ele

        self.axis_pnt_result = PointInteractorResult()
        self.axis_start_pnt  = AllplanGeo.Point3D()
        self.axis_end_pnt    = AllplanGeo.Point3D()

        self.arch_ele     = AllplanEleAdapter.BaseElementAdapterList()
        self.undo_service = None

        self.opening_polygons : list[AllplanGeo.Polygon2D] = []

        self.sel_query = AllplanIFW.SelectionQuery(AllplanIFW.QueryTypeID(AllplanEleAdapter.Slab_TypeUUID))

        self.multi_slabs                   : list[AllplanEleAdapter.BaseElementAdapter] = []
        self.opening_slabs                 : list[AllplanEleAdapter.BaseElementAdapter] = []
        self.opening_bottom_plane_surfaces : list[(AllplanGeo.Polyhedron3D | None)]     = []
        self.opening_top_plane_surfaces    : list[(AllplanGeo.Polyhedron3D | None)]     = []

        self.preview_elements : ModelEleList = ModelEleList()


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

        self.multi_slabs = [element for element in AllplanBaseEle.ElementsSelectService.SelectAllElements(self.document) \
                            if element == AllplanEleAdapter.MultiSlab_TypeUUID]


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


        #----------------- create the opening polygons

        self.undo_service = AllplanIFW.UndoRedoService(self.document, True, True, True)

        self.create_opening_polygons_and_planes()

        if not self.opening_polygons:
            self.start_input()

            return

        self.script_object_interactor = None

        build_ele.InputMode.value = build_ele.OPENING_INPUT


    def draw_axis_preview(self):
        """ draw the axis preview
        """

        build_ele = self.build_ele

        AllplanIFW.HighlightService.CancelAllHighlightedElements(self.document.GetDocumentID())

        if self.axis_start_pnt == self.axis_pnt_result.input_point:
            return

        model_ele_list = ModelEleList()

        match build_ele.Shape.value:
            case AllplanArchEle.ShapeType.eRectangular:
                if (opening_cut_geo := self.create_rectangular_subtraction_body()) is None:
                    return

            case AllplanArchEle.ShapeType.eCircular:
                if (opening_cut_geo := self.create_circular_subtraction_body()) is None:
                    return

            case _:
                if (opening_cut_geo := self.create_ngon_subtraction_body()) is None:
                    return

        model_ele_list.append_geometry_3d(opening_cut_geo)

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(), model_ele_list, False, None)


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.create_opening_element(), [],
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D(),
                                   preview_elements = self.preview_elements,
                                   as_static_preview = True)


    def modify_element_property(self,
                                _name : str,
                                _value: Any) -> bool:
        """ modify the element property

        Args:
            _name:  name
            _value: value

        Returns:
            update palette state
        """

        build_ele = self.build_ele

        if build_ele.InputMode.value != build_ele.OPENING_INPUT:
            return False

        self.create_opening_polygons_and_planes()

        return False


    def create_opening_polygons_and_planes(self):
        """ create the opening polygons and planes
        """

        build_ele = self.build_ele

        self.opening_slabs.clear()
        self.opening_polygons.clear()
        self.opening_bottom_plane_surfaces.clear()
        self.opening_top_plane_surfaces.clear()

        if build_ele.Shape.value == AllplanArchEle.ShapeType.eCircular:
            self.create_brep_opening_polygons_and_planes()
        else:
            self.create_polyhedron_opening_polygons_and_planes()


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value != build_ele.OPENING_INPUT:
            return OnCancelFunctionResult.CANCEL_INPUT

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        model_ele_list = ModelEleList()

        for opening_polygon, slab, bottom_surface, top_surface in zip(self.opening_polygons, self.opening_slabs,
                                                                      self.opening_bottom_plane_surfaces, self.opening_top_plane_surfaces):
            slab_ele = cast(AllplanArchEle.SlabElement, AllplanBaseEle.GetElement(slab))


            #----------------- create the properties

            opening_prop = AllplanArchEle.SlabOpeningProperties(AllplanArchEle.SlabOpeningType.eRecess)

            opening_prop.ShapeType        = AllplanArchEle.ShapeType.ePolygonal
            opening_prop.ShapePolygon     = opening_polygon
            opening_prop.CommonProperties = slab_ele.Properties.CommonProperties


            if bottom_surface is None:
                slab_ele = cast(AllplanArchEle.SlabElement, AllplanBaseEle.GetElement(slab))

                plane_ref = slab_ele.GetProperties().GetPlaneReferences()
            else:
                plane_ref = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())

                plane_ref.SetBottomPlaneSurface(bottom_surface)
                plane_ref.SetTopPlaneSurface(top_surface)

            opening_prop.PlaneReferences  = plane_ref


            #----------------- create the opening

            opening_ele = AllplanArchEle.SlabOpeningElement(opening_prop, AllplanGeo.Point2D(), slab.GetModelElementUUID())

            model_ele_list.append(opening_ele)

        return model_ele_list


    def create_polyhedron_opening_polygons_and_planes(self):
        """ create the opening polygons and planes for a Polyhedron surface
        """

        build_ele = self.build_ele

        slab_opening_util = SlabOpeningSlopedPolyhedronUtil(self.document)

        for multi_slab in self.multi_slabs:
            for slab in AllplanEleAdapter.BaseElementAdapterChildElementsService.GetTierElements(multi_slab):
                match build_ele.Shape.value:
                    case AllplanArchEle.ShapeType.eRectangular:
                        if (opening_cut_geo := self.create_rectangular_subtraction_body()) is None:
                            continue

                    case _:
                        if (opening_cut_geo := self.create_ngon_subtraction_body()) is None:
                            continue

                created, opening_polygon, bottom_plane_surface, top_plane_surface = \
                    slab_opening_util.create_opening_polygons_and_plane_surfaces(slab, opening_cut_geo)

                if not created:
                    continue

                self.opening_slabs.append(slab)
                self.opening_polygons.append(opening_polygon)
                self.opening_bottom_plane_surfaces.append(bottom_plane_surface)
                self.opening_top_plane_surfaces.append(top_plane_surface)


    def create_brep_opening_polygons_and_planes(self):
        """ create the opening polygons and planes for a BRep surface
        """

        slab_opening_util = SlabOpeningSlopedBRepUtil(self.document)

        for multi_slab in self.multi_slabs:
            for slab in AllplanEleAdapter.BaseElementAdapterChildElementsService.GetTierElements(multi_slab):
                if (opening_cut_geo := self.create_circular_subtraction_body()) is None:
                    continue

                created, opening_polygon, bottom_plane_surface, top_plane_surface = \
                    slab_opening_util.create_opening_polygons_and_plane_surfaces(slab, opening_cut_geo)

                if not created:
                    continue

                self.opening_slabs.append(slab)
                self.opening_polygons.append(opening_polygon)
                self.opening_bottom_plane_surfaces.append(bottom_plane_surface)
                self.opening_top_plane_surfaces.append(top_plane_surface)


    def create_rectangular_subtraction_body(self) -> (AllplanGeo.Polyhedron3D | None):
        """ create the rectangular subtraction body

        Returns:
            created subtraction body
        """

        build_ele = self.build_ele

        axis_start_pnt = self.axis_start_pnt
        axis_end_pnt   = self.axis_pnt_result.input_point

        if axis_start_pnt.Z > axis_end_pnt.Z:
            axis_start_pnt, axis_end_pnt = axis_end_pnt, axis_start_pnt

        norm_vec = AllplanGeo.Vector3D(axis_start_pnt, axis_end_pnt)

        plane = AllplanGeo.Plane3D(axis_start_pnt, norm_vec)

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

        err, body = AllplanGeo.CreateSweptPolyhedron3D(AllplanGeo.Polyline3DList([ele]), path, True, True,
                                                       AllplanGeo.Vector3D(0, 0, 0))

        return None if err else body


    def create_circular_subtraction_body(self) -> (AllplanGeo.BRep3D | None):
        """ create the circular subtraction body

        Returns:
            created subtraction body
        """

        build_ele = self.build_ele

        axis_start_pnt = self.axis_start_pnt
        axis_end_pnt   = self.axis_pnt_result.input_point

        if axis_start_pnt.Z > axis_end_pnt.Z:
            axis_start_pnt, axis_end_pnt = axis_end_pnt, axis_start_pnt

        norm_vec = AllplanGeo.Vector3D(axis_start_pnt, axis_end_pnt)

        radius = build_ele.PipeRadius.value

        arc = AllplanGeo.Arc3D(axis_start_pnt,
                               AllplanGeo.Plane3D(AllplanGeo.Point3D(), norm_vec).CalcPlaneVectors()[0],
                               norm_vec, radius, radius, 0, math.pi * 2)

        path = AllplanGeo.Polyline3D()
        path += arc.StartPoint
        path += arc.StartPoint + norm_vec

        err, body = AllplanGeo.CreateSweptBRep3D([arc], path, True, False, None, 0)

        return None if err else body


    def create_ngon_subtraction_body(self) -> (AllplanGeo.Polyhedron3D | None):
        """ create the ngon subtraction body

        Returns:
            created surface
        """

        build_ele = self.build_ele

        axis_start_pnt = self.axis_start_pnt
        axis_end_pnt   = self.axis_pnt_result.input_point

        if axis_start_pnt.Z > axis_end_pnt.Z:
            axis_start_pnt, axis_end_pnt = axis_end_pnt, axis_start_pnt

        norm_vec = AllplanGeo.Vector3D(axis_start_pnt, axis_end_pnt)

        plane = AllplanGeo.Plane3D(axis_start_pnt, norm_vec)

        delta_angle = math.pi * 2 / build_ele.NumberOfCorners.value
        end_angle   = math.pi * 2 - delta_angle / 2
        radius      = build_ele.PipeRadius.value

        angle = 0.

        ele = AllplanGeo.Polyline3D()

        while angle < end_angle:
            ele += AllplanGeo.Point3D(radius * math.cos(angle), radius * math.sin(angle), 0.)

            angle += delta_angle

        ele += ele.StartPoint

        trans_mat = plane.GetTransformationMatrix()

        ele = AllplanGeo.Transform(ele, trans_mat)

        path = AllplanGeo.Polyline3D()
        path += ele.StartPoint
        path += ele.StartPoint + norm_vec

        err, body = AllplanGeo.CreateSweptPolyhedron3D(AllplanGeo.Polyline3DList([ele]), path, True, True,
                                                       AllplanGeo.Vector3D(0, 0, 0))

        return None if err else body
