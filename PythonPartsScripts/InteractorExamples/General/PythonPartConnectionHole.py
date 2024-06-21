""" implementation of the plate
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BuildingElement import BuildingElement
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementParameterListUtil import BuildingElementParameterListUtil
from DocumentManager import DocumentManager
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction, ConnectToPythonPart, ConnectToPythonPartState
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModificationElementList import ModificationElementList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartConnectionHoleBuildingElement import PythonPartConnectionHoleBuildingElement
else:
    PythonPartConnectionHoleBuildingElement = BuildingElement

class PythonPartConnectionHole():
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
        self.build_ele             = cast(PythonPartConnectionHoleBuildingElement, self.build_ele_list[1])
        self.modification_ele_list = modification_ele_list
        self.modification_mode     = modification_ele_list.is_modification_element()
        self.ref_point_input       = not self.modification_mode
        self.model_ele_list        = []
        self.placement_mat         = AllplanGeo.Matrix3D() if not self.modification_mode else self.build_ele_list[0].get_insert_matrix()
        self.plate_uuid            = AllplanEleAdapter.GUID()

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Select the plate"))

        if self.modification_mode:
            self.create_hole()


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

        pyp_transaction = PythonPartTransaction(self.coord_input.GetInputViewDocument(),
                                                ConnectToPythonPart(self.plate_uuid,
                                                                    "__HoleConnectionUuidTimeStamp__",
                                                                    ConnectToPythonPartState.IS_PARENT_CHILD))

        pyp_transaction.execute(self.placement_mat,
                                self.coord_input.GetViewWorldProjection(),
                                pyp_util.create_pythonpart(self.build_ele_list,
                                                           type_uuid = "6069d5fe-3a10-4c86-9ee9-8ae90e04e686",
                                                           type_display_name = "PythonPart Hole"),
                                self.modification_ele_list)

        self.ref_point_input                         = True
        self.build_ele.__PlateConnectionUUID__.value = ""

        self.palette_service.update_palette(-1, False)


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
            self.build_ele.__PlateConnectionUUID__.value = ""

            if not self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True):
                return True

            sel_plate = self.coord_input.GetSelectedElement()

            _, name, parameters = AllplanBaseEle.PythonPartService.GetParameter(sel_plate)

            if name.lower().find("pythonpartconnection") == -1 or \
                not next((True for parameter in parameters if parameter.find("__HoleConnectionUuidTimeStamp__") != -1), False):
                return True

            self.build_ele.__PlateConnectionUUID__.value = str(sel_plate.GetModelElementUUID())

        if not self.coord_input.IsMouseMove(mouse_msg):
            self.ref_point_input = False

            self.palette_service.update_palette(-1, True)

        self.draw_preview()

        return True


    def create_hole(self):
        """ create the hole element
        """

        build_ele = self.build_ele

        self.plate_uuid = AllplanEleAdapter.GUID.FromString(build_ele.__PlateConnectionUUID__.value)

        plate = AllplanEleAdapter.BaseElementAdapter.FromGUID(self.plate_uuid, self.coord_input.GetInputViewDocument())

        if plate.IsNull():
            AllplanUtil.ShowMessageBox("Plate not found " + build_ele.__PlateConnectionUUID__.value, AllplanUtil.MB_OK)

            return


        #------------- create the placement data of the hole

        _, plate_place_mat = AllplanBaseEle.PythonPartService.GetPlacementMatrix(plate)

        build_ele.PlatePlacementMatrix.value = plate_place_mat

        axis_vec = AllplanGeo.Transform(AllplanGeo.Vector3D(0, 0, 1000), plate_place_mat)

        plane = AllplanGeo.Plane3D(AllplanGeo.Point3D(), axis_vec)

        axis_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(),
                                                    plane.CalcPlaneVectors()[0], axis_vec)

        ref_pnt = AllplanGeo.Transform(AllplanGeo.Point3D(build_ele.RefPointX.value,
                                                          build_ele.RefPointY.value, 0), plate_place_mat)

        self.placement_mat = AllplanGeo.Matrix3D()
        self.placement_mat.SetTranslation(AllplanGeo.Vector3D(ref_pnt))


        #----------------- get the height from the plate

        _, _, plate_param = AllplanBaseEle.PythonPartService.GetParameter(plate)

        plate_height = BuildingElementParameterListUtil.get_value_double(plate_param, "Height")

        build_ele.PlateHeight.value = plate_height  # needed for update of the Hole-PyP definition element after change


        #----------------- create the hole

        hole = AllplanGeo.BRep3D.CreateCylinder(axis_placement, build_ele.Radius.value, plate_height)

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        com_prop.HelpConstruction = True

        self.model_ele_list = [AllplanBasisEle.ModelElement3D(com_prop, hole)]


    def draw_preview(self):
        """ draw the preview
        """

        if not self.build_ele.__PlateConnectionUUID__.value:
            return

        self.create_hole()

        PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), self.placement_mat, self.model_ele_list, True, None,
                                  not self.modification_mode)


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
