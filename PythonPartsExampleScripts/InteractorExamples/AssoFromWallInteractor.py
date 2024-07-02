"""
Script for AssoFromWallInteractor
"""

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from TraceService import TraceService


print('Load AssoFromWallInteractor.py')


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

    line1 = AllplanGeo.Line2D(AllplanGeo.Point2D(),AllplanGeo.Point2D(1000,1000))
    line2 = AllplanGeo.Line2D(AllplanGeo.Point2D(1000,500),AllplanGeo.Point2D(2000,200))

    model_ele_list = [AllplanBasisElements.ModelElement2D(com_prop, line1),
                      AllplanBasisElements.ModelElement2D(com_prop, line2)]

    return (model_ele_list, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return AssoFromWallInteractor(coord_input, pyp_path, str_table_service)


class AssoFromWallInteractor():
    """
    Definition of class AssoFromWallInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class AssoFromWallInteractor

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
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\AssoFromWallInteractor.pal", self.str_table_service.str_table, False,
                                                      self.str_table_service.material_str_table)

        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select element"))

        type_query = AllplanIFW.QueryTypeID(AllplanElementAdapter.WallTier_TypeUUID)

        sel_query = AllplanIFW.SelectionQuery(type_query)

        self.element_filter = AllplanIFW.ElementSelectFilterSetting(sel_query, True)


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True


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

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        geo_ele = self.coord_input.GetSelectedGeometryElement()

        if not geo_ele:
            return True

        geo_type = str(geo_ele)
        geo_type = geo_type[0 : geo_type.find("(")]

        self.build_ele_list[0].ElementType.value = geo_type
        self.build_ele_list[0].Element.value     = geo_ele

        self.palette_service.update_palette(1, True)


        #----------------- get the view direction

        input_pnt = self.coord_input.GetViewWorldProjection().ViewToWorldBaseZ0(pnt)

        if isinstance(geo_ele, AllplanGeo.Polygon2D):
            geo_ele   = AllplanGeo.Polyline2D(geo_ele)

        local_pnt = AllplanGeo.TransformCoord.PointLocal(geo_ele, input_pnt)

        dir_pnt = AllplanGeo.TransformCoord.PointGlobal(geo_ele, local_pnt.X)

        dir_vec = AllplanGeo.Vector2D(AllplanGeo.Point2D(input_pnt), AllplanGeo.Point2D(dir_pnt))

        view_matrix = AllplanGeo.Matrix3D()

        view_matrix.SetRotation(AllplanGeo.Line3D(AllplanGeo.Point3D(), AllplanGeo.Point3D(0, 0, 1000)),
                                AllplanGeo.Angle(math.radians(90) - dir_vec.GetAngle().Rad))
        view_matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(), AllplanGeo.Point3D(1000, 0, 0)), AllplanGeo.Angle(math.radians(-90)))


        #----------------- create the view

        doc = self.coord_input.GetInputViewDocument()

        elements = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(self.coord_input.GetSelectedElement())

        minmax = AllplanBaseElements.GetMinMaxBox(elements)

        asso_view_props = AllplanBasisElements.AssociativeViewProperties(doc)

        asso_ele = AllplanBasisElements.AssociativeViewElement()

        asso_ele.PlacementPoint = minmax.Max
        asso_ele.ViewProperties = asso_view_props
        asso_ele.ViewMatrix     = view_matrix

        asso_ele_list = [asso_ele]

        AllplanBaseElements.CreateAssociativeViews(doc, AllplanGeo.Matrix3D(), elements, asso_ele_list,
                                                    self.coord_input.GetViewWorldProjection())

        return True
