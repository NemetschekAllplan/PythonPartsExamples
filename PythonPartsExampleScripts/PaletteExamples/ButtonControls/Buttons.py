""" Example script for buttons
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Palette as AllplanPalette

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ButtonsBuildingElement \
        import ButtonBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Buttons.py')


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
ö
    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\PaletteExamples\ButtonControls\Buttons.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return Buttons(build_ele, coord_input)


class Buttons(BaseScriptObject):
    """ Definition of class Buttons
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele


        #------------------ Define the cube polyhedron

        length = build_ele.Length.value

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(polyhed)


        #------------------ Append cube as new Allplan elements

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    def on_control_event(self,
                         event_id: int) -> bool:
        """ On control event

        Args:
            event_id: event id of the clicked button control

        Returns:
            event handled state
        """

        build_ele = self.build_ele

        print ("Buttons.py (on_control_event called, eventId: ", event_id, ")")

        match event_id:
            case build_ele.SET_LENGTH_1000:
                build_ele.Length.value = 100.0

            case build_ele.SET_LENGTH_2000:
                build_ele.Length.value = 2000.0

            case build_ele.SET_LENGTH_3000:
                build_ele.Length.value = 3000.0

            case build_ele.CENTER_OF_GRAVITY:
                build_ele.RefPointId.value = 0

            case build_ele.CENTER_OF_GRAVITY_SELECTED:
                build_ele.RefPointId.value = AllplanPalette.RefPointPosition.eCenterCenter

        self.execute()

        return True
