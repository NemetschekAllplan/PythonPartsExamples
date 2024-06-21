""" Script for CadDataFileReader
"""

from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from BuildingElement import BuildingElement
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementComposite import BuildingElementComposite
from BuildingElementListService import BuildingElementListService
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction
from PythonPartUtil import PythonPartUtil
from StringTableService import StringTableService

from TypeCollections.ModificationElementList import ModificationElementList

from Utils import LibraryBitmapPreview
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CadDataFileReaderBuildingElement import CadDataFileReaderBuildingElement
else:
    CadDataFileReaderBuildingElement = BuildingElement

print('Load CadDataFileReader.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
            version is supported state
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Create the library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\ExportImport\CadDataFileReader.png"))


def create_interactor(coord_input              : AllplanIFW.CoordinateInput,
                      pyp_path                 : str,
                      global_str_table_service : StringTableService,
                      build_ele_list           : list[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      build_ele_ctrl_props_list: list[BuildingElementControlProperties],
                      modification_ele_list    : ModificationElementList) -> CadDataFileReader:
    """ Create the interactor

    Args:
        coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
        pyp_path:                  path of the pyp file
        global_str_table_service:  global string table service
        build_ele_list:            list with the building elements
        build_ele_composite:       building element composite with the building element constraints
        build_ele_ctrl_props_list: list with the building element control properties
        modification_ele_list:     UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return CadDataFileReader(coord_input, pyp_path, global_str_table_service,
                                         build_ele_list, build_ele_composite, build_ele_ctrl_props_list, modification_ele_list)


class CadDataFileReader():
    """ Definition of class CadDataFileReader
    """

    def __init__(self,
                 coord_input              : AllplanIFW.CoordinateInput,
                 pyp_path                 : str,
                 global_str_table_service : StringTableService,
                 build_ele_list           : list[BuildingElement],
                 build_ele_composite      : BuildingElementComposite,
                 build_ele_ctrl_props_list: list[BuildingElementControlProperties],
                 modification_ele_list    : ModificationElementList):
        """ initialize and start the input

        Args:
            coord_input:               API object for the coordinate input, element selection, ... in the Allplan view
            pyp_path:                  path of the pyp file
            global_str_table_service:  global string table service
            build_ele_list:            list with the building elements
            build_ele_composite:       building element composite with the building element constraints
            build_ele_ctrl_props_list: list with the building element control properties
            modification_ele_list:     UUIDs of the existing elements in the modification mode
        """

        self.coord_input               = coord_input
        self.pyp_path                  = pyp_path
        self.str_table_service         = global_str_table_service
        self.build_ele_list            = build_ele_list
        self.build_ele_composite       = build_ele_composite
        self.build_ele_ctrl_props_list = build_ele_ctrl_props_list
        self.modification_ele_list     = modification_ele_list
        self.model_ele_list            = []
        self.placement_mat             = AllplanGeo.Matrix3D()
        self.modification_mode         = modification_ele_list.is_modification_element()
        self.placement_mat             = AllplanGeo.Matrix3D() if not self.modification_mode else self.build_ele_list[0].get_insert_matrix()
        self.ref_point_input           = True

        self.build_ele = cast(CadDataFileReaderBuildingElement, self.build_ele_list[0])


        #----------------- read the obj file

        self.read_data()


        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             None,
                                                             self.build_ele_ctrl_props_list,
                                                             "PythonPartsFramework\\InteractorExamples\\ExportImport\\CadDataFileReader")

        self.palette_service.show_palette("CadDataFileReader")

        if self.modification_mode:
            self.draw_preview()

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Placement point"))


    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        self.draw_preview()


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.on_preview_draw()


    def on_cancel_function(self) -> bool:
        """ Check for input function cancel in case of ESC

        Returns:
            cancel the function state
        """

        if self.modification_mode:
            self.create_element()

        self.palette_service.close_palette()

        return True


    def on_control_event(self,
                         _event_id: int) -> bool:
        """ Handle the control event

        Args:
            _event_id: event ID

        Returns:
            event was processed state
        """

        self.create_element()

        self.ref_point_input = True

        return True


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """ Modify property of element

        Args:
            page:  page index of the modified property
            name:  name of the modified property
            value: new value
        """

        build_ele = self.build_ele


        #----------------- initialize the file name

        if name == build_ele.ObjFile.name:
            if not build_ele.ObjFile.value:
                build_ele.ObjFile.value = AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + \
                                          r"PythonPartsExampleScripts\InteractorExamples\ExportImport\data\earth.obj"

        elif name == build_ele.IfcFile.name:
            if not build_ele.IfcFile.value:
                build_ele.ObjFile.value = AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + \
                                          r"PythonPartsExampleScripts\InteractorExamples\ExportImport\data\BoxCylinder.ifc"

        elif name == build_ele.SkpFile.name:
            if not build_ele.SkpFile.value:
                build_ele.ObjFile.value = AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + \
                                          r"PythonPartsExampleScripts\InteractorExamples\ExportImport\data\Chair.skp"


        #----------------- select the file and read the data

        self.palette_service.modify_element_property(page, name, value)

        if "File" in name:                      # pylint: disable=magic-value-comparison
            if name == build_ele.ObjFile.name:
                build_ele.SkpFile.value = ""
                build_ele.IfcFile.value = ""

            if name == build_ele.SkpFile.name:
                build_ele.ObjFile.value = ""
                build_ele.IfcFile.value = ""

            elif name == build_ele.IfcFile.name:
                build_ele.ObjFile.value = ""
                build_ele.SkpFile.value = ""

            self.read_data()

            self.palette_service.update_palette(-1, False)

        self.draw_preview()


    def read_data(self):
        """ read the data
        """

        build_ele = self.build_ele

        if build_ele.ObjFile.value:
            self.model_ele_list = AllplanBaseEle.CadDataFileReader.ReadOBJ(build_ele.ObjFile.value,
                                                                           AllplanBaseEle.eDesignPathLocation.OverrideFiles)

        elif build_ele.SkpFile.value:
            self.model_ele_list = AllplanBaseEle.CadDataFileReader.ReadSKP(build_ele.SkpFile.value,
                                                                           AllplanBaseEle.eDesignPathLocation.OverrideFiles)

        elif build_ele.IfcFile.value:
            ifc_data = AllplanBaseEle.CadDataFileReader.ReadIFC(self.coord_input.GetInputViewDocument(), build_ele.IfcFile.value)

            self.model_ele_list = []

            for _, model_elements in ifc_data:
                self.model_ele_list += model_elements

            build_ele.ObjFile.value = ""


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """ Handles the process mouse message event

        Args:
            mouse_msg: mouse message ID
            pnt:       input point in Allplan view coordinates
            msg_info:  additional mouse message info

        Returns:
            True/False for success.
        """

        if self.modification_mode or not self.ref_point_input:
            self.draw_preview()
            return True

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        self.placement_mat = AllplanGeo.Matrix3D()
        self.placement_mat.SetTranslation(AllplanGeo.Vector3D(input_pnt))

        self.draw_preview()

        if not self.coord_input.IsMouseMove(mouse_msg):
            self.ref_point_input = False

        return True


    def create_element(self):
        """ create the element
        """

        if not self.model_ele_list:
            AllplanUtil.ShowMessageBox("No elements are imported (mayby a corrupted data file)", AllplanUtil.MB_OK)
            return

        build_ele = self.build_ele

        local_placement_mat = RotationUtil(build_ele.RotationAngleX.value,
                                           build_ele.RotationAngleY.value,
                                           build_ele.RotationAngleZ.value).get_rotation_matrix()

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)

        pyp_transaction = PythonPartTransaction(self.coord_input.GetInputViewDocument())

        pyp_transaction.execute(self.placement_mat,
                                self.coord_input.GetViewWorldProjection(),
                                pyp_util.create_pythonpart(self.build_ele, local_placement_matrix = local_placement_mat),
                                self.modification_ele_list)

    def draw_preview(self):
        """ draw the preview
        """

        build_ele = self.build_ele

        local_placement_mat = RotationUtil(build_ele.RotationAngleX.value,
                                           build_ele.RotationAngleY.value,
                                           build_ele.RotationAngleZ.value).get_rotation_matrix()

        PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), local_placement_mat * self.placement_mat,
                                  self.model_ele_list, True, None)


    def update_after_favorite_read(self):
        """ execute the necessary update after a favorite read
        """

        self.palette_service.update_palette(-1, True)


    def __del__(self):
        """ save the default favorite data """

        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)
