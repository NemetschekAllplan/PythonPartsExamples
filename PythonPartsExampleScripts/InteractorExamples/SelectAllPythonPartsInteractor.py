"""
Script for SelectAllPythonPartsInteractor
"""

import math
from enum import Enum

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BuildingElementService import BuildingElementService
from TraceService import TraceService

print('Load SelectAllPythonPartsInteractor.py')


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

    return (None, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return SelectAllPythonPartsInteractor(coord_input, pyp_path, str_table_service)


class SelectAllPythonPartsInteractor():
    """
    Definition of class SelectAllPythonPartsInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class SelectAllPythonPartsInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Output is shown in the trace window"))

        self.select_python_parts()


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

        return True


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


    def select_python_parts(self):
        """
        Select all PythonParts from the document
        """

        for element in AllplanBaseElements.ElementsSelectService.SelectAllElements(self.coord_input.GetInputViewDocument()):
            if element != AllplanElementAdapter.PythonPart_TypeUUID:
                continue

            success, name, parameters = AllplanBaseElements.PythonPartService.GetParameter(element)

            success, placement_mat = AllplanBaseElements.PythonPartService.GetPlacementMatrix(element)

            print("----------------------------------------------------------------------")
            
            TraceService.trace_1(name)
            print("")

            for parameter in parameters:
                text = str(parameter).replace("\n", "")

                TraceService.trace_1(text)

            print()
            print()
