""" Example Script for the general opening creation for 3D solids
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult

from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.Architecture.GeneralOpeningSlopedBRepUtil import GeneralOpeningSlopedBRepUtil
from Utils.Architecture.GeneralOpeningSlopedPolyhedronUtil import GeneralOpeningSlopedPolyhedronUtil
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil
from Utils.ElementFilter.GeometryElementsQueryUtil import GeometryElementsQueryUtil
from Utils.ElementFilter.FilterCollection import FilterCollection
from Utils.ElementFilter.PythonPartFilter import PythonPartFilter

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeneralOpeningsFor3DSolidsBuildingElement \
        import GeneralOpeningsFor3DSolidsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load GeneralOpeningsFor3DSolids.py')

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
                               r"Examples\PythonParts\ArchitectureExamples\Objects\GeneralOpeningsFor3DSolids.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return GeneralOpeningsFor3DSolids(build_ele, script_object_data)


class GeneralOpeningsFor3DSolids(BaseScriptObject):
    """ Definition of class GeneralOpeningsFor3DSolids
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

        self.undo_service = None

        self.opening_polygons : list[AllplanGeo.Polygon2D] = []

        self.sel_result = MultiElementSelectInteractorResult()

        self.parent_ele : AllplanEleAdapter.BaseElementAdapterList = AllplanEleAdapter.BaseElementAdapterList()

        self.opening_parent_ele            : list[AllplanEleAdapter.BaseElementAdapter]                 = []
        self.opening_bottom_plane_surfaces : list[(AllplanGeo.Polyhedron3D | AllplanGeo.BRep3D | None)] = []
        self.opening_top_plane_surfaces    : list[(AllplanGeo.Polyhedron3D | AllplanGeo.BRep3D | None)] = []


    def start_input(self):
        """ start the input
        """

        if self.undo_service:
            self.undo_service.CreateUndoStep()
            self.undo_service = None

        build_ele = self.build_ele

        self.start_element_selection()

        build_ele.InputMode.value = self.build_ele.SOLID_SELECT


        #----------------- get all axis elements from the document

        sel_query = ArchitectureElementsQueryUtil.create_arch_general_opening_elements_query()

        self.parent_ele.clear()

        for element in AllplanBaseEle.ElementsSelectService.SelectAllElements(self.document):
            if sel_query(element):
                self.parent_ele.append(AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(element))


    def start_element_selection(self):
        """ start the element selection
        """

        build_ele = self.build_ele

        filter_collection = FilterCollection()

        if build_ele.Elements3D.value:
            filter_collection.append(GeometryElementsQueryUtil.create_surface_elements_query())

        if build_ele.PythonParts.value:
            filter_collection.append(PythonPartFilter())

        if self.script_object_interactor is not None:
            cast(MultiElementSelectInteractor, self.script_object_interactor).close_selection()

        self.script_object_interactor = MultiElementSelectInteractor(self.sel_result, filter_collection,
                                                                     "Select the elements")


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele


        #----------------- create the opening polygons

        self.undo_service = AllplanIFW.UndoRedoService(self.document, True, True, True)

        self.create_opening_polygons_and_planes()

        if not self.opening_polygons:
            self.start_input()

            return

        self.script_object_interactor = None

        build_ele.InputMode.value = build_ele.OPENING_INPUT


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.create_opening_element()

        return CreateElementResult(self.create_opening_element(), [],
                                   multi_placement = True,
                                   placement_point = AllplanGeo.Point3D(),
                                   as_static_preview = True)


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

        build_ele = self.build_ele

        if build_ele.InputMode.value != build_ele.OPENING_INPUT:
            if name in (build_ele.Elements3D.name, build_ele.PythonParts.name):
                self.start_element_selection()

                if self.script_object_interactor is not None:
                    self.script_object_interactor.start_input(self.coord_input)

            return False

        self.create_opening_polygons_and_planes()

        return False


    def create_opening_polygons_and_planes(self):
        """ create the opening polygons and planes
        """

        self.opening_parent_ele.clear()
        self.opening_polygons.clear()
        self.opening_bottom_plane_surfaces.clear()
        self.opening_top_plane_surfaces.clear()

        def create_ele_opening_polygons_and_planes(element_geo: (AllplanGeo.Polyhedron3D | AllplanGeo.BRep3D)):
            """ create the opening geometry

            Args:
                element_geo: element geometry
            """

            if isinstance(element_geo, AllplanGeo.BRep3D):
                self.create_brep_opening_polygons_and_planes(element_geo)
            else:
                self.create_polyhedron_opening_polygons_and_planes(element_geo)

        for ele in self.sel_result.sel_elements:
            element_geo = ele.GetModelGeometry()

            if isinstance(element_geo, list):
                for item in element_geo:
                    create_ele_opening_polygons_and_planes(item)

            else:
                create_ele_opening_polygons_and_planes(element_geo)


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value != build_ele.OPENING_INPUT:
            if self.script_object_interactor is not None:
                cast(MultiElementSelectInteractor, self.script_object_interactor).close_selection()

            return OnCancelFunctionResult.CANCEL_INPUT

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList()

        progress_bar = AllplanUtil.ProgressBar()

        progress_bar.StartProgressbar(len(self.opening_polygons), "Calculate the openings", False, True)

        for opening_polygon, opening_parent_ele, bottom_surface, top_surface in zip(self.opening_polygons,
                                                                                    self.opening_parent_ele,
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
            geometry_prop.Depth = AllplanEleAdapter.AxisElementAdapter(opening_parent_ele).GetThickness()

            OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())


            #----------------- create the opening

            opening_ele = AllplanArchEle.GeneralOpeningElement(opening_prop, opening_parent_ele, opening_polygon, False)

            model_ele_list.append(opening_ele)

            progress_bar.MakeStep(1)

        return model_ele_list


    def create_polyhedron_opening_polygons_and_planes(self,
                                                      solid_geo: AllplanGeo.Polyhedron3D):
        """ create the opening polygons and planes for a Polyhedron surface

        Args:
            solid_geo: solid geometry
        """

        for parent_ele in self.parent_ele:
            created, bottom_plane_surface, top_plane_surface, opening_polygon = \
                GeneralOpeningSlopedPolyhedronUtil.create_opening_polygon_and_plane_surfaces(parent_ele, solid_geo)

            if not created:
                continue

            self.opening_parent_ele.append(parent_ele)
            self.opening_polygons.append(opening_polygon)
            self.opening_bottom_plane_surfaces.append(bottom_plane_surface)
            self.opening_top_plane_surfaces.append(top_plane_surface)


    def create_brep_opening_polygons_and_planes(self,
                                                solid_geo: AllplanGeo.BRep3D):
        """ create the opening polygons and planes for a BRep surface

        Args:
            solid_geo: solid geometry
        """

        for parent_general in self.parent_ele:
            created, bottom_plane_surface, top_plane_surface, opening_polygon = \
                GeneralOpeningSlopedBRepUtil.create_opening_polygons_and_plane_surfaces(parent_general, solid_geo)

            if not created:
                continue

            self.opening_parent_ele.append(parent_general)
            self.opening_polygons.append(opening_polygon)
            self.opening_bottom_plane_surfaces.append(bottom_plane_surface)
            self.opening_top_plane_surfaces.append(top_plane_surface)
