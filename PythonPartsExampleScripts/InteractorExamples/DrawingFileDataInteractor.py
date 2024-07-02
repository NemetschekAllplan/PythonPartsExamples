"""
Script for DrawingFileDataInteractor
"""

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from BuildingElementListService import BuildingElementListService


print('Load DrawingFileDataInteractor.py')


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


def create_element(build_ele, doc):
    """
    Creation of element (only necessary for the library preview)

    Args:
        build_ele: the building element.
        doc:       input document
    """

    del build_ele
    del doc

    com_prop = AllplanBaseElements.CommonProperties()

    com_prop.GetGlobalProperties()

    text_prop = AllplanBasisElements.TextProperties()

    model_ele_list = [AllplanBasisElements.TextElement(com_prop, text_prop, "Drawing file data", AllplanGeo.Point2D(0, 100))]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, show_pal_close_btn, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return DrawingFileDataInteractor(coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list)


class DrawingFileDataInteractor():
    """
    Definition of class DrawingFileDataInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
        """
        Initialization of class DrawingFileDataInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input         = coord_input
        self.pyp_path            = pyp_path
        self.str_table_service   = str_table_service
        self.model_ele_list      = None
        self.build_ele_service   = BuildingElementService()
        self.drawing_minmax      = AllplanGeo.MinMax3D()
        self.build_ele_list      = build_ele_list
        self.build_ele_composite = build_ele_composite
        self.control_props_list  = control_props_list

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             "Drawing file data",
                                                             self.control_props_list, "DrawingFileDataInteractor")

        self.palette_service.show_palette("DrawingFileDataInteractor")



        #----------------- get the properties and start the input

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Execute by button click, info inside the trace window"))


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_control_event(self, event_id):
        """
        On control event

        Args:
            event_id: event id of control.
        """

        build_ele = self.build_ele_list[0]

        doc = self.coord_input.GetInputViewDocument()
            
        drawing_file_serv = AllplanBaseElements.DrawingFileService()


        #----------------- create elements inside the drawing file

        print("")
        print("---------------------------------------------------------------------------")
        print("")

        if event_id == 1001:
            print("State of the loaded drawing files:")
            print(drawing_file_serv.GetFileState())

            return

        if event_id == 1002:
            print("Name of the active drawing file: ", AllplanElementAdapter.DocumentNameService.GetActiveDocumentName())

            return

        if event_id == 1003:
            print("Name of the loaded drawing files by number:")

            file_list = drawing_file_serv.GetFileState()

            for number, _ in file_list:
                print(AllplanElementAdapter.DocumentNameService.GetDocumentNameByFileNumber(number, False, True, " - "))

            return

        if event_id == 1004:
            print("Name of the loaded drawing files by index:")

            file_list = drawing_file_serv.GetFileState()

            for index in range(1, len(file_list) + 1):
                print(index, ": ", AllplanElementAdapter.DocumentNameService.GetDocumentNameByFileIndex(index, True, True, " - "))

            return

        if event_id == 1005:
            print("Number and name of the loaded drawing files:")

            for name, number in AllplanElementAdapter.DocumentNameService.GetLoadedDocumentsNameData():
                print(number, name)

            return


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
