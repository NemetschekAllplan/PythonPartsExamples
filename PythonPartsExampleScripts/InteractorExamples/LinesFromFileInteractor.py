"""
Script for LinesFromFileInteractor
"""

from typing import List

import traceback

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW

from PythonPart import View2D3D, PythonPart
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementPaletteService import BuildingElementPaletteService
from StringTableService import StringTableService
from ControlProperties import ControlProperties

print('Load LinesFromFileInteractor.py')


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

    line1 = AllplanGeo.Line2D(AllplanGeo.Point2D(),AllplanGeo.Point2D(0,1000))
    line2 = AllplanGeo.Line2D(AllplanGeo.Point2D(300, 0),AllplanGeo.Point2D(300,500))
    line3 = AllplanGeo.Line2D(AllplanGeo.Point2D(0,-300),AllplanGeo.Point2D(1000,-300))
    line4 = AllplanGeo.Line2D(AllplanGeo.Point2D(0,-500),AllplanGeo.Point2D(2000,-500))

    model_ele_list = [AllplanBasisElements.ModelElement2D(com_prop, line1),
                      AllplanBasisElements.ModelElement2D(com_prop, line2),
                      AllplanBasisElements.ModelElement2D(com_prop, line3),
                      AllplanBasisElements.ModelElement2D(com_prop, line4)]

    return (model_ele_list, None, None)


def create_interactor(coord_input:               AllplanIFW.CoordinateInput,
                      pyp_path:                  str,
                      _global_str_table_service: StringTableService,
                      build_ele_list:            List[BuildingElement],
                      build_ele_composite:       BuildingElementComposite,
                      control_props_list:        List[ControlProperties],
                      modify_uuid_list:          list):
    """
    Create the interactor

    Args:
        coord_input:               coordinate input
        pyp_path:                  path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            building element list
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        modify_uuid_list:          UUIDs of the existing elements in the modification mode

      Returns:
          Created interactor object
      """

    interactor = LinesFromFileInteractor(coord_input, pyp_path, build_ele_list, build_ele_composite,
                                         control_props_list, modify_uuid_list)

    try:
        if not build_ele_list[0].FileName.value:
            interactor.create_lines()
        else:
            interactor.modify_line()

    except:
        traceback.print_exc()

    return interactor


class LinesFromFileInteractor():
    """
    Definition of class LinesFromFileInteractor
    """

    def __init__(self,
                 coord_input:           AllplanIFW.CoordinateInput,
                 pyp_path:              str,
                 build_ele_list:        List[BuildingElement],
                 build_ele_composite:   BuildingElementComposite,
                 control_props_list:    List[ControlProperties],
                 modify_uuid_list:      list):
        """
        Create the interactor

        Args:
            coord_input:               coordinate input
            pyp_path:                  path of the pyp file
            build_ele_list:            building element list
            build_ele_composite:       building element composite
            control_props_list:        control properties list
            modify_uuid_list:          UUIDs of the existing elements in the modification mode
        """

        self.coord_input         = coord_input
        self.pyp_path            = pyp_path
        self.build_ele_list      = build_ele_list
        self.build_ele_composite = build_ele_composite
        self.control_props_list  = control_props_list
        self.modify_uuid_list    = modify_uuid_list
        self.palette_service     = None
        self.model_ele_list      = []
        self.modification        = False
        self.file_name           = pyp_path + "\\LineData.txt"
        self.close_interactor    = False

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_list[0].script_name,
                                                             self.control_props_list, self.build_ele_list[0].pyp_file_name)

        self.palette_service.show_palette(self.build_ele_list[0].pyp_file_name)

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Modify the properties"))

        self.set_common_properties()
        self.read_lines()


    def read_lines(self):
        self.line_data = {}

        with open(self.file_name, 'r', encoding = "utf-8") as line_file:
            for line in line_file:
                data_list = line.split(",")

                self.line_data[data_list[0]] = data_list[1:]


    def set_common_properties(self):
        """
        Set the common properties
        """

        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()

        if self.build_ele_list[0].VersionNumber.value == 0:
            return

        self.com_prop.Color  = self.build_ele_list[0].Color.value
        self.com_prop.Pen    = self.build_ele_list[0].Pen.value
        self.com_prop.Stroke = self.build_ele_list[0].Stroke.value


    def create_lines(self):
        build_ele = self.build_ele_list[0]

        build_ele.Color.value  = self.com_prop.Color
        build_ele.Pen.value    = self.com_prop.Pen
        build_ele.Stroke.value = self.com_prop.Stroke

        filter = "Vertical" if build_ele.ElementFilter.value == 0 else "Horizontal"

        for key, value in self.line_data.items():
            if filter == value[0].strip():
                build_ele.FileName.value      = self.file_name
                build_ele.LineName.value      = key
                build_ele.VersionNumber.value = 1

                self.create_model_line(value, build_ele)

        self.on_preview_draw()


    def modify_line(self):
        self.modification = True

        build_ele = self.build_ele_list[0]

        if not build_ele.LineName.value in self.line_data:
            return

        build_ele.VersionNumber.value += 1                  # one property must be modified to create a new PythonPart in Allplan

        self.create_model_line(self.line_data[build_ele.LineName.value], build_ele)

        self.on_preview_draw()


    def create_model_line(self, line_data, build_ele):
        line = AllplanGeo.Line2D(AllplanGeo.Point2D(float(line_data[1]), float(line_data[2])),
                                 AllplanGeo.Point2D(float(line_data[3]), float(line_data[4])))

        views = [View2D3D ([AllplanBasisElements.ModelElement2D(self.com_prop, line)])]

        pythonpart = PythonPart("LineFromFile",
                                parameter_list = build_ele.get_params_list(),
                                hash_value = build_ele.get_hash(),
                                python_file = build_ele.pyp_file_name,
                                views = views)

        self.model_ele_list += pythonpart.create()


    def on_cancel_function(self):
        if self.palette_service:
            self.palette_service.close_palette()

        self.palette_service = None

        self.close_interactor = True


        #----------------- get the original line back

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           [], self.modify_uuid_list, None)

        return False


    def on_preview_draw(self):
        if self.build_ele_list[0].VersionNumber.value == 0:
            return

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, True, None)


    def on_control_event(self, event_id):
        """
        On control event

        Args:
            event_id: event id of control.
        """

        if event_id != 1001:
            return

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           self.model_ele_list, self.modify_uuid_list, None)

        self.close_interactor = True


    def modify_element_property(self, page, name, value):
        self.palette_service.modify_element_property(page, name, value)

        build_ele = self.build_ele_list[0]

        self.model_ele_list = []

        if not self.modification:
            self.create_lines()
        else:
            self.set_common_properties()

            self.create_model_line(self.line_data[build_ele.LineName.value], build_ele)

        self.on_preview_draw()


    def on_mouse_leave(self):
        self.on_preview_draw()

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

        if self.close_interactor:
            if self.palette_service:
                self.palette_service.close_palette()

            self.palette_service = None

            return False

        self.on_preview_draw()

        return True
