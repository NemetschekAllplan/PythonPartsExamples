"""
Script for DrawingLayoutFileInteractor
"""

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_AllplanSettings as AllplanSettings

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from BuildingElementListService import BuildingElementListService


print('Load DrawingLayoutFileInteractor.py')


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

    model_ele_list = [AllplanBasisElements.TextElement(com_prop, text_prop, "Load drawing file", AllplanGeo.Point2D(0, 100)),
                      AllplanBasisElements.TextElement(com_prop, text_prop, "Load layout file", AllplanGeo.Point2D(0, 0))]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return DrawingLayoutFileInteractor(coord_input, pyp_path, str_table_service)


class DrawingLayoutFileInteractor():
    """
    Definition of class DrawingLayoutFileInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class DrawingLayoutFileInteractor

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
        self.drawing_minmax    = AllplanGeo.MinMax3D()


        #----------------- read the data and show the palette

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\DrawingLayoutFileInteractor.pal", self.str_table_service.str_table, False, 
                                                      self.str_table_service.material_str_table)

        if not result:
            return

        self.build_ele_list[0].PrintProfile.value = AllplanSettings.AllplanPaths.GetEtcPath() + "standard.npp"

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
            
        drawing_file_serv = AllplanBaseElements.DrawingFileService()


        #----------------- create elements inside the drawing file

        if event_id == 1001:
            drawing_file_serv.UnloadAll(doc)

            drawing_file_serv.LoadFile(doc, build_ele.DrawingFileNumber.value,
                                       AllplanBaseElements.DrawingFileLoadState.ActiveForeground)

            drawing_file_serv.SetScalingFactor(doc, 20)

            if build_ele.DeleteDrawingDocument.value:
                drawing_file_serv.DeleteDocument(doc)

            ref_pnt = AllplanGeo.Point3D()

            length = build_ele.BoxLength.value
            width  = build_ele.BoxWidth.value
            height = build_ele.BoxHeight.value
            x_dist = build_ele.BoxDistance.value
            y_dist = build_ele.BoxDistance.value

            com_prop = AllplanBaseElements.CommonProperties()

            com_prop.GetGlobalProperties()

            model_ele_list = []

            rot_mat = RotationAngles(0, 0, build_ele.DrawingRotationAngle.value).get_rotation_matrix()

            for i in range(5):
                layer = 3700
                color = 1
                pen   = 1
                pnt1  = ref_pnt

                for j in range(4):
                    com_prop.Layer = layer;
                    com_prop.Color = color;
                    com_prop.Pen   = pen;

                    pnt2 = pnt1 + AllplanGeo.Point3D(length, width, height)

                    polyhed = AllplanGeo.Transform(AllplanGeo.Polyhedron3D.CreateCuboid(pnt1, pnt2), rot_mat)

                    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

                    pnt1 = pnt1 + AllplanGeo.Point3D(0, y_dist, 0)

                    layer += 1
                    color += 1
                    pen   += 1

                ref_pnt = ref_pnt + AllplanGeo.Point3D(x_dist, 0 , 0)

            text_angle     = AllplanGeo.Angle()
            text_angle.Deg = build_ele.DrawingRotationAngle.value

            text_prop = AllplanBasisElements.TextProperties()

            text_prop.Height = y_dist /100
            text_prop.Width  = text_prop.Height
            text_prop.TextAngle = text_angle

            text_pnt = AllplanGeo.Transform(AllplanGeo.Point3D(0, y_dist * 4, 0), rot_mat)

            model_ele_list.append(AllplanBasisElements.TextElement(com_prop, text_prop, "Load drawing file " + str(build_ele.DrawingFileNumber.value),
                                                                   AllplanGeo.Point2D(text_pnt)))

            elements = AllplanBaseElements.CreateElements(doc, AllplanGeo.Matrix3D(), model_ele_list, [], None)

            self.drawing_minmax = AllplanBaseElements.GetMinMaxBox(elements, build_ele.DrawingRotationAngle.value)

            print("#######################################")
            print(self.drawing_minmax)

            return

        if event_id == 1002:
            drawing_file_serv.CreateBendingSchedule(doc,AllplanGeo.Point2D(build_ele.XCoord.value, build_ele.YCoord.value))
            return


        #----------------- add drawing file to the layout file

        if event_id == 2001:
            file_index = build_ele.DrawingFileNumber.value

            drawing_file_serv.UnloadFile(doc, file_index)       # currently necessary to save the data for next step !!!!!!!!!!!!!
            drawing_file_serv.LoadFile(doc, file_index, AllplanBaseElements.DrawingFileLoadState.ActiveForeground)

            layout_file_serv = AllplanBaseElements.LayoutFileService()

            layout_file_serv.LoadFile(doc, build_ele.LayoutFileNumber.value)

            if build_ele.DeleteLayoutDocument.value:
                layout_file_serv.DeleteDocument(doc)


            #----------------- create the page

            layout_size = AllplanBaseElements.LayoutSize()

            layout_size.Width       = build_ele.PageWidth.value
            layout_size.Height      = build_ele.PageHeight.value
            layout_size.UserDefined = 1

            layout_margin = AllplanBaseElements.LayoutMargin()

            layout_margin.Left = 10
            layout_margin.Right = 10
            layout_margin.Top = 10
            layout_margin.Bottom = 10

            layout_legend = AllplanBaseElements.LayoutMasterLegendData()

            layout_legend.PathID     = AllplanBaseElements.PathID.PathDefaultID
            layout_legend.FileID     = 7
            layout_legend.ItemID     = 1
            layout_legend.LegendName = "Legend"

            layout_stamp = AllplanBaseElements.LayoutMasterStampData()

            layout_stamp.PathID    = AllplanBaseElements.PathID.PathDefaultID
            layout_stamp.FileID    = 7
            layout_stamp.ItemID    = 1
            layout_stamp.StampName = "Stamp"

            layout_border = AllplanBaseElements.LayoutBorderDefinition()

            layout_border.Index           = 5
            #layout_border.UserDefined     = 1
            layout_border.Name            = "Heftrand"
            layout_border.OuterLinePen    = 1
            layout_border.OuterLineColor  = 1
            layout_border.OuterlineStroke = 1

            layout_master = AllplanBaseElements.LayoutMasterData()

            layout_master.SheetSize        = layout_size
            layout_master.Margin           = layout_margin
            layout_master.Legend           = layout_legend
            layout_master.Stamp            = layout_stamp
            layout_master.Border           = layout_border
            layout_master.LayoutHeaderType = 2
            layout_master.UseBorder        = 1

            layout_file_serv.CreateMasterLayoutElement(doc, layout_master)


            #----------------- set the clipping

            clip_left_bottom = AllplanGeo.Point2D()
            clip_right_top   = AllplanGeo.Point2D()

            if build_ele.Clipping.value:
                clip_left_bottom.X = build_ele.ClipLeft.value
                clip_left_bottom.Y = build_ele.ClipBottom.value
                clip_right_top.X   = build_ele.ClipRight.value
                clip_right_top.Y   = build_ele.ClipTop.value


                #----------------- adapt the size from the drawing file (for testing)

                if self.drawing_minmax.IsValid():
                    angle = math.radians(build_ele.DrawingRotationAngle.value)

                    diff_hypo = self.drawing_minmax.GetSizeY() * math.sin(math.fabs(angle))

                    clip_left_bottom.X = -diff_hypo * math.cos(angle)
                    clip_left_bottom.Y = -diff_hypo * math.sin(angle)
                    clip_right_top.X   = clip_left_bottom.X + self.drawing_minmax.GetSizeX()
                    clip_right_top.Y   = clip_left_bottom.Y + self.drawing_minmax.GetSizeY()

            layer_list = AllplanUtil.VecIntList()

            if not build_ele.ShowAllLayer.value:
                if build_ele.Layer3700.value:
                    layer_list.append(3700)
                if build_ele.Layer3701.value:
                    layer_list.append(3701)
                if build_ele.Layer3702.value:
                    layer_list.append(3702)
                if build_ele.Layer3703.value:
                    layer_list.append(3703)

            layout_file_serv.InsertDrawingFile(doc, [file_index],
                                               AllplanGeo.Point2D(build_ele.PlacePntX.value, build_ele.PlacePntY.value),
                                               build_ele.RotationAngle.value,
                                               build_ele.Scale.value,
                                               clip_left_bottom, clip_right_top, layer_list,
                                               build_ele.TextFactor.value,
                                               build_ele.UseRefPnt.value,
                                               AllplanGeo.Point2D(build_ele.RefPntX.value, build_ele.RefPntY.value),
                                               self.drawing_minmax)

            layout_file_serv.AssignPrintProfile(doc,build_ele.PrintProfile.value)


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


    def execute_save_favorite(self, file_name):
        """
        Execute the favorite save

        Args:
            file_name: Full name of the favorite file
        """

        BuildingElementListService.write_to_file(file_name, self.build_ele_list)


    def execute_load_favorite(self, file_name):
        """
        Execute the favorite load

        Args:
            file_name: Full name of the favorite file
        """

        BuildingElementListService.read_from_file(file_name, self.build_ele_list)

        self.palette_service.update_palette(-1, True)
