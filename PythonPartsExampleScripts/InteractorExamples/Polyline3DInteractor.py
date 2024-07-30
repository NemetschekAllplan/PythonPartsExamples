"""
Script for Line3DInteractor
"""
import math
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import GeometryValidate as GeometryValidate

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService


print('Load Polyline3DInteractor.py')


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

    poly = AllplanGeo.Polyline3D()
    poly += AllplanGeo.Point3D(0,0,0)
    poly += AllplanGeo.Point3D(0,0,1000)
    poly += AllplanGeo.Point3D(500,0,1000)
    poly += AllplanGeo.Point3D(500,500,2000)

    model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, poly)]
    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return Line3DInteractor(coord_input, pyp_path, str_table_service)


class Line3DInteractor():
    """
    Definition of class Line3DInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class Line3DInteractor

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

        ####
        self.current_point     = AllplanGeo.Point3D()
        self.valid_input       = False
        self.b_use_input_pnt   = True
        self.polyline_lenght   = 0.0
        self.frist_run_transf  = True
        self.cont_polyline     = AllplanGeo.Polyline3D()


        #----------------- read the data and show the palette
        print(pyp_path + "\\Line3DInteractor.pal")

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\Polyline3DInteractor.pal", self.str_table_service.str_table, False, 
                                                      self.str_table_service.material_str_table)

        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)

        self.points         = []


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
        if self.valid_input:
            self.create_element()
            self.palette_service.close_palette()
            return True

        self.palette_service.close_palette()
        return True


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """
        if self.first_point_input:
            return

        input_pnt = self.coord_input.GetCurrentPoint(self.first_point).GetPoint()
        self.draw_preview(input_pnt, False)

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
        self.draw_preview(input_pnt, True)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        #----------------- New point for polygon
        self.current_point = input_pnt
        self.points.append(input_pnt)
        if len(self.points) > 1:
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
        dmmy_pnt = AllplanGeo.Point3D()
        self.b_use_input_pnt = False
        self.__create_model_element__(dmmy_pnt)
        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           self.model_ele_list, [], None)

        self.polyline_lenght = 0.0 #reset value


    def draw_preview(self, input_pnt, b_use_input_pnt):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """
        if len(self.points) < 1:
            return

        if b_use_input_pnt == True:
            self.b_use_input_pnt = True
        else:
            self.b_use_input_pnt = False

        self.__create_model_element__(input_pnt)
        if not self.model_ele_list:
            return

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, False, None)


    def __create_model_element__(self, input_pnt):
         """
         Creates the element
         Args:
            input_pnt:   input point

         Returns:
            Elementlist
         """
         if len(self.points) < 1:
            return

         if self.b_use_input_pnt ==False:
             #calc only without mouse movement, this means for create
             self.polyline_lenght = 0.0
             for index in range(1, len(self.points)):
                line_tmp = AllplanGeo.Line3D(self.points[index-1],self.points[index])
                self.polyline_lenght += AllplanGeo.CalcLength(line_tmp)

         if len(self.points) == 1:
            if self.b_use_input_pnt == False:
                self.model_ele_list = []
                return

            line = AllplanGeo.Line3D(self.points[0],input_pnt)
            self.model_ele_list = [AllplanBasisElements.ModelElement3D(self.com_prop, line)]
            return

         if len(self.points) >= 2: # polyline could be created
            polygon = AllplanGeo.Polyline3D()
            for point in self.points:
                polygon += point

            if self.b_use_input_pnt == True:
                polygon += input_pnt

         if self.frist_run_transf == True:
             #prepare polygon for polyhedron swept
             lenght = 1000
             width = 500
             base_pnt = AllplanGeo.Point3D()
             base_pnt.X -= lenght/2
             base_pnt.Y -= width/2

             polyline3D_contur = AllplanGeo.Polyline3D()
             polyline3D_contur += base_pnt
             polyline3D_contur += AllplanGeo.Point3D(base_pnt.X + lenght,
                                            base_pnt.Y,
                                            base_pnt.Z)
             polyline3D_contur += AllplanGeo.Point3D(base_pnt.X + lenght,
                                            base_pnt.Y + width,
                                            base_pnt.Z)
             polyline3D_contur += AllplanGeo.Point3D(base_pnt.X,
                                            base_pnt.Y + width,
                                            base_pnt.Z)
             polyline3D_contur += base_pnt

             self.frist_run_transf = False
             self.cont_polyline = self.__transform_base_polygon__(polygon, polyline3D_contur)

         if not self.cont_polyline.IsValid():
            return

         print("path polygon = ", ' ' , polygon)
         objlist = AllplanGeo.Polyline3DList()
         objlist.append(self.cont_polyline)

         vector = AllplanGeo.Vector3D()
         err, polyhedron = AllplanGeo.CreateSweptPolyhedron3D(objlist, polygon, True, True, vector)

         if not GeometryValidate.polyhedron(err):
            elems = []
            elems.append(AllplanBasisElements.ModelElement3D(self.com_prop, polygon))
            elems[-1].SetAttributes(self.create_attribute_list(self.polyline_lenght))
            self.model_ele_list = elems
            return

         elems = []
         elems.append(AllplanBasisElements.ModelElement3D(self.com_prop, polyhedron))
         elems[-1].SetAttributes(self.create_attribute_list(self.polyline_lenght))
         self.model_ele_list = elems
         return

    def __transform_base_polygon__(self, path, polyline3D_contur):
        """
        Transforms the base polygon3D

        Args:
            path:               only the first segment is needed
            polyline3D_contur:  will be transformed to placed perpendicular on the first segment of the path

        Returns:
            transformed polyline3D_contur

        """
        pnt1 = path.GetPoint(0)
        pnt2 = path.GetPoint(1)

        diff_x = pnt2.X - pnt1.X
        diff_y = pnt2.Y - pnt1.Y
        diff_z = pnt2.Z - pnt1.Z

        tmp_plane = AllplanGeo.Plane3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Vector3D(diff_x, diff_y, diff_z))

        matrix = AllplanGeo.Matrix3D()
        matrix = tmp_plane.GetTransformationMatrix()
        result = AllplanGeo.Transform(polyline3D_contur, matrix)
        matrix2 = AllplanGeo.Matrix3D()
        matrix2.SetTranslation(AllplanGeo.Vector3D(pnt1.X, pnt1.Y, pnt1.Z))
        result = AllplanGeo.Transform(result, matrix2)
        return result

    def create_attribute_list(self, value):
        """
        Create an attribute set

        Args:
            value:  double value for attribute 1832 Allfa Zahl03

        Returns:
            AllplanBaseElements.Attributes object filled with attributes
        """
        #------------------ Define attributes for elements
        attr_list = []
        attr_list.append(AllplanBaseElements.AttributeDouble(1832, value))#Allfa Zahl03

        attr_set_list = []
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))

        attributes = AllplanBaseElements.Attributes(attr_set_list)
        return attributes
