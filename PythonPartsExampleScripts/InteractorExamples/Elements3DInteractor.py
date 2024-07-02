"""
Script for Line2DInteractor
"""

from typing import Any

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseInteractor import BaseInteractor
from BuildingElement import BuildingElement
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from StringTableService import StringTableService

print('Load Elements3DInteractor.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter):
    """
    Creation of the element preview

    Args:
        build_ele: the building element.
        doc:       input document
    """

    com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    com_prop.GetGlobalProperties()

    cuboid = AllplanGeo.Polyhedron3D.CreateCuboid(2000, 1000, 5000)

    axis     = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(3000, 500 , 0))
    cylinder = AllplanGeo.BRep3D.CreateCylinder(axis, 500, 3000)

    model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, cuboid),
                      AllplanBasisElements.ModelElement3D(com_prop, cylinder)]

    return (model_ele_list, None, None)


def create_interactor(coord_input      : AllplanIFW.CoordinateInput,
                      pyp_path         : str,
                      str_table_service: StringTableService) -> Any:
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return Elements3DInteractor(coord_input, pyp_path, str_table_service)


class Elements3DInteractor(BaseInteractor):
    """
    Definition of class 3D_ElementsInteractor
    """

    def __init__(self,
                 coord_input      : AllplanIFW.CoordinateInput,
                 pyp_path         : str,
                 str_table_service: StringTableService):
        """
        Initialization of class 3D_ElementsInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service
        self.first_point       = AllplanGeo.Point3D()
        self.build_ele_service = BuildingElementService()
        self.input_event       = 0
        self.model_ele_list    = []

        self.palette_service : BuildingElementPaletteService = Any

        self.show_palette("Elements3DSelect.pal")


    def show_palette(self,
                     palette_name: str):
        """
        Show the palette

        Args:
            palette_name:   File name of the palette
        """

        if self.palette_service is not Any:
            self.palette_service.close_palette()

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(self.pyp_path + "\\" + palette_name,
                                                      self.str_table_service.str_table, False,
                                                      self.str_table_service.material_str_table)

        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)

        if palette_name == "Elements3DSelect.pal":
            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select the geometry type"))

        elif palette_name== "Cuboid.pal":
            self.coord_input.InitFirstPointValueInput(AllplanIFW.InputStringConvert("Reference point / angle"),
                                                      AllplanIFW.ValueInputControlData(AllplanIFW.eValueInputControlType.eANGLE_COMBOBOX,
                                                                                       True, False))
        else:
            self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("Reference point"))


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: str):
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


    def on_control_event(self,
                         event_id: int):
        """
        Handles on control event

        Args:
            event_id: event id of control.
        """

        if event_id == 1000:
            self.show_palette("Cuboid.pal")
        else:
            self.show_palette("Cylinder.pal")

        self.input_event = event_id


    def on_cancel_function(self) -> bool:
        """
        Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False for success.
        """

        if self.input_event == 0:
            self.palette_service.close_palette()

            return True

        self.input_event = 0

        self.show_palette("Elements3DSelect.pal")

        return False


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """

        input_pnt = self.coord_input.GetCurrentPoint().GetPoint()

        self.draw_preview(input_pnt)


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """
        self.on_preview_draw()


    def on_value_input_control_enter(self) -> bool:
        """
        Handles the enter inside the value input control event

        Returns:
            True/False for success.
        """

        return True


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        if self.input_event == 0:
            return True

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()

        self.draw_preview(input_pnt)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- Create the element and continue with the input

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeo.Matrix3D(),
                                           self.model_ele_list, [], None)

        return True


    def draw_preview(self,
                     input_pnt: AllplanGeo.Point3D):
        """
        Draw the preview

        Args:
            input_pnt:  Input point
        """

        build_ele = self.build_ele_list[0]

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        if self.input_event == 1000:
            cuboid = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value, build_ele.Width.value,
                                                          build_ele.Height.value)

            angle = self.coord_input.GetInputControlValue()

            cuboid = AllplanGeo.Rotate(cuboid, AllplanGeo.Axis3D(AllplanGeo.Point3D(), AllplanGeo.Vector3D(0, 0, 1000)),
                                       AllplanGeo.Angle(angle))

            self.model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, cuboid)]

        elif self.input_event == 1001:
            axis     = AllplanGeo.AxisPlacement3D()
            cylinder = AllplanGeo.BRep3D.CreateCylinder(axis, build_ele.Radius.value, build_ele.Height.value)

            self.model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, cylinder)]

        else:
            return

        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(input_pnt), 0, 0, 0, self.model_ele_list)

        AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.model_ele_list, False, None)
