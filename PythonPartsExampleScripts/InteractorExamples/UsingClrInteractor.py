"""
Script for UsingClrInteractor
"""

import sys

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_AllplanSettings as AllplanSettings

etc_path = AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()


#----------------- using pythonnet, see http://pythonnet.github.io/

import clr

clr.AddReference(etc_path + "\\PythonPartsExampleScripts\\InteractorExamples\\PythonWPFConnection\\Bin\\PythonWPFConnection.dll")

from PythonWPFConnection import BoxDialog
from PythonWPFConnection import NameValueArgs

print('Load UsingClrInteractor.py')


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

    model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, AllplanGeo.Polyhedron3D.CreateCuboid(1000, 2000, 3000))]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):

    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return UsingClrInteractor(coord_input, pyp_path, str_table_service)


class UsingClrInteractor():
    """
    Definition of class UsingClrInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class UsingClrInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service

        self.box_length = 1000.
        self.box_width  = 2000.
        self.box_height = 3000.

        self.box_dialog = BoxDialog(self.box_length, self.box_width, self.box_height)

        self.box_dialog.ShowInTaskbar = False
        self.box_dialog.Show()

        self.box_dialog.UpdateValue += self.on_value_changed_handler

        self.com_prop = AllplanBaseElements.CommonProperties()

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))


    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.box_dialog.Close()

        return True


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """

        self.draw_preview(self.coord_input.GetCurrentPoint().GetPoint())


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """

        self.on_preview_draw()


    def on_value_changed_handler(self, sender, args):
        if args.Name == "Length":
            self.box_length = args.Value

        elif args.Name == "Width":
            self.box_width = args.Value

        elif args.Name == "Height":
            self.box_height = args.Value

        self.draw_preview(self.coord_input.GetCurrentPoint().GetPoint())


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

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        self.draw_preview(input_pnt)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- Create the line and continue with from point input

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                            AllplanGeo.Matrix3D(),
                                            self.model_ele_list, [], None)

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

        return True


    def draw_preview(self, input_pnt):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """

        box = AllplanGeo.Move(AllplanGeo.Polyhedron3D.CreateCuboid(self.box_length, self.box_width, self.box_height),
                              AllplanGeo.Vector3D(input_pnt))

        self.model_ele_list = [AllplanBasisElements.ModelElement3D(self.com_prop, box)]

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                                AllplanGeo.Matrix3D(),
                                                self.model_ele_list, True, None)
