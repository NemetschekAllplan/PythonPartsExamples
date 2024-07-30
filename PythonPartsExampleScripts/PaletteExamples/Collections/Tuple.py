""" Example script for include controls
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
    from __BuildingElementStubFiles.TupleBuildingElement import TupleBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Tuple.py')


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
                               r"Examples\PythonParts\PaletteExamples\Collections\Tuple.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Tuple(build_ele, script_object_data)


class Tuple(BaseScriptObject):
    """ Definition of class Tuple
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


        #----------------- elements from the single tuples

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.MultiRowTuple.value))

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.OneRowTuple.value)

        x_ref = build_ele.MultiRowTuple.value[0] + 1000

        model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_ref, 0, 0)))

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.FullOneRowTuple.value)

        x_ref += build_ele.OneRowTuple.value[0] + 1000

        model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_ref, 0, 0)))


        #----------------- objects from the tuple lists

        y_ref = max([build_ele.MultiRowTuple.value[1], build_ele.OneRowTuple.value[1], build_ele.FullOneRowTuple.value[1]]) + 1000

        y_ref += self.create_polyhedrons(build_ele.ListMultiRowTuple.value, model_ele_list, y_ref) + 1000
        y_ref += self.create_polyhedrons(build_ele.ListOneRowTuple.value, model_ele_list, y_ref) + 1000

        self.create_polyhedrons_by_check(build_ele.ListFullOneRowTuple.value, model_ele_list, y_ref)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    @staticmethod
    def create_polyhedrons(size_list     : list[tuple[float, float, float]],
                           model_ele_list: ModelEleList,
                           y_ref         : float) -> float:
        """ create the polyhedrons

        Args:
            size_list:      size list
            model_ele_list: model element list
            y_ref:          y reference point

        Returns:
            max width
        """

        max_width = 0
        x_ref     = 0

        for sizes in size_list:
            polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*sizes)

            model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_ref, y_ref, 0)))

            x_ref += sizes[0] + 1000

            max_width = max(max_width, sizes[1])

        return max_width


    @staticmethod
    def create_polyhedrons_by_check(size_list     : list[tuple[AllplanGeo.Vector3D, bool]],
                                    model_ele_list: ModelEleList,
                                    y_ref         : float):
        """ create the polyhedrons

        Args:
            size_list:      size list
            model_ele_list: model element list
            y_ref:          y reference point
        """

        x_ref = 0

        for sizes in size_list:
            if sizes[1]:
                polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*sizes[0].GetCoords())

                model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_ref, y_ref, 0)))

            x_ref += sizes[0].X + 1000
