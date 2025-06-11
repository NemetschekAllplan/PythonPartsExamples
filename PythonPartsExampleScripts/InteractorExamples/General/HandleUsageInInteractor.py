"""Script for HandleUsageInInteractor show the usage of handles in an interactor PythonPart"""
from __future__ import annotations

import enum

from typing import TYPE_CHECKING, Any, cast
from pathlib import Path

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseInteractor import BaseInteractor, BaseInteractorData
from BuildingElementAttributeList import BuildingElementAttributeList
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from HandleDirection import HandleDirection
from HandleModificationService import HandleModificationService
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from PythonPartTransaction import PythonPartTransaction
from PythonPartUtil import PythonPartUtil
from StringTableService import StringTableService
from TypeCollections.ModelEleList import ModelEleList
from TypeCollections.ModificationElementList import ModificationElementList
from CreateElementResult import CreateElementResult
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.HandleUsageInInteractorBuildingElement import HandleUsageInInteractorBuildingElement as BuildingElement
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """
    return True     # All versions are supported


def create_preview(build_ele : BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele:  building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    script_path    = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_interactor(interactor_data: BaseInteractorData) -> object:
    """ Create the interactor

    Args:
        interactor_data: interactor data

    Returns:
        Created interactor object
    """

    return HandleUsageInInteractor(interactor_data)


class HandleUsageInInteractor(BaseInteractor):
    """Definition of the interactor
    """

    class InteractorInputMode(enum.IntEnum):
        """ definition of the interactor modes"""
        PLACEMENT       = 0
        """ Mode, when the PythonPart is about to be placed. It should follow the mouse cursor """
        PARAMETER_INPUT = 1
        """ Mode, when the PythonPart is placed and the user can input the parameters in the palette"""
        HANDLE_MODIFY   = 2
        """ Mode, when the user is modifying the handle. The handle is grabbed and follows the mouse"""

    def __init__(self,
                 interactor_data: BaseInteractorData):
        """ Create the interactor

        Args:
            interactor_data: interactor data
        """

        # set initial values
        self.build_ele                 = cast(BuildingElement, interactor_data.build_ele_list[0])
        self.coord_input               = interactor_data.coord_input
        self.modification_element_list = interactor_data.modify_uuid_list
        self.handle_modi_service       = HandleModificationService(interactor_data.coord_input,
                                                                   interactor_data.build_ele_list, interactor_data.control_props_list)
        self.global_str_table_service  = interactor_data.global_str_table_service
        self.box                       = Box(self.build_ele)
        self.rotation                  = AllplanGeo.Angle()

        # show palette
        self.palette_service = BuildingElementPaletteService(interactor_data.build_ele_list,
                                                             interactor_data.build_ele_composite,
                                                             self.build_ele.script_name,
                                                             interactor_data.control_props_list,
                                                             self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)

        if self.modification_element_list.is_modification_element():
            self.input_mode       = self.InteractorInputMode.PARAMETER_INPUT
            self.placement_matrix = self.build_ele.get_insert_matrix()

            self.start_handle_select() # palette must be shown, before this call!

        else:
            self.input_mode       = self.InteractorInputMode.PLACEMENT
            self.placement_matrix = AllplanGeo.Matrix3D()
            input_control_data    = AllplanIFW.ValueInputControlData(AllplanIFW.eValueInputControlType.eANGLE_COMBOBOX,
                                                                     bDisableCoord=False)

            self.coord_input.InitFirstPointValueInput(AllplanIFW.InputStringConvert("Place PythonPart"), input_control_data)


    def modify_element_property(self,
                                page: int,
                                name: str,
                                value: Any):
        """Handles the event of modifying a property value in the property palette or in the handle input field

        Args:
            page:   page number of the palette page
            name:   name of the property
            value:  new value of the property
        """

        # process the input in handle's input field
        if name == "___SubmitChanges___":
            self.palette_service.update_palette(-1, True)
            return

        # process the input in the palette done while a handle is grabbed
        if self.input_mode == self.InteractorInputMode.HANDLE_MODIFY:
            self.input_mode = self.InteractorInputMode.PARAMETER_INPUT

        # process the regular input in the palette
        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

        # update the value in the handle input field after the input in the palette
        if self.input_mode == self.InteractorInputMode.PARAMETER_INPUT:
            self.update_handle_input()

        self.draw_preview()


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """Processes the mouse message event

        The event is triggered with every mouse movement or click inside the viewport

        Args:
            mouse_msg:  Mouse message
            pnt:        Mouse position in the viewport
            msg_info:   additional Message info

        Returns:
            True, when the event is processed, False otherwise
        """

        #------- handling mouse move

        match self.input_mode:
            case self.InteractorInputMode.PLACEMENT:
                coord_input_result = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info)

                self.placement_matrix.SetRotation(AllplanGeo.Line3D(0,0,0,0,0,1), self.rotation)
                self.placement_matrix = self.recalculate_placement(coord_input_result.GetPoint())

            case _:
                handle_grabbed = self.handle_modi_service.process_mouse_msg(mouse_msg, pnt, msg_info)

        self.draw_preview()

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        #------- handling mouse click

        match self.input_mode:
            case self.InteractorInputMode.PLACEMENT:
                self.input_mode = self.InteractorInputMode.PARAMETER_INPUT
                self.start_handle_select()

            case self.InteractorInputMode.PARAMETER_INPUT:
                if handle_grabbed:
                    self.input_mode = self.InteractorInputMode.HANDLE_MODIFY
                    self.handle_modi_service.start_new_handle_point_input(self.global_str_table_service)

            case self.InteractorInputMode.HANDLE_MODIFY:
                self.input_mode = self.InteractorInputMode.PARAMETER_INPUT
                self.palette_service.update_palette(-1, True)
                self.start_handle_select()

        return True

    def on_cancel_function(self) -> bool:
        """Handles the event of the cancel the input by pressing ESC

        Returns:
            True, when PythonParts can be terminated, False otherwise
        """

        if self.input_mode == self.InteractorInputMode.HANDLE_MODIFY:
            self.handle_modi_service.reset_value()
            self.start_handle_select()
            self.input_mode = self.InteractorInputMode.PARAMETER_INPUT
            return False

        if self.input_mode == self.InteractorInputMode.PARAMETER_INPUT:
            self.handle_modi_service.stop()
            self.execute_db_transaction()

        BuildingElementListService.write_to_default_favorite_file([self.build_ele])
        self.palette_service.close_palette()
        return True

    def on_control_event(self, _event_id: int) -> None:
        """Handles the event of hitting a button in the property palette

        Args:
            _event_id: ID of the event
        """

    def on_mouse_leave(self):
        """Handles the event of mouse leaving the viewport"""

        self.draw_preview()

    def on_preview_draw(self):
        """Handles the event on_preview_draw

        The event is triggered e.g. during the input in the dialog line
        """

        if self.input_mode == self.InteractorInputMode.PLACEMENT:
            self.rotation = AllplanGeo.Angle(self.coord_input.GetInputControlValue())
            self.placement_matrix = self.recalculate_placement(self.coord_input.GetCurrentPoint().GetPoint())

        self.draw_preview()

    def recalculate_placement(self, point: AllplanGeo.Point3D) -> AllplanGeo.Matrix3D:
        """Recalculate the placement of the PythonPart

        Args:
            point: placement point

        Returns:
            Placement matrix
        """

        placement = AllplanGeo.Matrix3D()
        placement.SetRotation(AllplanGeo.Line3D(0,0,0,0,0,1), self.rotation)
        placement.Translate(AllplanGeo.Vector3D(point))

        return placement

    def draw_preview(self, static: bool = False):
        """Draws the preview of the PythonPart

        Args:
            static: True to draw a static preview (not refreshed with every mouse movement), False otherwise
        """

        self.box.update()

        AllplanBaseEle.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                          self.placement_matrix,
                                          self.box.preview_elements,
                                          True, None,
                                          asStaticPreview = static)

    def execute_db_transaction(self):
        """Execute the transaction by writing the elements in the database"""

        pyp_transaction = PythonPartTransaction(self.coord_input.GetInputViewDocument())
        pyp_transaction.execute(self.placement_matrix,
                                self.coord_input.GetViewWorldProjection(),
                                self.box.create_pythonpart(self.build_ele),
                                self.modification_element_list)


    def on_value_input_control_enter(self) -> bool:
        """Handles the event of pressing Enter in the input field in the dialog line

        Returns:
            True for success.
        """
        return True

    def start_handle_select(self):
        """ Start the handle selection

        Show the handles and prompt the user to select a handle
        """

        self.handle_modi_service.start(self.box.handles, self.placement_matrix,
                                       self.coord_input.GetInputViewDocument(),
                                       self.coord_input.GetViewWorldProjection(),
                                       True)

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Select handle"))

    def update_handle_input(self):
        """Update the handle input """

        #----------------- start a new handle selection

        if self.input_mode == self.InteractorInputMode.HANDLE_MODIFY:
            self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Select the handle"))


        #----------------- update the palette, preview and handles

        self.draw_preview()

        self.handle_modi_service.start(self.box.handles, self.placement_matrix,
                                       self.coord_input.GetInputViewDocument(),
                                       self.coord_input.GetViewWorldProjection(),
                                       True)

        AllplanBaseEle.ExecutePreviewDraw(self.coord_input.GetInputViewDocument())



class Box:
    """Definition of the box"""

    def __init__(self, build_ele: BuildingElement):
        """Initialize the box

        Args:
            build_ele: Building element with the parameter properties
        """

        self.build_ele = build_ele
        self.update()

    def update(self):
        """Update the box"""

        self._length = self.build_ele.Length.value
        self._width  = self.build_ele.Width.value
        self._height = self.build_ele.Height.value

        # do initial calculations
        self._geometry   = self._calculate_geometry()
        self._attributes = self._calculate_atributes()
        self._handles    = self._calculate_handles()

    @property
    def length(self) -> float:
        """Length of the box"""
        return self._length

    @property
    def width(self) -> float:
        """Width of the box"""
        return self._width

    @property
    def height(self) -> float:
        """Height of the box"""
        return self._height

    @property
    def geometry(self) -> AllplanGeo.Polyhedron3D:
        """Geometry of the box"""
        return self._geometry

    @property
    def attributes(self) -> BuildingElementAttributeList:
        """Attributes of the box"""
        return self._attributes

    @property
    def handles(self) -> list[HandleProperties]:
        """Handle list"""
        return self._handles

    @property
    def preview_elements(self) -> ModelEleList:
        """List with model elements e.g. for a preview"""

        model_ele_list = ModelEleList()
        model_ele_list.append_geometry_3d(self._geometry)
        return model_ele_list

    def _calculate_geometry(self) -> AllplanGeo.Polyhedron3D:
        """Calculate the geometry of the box

        Returns:
            Geometry of the box as polyhedron
        """
        return AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.AxisPlacement3D(), self._length, self._width, self._height)

    def _calculate_atributes(self) -> BuildingElementAttributeList:
        """Calculate the attributes of the box

        Returns:
            List of attributes
        """

        _err, volume, surface, _cg_point = AllplanGeo.CalcMass(self._geometry)

        attributes = BuildingElementAttributeList()
        attributes.add_attribute(220, self._length / 1e3)
        attributes.add_attribute(221, self._width / 1e3)
        attributes.add_attribute(222, self._height / 1e3)
        attributes.add_attribute(722, surface / 1e6)
        attributes.add_attribute(223, volume / 1e9)

        return attributes

    def _calculate_handles(self) -> list[HandleProperties]:
        """Calculate the handles

        Returns:
            List with the handles
        """
        handles: list[HandleProperties] = []

        x_handle_parameter_data = [HandleParameterData("Length",
                                                    HandleParameterType.X_DISTANCE)]

        x_handle = HandleProperties("Length",
                                    AllplanGeo.Point3D(self._length,0,0),
                                    AllplanGeo.Point3D(),
                                    x_handle_parameter_data,
                                    HandleDirection.X_DIR)

        handles.append(x_handle)

        y_handle_parameter_data = [HandleParameterData("Width",
                                                    HandleParameterType.Y_DISTANCE)]

        y_handle = HandleProperties("Width",
                                    AllplanGeo.Point3D(0,self._width,0),
                                    AllplanGeo.Point3D(),
                                    y_handle_parameter_data,
                                    HandleDirection.Y_DIR)
        handles.append(y_handle)

        z_handle_parameter_data = [HandleParameterData("Height",
                                                    HandleParameterType.Z_DISTANCE)]

        z_handle = HandleProperties("Height",
                                    AllplanGeo.Point3D(0,0,self._height),
                                    AllplanGeo.Point3D(),
                                    z_handle_parameter_data,
                                    HandleDirection.Z_DIR)
        handles.append(z_handle)

        xyz_handle_parameter_data = [HandleParameterData("Length", HandleParameterType.X_DISTANCE,False),
                                    HandleParameterData("Width", HandleParameterType.Y_DISTANCE,False),
                                    HandleParameterData("Height", HandleParameterType.Z_DISTANCE,False)]

        xyz_handle = HandleProperties("XYZ",
                                    AllplanGeo.Point3D(self._length,
                                                            self._width,
                                                            self._height),
                                    AllplanGeo.Point3D(),
                                    xyz_handle_parameter_data,
                                    HandleDirection.XYZ_DIR)

        handles.append(xyz_handle)

        return handles


    def create_pythonpart(self, build_ele: BuildingElement) -> list[Any]:
        """Create the PythonPart as a list containing MacroElement and MacroPlacementElement

        Args:
            build_ele: Building element with the parameter properties

        Returns:
            List with the created PythonPart elements
        """

        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.preview_elements)
        pyp_util.add_attribute_list(self._attributes)

        return pyp_util.create_pythonpart(build_ele)
