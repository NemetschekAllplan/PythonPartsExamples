""" Script for ModelPolygonExtrudeInteractor
"""

from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil

from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction, ReinforcementRearrange
from PythonPartUtil import PythonPartUtil
from StringTableService import StringTableService

from TypeCollections.ModificationElementList import ModificationElementList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModelPolygonExtrudeInteractorBuildingElement import ModelPolygonExtrudeInteractorBuildingElement
else:
    ModelPolygonExtrudeInteractorBuildingElement = BuildingElement

print('Load ModelPolygonExtrudeInteractor.py')


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
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the library preview

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        created element result
    """

    return CreateElementResult()


def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties],
                      modification_ele_list   : ModificationElementList) -> ModelPolygonExtrudeInteractor:
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

    return ModelPolygonExtrudeInteractor(coord_input, pyp_path, global_str_table_service,
                                         build_ele_list, build_ele_composite, control_props_list, modification_ele_list)


class ModelPolygonExtrudeInteractor():
    """ Definition of class ModelPolygonExtrudeInteractor
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

        self.build_ele = cast(ModelPolygonExtrudeInteractorBuildingElement, self.build_ele_list[0])


        #----------------- modification mode

        build_ele = self.build_ele

        self.model_polygon = None

        if modification_ele_list.is_modification_element():
            python_part = modification_ele_list.get_base_element_adapter(coord_input.GetInputViewDocument())

            polygon_uuid = AllplanElementAdapter.GUID.FromString(build_ele.PolygonUUID.value)

            self.model_polygon = AllplanElementAdapter.BaseElementAdapter.FromGUID(polygon_uuid,
                                                                                   coord_input.GetInputViewDocument())

            if str(python_part.GetModelElementUUID()) != build_ele.PythonPartUUID.value:
                AllplanUtil.ShowMessageBox("You are modifying a copied PythonPart!\n\n"
                                           "The original polygon is used",
                                           AllplanUtil.MB_OK)

                build_ele.Polygon.value = AllplanGeo.Transform(build_ele.Polygon.value, build_ele.get_insert_matrix().ReduceZDimension())

            else:
                geo_ele = self.model_polygon.GetModelGeometry()

                if isinstance(geo_ele, AllplanGeo.Polyline2D):
                    geo_ele = AllplanGeo.Polygon2D(geo_ele.Points)

                build_ele.Polygon.value = geo_ele


        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             "PythonPartsFramework\\InteractorExamples\\ModelPolygonExtrudeInteractor")

        self.palette_service.show_palette(self.build_ele.script_name)

        if modification_ele_list.is_modification_element():
            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Modify properties"))
        else:
            self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select 2D-polygon"))


    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        self.draw_preview(self.build_ele.Polygon.value)


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.draw_preview(self.build_ele.Polygon.value)


    def on_cancel_function(self) -> bool:
        """ Check for input function cancel in case of ESC

        Returns:
            True
        """

        if self.model_polygon:
            self.create_pythonpart()

        self.palette_service.close_palette()

        return True


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """ Modify property of element

        Args:
            page:  the page of the property
            name:  the name of the property.
            value: new value for property.
        """

        update_palette = self.palette_service.modify_element_property(page, name, value)

        if self.build_ele.Polygon.value:
            self.draw_preview(self.build_ele.Polygon.value)

        if update_palette:
            self.palette_service.update_palette(-1, False)


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Handles the process mouse message event

        Args:
            mouse_msg: the mouse message.
            pnt:       the input point.
            msg_info:  additional message info.

        Returns:
            True/False for success.
        """

        #----------------- modification mode

        build_ele = self.build_ele

        if self.model_polygon:
            self.draw_preview(build_ele.Polygon.value)

            return True


        #----------------- select the geometry

        build_ele.Polygon.value = AllplanGeo.Polygon2D()

        if not self.coord_input.SelectElement(mouse_msg, pnt, msg_info, True, True, True):
            return True

        if not (geo_ele := self.coord_input.GetSelectedGeometryElement()):
            return True


        #----------------- check for a Polygon2D geometry

        if isinstance(geo_ele, AllplanGeo.Polyline2D):
            geo_ele = AllplanGeo.Polygon2D(geo_ele.Points)

            if not geo_ele.IsValid():
                return True

        elif not isinstance(geo_ele, AllplanGeo.Polygon2D):
            return True


        #----------------- draw the preview

        build_ele.Polygon.value     = geo_ele
        build_ele.PolygonUUID.value = str(self.coord_input.GetSelectedElement().GetModelElementUUID())

        self.draw_preview(geo_ele)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        self.create_pythonpart()

        return True


    def create_pythonpart(self):
        """ create the PythonPart """

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)

        pyp_transaction = PythonPartTransaction(self.coord_input.GetInputViewDocument())

        pyp_transaction.execute(AllplanGeo.Matrix3D(),
                                self.coord_input.GetViewWorldProjection(),
                                pyp_util.create_pythonpart(self.build_ele),
                                self.modification_ele_list,
                                ReinforcementRearrange(), True,
                                uuid_parameter_name = "PythonPartUUID" if self.model_polygon is None else "",
                                use_system_angle = False)


    def draw_preview(self,
                     geo_ele: AllplanGeo.Polygon2D):
        """ draw the preview
        Args:
            geo_ele: polygon
        """

        if not geo_ele.IsValid():
            return


        #----------------- extrusion path

        start_pnt = AllplanGeo.Point3D(geo_ele.StartPoint)

        path = AllplanGeo.Polyline3D()
        vec  = self.build_ele.ExtrusionVector.value

        path += start_pnt
        path += start_pnt + AllplanGeo.Point3D(vec.X, vec.Y, vec.Z)


        #----------------- extrusion polygon

        result, polygon3d = AllplanGeo.ConvertTo3D(geo_ele)

        if not result:
            return

        err, polyline3d = AllplanGeo.CreatePolyline3D(polygon3d)

        if err:
            return


        #----------------- extrude the polygon

        poly_list = AllplanGeo.Polyline3DList()

        poly_list.append(polyline3d)

        err, extruded_ele = AllplanGeo.CreateSweptPolyhedron3D(poly_list, path, True, True, AllplanGeo.Vector3D())

        self.model_ele_list = []

        if err:
            return

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        self.model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, extruded_ele)]

        PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), AllplanGeo.Matrix3D(),
                                  self.model_ele_list, True, None,
                                  False)
