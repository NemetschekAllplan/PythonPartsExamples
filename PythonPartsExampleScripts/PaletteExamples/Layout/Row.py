""" Example script for Row
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.RowBuildingElement import RowBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Row.py')


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
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\PaletteExamples\Layout\Row.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Row(build_ele, script_object_data)


class Row(BaseScriptObject):
    """ Definition of class Row
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele


        #------------------ Define the cube polyhedrons

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length1.value, build_ele.Width1.value, build_ele.Height1.value)
        polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length2.value, build_ele.Width2.value, build_ele.Height2.value)
        polyhed3 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length3.value, build_ele.Width3.value, build_ele.Height3.value)


        #------------------ Translation of second cube in WCS

        translate_matrix = AllplanGeo.Matrix3D()
        translate_matrix.Translate(AllplanGeo.Vector3D(build_ele.Length1.value + 1000, 0, 0))

        polyhed2 = AllplanGeo.Transform(polyhed2, translate_matrix)

        translate_matrix.Translate(AllplanGeo.Vector3D(build_ele.Length2.value + 1000, 0, 0))

        polyhed3 = AllplanGeo.Transform(polyhed3, translate_matrix)


        #------------------ Append cubes as new Allplan elements

        model_ele_list = ModelEleList()

        model_ele_list.set_color(build_ele.Color1.value)
        model_ele_list.append_geometry_3d(polyhed1)

        model_ele_list.set_color(build_ele.Color2.value)
        model_ele_list.append_geometry_3d(polyhed2)

        model_ele_list.set_color(build_ele.Color3.value)
        model_ele_list.append_geometry_3d(polyhed3)

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
