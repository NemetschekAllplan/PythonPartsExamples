"""
Script for ReinfLinkPlacementInteractor
"""
import os

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService


print('Load ReinfLinkPlacementInteractor.py')


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

    del doc

    pyp_path, _ = os.path.split(build_ele.pyp_file_name)

    build_ele_service = BuildingElementService()

    _, _, build_ele_list, _, _, _, _ = \
        build_ele_service.read_data_from_pyp(pyp_path + "\\ReinfULinkPlacementInteractor.pal", None, False)

    model_angles = RotationAngles(0, -90, 0)

    shape_props = ReinforcementShapeProperties.rebar(build_ele_list[0].Diameter.value,
                                                     build_ele_list[0].BendingRoller.value,
                                                     build_ele_list[0].SteelGrade.value,
                                                     build_ele_list[0].ConcreteGrade.value,
                                                     AllplanReinf.BendingShapeType.OpenStirrup)

    shape = GeneralShapeBuilder. \
        create_u_link(build_ele_list[0].Thickness.value,
                      build_ele_list[0].SideLength.value,
                      model_angles,
                      shape_props,
                      ConcreteCoverProperties.all(build_ele_list[0].ConcreteCoverShape.value), -1)

    placement = LinearBarBuilder. \
        create_linear_bar_placement_from_to_by_dist(1, shape,
                                                    AllplanGeo.Point3D(),
                                                    AllplanGeo.Point3D(1000,0,0),
                                                    build_ele_list[0].ConcreteCoverPlacement.value,
                                                    build_ele_list[0].ConcreteCoverPlacement.value,
                                                    build_ele_list[0].Distance.value,
                                                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance)

    model_ele_list = [placement]

    return (model_ele_list, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return ReinfLinkPlacementInteractor(coord_input, pyp_path, str_table_service)


class ReinfLinkPlacementInteractor():
    """
    Definition of class ReinfLinkPlacementInteractor
    """

    def __init__(self,  coord_input, pyp_path, str_table_service):
        """
        Initialization of class ReinfLinkPlacementInteractor

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
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\ReinfULinkPlacementInteractor.pal",
                                                      self.str_table_service.str_table, False, 
                                                      self.str_table_service.material_str_table)

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))


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


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        if not self.first_point_input:
            self.first_point_input = True

            self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

            return False

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
                                           AllplanGeo.Matrix3D(), self.model_ele_list, [], None)

        self.first_point = input_pnt

        self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("From point"))

        return True


    def draw_preview(self, input_pnt):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """

        line = AllplanGeo.Line2D(AllplanGeo.Point2D(self.first_point),AllplanGeo.Point2D(input_pnt))

        rot_angle = AllplanGeo.CalcAngle(line.GetStartPoint(),line.GetEndPoint())

        model_angles = RotationAngles(0, -90, rot_angle.Deg)

        shape_props = ReinforcementShapeProperties.rebar(self.build_ele_list[0].Diameter.value,
                                                         self.build_ele_list[0].BendingRoller.value,
                                                         self.build_ele_list[0].SteelGrade.value,
                                                         self.build_ele_list[0].ConcreteGrade.value,
                                                         AllplanReinf.BendingShapeType.OpenStirrup)

        shape = GeneralShapeBuilder. \
            create_u_link(self.build_ele_list[0].Thickness.value,
                          self.build_ele_list[0].SideLength.value,
                          model_angles,
                          shape_props,
                          ConcreteCoverProperties.all(self.build_ele_list[0].ConcreteCoverShape.value), -1)

        placement = LinearBarBuilder. \
            create_linear_bar_placement_from_to_by_dist(1, shape,
                                                        self.first_point,
                                                        input_pnt,
                                                        self.build_ele_list[0].ConcreteCoverPlacement.value,
                                                        self.build_ele_list[0].ConcreteCoverPlacement.value,
                                                        self.build_ele_list[0].Distance.value,
                                                        LinearBarBuilder.StartEndPlacementRule.AdaptDistance)

        self.model_ele_list = [placement]

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, False, None)
