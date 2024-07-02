"""
Script for HaunchReinforcementFromFileInteractor
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Utility as AllplanUtil

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from BuildingElementConverter import BuildingElementConverter
from Utils.TabularDataUtil import read_csv
from Utils.LibraryBitmapPreview import create_libary_bitmap_preview

print('Load HaunchReinforcementFromFileInteractor.py')


def check_allplan_version(_build_ele, _version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_preview(_build_ele, _doc):
    """
    Creation of element (only necessary for the library preview)

    Args:
        build_ele: the building element.
        doc:       input document
    """

    elements = create_libary_bitmap_preview(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                                            r"\Examples\PythonParts\InteractorExamples\HaunchReinforcementFromFileInteractor.png")

    return (elements, None, None)


def create_interactor(coord_input, pyp_path, _show_pal_close_btn, global_str_table_service, build_ele_list,
                      build_ele_composite, control_props_list, modify_uuid_list):
    """
    Create the interactor

    Args:
        coord_input:               coordinate input
        pyp_path:                  path of the pyp file
        global_str_table_service:  global string table service
        build_ele_list:            building element list
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        modify_uuid_list:          UUIDs of the existing elements in the modification mode
    """

    interactor = HaunchReinforcementFromFileInteractor(coord_input, pyp_path, global_str_table_service, build_ele_list,
                                                       build_ele_composite, control_props_list, modify_uuid_list)

    return interactor


class HaunchReinforcementFromFileInteractor():
    """
    Definition of class HaunchReinforcementFromFileInteractor
    """

    def __init__(self, coord_input, pyp_path, global_str_table_service, build_ele_list, build_ele_composite,
                 control_props_list, modify_uuid_list):
        """
        Create the interactor

        Args:
            coord_input:         coordinate input
            pyp_path:            path of the pyp file
            global_str_table_service:   string table service
            build_ele_list:      building element list
            build_ele_composite: building element composite
            control_props_list:  control properties list
            modify_uuid_list:    UUIDs of the existing elements in the modification mode
        """

        self.coord_input              = coord_input
        self.pyp_path                 = pyp_path
        self.global_str_table_service = global_str_table_service
        self.build_ele_list           = build_ele_list
        self.build_ele_composite      = build_ele_composite
        self.control_props_list       = control_props_list
        self.modify_uuid_list         = modify_uuid_list
        self.palette_service          = None
        self.modification             = False
        self.file_name                = pyp_path + "\\LineData.txt"
        self.close_interactor         = False

        self.haunch_build_ele_script = None
        self.haunch_build_ele_list   = None
        self.haunch_model_ele_list   = []
        self.haunch_placement_mat    = []

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_list[0].script_name,
                                                             self.control_props_list, self.build_ele_list[0].pyp_file_name)

        self.palette_service.show_palette(self.build_ele_list[0].pyp_file_name)

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Modify the properties"))

        self.haunch_data = read_csv(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + \
                                    r"PythonPartsExampleScripts\InteractorExamples\HaunchReinforcementData.csv")

        self.read_haunch_pyp()


    def read_haunch_pyp(self):
        """" read the haunch PythonPart """

        pyp_file = AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + \
                   r"Library\PythonParts\Reinforcement objects\HaunchReinforcement.pyp"

        result, self.haunch_build_ele_script, self.haunch_build_ele_list, _, _, _, _ = \
            BuildingElementService.read_data_from_pyp(pyp_file, self.global_str_table_service.str_table, False,
                                                      self.global_str_table_service.material_str_table)

        if not result:
            AllplanUtil.ShowMessageBox(pyp_file + " was not found", AllplanUtil.MB_OK)

            return

        self.draw_preview()


    def on_cancel_function(self):
        """ cancel the input """

        self.palette_service.close_palette()

        doc = self.coord_input.GetInputViewDocument()

        undo_step = AllplanIFW.UndoRedoService(doc, True)

        for model_ele_list, place_mat in zip(self.haunch_model_ele_list, self.haunch_placement_mat):
            print(place_mat)
            AllplanBaseElements.CreateElements(doc, place_mat, model_ele_list, [], None, createUndoStep = False)

        undo_step.CreateUndoStep()

        return True


    def on_preview_draw(self):
        """ draw the preview """

        self.draw_preview()


    def on_mouse_leave(self):
        """ process the mouse leave """

        self.on_preview_draw()


    def process_mouse_msg(self, _mouse_msg, _pnt, _msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        self.draw_preview()

        return True


    def draw_preview(self):
        """ draw the preview """

        self.haunch_model_ele_list = []
        self.haunch_placement_mat  = []

        doc = self.coord_input.GetInputViewDocument()

        end_index = len(self.haunch_data) - 1

        for index, data in enumerate(self.haunch_data):
            place_mat = AllplanGeo.Matrix3D()

            place_mat.SetTranslation(AllplanGeo.Vector3D(float(data["X_Coord"]), float(data["Y_Coord"]), float(data["Z_Coord"])))

            build_ele = self.haunch_build_ele_list[0].deep_copy()

            parameter = data["Parameter"]

            if parameter:
                BuildingElementConverter.read_from_list(build_ele, parameter.split(";"))

            elements = self.haunch_build_ele_script.create_element(build_ele,
                                                                   self.coord_input.GetInputViewDocument(),)

            self.haunch_model_ele_list.append(elements[0])
            self.haunch_placement_mat.append(place_mat)

            AllplanBaseElements.DrawElementPreview(doc, place_mat,
                                                   elements[0], index == end_index, None)
