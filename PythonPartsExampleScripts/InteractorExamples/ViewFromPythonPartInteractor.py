"""
Script for ViewFromPythonPartInteractor
"""

import math
from enum import Enum

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtility
import NemAll_Python_Reinforcement as AllplanReinf

from BuildingElementService import BuildingElementService
from BuildingElementListService import BuildingElementListService
from TraceService import TraceService
from StdReinfShapeBuilder.RotationAngles import RotationAngles

print('Load ViewFromPythonPartInteractor.py')

class InputState(Enum):
    SELECT         = 1
    CREATE_VIEW    = 2
    CREATE_SECTION = 3


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

    return (None, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return ViewFromPythonPartInteractor(coord_input, pyp_path, str_table_service)


class ViewFromPythonPartInteractor():
    """
    Definition of class ViewFromPythonPartInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class ViewFromPythonPartInteractor

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
        self.input_state       = InputState.SELECT
        self.model_element     = []
        self.python_part       = None
        self.view_ele          = None

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select the PythonPart"))

        pythonpart_query     = AllplanIFW.QueryTypeID(AllplanElementAdapter.PythonPart_TypeUUID)
        sub_pythonpart_query = AllplanIFW.QueryTypeID(AllplanElementAdapter.SubPythonPart_TypeUUID)

        sel_query = AllplanIFW.SelectionQuery([pythonpart_query, sub_pythonpart_query])

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

        if self.input_state == InputState.SELECT:
            return self.select_python_part(mouse_msg, pnt, msg_info)

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info,
                                                   self.first_point, not self.first_point_input).GetPoint()


        #----------------- set the placement point

        placement_mat = AllplanGeo.Matrix3D()

        view_props = self.view_ele.GeneralSectionProperties

        view_props.PlacementPoint = AllplanGeo.Point2D(input_pnt)

        self.view_ele.GeneralSectionProperties = view_props


        #----------------- draw the preview

        self.view_ele.DrawElement(self.model_elements, placement_mat, self.coord_input.GetInputViewDocumentID(), False)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        ele_list = AllplanElementAdapter.BaseElementAdapterList()
        ele_list.append(self.python_part)

        AllplanBaseElements.CreateSectionsAndViews(self.coord_input.GetInputViewDocument(),
                                                   placement_mat,
                                                   ele_list,
                                                   [self.view_ele],
                                                   self.coord_input.GetViewWorldProjection())

        if self.input_state == InputState.CREATE_SECTION:
            self.input_state = InputState.SELECT
            return True

        self.create_section_element()

        return True


    def select_python_part(self, mouse_msg, pnt, msg_info):
        """ Select the PythonPart """

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True, self.element_filter)

        self.python_part = self.coord_input.GetSelectedElement()

        if self.coord_input.IsMouseMove(mouse_msg)  or  self.python_part.IsNull():
            return True

        success, name, parameter = AllplanBaseElements.PythonPartService.GetParameter(self.python_part)

        success, placement_mat = AllplanBaseElements.PythonPartService.GetPlacementMatrix(self.python_part)

        print("--------------------------------------")
        print(name)
        print()
        print(parameter)
        print()

        build_ele_service = BuildingElementService()

        result, build_ele_script, build_ele_list, control_props_list, build_ele_composite, part_name, file_name = \
            build_ele_service.read_data_from_pyp(name, self.str_table_service.str_table, False,
                                                      self.str_table_service.material_str_table)

        BuildingElementListService.read_fav_data(parameter, build_ele_list)

        if len(build_ele_list) == 1:
            created_elements = build_ele_script.create_element(build_ele_list[0], self.coord_input.GetInputViewDocument())

        else:
            build_ele_composite.connect_building_element_values(build_ele_list)

            created_elements = build_ele_script.create_element(build_ele_list, build_ele_composite, self.coord_input.GetInputViewDocument())


        #----------------- Transform to get the model geometry

        self.model_elements = []

        for model_ele in created_elements[0] if isinstance(created_elements, tuple) else created_elements.elements:
            if isinstance(model_ele, AllplanBasisElements.MacroPlacementElement):
                for slide in model_ele.GetMacro().GetSlideList():
                    for ele in slide.GetObjectList():
                        if isinstance(ele, AllplanBasisElements.ModelElement3D):
                            geo_ele = ele.GetGeometryObject()

                            ele.SetGeometryObject(AllplanGeo.Transform(geo_ele, placement_mat))

                            self.model_elements.append(ele)

                for reinf_ele in model_ele.GetReinforcementList():
                    reinf_ele.Transform(placement_mat)

                    self.model_elements.append(reinf_ele)

        self.input_state = InputState.CREATE_VIEW

        self.create_front_view_element()

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Placement point of the view"))

        return True


    def create_front_view_element(self):
        """
        Create the ViewSectionElement for the front view
        """

        #----------------- initialize the section and view properties

        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_format_props = view_props.FormatProperties
        view_filter_props = view_props.FilterProperties
        view_label_props  = view_props.LabelingProperties


        #----------------- section format properties

        view_format_props.IsEliminationOn  = True
        view_format_props.EliminationAngle = 22


        #----------------- labeling properties

        view_label_props.HeadingOn = False


        #----------------- section drawing files properties

        view_draw_files_props = AllplanBasisElements.SectionDrawingFilesProperties()

        drawing_file_number = AllplanUtility.VecIntList()
        drawing_file_number.append(self.python_part.GetDrawingfileNumber())

        view_draw_files_props.DrawingNumbers = drawing_file_number


        #----------------- section filter properties

        view_filter_props.DrawingFilesProperties = view_draw_files_props


        #----------------- general section properties

        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_props.Status             = AllplanBasisElements.SectionGeneralProperties.State.Hidden
        view_props.ShowSectionBody    = True
        view_props.FormatProperties   = view_format_props
        view_props.FilterProperties   = view_filter_props
        view_props.LabelingProperties = view_label_props
        view_props.PlacementPoint     = AllplanGeo.Point2D()
        view_props.PlacementPointType = AllplanBasisElements.SectionGeneralProperties.PlacementPointPosition.TopLeft


        #----------------- view element

        view_ele = AllplanBasisElements.ViewSectionElement()

        view_ele.GeneralSectionProperties = view_props
        view_ele.ViewMatrix               = RotationAngles(-90, 0, 0).get_rotation_matrix()

        self.view_ele = view_ele


    def create_section_element(self):
        """
        Create the ViewSectionElement for the section
        """

        self.input_state = InputState.CREATE_SECTION


        #----------------- initialize the section and view properties

        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_format_props = view_props.FormatProperties
        view_filter_props = view_props.FilterProperties
        view_label_props  = view_props.LabelingProperties


        #----------------- section format properties

        view_format_props.IsEliminationOn  = True
        view_format_props.EliminationAngle = 22


        #----------------- labeling properties

        view_label_props.HeadingOn = False


        #----------------- section drawing files properties

        view_draw_files_props = AllplanBasisElements.SectionDrawingFilesProperties()

        drawing_file_number = AllplanUtility.VecIntList()
        drawing_file_number.append(self.python_part.GetDrawingfileNumber())

        view_draw_files_props.DrawingNumbers = drawing_file_number


        #----------------- section filter properties

        view_filter_props.DrawingFilesProperties = view_draw_files_props


        #----------------- general section properties

        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_props.Status             = AllplanBasisElements.SectionGeneralProperties.State.Hidden
        view_props.ShowSectionBody    = True
        view_props.FormatProperties   = view_format_props
        view_props.FilterProperties   = view_filter_props
        view_props.LabelingProperties = view_label_props
        view_props.PlacementPoint     = AllplanGeo.Point2D()
        view_props.PlacementPointType = AllplanBasisElements.SectionGeneralProperties.PlacementPointPosition.TopLeft


        #----------------- create the section body

        ele_list = AllplanElementAdapter.BaseElementAdapterList()
        ele_list.append(self.python_part)

        minmax = AllplanBaseElements.GetMinMaxBox(ele_list)

        dx = minmax.GetSizeX() * 4 / 10
        dy = minmax.GetSizeY() / 10
        dz = minmax.GetSizeZ() / 10

        minmax.Deflate(dx, -dy, -dz)

        section_def_data = AllplanBasisElements.SectionDefinitionData()

        section_def_data.SectionBody = AllplanGeo.Polyhedron3D.CreateCuboid(minmax.Min, minmax.Max)

        min_sect_pnt = AllplanGeo.Point2D(minmax.Min)
        max_sect_pnt = AllplanGeo.Point2D(minmax.Max)

        section_path = AllplanGeo.Polyline2D()
        section_path += min_sect_pnt
        section_path += AllplanGeo.Point2D(max_sect_pnt.X, min_sect_pnt.Y)
        section_path += max_sect_pnt
        section_path += AllplanGeo.Point2D(min_sect_pnt.X, max_sect_pnt.Y)
        section_path += min_sect_pnt

        section_def_data.ClippingPath    = section_path
        section_def_data.DirectionVector = AllplanGeo.Vector3D(1, 0, 0)


        #----------------- view element

        view_ele = AllplanBasisElements.ViewSectionElement()

        view_ele.GeneralSectionProperties = view_props
        view_ele.ViewMatrix               = RotationAngles(0, 90, 90).get_rotation_matrix()
        view_ele.SectionDefinitionData    = section_def_data

        self.view_ele = view_ele

