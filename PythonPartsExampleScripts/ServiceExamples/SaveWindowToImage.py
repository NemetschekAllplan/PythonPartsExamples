"""An example script showing the API functionality of saving the content
of a viewport into an image file
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
import NemAll_Python_Utility as AllplanUtil
from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from StringTableService import StringTableService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SaveWindowToImageBuildingElement import SaveWindowToImageBuildingElement
else:
    SaveWindowToImageBuildingElement = BuildingElement


def check_allplan_version(build_ele: BuildingElement,
                          version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        build_ele: building element with the parameter properties
        version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_preview(build_ele:   BuildingElement,
                   doc:         AllplanElementAdapter.DocumentAdapter) :
    """ Create the library preview

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """
    pass

def create_interactor(coord_input:                 AllplanIFWInput.CoordinateInput,
                      pyp_path:                    str,
                      global_str_table_service:    StringTableService,
                      build_ele_list:              list[BuildingElement],
                      build_ele_composite:         BuildingElementComposite,
                      control_props_list:          list[BuildingElementControlProperties],
                      modify_uuid_list:            list[str]) -> ...:
    """Function for the interactor creation, called when PythonPart is initialized.
    When called, the PythonPart framework performs the following steps:

    - reads the parameters and their values from the xxx.pyp file and stores them in the buld_ele_list
    - if tag `ReadLastInput` is set to True: read the parameter values from the last input,
        (stored in ...\\Usr\\_user_name_\\tmp\\_python_part_name.pyv) and assign them to the parameters
        in build_ele_list
    - if starting an input by Match from the context menu or double right click: read the parameter
        values from the attribute @611@ of the matched PythonPart and assign them to the parameters
        in build_ele_list
    - if in modification mode: read the parameter values from the attribute @611@ of the selected
        PythonPart and assign them to the parameters in build_ele_list

    Args:
        coord_input:               coordinate input
        pyp_path:                  path of the pyp file
        global_str_table_service:  global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        modify_uuid_list:          UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return SaveWindowToImage(coord_input, pyp_path, global_str_table_service, build_ele_list,
                             build_ele_composite, control_props_list, modify_uuid_list)


class SaveWindowToImage(BaseInteractor):
    """ Interactor class to show the feature of saving a viewport content as
    an image file.

    This interactor shows a palette, where the user can enter parameters of the image
    (save location, resolution, etc...). When the save path is selected, the user
    can click in any viewport to save its content as an image.

    The user can click on multiple viewports. The files are then as: file.jpg, file(1).jpg, file(2).jpg...
    """

    def __init__(self,
                 coord_input:                AllplanIFWInput.CoordinateInput,
                 _pyp_path:                  str,
                 _global_str_table_service:  StringTableService,
                 build_ele_list:             list[BuildingElement],
                 build_ele_composite:        BuildingElementComposite,
                 control_props_list:         list[BuildingElementControlProperties],
                 _modify_uuid_list:          list[str]):
        """ Constructor

        Args:
            coord_input:               coordinate input
            _pyp_path:                 path of the pyp file
            _global_str_table_service: global string table service for default strings
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
            _modify_uuid_list:         UUIDs of the existing elements in the modification mode
        """
        self.coord_input         = coord_input
        self.build_ele_list      = build_ele_list
        self.build_ele           = cast(SaveWindowToImageBuildingElement, build_ele_list[0])
        self.build_ele_composite = build_ele_composite
        self.control_props_list  = control_props_list
        self.image_path          = Path()

        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list,
                                                             self.build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)
        self.coord_input.SetInputText(AllplanIFWInput.InputStringConvert("Define the file path for the screenshot"))

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any) -> None:
        """ Called after each property modification (e.g., in the property palette
        or by using a handle)

        Args:
            page:   index of the page, beginning with 0
            name:   name of the modified property
            value:  new property value
        """
        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

    def on_control_event(self,
                         event_id: int) -> None:
        """ Called when an event is triggered by a palette control (ex. button)

        Args:
            event_id:   id of the triggered event, defined in the tag `<EventId>`
        """

    def on_mouse_leave(self) -> None:
        """ Called when the mouse leaves the viewport window """

    def on_preview_draw(self) -> None:
        """ Called when an input in the dialog line is done (e.g. input of a coordinate)."""

    def on_value_input_control_enter(self) -> bool:
        """Called when enter key is pressed inside the value input control

            Returns:
                True/False for success.
        """

        return True

    def process_mouse_msg(self,
                          mouse_msg:    int,
                          pnt:          AllplanGeometry.Point2D,
                          msg_info:     AllplanIFWInput.AddMsgInfo) -> bool:
        """ Called on each mouse message. A mouse message can be mouse movement, pressing a mouse button
        or releasing it.

        Args:
            mouse_msg:  the mouse message (e.g. 512 - mouse movement)
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """
        if not self.coord_input.IsMouseMove(mouse_msg) and self.image_path != Path():
            save_path = self.obtain_save_path(self.image_path)

            # implementation for creating a snapshot with a specific resolution
            if self.build_ele.SetImageSize.value:
                success = AllplanBaseElements.DrawingService.SaveWindowToImageFile(str(save_path),
                                                                                   pixelWidth  = self.build_ele.ImageSize.value[0],
                                                                                   pixelHeight = self.build_ele.ImageSize.value[1])

            # implementation for creating a snapshot with the viewport's resolution
            else:
                success = AllplanBaseElements.DrawingService.SaveWindowToImageFile(str(save_path))

            if success:
                AllplanUtil.ShowMessageBox(f"Snapshot created under {str(save_path)}", AllplanUtil.MB_OK)
            else:
                AllplanUtil.ShowMessageBox(f"An error occured when creating a snapshot.", AllplanUtil.MB_OK)

            self.coord_input.SetInputText(AllplanIFWInput.InputStringConvert("Click another viewport"))

        return True

    def set_active_palette_page_index(self, active_page_index: int):
        """ Called when changing page in the property palette

        Args:
            active_page_index: index of the active page, starting from 0
        """
        if self.build_ele.ImageFilePath.value != "":
            self.image_path = Path(self.build_ele.ImageFilePath.value)
            self.coord_input.SetInputText(AllplanIFWInput.InputStringConvert("Click on the desired viewport to make a screenshot"))


    def on_cancel_function(self) -> bool:
        """ Called when ESC key is pressed.

        Returns:
            True when the PythonPart framework should terminate the PythonPart, False otherwise.
        """
        self.palette_service.close_palette()
        return True

    @staticmethod
    def obtain_save_path(path: Path):
        """Obtain the absolute path to save the image file to prevent overwriting existing file.

        If the given path already exists, add "(1)" to the file name, like: C:/file_name(1).jpg.
        If this file also exists, add (2) and so one, until the obtained path is non-existent.

        Args:
            path:   absolute file path to check

        Returns:
            obtained absolute file path
        """
        counter = 1
        save_path = path
        while save_path.exists():
            save_path = Path(path.parent,path.stem + f"({counter})").with_suffix(path.suffix)
            counter +=1
        return save_path
