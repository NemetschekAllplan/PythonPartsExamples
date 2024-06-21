"""
Script for FillingInteractor
"""
import os

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW

import BasisExamples.Filling as FillingExample

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService

print('Load FillingInteractor.py')


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

    pyp_path, _ = os.path.split(build_ele.pyp_file_name)

    build_ele_service = BuildingElementService()

    result, _, build_ele_list, _, _, _, _ = \
        build_ele_service.read_data_from_pyp(pyp_path + "\\Fillinginteractor.pal", None, False, None)

    if not result:
        return

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    geo = AllplanGeo.Polygon2D()
    geo += AllplanGeo.Point2D(0, 0)
    geo += AllplanGeo.Point2D(1000, 0)
    geo += AllplanGeo.Point2D(500, 1000)
    geo += AllplanGeo.Point2D(0, 0)

    props = FillingExample.FillingExample(doc).create_properties(build_ele_list[0])

    model_ele_list = [AllplanBasisElements.FillingElement(com_prop, props, geo)]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return FillingInteractor(coord_input, pyp_path, str_table_service)


class FillingInteractor():
    """
    Definition of class FillingInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class FillingInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service
        self.first_point_input = True
        self.first_point       = AllplanGeo.Point3D()
        self.model_ele_list    = None
        self.build_ele_service = BuildingElementService()


        #----------------- read the data and show the palette

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\Fillinginteractor.pal", self.str_table_service.str_table,False,
                                                      self.str_table_service.material_str_table)

        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)


        self.valid_input    = False
        self.points         = []
        self.current_point  = AllplanGeo.Point3D()
        self.model_ele_list = []

        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()

        self.props = AllplanBasisElements.FillingProperties()

        self.__start_input__()


    def __start_input__(self):
        """
        Start a new polygon input
        """
        self.first_point_input = True
        self.valid_input = False
        self.points = []
        self.current_point = AllplanGeo.Point3D()
        self.model_ele_list = []
        self.__set_properties__()
        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("First point"))

    def __set_properties__(self):
        """
        Set element properties
        """
        self.com_prop.GetGlobalProperties()
        self.props = FillingExample.FillingExample(self.coord_input.GetInputViewDocument()).create_properties(self.build_ele_list[0])

    def __create_model_element__(self, point_list):
        """
        Create model element (depending to available point count)

        Args:
            point_list:      Points for polygon
        """
        if len(point_list) <= 1: # nothing could be created
            self.model_ele_list = []
            return

        if len(point_list) == 2: # only line2D could be created
            geo = AllplanGeo.Line2D(AllplanGeo.Point2D(point_list[0]), AllplanGeo.Point2D(point_list[1]))
            self.model_ele_list = [AllplanBasisElements.ModelElement2D(self.com_prop, geo)]

        if len(point_list) >= 3: # polygon / filling could be created
            geo = AllplanGeo.Polygon2D()
            for point in point_list:
                geo += AllplanGeo.Point2D(point) # convert to 2D
            geo += AllplanGeo.Point2D(point_list[0])

            if len(point_list) >= 4:
                geo.Normalize(AllplanGeo.ePolygonNormalizeType.HATCHING_NORM_TYPE, True)

            self.model_ele_list = [AllplanBasisElements.FillingElement(self.com_prop, self.props, geo)]

    def __get_point_list__(self, input_point):
        """
        Create a temp point list of already used points + current input point

        Args:
            input_point:      Current input point
        """
        point_list = []
        for point in self.points:
            point_list.append(point)
        point_list.append(input_point)
        return point_list


    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        update_palette = self.palette_service.modify_element_property(page, name, value)

        if (name == "FirstColorRed") or (name == "FirstColorBlue") or (name == "FirstColorGreen"):
            used_color = AllplanBasisElements.ARGB (self.build_ele_list[0].FirstColorRed.value,
                                                           self.build_ele_list[0].FirstColorGreen.value,
                                                           self.build_ele_list[0].FirstColorBlue.value,
                                                           self.build_ele_list[0].SecondColorAlpha.value)

            self.build_ele_list[0].AllplanColor.value = AllplanBaseElements.GetIdByColor(used_color)
            update_palette = True

        if update_palette:
            self.palette_service.update_palette(-1, False)

        self.__set_properties__()


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """
        if self.valid_input:
            self.create_element()
            self.__start_input__()
            return False

        self.palette_service.close_palette()

        return True


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """
        if self.first_point_input:
            return

        input_pnt = self.coord_input.GetCurrentPoint(self.current_point).GetPoint()
        self.draw_preview(self.__get_point_list__(input_pnt))


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
        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info, self.current_point,
                                                   not self.first_point_input).GetPoint()

        self.draw_preview(self.__get_point_list__(input_pnt))

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        #----------------- New point for polygon
        self.current_point = input_pnt
        self.points.append(input_pnt)

        #----------------- Enough points for polygon / filling ?
        if len(self.points) > 2:
            self.valid_input = True

        #----------------- Change to "Next point" input
        if self.first_point_input:
            self.first_point_input = False

        self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("Next point"))

        return True

    def create_element(self):
        """
        Create the element

        Args:
            point_list:  Point list
        """
        self.__create_model_element__(self.points)
        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           self.model_ele_list, [], None)


    def draw_preview(self, point_list):
        """
        Draw the preview

        Args:
            point_list:  Point list
        """
        self.__create_model_element__(point_list)
        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, True, None)

