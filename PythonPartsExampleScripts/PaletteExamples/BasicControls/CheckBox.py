""" Example script for CheckBox
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CheckBoxBuildingElement import CheckBoxBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load CheckBox.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """


    element = CheckBox(doc)

    return element.create(build_ele)


class CheckBox():
    """ Definition of class CheckBox
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class CheckBox

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            create element result
        """

        return CreateElementResult(self.create_geometry(build_ele))


    def create_geometry(self,                                           # pylint: disable=no-self-use
                        build_ele: BuildingElement) -> list[Any]:
        """ Create the element geometries

        Args:
            build_ele: building element with the parameter properties

        Returns:
            list with the created elements
        """


        #------------------ Define the cube polyhedron

        length = 1000

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        if build_ele.DrawCube.value:
            model_ele_list.append_geometry_3d(polyhed)


        #----------------- create the cubes from the 1-dim list

        distance   = length * 1.2
        y_placment = distance + length / 2

        for draw_cube in build_ele.DrawCubeList.value:
            if draw_cube:
                model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(0, y_placment, 0)))

            y_placment += distance


        #----------------- create the cubes from the 2-dim list

        y_placment += length / 2

        for draw_cube_row in build_ele.DrawCubeList2Dim.value:
            x_placement = 0

            for draw_cube_col in draw_cube_row:
                if draw_cube_col:
                    model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_placement, y_placment, 0)))

                x_placement += distance

            y_placment += distance



        #------------------ Append for creation as new Allplan elements

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return pyp_util.create_pythonpart(build_ele)
