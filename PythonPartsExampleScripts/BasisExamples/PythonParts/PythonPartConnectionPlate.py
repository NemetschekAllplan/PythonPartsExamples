""" implementation of the plate
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW

from BuildingElement import BuildingElement
from BuildingElementPaletteService import BuildingElementPaletteService
from DocumentManager import DocumentManager
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList
from TypeCollections.ModificationElementList import ModificationElementList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartConnectionPlateBuildingElement import PythonPartConnectionPlateBuildingElement
else:
    PythonPartConnectionPlateBuildingElement = BuildingElement

class PythonPartConnectionPlate():
    """ implementation of the plate
    """

    def __init__(self,
                 coord_input          : AllplanIFW.CoordinateInput,
                 palette_service      : BuildingElementPaletteService,
                 build_ele_list       : list[BuildingElement],
                 modification_ele_list: ModificationElementList):
        """ initialize

        Args:
            coord_input:           API object for the coordinate input, element selection, ... in the Allplan view
            palette_service:       palette service
            build_ele_list:        list with the building elements
            modification_ele_list: list with the modification elements in modification mode
        """

        self.coord_input           = coord_input
        self.palette_service       = palette_service
        self.build_ele_list        = build_ele_list
        self.build_ele             = cast(PythonPartConnectionPlateBuildingElement, self.build_ele_list[1])
        self.modification_ele_list = modification_ele_list
        self.modification_mode     = modification_ele_list.is_modification_element()
        self.ref_point_input       = not self.modification_mode
        self.model_ele_list        = ModelEleList()
        self.placement_mat         = self.build_ele_list[0].get_insert_matrix() if self.modification_mode else AllplanGeo.Matrix3D()
        self.elements_to_hide      = AllplanEleAdapter.BaseElementAdapterList()
        self.elements_to_show      = AllplanEleAdapter.BaseElementAdapterList()

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Reference point"))

        if self.modification_mode:
            self.create_plate()


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.draw_preview()


    def on_cancel_function(self):
        """ Check for input function cancel in case of ESC
        """

        if self.modification_mode:
            AllplanBaseEle.DrawingService.ResetAndDrawHiddenElement(self.coord_input.GetInputViewDocument(),
                                                                    DocumentManager.get_instance().pythonpart_element)

    def create_python_part(self):
        """ create the PythonPart
        """

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)


        #----------------- create the PythonPart

        pyp_transaction = PythonPartTransaction(self.coord_input.GetInputViewDocument())

        pyp_transaction.execute(self.placement_mat,
                                self.coord_input.GetViewWorldProjection(),
                                pyp_util.create_pythonpart(self.build_ele_list,
                                                           type_uuid         = "c0398407-1d54-4087-a8da-7d6aaffb25ec",
                                                           type_display_name = "PythonPart Plate"),
                                self.modification_ele_list,
                                elements_to_hide = self.elements_to_hide,
                                elements_to_show = self.elements_to_show)

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Reference point"))

        self.ref_point_input = True


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """ Handles the process mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        if self.ref_point_input:
            ref_point = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

            self.placement_mat = AllplanGeo.Matrix3D()
            self.placement_mat.SetTranslation(AllplanGeo.Vector3D(ref_point))

        if not self.coord_input.IsMouseMove(mouse_msg):
            self.ref_point_input = False

        self.draw_preview()

        return True


    def create_plate(self):
        """ create the plate element
        """

        build_ele = self.build_ele

        plate = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value, build_ele.Width.value, build_ele.Height.value)


        #----------------- cut out the holes at the model position

        if build_ele.__HoleConnection__.value:
            _, plate = AllplanGeo.CreateBRep3D(AllplanGeo.Transform(plate, self.placement_mat))

            for hole_connection, visible in zip(build_ele.__HoleConnection__.value, build_ele.HoleVisibility.value):
                if hole_connection.element.IsNull() or not visible:
                    continue

                _, plate = AllplanGeo.MakeSubtraction(plate, hole_connection.element.GetModelGeometry()[0])

            rev_placement_mat = AllplanGeo.Matrix3D(self.placement_mat)
            rev_placement_mat.Reverse()

            plate = AllplanGeo.Transform(plate, rev_placement_mat)

        self.model_ele_list = ModelEleList(build_ele.CommonProp.value)

        self.model_ele_list.append_geometry_3d(plate)

        self.set_show_hide_elements()


    def set_show_hide_elements(self):
        """ set the show/hide elements
        """

        build_ele = self.build_ele

        self.elements_to_hide = AllplanEleAdapter.BaseElementAdapterList()
        self.elements_to_show = AllplanEleAdapter.BaseElementAdapterList()

        if self.modification_mode:
            for hole, visible in zip(build_ele.__HoleConnection__.value, build_ele.HoleVisibility.value):
                if hole.element.IsNull():
                    continue

                if visible:
                    self.elements_to_show.append(hole.element)
                else:
                    self.elements_to_hide.append(hole.element)


    def draw_preview(self):
        """ draw the preview
        """

        self.create_plate()

        PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), self.placement_mat,
                                  self.model_ele_list, True, None, not self.modification_mode,
                                  False, self.elements_to_hide, self.elements_to_show)


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        self.palette_service.modify_element_property(page, name, value)

        self.draw_preview()
