""" Script for RoomInput
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from AttributeIdValue import AttributeIdValue
from BaseScriptObject import BaseScriptObject, BaseScriptObjectData, OnCancelFunctionResult
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

from Utils import LibraryBitmapPreview, ElementPropertiesAttributeUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.RoomInputBuildingElement import RoomInputBuildingElement as BuildingElement
else:
    from BuildingElement import BuildingElement

print('Load RoomInput.py')


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

    print(_build_ele.pyp_file_path)

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ArchitectureExamples\Objects\RoomInput.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return RoomScript(build_ele, script_object_data)


class RoomScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural room

    This script objects prompts the user to input the outline by drawing a 2D-polygon and
    subsequently creates a room
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ function description

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.polygon_result = PolygonInteractorResult()
        self.build_ele      = build_ele


        #----------------- get the default attributes

        usr_attr = self.build_ele.UserAttributes.value

        room_attr = {230, 246, 501, 502, 503, 504, 505, 506, 507}

        fav_attr = {attr.attribute_id for attr in usr_attr}

        for attr_id, attr_value in AllplanArchEle.RoomProperties().GetAttributes(self.coord_input.GetInputViewDocument(), True):
            if attr_id not in room_attr and attr_id not in fav_attr:
                usr_attr.insert(-1, AttributeIdValue(attr_id, attr_value))

        build_ele.InputMode.value = build_ele.POLYGON_INPUT


    def start_input(self):
        """Starts the slab outline input at the beginning of the script runtime"""

        self.script_object_interactor = PolygonInteractor(self.polygon_result,
                                                          z_coord_input       = False,
                                                          multi_polygon_input = False,
                                                          preview_function    = self.create_preview_elements)

        self.build_ele.InputMode.value = self.build_ele.POLYGON_INPUT


    def start_next_input(self):
        """Terminate the outline input after successful input of a closed
        polygon consisting of at least 3 vertices
        """

        if not self.polygon_result.input_polygon.IsValid():
            return

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.POLYGON_INPUT


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        return CreateElementResult([self.create_room(self.polygon_result.input_polygon)],
                                   placement_point = AllplanGeo.Point3D(), multi_placement = True)


    def create_room(self,
                    polygon: AllplanGeo.Polygon3D) -> AllplanArchEle.RoomElement:
        """ create the room element

        Args:
            polygon: room polygon

        Returns:
            room element
        """

        _, room_polygon = AllplanGeo.ConvertTo2D(polygon)

        build_ele = self.build_ele
        room_prop = AllplanArchEle.RoomProperties()

        room_prop.StoreyCode      = build_ele.StoreyCode.value
        room_prop.Name            = build_ele.Name.value
        room_prop.Function        = build_ele.Function.value
        room_prop.Factor          = build_ele.Factor.value
        room_prop.PlaneReferences = build_ele.PlaneReferences.value

        for index, text in enumerate(build_ele.Texts.value):
            room_prop.SetText(text, index + 1)

        ElementPropertiesAttributeUtil.set_attributes(self.document,
                                                      room_prop, build_ele.UserAttributes.value)

        room_ele = AllplanArchEle.RoomElement(room_prop, room_polygon)

        room_ele.CommonProperties = build_ele.CommonProp.value

        return room_ele


    def create_preview_elements(self, polygon: AllplanGeo.Polygon3D) -> list:
        """Create the list of slab elements to preview based on 3d polygon

        Args:
            polygon: input 3d polygon

        Returns:
            list of elements to preview - one slab element
        """

        if polygon.Count() <= 2 or not polygon.IsValid():       # pylint: disable=magic-value-comparison
            return []

        return [self.create_room(polygon)]


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if self.script_object_interactor is not None:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS
