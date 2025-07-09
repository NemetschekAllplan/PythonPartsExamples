""" Example script showing the integration of WPF technology (C#) into a PythonPart script"""

from pathlib import Path

import clr
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from CreateElementResult import CreateElementResult
from StringTableService import StringTableService
from TypeCollections.ModelEleList import ModelEleList
from TypeCollections.ModificationElementList import ModificationElementList

# ----------------- using pythonnet, see http://pythonnet.github.io/

script_path = Path(__file__).resolve()

clr.AddReference(str(script_path.parent / "PythonWPFConnection/Bin/PythonWPFConnection.dll"))

from PythonWPFConnection import BoxDialog, NameValueArgs

print('Load UsingClrInteractor.py')


def check_allplan_version(_build_ele: BuildingElement, _version: float) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(_build_ele: BuildingElement, _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of an element only for the library preview

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        CreateElementResult with the created element
    """

    model_ele_list = ModelEleList()
    model_ele_list.append_geometry_3d(AllplanGeo.Polyhedron3D.CreateCuboid(1000, 2000, 3000))

    return CreateElementResult(model_ele_list)


def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties],
                      modification_ele_list   : ModificationElementList) -> BaseInteractor:
    """ Create the interactor

    Args:
        coord_input:              API object for the coordinate input, element selection, ... in the Allplan view
        pyp_path:                 path of the pyp file
        global_str_table_service: global string table service
        build_ele_list:           list with the building elements
        build_ele_composite:      building element composite with the building element constraints
        control_props_list:       control properties list
        _modification_ele_list:   UUIDs of the existing elements in the modification mode

    Returns:
          Created interactor object
    """

    return UsingClrInteractor(coord_input, pyp_path, global_str_table_service,
                              build_ele_list, build_ele_composite, control_props_list, modification_ele_list)


class UsingClrInteractor(BaseInteractor):
    """Definition of class UsingClrInteractor"""

    def __init__(self,
                 coord_input:                AllplanIFW.CoordinateInput,
                 _pyp_path:                   str,
                 _global_str_table_service:   StringTableService,
                 _build_ele_list:             list[BuildingElement],
                 _build_ele_composite:        BuildingElementComposite,
                 _control_props_list:         list[BuildingElementControlProperties],
                 _modify_uuid_list:           ModificationElementList
                 ):
        """Initialize

        Args:
            coord_input:                API object for the coordinate input, element selection, ... in the Allplan view
            _pyp_path:                   path of the pyp file
            _global_str_table_service:   global string table service
            _build_ele_list:             list with the building elements
            _build_ele_composite:        building element composite with the building element constraints
            _control_props_list:         control properties list
            _modify_uuid_list:           UUIDs of the existing elements in the modification mode
        """

        self.coord_input    = coord_input
        self.model_ele_list = ModelEleList()

        # Show the WPF dialog
        self.box_length = 1000.
        self.box_width  = 2000.
        self.box_height = 3000.

        self.box_dialog = BoxDialog(self.box_length, self.box_width, self.box_height)

        self.box_dialog.ShowInTaskbar = False
        self.box_dialog.Show()

        # subscribe to events
        self.box_dialog.UpdateValue += self.on_value_changed_handler

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

    def modify_element_property(self, page, name, value):
        """Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

    def on_cancel_function(self):
        """Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.box_dialog.Close()

        return True

    def on_preview_draw(self):
        """Handles the preview draw event"""

        self.draw_preview(self.coord_input.GetCurrentPoint().GetPoint())

    def on_control_event(self, event_id: int) -> bool:
        """Handles the control event

        Args:
            event_id:  the event id.

        Returns:
            True/False for success.
        """
        return False

    def on_value_input_control_enter(self) -> bool:
        """Handles the value input control enter event

        Returns:
            True/False for success.
        """
        return False

    def on_mouse_leave(self):
        """Handles the mouse leave event"""

        self.on_preview_draw()

    def on_value_changed_handler(self, _sender: BoxDialog, args: NameValueArgs) -> None:
        """ Handles the value changed event from the box dialog

        Args:
            _sender: the sender of the event.
            args:    the event arguments containing the name and value of the changed property.
        """
        if args.Name == "Length":
            self.box_length = args.Value

        elif args.Name == "Width":
            self.box_width = args.Value

        elif args.Name == "Height":
            self.box_height = args.Value

        self.draw_preview(self.coord_input.GetCurrentPoint().GetPoint())

    def process_mouse_msg(self, mouse_msg: int, pnt: AllplanGeo.Point2D, msg_info: AllplanIFW.AddMsgInfo) -> bool:
        """Handle mouse messages

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        self.draw_preview(input_pnt)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        # ----------------- Create the line and continue with from point input

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           self.model_ele_list, [], None)

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

        return True

    def draw_preview(self, input_pnt: AllplanGeo.Point3D):
        """Draw the preview

        Args:
            input_pnt:  Input point
        """

        box = AllplanGeo.Move(AllplanGeo.Polyhedron3D.CreateCuboid(self.box_length, self.box_width, self.box_height),
                              AllplanGeo.Vector3D(input_pnt))

        self.model_ele_list = ModelEleList()
        self.model_ele_list.append_geometry_3d(box)

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, True, None)
