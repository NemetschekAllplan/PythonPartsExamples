""" Example script for AxisPlacement3D
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.AxisPlacement3DBuildingElement \
        import AxisPlacement3DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load AxisPlacement3D.py')


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
                               r"Examples\PythonParts\PaletteExamples\GeometryElements\AxisPlacement3D.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return AxisPlacement3D(build_ele, coord_input)


class AxisPlacement3D(BaseScriptObject):
    """ Definition of class AxisPlacement3D
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

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        model_ele_list.append_geometry_3d(self.create_circle(build_ele.AxisPlacement1.value))
        model_ele_list.append_geometry_3d(self.create_circle(build_ele.AxisPlacement2.value))

        for axis_placement in build_ele.AxisPlacementList.value:
            model_ele_list.append_geometry_3d(self.create_circle(axis_placement))

        model_ele_list.append_geometry_3d(self.create_circle(build_ele.AxisPlacement3.value))
        model_ele_list.append_geometry_3d(self.create_circle(build_ele.AxisPlacement4.value))


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    def create_circle(self,
                      axis_placement: AllplanGeo.AxisPlacement3D) -> AllplanGeo.Arc3D:
        """ create the circle

        Args:
            axis_placement: axis placement

        Returns:
            created circle
        """

        return AllplanGeo.Arc3D(axis_placement, self.build_ele.CircleRadius.value, self.build_ele.CircleRadius.value,
                                math.pi, math.pi * 2)
