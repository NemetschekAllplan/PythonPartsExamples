""" Script for the wall geometry selection example
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService

from Utils import LibraryBitmapPreview

from TypeCollections.ModelEleList import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.WallGeometrySelectionBuildingElement import WallGeometrySelectionBuildingElement
else:
    WallGeometrySelectionBuildingElement = BuildingElement

print('Load WallGeometrySelection.py')


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
                               r"Examples\PythonParts\ModelObjectExamples\SelectionExamples\WallGeometrySelection.png"))


def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : list[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : list[BuildingElementControlProperties],
                      _modify_uuid_list        : list) -> object:
    """ Create the interactor

    Args:
        coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            list with the building elements
        build_ele_composite:       building element composite with the building element constraints
        control_props_list:        control properties list
        _modify_uuid_list:         list with the UUIDs of the modified elements

    Returns:
          Created interactor object
    """

    return WallGeometrySelection(coord_input, build_ele_list, build_ele_composite, control_props_list)


class WallGeometrySelection(BaseInteractor):
    """ Definition of class WallGeometrySelection
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : list[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : list[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:         API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list:      list with the building elements
            build_ele_composite: building element composite with the building element constraints
            control_props_list:  control properties list
        """

        self.coord_input = coord_input
        self.build_ele   = cast(WallGeometrySelectionBuildingElement, build_ele_list[0])

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select wall"))

        sel_query = AllplanIFW.SelectionQuery([AllplanIFW.QueryTypeID(AllplanEleAdapter.WallTier_TypeUUID),
                                               AllplanIFW.QueryTypeID(AllplanEleAdapter.CircularWallTier_TypeUUID),
                                               AllplanIFW.QueryTypeID(AllplanEleAdapter.PolygonWallTier_TypeUUID)])

        self.element_filter = AllplanIFW.ElementSelectFilterSetting(sel_query, True)

        self.in_selection = True

        self.model_ele_list = ModelEleList()
        self.placment_mat   = AllplanGeo.Matrix3D()
        self.ref_pnt        = AllplanGeo.Point3D()


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: str):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

        if name == self.build_ele.GeometryType.name:
            self.in_selection = True

            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select wall"))

    def on_control_event(self,
                         event_id: int):
        """ Handles on control event

        Args:
            event_id: event id of the clicked button control
        """

    def on_cancel_function(self) -> bool:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True

    def on_preview_draw(self):
        """ Handles the preview draw event
        """

    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.on_preview_draw()

    def on_value_input_control_enter(self) -> bool:
        """ Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Process the mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        build_ele = self.build_ele


        #----------------- select the wall tier

        if self.in_selection:
            self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter)

            wall_tier = self.coord_input.GetSelectedElement()

            if wall_tier.IsNull():
                return True

            self.model_ele_list = ModelEleList()

            if self.coord_input.IsMouseMove(mouse_msg):
                self.model_ele_list.set_color(6)

            if build_ele.GeometryType.value == build_ele.PURE_WALL_GEOMETRY:
                self.model_ele_list.append_geometry_3d(wall_tier.GetPureArchitectureElementGeometry())

            elif build_ele.GeometryType.value == build_ele.MODEL_GEOMETRY:
                self.model_ele_list.append_geometry_3d(wall_tier.GetModelGeometry())

            else:
                self.model_ele_list.append_geometry_2d(wall_tier.GetGroundViewArchitectureElementGeometry())

            AllplanBaseEle.DrawElementPreview(self.coord_input.GetInputViewDocument(), AllplanGeo.Matrix3D(),
                                              self.model_ele_list, True, AllplanEleAdapter.BaseElementAdapter())

            self.placment_mat = AllplanGeo.Matrix3D()


        #----------------- place the geometry

        else:
            input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

            self.placment_mat = AllplanGeo.Matrix3D()

            self.placment_mat.Translate(AllplanGeo.Vector3D(input_pnt - self.ref_pnt))


        #----------------- draw the preview

        AllplanBaseEle.DrawElementPreview(self.coord_input.GetInputViewDocument(), self.placment_mat,
                                          self.model_ele_list, True, None)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- change to placement input

        if self.in_selection:
            if build_ele.GeometryType.value == build_ele.GROUND_VIEW_GEOMETRY:
                build_ele.WallGroundViewGeometry.value = self.model_ele_list[0].GetGeometryObject()
                build_ele.WallGeometry.value           = []

                self.ref_pnt = AllplanGeo.Point3D(build_ele.WallGroundViewGeometry.value[0])
            else:
                build_ele.WallGroundViewGeometry.value = []
                build_ele.WallGeometry.value           = self.model_ele_list[0].GetGeometryObject()

                self.ref_pnt = build_ele.WallGeometry.value.GetVertex(0)[1]

            self.palette_service.update_palette(-1, True)

            self.in_selection = False

            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Place geometry"))


        #----------------- place the wall geometry

        else:
            AllplanBaseEle.CreateElements(self.coord_input.GetInputViewDocument(), self.placment_mat,
                                          self.model_ele_list, [], None)

            self.in_selection = True

            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select wall"))



        return True
