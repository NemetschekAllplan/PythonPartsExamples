"""
Script for Line2DInteractor
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from BuildingElementListService import BuildingElementListService
from StringTableService import StringTableService
from TraceService import TraceService


print('Load Line2DInteractor.py')


def check_allplan_version(build_ele: BuildingElement,
                          version:   float):
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


def create_preview(build_ele: BuildingElement,
                   doc:       AllplanElementAdapter.DocumentAdapter):
    """
    Creation of the library preview

    Args:
        build_ele: the building element.
        doc:       input document
    """

    del build_ele
    del doc

    com_prop = AllplanBaseElements.CommonProperties()

    com_prop.GetGlobalProperties()

    line1 = AllplanGeo.Line2D(AllplanGeo.Point2D(),AllplanGeo.Point2D(1000,1000))
    line2 = AllplanGeo.Line2D(AllplanGeo.Point2D(1000,500),AllplanGeo.Point2D(2000,200))

    model_ele_list = [AllplanBasisElements.ModelElement2D(com_prop, line1),
                      AllplanBasisElements.ModelElement2D(com_prop, line2)]

    return (model_ele_list, None, None)


def create_interactor(coord_input:              AllplanIFW.CoordinateInput,
                      pyp_path:                 str,
                      global_str_table_service: StringTableService):
    """
    Create the interactor

    Args:
        coord_input:               coordinate input
        pyp_path:                  path of the pyp file
        global_str_table_service:  global string table service

    Returns:
        Created interactor object
    """

    return Line2DInteractor(coord_input, pyp_path, global_str_table_service)


class Line2DInteractor():
    """
    Definition of class Line2DInteractor
    """

    def __init__(self,
                 coord_input:              AllplanIFW.CoordinateInput,
                 pyp_path:                 str,
                 global_str_table_service: StringTableService):
        """
        Initialization of class Line2DInteractor

        Args:
            coord_input:               coordinate input
            pyp_path:                  path of the pyp file
            global_str_table_service:  global string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.first_point_input = True
        self.first_point       = AllplanGeo.Point3D()
        self.model_ele_list    = None
        self.build_ele_service = BuildingElementService()


        #----------------- read the data and show the palette

        TraceService.trace_1(pyp_path + "\\Line2DInteractor.pal")

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\Line2DInteractor.pal", global_str_table_service.str_table, False,
                                                      global_str_table_service.material_str_table)

        if not result:
            return

        BuildingElementListService.read_from_default_favorite_file(self.build_ele_list)

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)



        #----------------- get the properties and start the input

        self.com_prop = AllplanBaseElements.CommonProperties()

        self.set_common_properties()

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))


    def set_common_properties(self):
        """
        Set the common properties
        """

        self.com_prop.Color         = self.build_ele_list[0].Color.value
        self.com_prop.Pen           = self.build_ele_list[0].Pen.value
        self.com_prop.Stroke        = self.build_ele_list[0].Stroke.value
        self.com_prop.ColorByLayer  = self.build_ele_list[0].ColorByLayer.value
        self.com_prop.PenByLayer    = self.build_ele_list[0].PenByLayer.value
        self.com_prop.StrokeByLayer = self.build_ele_list[0].StrokeByLayer.value
        self.com_prop.Layer         = self.build_ele_list[0].Layer.value


    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        update_palette = self.palette_service.modify_element_property(page, name, value)

        if update_palette:
            self.palette_service.update_palette(-1, False)

        self.set_common_properties()


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

        if self.first_point_input:
            return

        input_pnt = self.coord_input.GetCurrentPoint(self.first_point).GetPoint()

        self.draw_preview(input_pnt)


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """
        self.on_preview_draw()


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


        #----------------- Create the line and continue with from point input

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           self.model_ele_list, [], None)

        self.first_point_input = True

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

        return True


    def draw_preview(self, input_pnt):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """

        line = AllplanGeo.Line2D(AllplanGeo.Point2D(self.first_point),AllplanGeo.Point2D(input_pnt))

        self.model_ele_list = [AllplanBasisElements.ModelElement2D(self.com_prop, line)]

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, False, None)


    def reset_param_values(self, _build_ele_list):
        """ reset the parameter values """

        BuildingElementListService.reset_param_values(self.build_ele_list)

        self.palette_service.update_palette(-1, True)


    def execute_save_favorite(self, file_name):
        """ save the favorite data """

        BuildingElementListService.write_to_file(file_name, self.build_ele_list)


    def execute_load_favorite(self, file_name):
        """ load the favorite data """

        BuildingElementListService.read_from_file(file_name, self.build_ele_list)

        self.palette_service.update_palette(-1, True)


    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
