"""
Script for starting the Python debugger
"""

import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementListService import BuildingElementListService

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_preview(_build_ele_list, _build_ele_composite, _doc):
    return ([], None, None)


def create_interactor(coord_input, pyp_path, show_pal_close_btn, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
    """ Create the interactor """

    return SetTraceLevel(coord_input, build_ele_list, build_ele_composite,  control_props_list)


class SetTraceLevel():
    def __init__(self, coord_input, build_ele_list, build_ele_composite,  control_props_list):
        self.build_ele_list = build_ele_list

        BuildingElementListService.read_from_file(AllplanSettings.AllplanPaths.GetUsrPath() + "PythonPartTraceLevel.dat", self.build_ele_list)

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             "SetTraceLevel",
                                                             control_props_list, "")

        self.palette_service.show_palette("SetTraceLevel")

        coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Set the trace level"))


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True


    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            build_ele:  the building element.
            name:       the name of the property.
            value:      new value for property.

        Returns:
            True/False if palette refresh is necessary
        """

        self.palette_service.modify_element_property(page, name, value)

        BuildingElementListService.write_to_file(AllplanSettings.AllplanPaths.GetUsrPath() + "PythonPartTraceLevel.dat", self.build_ele_list)

        return False


    def process_mouse_msg(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        return True