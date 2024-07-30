""" Script for BottomTopPlaneService
"""

from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction
from StringTableService import StringTableService

from Utils import LibraryBitmapPreview

from TypeCollections.ModificationElementList import ModificationElementList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BottomTopPlaneServiceBuildingElement import BottomTopPlaneServiceBuildingElement
else:
    BottomTopPlaneServiceBuildingElement = BuildingElement

print('Load BottomTopPlaneService.py')


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
    """ Creation of the library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ServiceExamples\BottomTopPlaneService.png"))


def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties],
                      modification_ele_list   : ModificationElementList) -> BottomTopPlaneService:
    """ Create the interactor

    Args:
        coord_input:              API object for the coordinate input, element selection, ... in the Allplan view
        pyp_path:                 path of the pyp file
        global_str_table_service: global string table service
        build_ele_list:           list with the building elements
        build_ele_composite:      building element composite with the building element constraints
        control_props_list:       control properties list
        modification_ele_list:    UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return BottomTopPlaneService(coord_input, pyp_path, global_str_table_service,
                                build_ele_list, build_ele_composite, control_props_list, modification_ele_list)


class BottomTopPlaneService():
    """ Definition of class BottomTopPlaneService
    """

    def __init__(self,
                 coord_input             : AllplanIFW.CoordinateInput,
                 pyp_path                : str,
                 global_str_table_service: StringTableService,
                 build_ele_list          : list[BuildingElement],
                 build_ele_composite     : BuildingElementComposite,
                 control_props_list      : list[BuildingElementControlProperties],
                 modification_ele_list   : ModificationElementList):
        """ initialize and start the input

        Args:
            coord_input:              API object for the coordinate input, element selection, ... in the Allplan view
            pyp_path:                 path of the pyp file
            global_str_table_service: global string table service
            build_ele_list:           list with the building elements
            build_ele_composite:      building element composite with the building element constraints
            control_props_list:       control properties list
            modification_ele_list:    UUIDs of the existing elements in the modification mode
        """

        self.coord_input           = coord_input
        self.pyp_path              = pyp_path
        self.str_table_service     = global_str_table_service
        self.build_ele_list        = build_ele_list
        self.build_ele_composite   = build_ele_composite
        self.control_props_list    = control_props_list
        self.modification_ele_list = modification_ele_list
        self.model_ele_list        = []
        self.modification_mode     = modification_ele_list.is_modification_element()
        self.com_prop              = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()
        self.placement_point       = AllplanGeo.Point3D()

        self.build_ele = cast(BottomTopPlaneServiceBuildingElement, self.build_ele_list[0])

        self.set_plane_data()


        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             "PythonPartsFramework\\ServiceExamples\\BottomTopPlaneService")

        self.palette_service.show_palette("BottomTopPlaneService")

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Placement point"))


    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        self.draw_preview()


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.draw_preview()


    def on_cancel_function(self) -> bool:
        """ Check for input function cancel in case of ESC

        Returns:
            cancel the function state
        """

        if self.modification_mode:
            self.create_pythonpart()

        self.palette_service.close_palette()

        return True


    def on_control_event(self,                          # pylint: disable=no-self-use
                         _event_id: int) -> bool:
        """ Handle the control event

        Args:
            _event_id: event ID

        Returns:
            event was processed state
        """

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

        self.palette_service.modify_element_property(page, name, value)

        self.set_plane_data()
        self.draw_preview()

        self.palette_service.update_palette(-1, False)



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

        if self.modification_mode:
            self.draw_preview()
            return True


        #-----------------  get the placement matrix

        self.placement_point = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        self.draw_preview()

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        self.create_pythonpart()

        return True


    def draw_preview(self):
        """ draw the preview
        """

        self.create_cylinder()

        if self.model_ele_list:
            placement_mat = AllplanGeo.Matrix3D()
            placement_mat.SetTranslation(AllplanGeo.Vector3D(self.placement_point))

            PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), placement_mat,
                                      self.model_ele_list, True, None, not self.modification_mode)


    def create_cylinder(self):
        """ create the cylinder
        """

        doc       = self.coord_input.GetInputViewDocument()
        build_ele = self.build_ele

        self.model_ele_list  = []


        #----------------- get the default plane z coordinates

        plane_refs = build_ele.PlaneReferences.value

        z_bottom = plane_refs.GetAbsBottomElevation()

        if not isinstance(build_ele.ReferencePlaneBottom.value, AllplanGeo.Plane3D):
            z_bottom = min(z_bottom,
                           AllplanArchEle.BottomTopPlaneService.GetAbsoluteBottomElevation(AllplanEleAdapter.BaseElementAdapter(),
                                                                                           doc, plane_refs))

        z_top = plane_refs.GetAbsTopElevation()

        if not isinstance(build_ele.ReferencePlaneTop.value, AllplanGeo.Plane3D):
            z_top = max(z_top,
                        AllplanArchEle.BottomTopPlaneService.GetAbsoluteTopElevation(AllplanEleAdapter.BaseElementAdapter(),
                                                                                     doc, plane_refs))

        cylinder = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(self.placement_point + \
                                                                               AllplanGeo.Point3D(0, 0, z_bottom)),
                                                    500, z_top - z_bottom)

        doc_bottom_plane, doc_top_plane = AllplanArchEle.BottomTopPlaneService.GetDocumentDefaultPlanes(doc)


        #----------------- cut the cylinder with the bottom plane

        if not isinstance(build_ele.ReferencePlaneBottom.value, AllplanGeo.Plane3D):
            if isinstance(build_ele.ReferencePlaneBottom.value, AllplanGeo.Polyhedron3D):
                error, brep_plane = AllplanGeo.CreateBRep3D(build_ele.ReferencePlaneBottom.value)

                if error:
                    return

            else:
                brep_plane = build_ele.ReferencePlaneBottom.value

            brep_plane = AllplanGeo.Move(brep_plane, AllplanGeo.Vector3D(0, 0, plane_refs.GetBottomElevation()))


            #------------- calculate the cylinder - plane intersection

            error, cylinder_parts = AllplanGeo.MakeSectionWithSurfaces(cylinder, brep_plane)

            if error != AllplanGeo.eGeometryErrorCode.eOK:
                result, above, below = AllplanGeo.CutBrepWithPlane(cylinder, doc_bottom_plane)

                cylinder_part = []

                if result:
                    cylinder_parts = [above, below]


            #------------- get the bottom part of the cylinder

            for cylinder_part in cylinder_parts:
                min_max, result = AllplanGeo.CalcMinMax(cylinder_part)

                if result == AllplanGeo.eServiceResult.NO_ERR:
                    if abs(min_max.Max.Z - z_top) < 1.:
                        cylinder = cylinder_part

                        z_bottom = min_max.Min.Z

                        break


        #----------------- cut the cylinder with the top plane

        if not isinstance(build_ele.ReferencePlaneTop.value, AllplanGeo.Plane3D):
            if isinstance(build_ele.ReferencePlaneTop.value, AllplanGeo.Polyhedron3D):
                error, brep_plane = AllplanGeo.CreateBRep3D(build_ele.ReferencePlaneTop.value)

                if error:
                    return

            else:
                brep_plane = build_ele.ReferencePlaneTop.value

            brep_plane = AllplanGeo.Move(brep_plane, AllplanGeo.Vector3D(0, 0, plane_refs.GetTopElevation()))


            #------------- calculate the cylinder - plane intersection

            error, cylinder_parts = AllplanGeo.MakeSectionWithSurfaces(cylinder, brep_plane)

            if error != AllplanGeo.eGeometryErrorCode.eOK:
                result, above, below = AllplanGeo.CutBrepWithPlane(cylinder, doc_top_plane)

                cylinder_part = []

                if result:
                    cylinder_parts = [above, below]


            #------------- get the bottom part of the cylinder

            for cylinder_part in cylinder_parts:
                min_max, result = AllplanGeo.CalcMinMax(cylinder_part)

                if result == AllplanGeo.eServiceResult.NO_ERR:
                    if abs(min_max.Min.Z - z_bottom) < 1.:
                        cylinder = cylinder_part

                        z_top = min_max.Max.Z

                        break

        if not cylinder.IsValid():
            return

        cylinder = AllplanGeo.Move(cylinder, AllplanGeo.Vector3D(self.placement_point, AllplanGeo.Point3D()))

        self.model_ele_list = [AllplanBasisEle.ModelElement3D(self.com_prop, cylinder)]


    def create_pythonpart(self):
        """ create the PythonPart
        """

        self.create_cylinder()

        if not self.model_ele_list:
            return

        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)

        pyp_trans = PythonPartTransaction(self.coord_input.GetInputViewDocument())

        placement_mat = AllplanGeo.Matrix3D()
        placement_mat.SetTranslation(AllplanGeo.Vector3D(self.placement_point))

        pyp_trans.execute(placement_mat, self.coord_input.GetViewWorldProjection(),
                          pyp_util.create_pythonpart(self.build_ele), self.modification_ele_list)


    def set_plane_data(self):
        """ set the data for the planes
        """

        build_ele = self.build_ele
        doc       = self.coord_input.GetInputViewDocument()

        build_ele.ReferencePlaneBottom.value = \
            AllplanArchEle.BottomTopPlaneService.GetBottomReferencePlane(AllplanEleAdapter.BaseElementAdapter(),
                                                                         doc, build_ele.PlaneReferences.value)

        build_ele.PlaneTextBottom.value = "as Polyhedron3D" \
            if isinstance(build_ele.ReferencePlaneBottom.value, AllplanGeo.Polyhedron3D) else "as Plane3D"

        build_ele.ReferencePlaneTop.value = \
            AllplanArchEle.BottomTopPlaneService.GetTopReferencePlane(AllplanEleAdapter.BaseElementAdapter(),
                                                                      doc, build_ele.PlaneReferences.value)

        build_ele.PlaneTextTop.value = "as Polyhedron3D" \
            if isinstance(build_ele.ReferencePlaneTop.value, AllplanGeo.Polyhedron3D) else "as Plane3D"
