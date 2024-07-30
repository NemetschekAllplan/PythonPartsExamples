""" Script for MinValue and MaxValue
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
    from __BuildingElementStubFiles.MinMaxValueBuildingElement import MinMaxValueBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load MinMaxValue.py')


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
                               r"Examples\PythonParts\PaletteExamples\OptionalTags\MinMaxValue.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return MinMaxValue(build_ele, script_object_data)


class MinMaxValue(BaseScriptObject):
    """ Definition of class AnyValueByType
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


        #--------------------- create the geometry

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.NamedTupleSizes.value.Length, build_ele.NamedTupleSizes.value.Width,
                                                        build_ele.NamedTupleSizes.value.Height)

        polyhed2 = AllplanGeo.Move(AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.TupleSizes.value),
                                   AllplanGeo.Vector3D(build_ele.NamedTupleSizes.value.Length * 1.5, 0, 0))

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(polyhed1)
        model_ele_list.append_geometry_3d(polyhed2)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
