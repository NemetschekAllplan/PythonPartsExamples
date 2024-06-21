"""
Script for ExecuteVisualScript
"""

from typing import Any, List

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementListService import BuildingElementListService
from ControlProperties import ControlProperties
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService
from VisualScriptService import VisualScriptService

from Utils import LibraryBitmapPreview

print('Load ExecuteVisualScript.py')


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
                               r"Examples\PythonParts\InteractorExamples\General\ExecuteVisualScript.png"))



def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path               : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : List[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : List[List[ControlProperties]],
                      _modify_uuid_list       : list) -> Any                 :
    """
    Create the interactor

    Args:
        coord_input:               coordinate input
        _pyp_path:                 path of the pyp file
        global_str_table_service:  global string table service
        build_ele_list:            building element list
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

      Returns:
          Created interactor object
      """

    return ExecuteVisualScript(coord_input, global_str_table_service, build_ele_list, build_ele_composite,
                               control_props_list)


class ExecuteVisualScript(BaseInteractor):
    """
    Definition of class ExecuteVisualScript
    """

    def __init__(self,
                 coord_input             : AllplanIFW.CoordinateInput,
                 global_str_table_service: StringTableService,
                 build_ele_list          : List[BuildingElement],
                 _build_ele_composite    : BuildingElementComposite,
                 control_props_list      : List[List[ControlProperties]]):
        """
        initialize and start the input

        Args:
            coord_input:               coordinate input
            global_str_table_service:  global string table service
            build_ele_list:            building element list
            _build_ele_composite:      building element composite
            control_props_list:        control properties list
        """

        self.coord_input              = coord_input
        self.first_point_input        = True
        self.first_point              = AllplanGeo.Point3D()
        self.model_ele_list           = []
        self.build_ele_list           = build_ele_list
        self.control_props_list       = control_props_list
        self.global_str_table_service = global_str_table_service
        self.vs_service               = self.create_vs_service()


        #----------------- start the input

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))


    def create_vs_service(self) -> VisualScriptService:
        """ create the service for the VS script

        Returns:
            created script service
        """

        script_name = "Examples\\VisualScripting\\Buildings\\Domes\\WireFrameDome.pyp" if self.build_ele_list[0].Script.value == 1 else \
                      "Examples\\VisualScripting\\Reinforcement\\AugerPileReinforcement.pyp"

        return VisualScriptService(self.coord_input,
                                   AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + script_name,
                                   self.global_str_table_service,
                                   self.build_ele_list, self.control_props_list,
                                   [])


    def on_control_event(self,
                         event_id: int):
        """
        Handles on control event

        Args:
            event_id: event id of control.
        """

        if self.vs_service:
            self.vs_service.on_control_event(event_id)


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

        if self.vs_service is None:
            return

        self.vs_service.modify_element_property(page, name, value)

        if name == "Script":
            self.vs_service.close_all()

            self.vs_service = self.create_vs_service()


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        if self.vs_service is not None:
            self.vs_service.on_cancel_function()

        return True


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """

        if self.first_point_input:
            return

        input_pnt = self.coord_input.GetCurrentPoint(self.first_point).GetPoint()

        self.draw_preview(input_pnt)


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

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info,
                                                   self.first_point, not self.first_point_input).GetPoint()


        #----------------- Set the input point

        if self.first_point_input:
            self.first_point = input_pnt

        else:
            self.draw_preview(input_pnt)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- Change to "To point" input

        if self.first_point_input:
            self.first_point_input = False

            self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("To point"))

            return True


        #----------------- Create the domes and continue with from point input

        line = AllplanGeo.Line3D(self.first_point, input_pnt)

        div_points = AllplanGeo.DivisionPoints(line, self.build_ele_list[0].Distance.value, 1.)

        model_ele_list = []

        for div_point in div_points.GetPoints():
            placement_mat = AllplanGeo.Matrix3D()
            placement_mat.SetTranslation(AllplanGeo.Vector3D(div_point))

            model_ele_list += self.vs_service.create_pythonpart(placement_mat, AllplanGeo.Matrix3D())

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                            AllplanGeo.Matrix3D(),
                                            model_ele_list, [], None)


        #----------------- change to from point input

        self.first_point_input = True

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

        return True


    def draw_preview(self, input_pnt: AllplanGeo.Point3D):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """

        line = AllplanGeo.Line3D(self.first_point, input_pnt)

        div_points = AllplanGeo.DivisionPoints(line, self.build_ele_list[0].Distance.value, 1.)

        preview_ele = self.vs_service.get_preview_elements()

        for div_point in div_points.GetPoints():
            placement_mat = AllplanGeo.Matrix3D()
            placement_mat.SetTranslation(AllplanGeo.Vector3D(div_point))

            AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                                   placement_mat,
                                                   preview_ele, False, None, False)


    def reset_param_values(self, _build_ele_list: List[BuildingElement]):
        """ reset the parameter values

        Args:
            _build_ele_list:            building element list
        """

        BuildingElementListService.reset_param_values(self.build_ele_list)

        self.vs_service.reset_param_values()


    def execute_save_favorite(self, file_name: str):
        """ save the favorite data

        Args:
            file_name: name of the favorite file
        """

        self.vs_service.execute_save_favorite(file_name)


    def execute_load_favorite(self, file_name: str):
        """ load the favorite data

        Args:
            file_name: name of the favorite file
        """

        BuildingElementListService.read_from_file(file_name, self.build_ele_list)

        self.vs_service.execute_load_favorite(file_name)


    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
