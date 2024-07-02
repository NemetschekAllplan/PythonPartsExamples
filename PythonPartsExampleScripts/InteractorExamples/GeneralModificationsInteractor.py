"""
Script for GeneralModificationsInteractor
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService


print('Load GeneralModificationsInteractor.py')


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

    model_ele_list = [AllplanBasisElements.TextElement(com_prop, text_prop, "Rotate elements", AllplanGeo.Point2D(0, 200)),
                      AllplanBasisElements.TextElement(com_prop, text_prop, "Scale elements", AllplanGeo.Point2D(0, 0))]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return GeneralModificationsInteractor(coord_input, pyp_path, str_table_service)


class GeneralModificationsInteractor():
    """
    Definition of class GeneralModificationsInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class GeneralModificationsInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service
        self.model_ele_list    = None
        self.build_ele_service = BuildingElementService()


        #----------------- read the data and show the palette

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\GeneralModificationsInteractor.pal", self.str_table_service.str_table, False, 
                                                      self.str_table_service.material_str_table)

        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)


        #----------------- create the elements

        doc = self.coord_input.GetInputViewDocument()

        ref_pnt = AllplanGeo.Point3D()

        length = 1000
        width  = 1000
        height = 1000
        x_dist = 2000
        y_dist = 2000

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        model_ele_list = []

        for i in range(5):
            color = 1
            pen   = 1
            pnt1  = ref_pnt

            for j in range(4):
                com_prop.Color = color;
                com_prop.Pen   = pen;

                pnt2 = pnt1 + AllplanGeo.Point3D(length, width, height)

                polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(pnt1, pnt2)

                model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

                pnt1 = pnt1 + AllplanGeo.Point3D(0, y_dist, 0)

                color += 1
                pen   += 1

            ref_pnt = ref_pnt + AllplanGeo.Point3D(x_dist, 0 , 0)

        self.elements = AllplanBaseElements.CreateElements(doc, AllplanGeo.Matrix3D(), model_ele_list, [], None)


        #----------------- get the properties and start the input

        self.com_prop = AllplanBaseElements.CommonProperties()

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Execute by button click"))


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

        doc       = self.coord_input.GetInputViewDocument()
        view_proj = self.coord_input.GetViewWorldProjection()

        if event_id == 1001:
            AllplanBaseElements.RotateElements(doc,self.elements,
                                               AllplanGeo.Point2D(build_ele.RefPntX.value, build_ele.RefPntY.value),
                                               build_ele.RotationAngle.value, view_proj)
            return

        if event_id == 1002:
            AllplanBaseElements.ScaleElements(doc,self.elements,
                                              AllplanGeo.Point3D(build_ele.RefPntX.value, build_ele.RefPntY.value, build_ele.RefPntZ.value),
                                              build_ele.ScaleX.value, build_ele.ScaleY.value, build_ele.ScaleZ.value,
                                              AllplanGeo.Angle(), view_proj)

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
