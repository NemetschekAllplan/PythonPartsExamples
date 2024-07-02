"""
Script for ExportImportInteractor
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService


print('Load ExportImportInteractor.py')


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

    model_ele_list = [AllplanBasisElements.TextElement(com_prop, text_prop, "Export/import", AllplanGeo.Point2D(0, 100)),
                      AllplanBasisElements.TextElement(com_prop, text_prop, "DWG, PDF", AllplanGeo.Point2D(0, 0))]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return ExportImportInteractor(coord_input, pyp_path, str_table_service)


class ExportImportInteractor():
    """
    Definition of class ExportImportInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class ExportImportInteractor

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
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\ExportImportInteractor.pal", self.str_table_service.str_table, False,
                                                      self.str_table_service.material_str_table)

        self.build_ele_list[0].DwgExportConfigFileName.value = AllplanSettings.AllplanPaths.GetUsrPath() + "\\nx_AllFT_AutoCad.cfg"
        self.build_ele_list[0].DwgImportConfigFileName.value = AllplanSettings.AllplanPaths.GetUsrPath() + "\\nx_AutoCad_AllFT.cfg"

        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)



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

        doc = self.coord_input.GetInputViewDocument()


        #----------------- import for the drawing file

        if event_id < 2000:
            file_index = build_ele.DrawingFileNumber.value

            drawing_file_serv = AllplanBaseElements.DrawingFileService()

            drawing_file_serv.UnloadAll(doc)
            drawing_file_serv.LoadFile(doc, file_index, AllplanBaseElements.DrawingFileLoadState.ActiveForeground)

            if event_id == 1001:
                drawing_file_serv.ExportDWG(doc, build_ele.DwgDrawingFileName.value, build_ele.DwgExportConfigFileName.value, 0)

            elif event_id == 1002:
                elements = drawing_file_serv.ImportDWG(doc, build_ele.DwgDrawingFileName.value, build_ele.DwgImportConfigFileName.value,
                                                       AllplanGeo.Point3D(build_ele.DrawingXOffset.value,build_ele.DrawingYOffset.value,
                                                                          build_ele.DrawingZOffset.value))

                if build_ele.DrawingZAngle.value:
                    AllplanBaseElements.RotateElements(doc, elements,
                                                       AllplanGeo.Point2D(build_ele.DrawingXRotation.value,
                                                                          build_ele.DrawingYRotation.value),
                                                       build_ele.DrawingZAngle.value,
                                                       self.coord_input.GetViewWorldProjection())

            elif event_id == 1004:
                drawing_file_serv.ExportBendingMachine(doc, build_ele.BvbsDrawingFileName.value, build_ele.BvbsProject.value,
                                                       build_ele.BvbsPlan.value, build_ele.BvbsIndex.value, build_ele.BvbsSplitGroups.value)


        #----------------- export/import for the layout file

        if event_id > 2000:
            file_index = build_ele.LayoutFileNumber.value

            layout_file_serv = AllplanBaseElements.LayoutFileService()

            layout_file_serv.LoadFile(doc, file_index)

            if event_id == 2001:
                layout_file_serv.ExportDWG(doc, file_index, build_ele.DwgLayoutFileName.value, build_ele.DwgExportConfigFileName.value, 0)

            elif event_id == 2002:
                layout_file_serv.ImportDWG(doc, build_ele.DwgLayoutFileName.value, build_ele.DwgImportConfigFileName.value,
                                           AllplanGeo.Point2D(build_ele.LayoutXOffset.value,build_ele.LayoutYOffset.value))

            elif event_id == 2003:
                layout_file_serv.ExportPDF(doc, file_index, build_ele.PdfLayoutFileName.value, build_ele.PdfFavLayoutFileName.value)

            layout_file_serv.LoadFile(doc, file_index)


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
