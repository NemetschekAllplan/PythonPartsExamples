""" Script for SectionAlongPath
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

import enum

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction
from StringTableService import StringTableService

from TypeCollections.ModificationElementList import ModificationElementList
from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SectionAlongPathBuildingElement import SectionAlongPathBuildingElement
else:
    SectionAlongPathBuildingElement = BuildingElement

print('Load SectionAlongPath.py')

class InputState(enum.IntEnum):
    """" input states
    """

    SECTION_PATH_INPUT  = 1
    SECTION_PATH_SELECT = 2
    SECTION_PLACEMENT   = 3


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\ObjectCreation\SectionAlongPath.png"))

def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : list[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : list[BuildingElementControlProperties],
                      _modification_ele_list   : ModificationElementList) -> object:
    """ Create the interactor

    Args:
        coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service
        build_ele_list:            list with the building elements
        build_ele_composite:       building element composite with the building element constraints
        control_props_list:        control properties list
        _modification_ele_list:    list with the UUIDs of the modified elements

    Returns:
          Created interactor object
    """

    return SectionAlongPath(coord_input, build_ele_list, build_ele_composite, control_props_list)


class SectionAlongPath(BaseInteractor):
    """ Definition of class SectionAlongPath
    """

    def __init__(self,
                 coord_input        : AllplanIFW.CoordinateInput,
                 build_ele_list     : list[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : list[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:         API object for the coordinate input, element selection, ... in the Allplan view
            build_ele_list:      list with the building elements
            build_ele_composite: building element composite with the building element constraints
            control_props_list:  control properties list
        """

        self.coord_input    = coord_input
        self.build_ele_list = build_ele_list
        self.build_ele      = cast(SectionAlongPathBuildingElement, build_ele_list[0])

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list, self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)

        self.place_pnt        = AllplanGeo.Point3D()
        self.input_state      = InputState.SECTION_PATH_INPUT
        self.section_path_ele = AllplanEleAdapter.BaseElementAdapter()
        self.section_path     = AllplanGeo.Path2D()
        self.model_ele_list   = ModelEleList(self.build_ele.CommonProp.value)
        self.polyline_input   = None

        self.start_input()


    def start_input(self):
        """ start the input
        """

        self.input_state = InputState.SECTION_PATH_INPUT

        self.section_path.Clear()

        if self.build_ele.SectionPathInput.value == 1:
            self.polyline_input = AllplanIFW.PolylineInput(self.coord_input, False)

        else:
            self.polyline_input = None

            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select the section path"))


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: str):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        if name == self.build_ele.SectionPathInput.name:
            if self.input_state == InputState.SECTION_PATH_INPUT:
                self.input_state    = InputState.SECTION_PATH_SELECT
                self.section_path   = AllplanGeo.Path2D()
                self.polyline_input = None

                self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select the section path"))

            else:
                self.input_state      = InputState.SECTION_PATH_INPUT
                self.polyline_input   = AllplanIFW.PolylineInput(self.coord_input, False)
                self.section_path_ele = AllplanEleAdapter.BaseElementAdapter()

            return

        if self.palette_service.modify_element_property(page, name, value):
            self.palette_service.update_palette(-1, False)

    def on_control_event(self,
                         event_id: int):
        """ Handles on control event

        Args:
            event_id: event id of the clicked button control
        """

    def on_cancel_function(self) -> bool:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False for success.
        """

        if self.input_state == InputState.SECTION_PATH_INPUT:
            if self.polyline_input is None:
                self.palette_service.close_palette()
                return True

            polyline = self.polyline_input.GetPolyline()

            self.section_path += AllplanGeo.ConvertTo2D(polyline)[1]

            self.polyline_input = None

            if polyline.Count() > 1:
                self.input_state = InputState.SECTION_PLACEMENT

                self.coord_input.InitNextPointValueInput(
                    AllplanIFW.InputStringConvert("Set the placement point"),
                    AllplanIFW.ValueInputControlData(AllplanIFW.eValueInputControlType.eANGLE_COMBOBOX, True, False),
                                                     AllplanIFW.CoordinateInputMode())

                return False

        self.palette_service.close_palette()

        return True

    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        self.draw_preview()

    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.draw_preview()

    def on_value_input_control_enter(self) -> bool:
        """ Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Process the mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        if self.input_state == InputState.SECTION_PATH_INPUT:
            if self.polyline_input:
                self.polyline_input.ExecuteInput(mouse_msg, pnt, msg_info)

            self.draw_preview()

            return True

        if self.input_state == InputState.SECTION_PATH_SELECT:
            self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True)

            if self.coord_input.IsMouseMove(mouse_msg):
                return True

            self.section_path_ele = self.coord_input.GetSelectedElement()

            self.input_state = InputState.SECTION_PLACEMENT

            self.coord_input.InitNextElementInput(AllplanIFW.InputStringConvert("Set the placement point"))

            return True


        #----------------- place the section

        self.place_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        self.draw_preview()

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        self.execute_transaction()

        self.start_input()

        return True


    def draw_preview(self):
        """ draw the preview
        """

        if self.input_state == InputState.SECTION_PATH_SELECT:
            return


        #----------------- draw the polyline

        if self.input_state == InputState.SECTION_PATH_INPUT:
            if self.polyline_input is None:
                return

            model_ele_list = ModelEleList(self.build_ele.CommonProp.value)

            model_ele_list.append_geometry_3d(self.polyline_input.GetPreviewPolyline())

            PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), AllplanGeo.Matrix3D(),
                                      model_ele_list, True, None, False)

            return


        #----------------- draw the preview

        self.create_element()

        AllplanBaseEle.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                          self.get_placement_matrix(), self.model_ele_list, True, None)


    def execute_transaction(self):
        """ execute the transaction
        """

        pyp_trans = PythonPartTransaction(self.coord_input.GetInputViewDocument())

        pyp_trans.execute(self.get_placement_matrix(), self.coord_input.GetViewWorldProjection(),
                          self.model_ele_list, ModificationElementList())


    def get_placement_matrix(self) -> AllplanGeo.Matrix3D:
        """ get the placement matrix

        Returns:
            placement matrix
        """

        z_angle = AllplanGeo.Angle(self.coord_input.GetInputControlValue())

        place_mat = AllplanGeo.Matrix3D()

        place_mat.SetRotation(AllplanGeo.Line3D(0, 0, 0, 0, 0, 1000), z_angle)

        place_mat.Translate(AllplanGeo.Vector3D(self.place_pnt))

        return place_mat


    def create_element(self):
        """ create the element
        """

        build_ele = self.build_ele

        section_props = AllplanBasisEle.SectionAlongPathProperties()


        #----------------- filter properties

        section_filter_props = section_props.FilterProperties

        drawing_file_props = section_filter_props.DrawingFilesProperties

        drawing_file_props.DrawingNumbers = [AllplanBaseEle.DrawingFileService.GetActiveFileNumber()]

        section_filter_props.DrawingFilesProperties = drawing_file_props

        section_props.FilterProperties = section_filter_props


        #----------------- labeling properties

        general_props = section_props.GeneralSectionProperties

        labeling_props = general_props.SectionLabelingProperties

        labeling_props.HeadingText = build_ele.Header.value

        general_props.SectionLabelingProperties = labeling_props

        section_props.GeneralSectionProperties = general_props


        #----------------- clipping path properties

        length = AllplanGeo.CalcLength(self.section_path) if self.section_path_ele.IsNull() else \
                 AllplanGeo.CalcLength(self.section_path_ele.GetGeometry())

        path_props = section_props.ClippingPathProperties

        path_props.StartCoord        = 0
        path_props.EndCoord          = length
        path_props.StationingStart   = 0
        path_props.StationingEnd     = 0
        path_props.SectionIdentifier = build_ele.SectionIdentifier.value

        section_props.ClippingPathProperties = path_props

        self.model_ele_list.clear()

        if self.section_path_ele.IsNull():
            self.model_ele_list.append(AllplanBasisEle.SectionAlongPathElement(section_props, self.section_path,
                                                                               self.build_ele.CommonProp.value))
        else:
            self.model_ele_list.append(AllplanBasisEle.SectionAlongPathElement(section_props, self.section_path_ele))
