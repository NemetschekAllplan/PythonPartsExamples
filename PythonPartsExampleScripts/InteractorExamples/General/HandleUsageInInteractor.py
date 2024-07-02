"""
Script for HandleUsageInInteractor show the usage of handles in an interactor PythonPart
"""

from typing import Any, List

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from ControlProperties import ControlProperties
from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleModificationService import HandleModificationService
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil
from StringTableService import StringTableService
from InputMode import InputMode

from Utils import LibraryBitmapPreview

print('Load HandleUsageInInteractor.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc:       AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of the library preview

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_libary_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\InteractorExamples\General\HandleUsageInInteractor.png"))


def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      _pyp_path               : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : List[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : List[List[ControlProperties]],
                      modify_uuid_list        : List[str]) -> Any:
    """
    Create the interactor

    Args:
        coord_input:               coordinate input
        _pyp_path:                 path of the pyp file
        global_str_table_service:  global string table service
        build_ele_list:            building element list
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        modify_uuid_list:          UUIDs of the existing elements in the modification mode

      Returns:
        Created interactor object
    """

    return HandleUsageInInteractor(coord_input, global_str_table_service, build_ele_list, build_ele_composite,
                                   control_props_list, modify_uuid_list)


class HandleUsageInInteractor(BaseInteractor):
    """
    Definition of class HandleUsageInInteractor
    """

    def __init__(self,
                 coord_input             : AllplanIFW.CoordinateInput,
                 global_str_table_service: StringTableService,
                 build_ele_list          : List[BuildingElement],
                 build_ele_composite     : BuildingElementComposite,
                 control_props_list      : List[List[ControlProperties]],
                 modify_uuid_list        : List[str]):
        """
        initialize and start the input

        Args:
            coord_input:               coordinate input
            global_str_table_service:  global string table service
            build_ele_list:            building element list
            build_ele_composite:       building element composite
            control_props_list:        control properties list
            modify_uuid_list:          UUIDs of the existing elements in the modification mode
        """

        self.coord_input              = coord_input
        self.model_ele_list           = []
        self.build_ele_list           = build_ele_list
        self.control_props_list       = control_props_list
        self.global_str_table_service = global_str_table_service
        self.input_mode               = InputMode.RefPoint
        self.handle_modi_service      = HandleModificationService(coord_input, build_ele_list, control_props_list)
        self.placement_mat            = AllplanGeo.Matrix3D()
        self.modify_uuid_list         = modify_uuid_list
        self.modification_mode        = modify_uuid_list and modify_uuid_list[0] != "00000000-0000-0000-0000-000000000000--0"


        #----------------- show the palette

        if not self.modification_mode:
            BuildingElementListService.read_from_default_favorite_file(self.build_ele_list)

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             self.build_ele_list[0].pyp_file_path)

        self.palette_service.show_palette(self.build_ele_list[0].pyp_file_name)


        #----------------- start the input

        if not self.modification_mode:
            self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Placement point"))

            return


        #----------------- start the modification

        self.placement_mat = build_ele_list[0].get_insert_matrix()

        self.start_handle_select()


    def on_control_event(self,
                         event_id: int):
        """
        Handles on control event

        Args:
            event_id: event id of control.
        """


    def on_value_input_control_enter(self) -> bool:
        """
        Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        #----------------- ENTER inside a view control

        if name == "___DOM___SubmitChanges___":
            self.palette_service.update_palette(-1, True)

            return


        #----------------- execute the value update

        if self.input_mode == InputMode.HandleModify:
            self.handle_modi_service.reset_value()

        self.palette_service.modify_element_property(page, name, value)

        self.update_handle_input()


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        #----------------- cancel the input

        if self.input_mode == InputMode.RefPoint:
            self.palette_service.close_palette()

            return True


        #----------------- cancel the handle modification

        if self.input_mode == InputMode.HandleModify:
            self.handle_modi_service.reset_value()
            self.palette_service.update_palette(-1, True)
            self.update_handle_input()

            return False


        #----------------- create the PythonPart in Allplan and start the next input

        self.handle_modi_service.stop()

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(), self.placement_mat,
                                           self.model_ele_list, self.modify_uuid_list, None)


        #----------------- close the modification mode

        if self.modification_mode:
            self.palette_service.close_palette()

            return True


        #----------------- start the next placement

        self.input_mode = InputMode.RefPoint

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Placement point"))

        return False


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """

        if self.input_mode == InputMode.RefPoint:
            input_pnt = self.coord_input.GetCurrentPoint().GetPoint()

            self.placement_mat = AllplanGeo.Matrix3D()
            self.placement_mat.SetTranslation(AllplanGeo.Vector3D(input_pnt))

        self.draw_preview()


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """

        self.on_preview_draw()


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """
        Handles the process mouse message event

        Args:
            mouse_msg: the mouse message.
            pnt      : the input point.
            msg_info : additional message info.

        Returns:
            True/False for success.
        """

        result = True

        if self.input_mode == InputMode.RefPoint:
            input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

            self.placement_mat = AllplanGeo.Matrix3D()
            self.placement_mat.SetTranslation(AllplanGeo.Vector3D(input_pnt))


        #----------------- Select a handle

        else:
            result = self.handle_modi_service.process_mouse_msg(mouse_msg, pnt, msg_info)


        #----------------- draw the preview and check for final point input

        self.draw_preview()

        if not result or self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- change to handle selection

        if self.input_mode in [InputMode.RefPoint, InputMode.HandleModify]:
            self.palette_service.update_palette(-1, True)

            self.start_handle_select()

            return True


        #----------------- change to handle modification

        if self.input_mode == InputMode.HandleSelect:
            self.input_mode = InputMode.HandleModify

            self.handle_modi_service.start_new_handle_point_input(self.global_str_table_service)

        return True


    def create_show_handles(self):
        """ create and show the handles
        """

        self.input_mode = InputMode.HandleSelect

        build_ele = self.build_ele_list[0]

        handle_list = [HandleProperties("Length",
                                        AllplanGeo.Point3D(build_ele.Length.value, 0, 0), AllplanGeo.Point3D(),
                                        [HandleParameterData("Length", HandleParameterType.X_DISTANCE)],
                                        HandleDirection.X_DIR)]

        handle_list[0].info_text = "Length"

        handle_list.append(HandleProperties("Width",
                                            AllplanGeo.Point3D(0, build_ele.Width.value, 0), AllplanGeo.Point3D(),
                                            [HandleParameterData("Width", HandleParameterType.Y_DISTANCE)],
                                            HandleDirection.Y_DIR))

        handle_list[1].info_text = "Width"

        handle_list.append(HandleProperties("Height",
                                            AllplanGeo.Point3D(0, 0, build_ele.Height.value), AllplanGeo.Point3D(),
                                            [HandleParameterData("Height", HandleParameterType.Z_DISTANCE)],
                                            HandleDirection.Z_DIR))

        handle_list[1].info_text = "Height"

        self.handle_modi_service.start(handle_list, self.placement_mat,
                                       self.coord_input.GetInputViewDocument(),
                                       self.coord_input.GetViewWorldProjection(),
                                       True)


    def update_handle_input(self):
        """ update the handle input """

        #----------------- start a new handle selection

        if self.input_mode == InputMode.HandleModify:
            input_str = self.global_str_table_service.get_string("e_SELECT_HANDLE", "Select the handle")

            self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert(input_str))


        #----------------- update the palette, preview and handles

        self.draw_preview()

        self.create_show_handles()

        AllplanBaseElements.ExecutePreviewDraw(self.coord_input.GetInputViewDocument())


    def draw_preview(self):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """

        build_ele = self.build_ele_list[0]

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value,
                                                       build_ele.Width.value,
                                                       build_ele.Height.value)

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


        #------------------ Append cubes as new Allplan elements

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(), self.placement_mat,
                                               self.model_ele_list, False, None, False)


    def start_handle_select(self):
        """ start the handle select """

        self.create_show_handles()

        input_str = self.global_str_table_service.get_string("e_SELECT_HANDLE", "Select the handle")

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert(input_str))


    def update_after_favorite_read(self):
        """ update after favorite read """

        self.handle_modi_service.stop()

        self.palette_service.update_palette(-1, True)

        if self.input_mode != InputMode.RefPoint:
            self.update_handle_input()


    def reset_param_values(self, _build_ele_list: List[BuildingElement]):
        """ reset the parameter values

        Args:
            _build_ele_list:            building element list
        """

        BuildingElementListService.reset_param_values(self.build_ele_list)

        self.update_after_favorite_read()


    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
