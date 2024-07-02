""" Example script for RadioButtons
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElementTupleUtil import BuildingElementTupleUtil
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.RadioButtonsBuildingElement import RadioButtonsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load RadioButtons.py')

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


    element = RadioButtons(doc)

    return element.create(build_ele)


class RadioButtons():
    """ Definition of class RadioButtons
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class RadioButtons

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

        #----------------- fill the file list

        if not build_ele.ImportFileSelection.value:
            if (file_list_tuple := BuildingElementTupleUtil.create_namedtuple_from_definition(build_ele.ImportFileSelection)) is not None:
                build_ele.ImportFileSelection.value = [  \
                    file_list_tuple(AllplanEleAdapter.DocumentNameService.GetDocumentNameByFileNumber(number, True, False, "-"), number) \
                    for index, (number, _) in enumerate(AllplanBaseEle.DrawingFileService().GetFileState())]

            build_ele.ImportFileNumber.value = AllplanBaseEle.DrawingFileService.GetActiveFileNumber()


        #----------------- create the element

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

        length = build_ele.Length.value

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        if build_ele.LengthRadioGroup.value == 0:
            polyhed = AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(build_ele.DistanceLeft.value, 0, 0))
        else:
            polyhed = AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(-build_ele.DistanceRight.value - build_ele.Length.value, 0, 0))

        model_ele_list = ModelEleList()
        model_ele_list.set_color(build_ele.RadioGroup.value)
        model_ele_list.append_geometry_3d(polyhed)


        #----------------- create the lines with the different colors for the one dimensional lists

        distance = length if build_ele.LengthRadioGroup.value == 0 else -length

        x_start     = build_ele.DistanceLeft.value if build_ele.LengthRadioGroup.value == 0 else -build_ele.DistanceRight.value
        y_start     = length * 2
        x_start_row = x_start + distance
        y_end       = length * 3

        for color, row_color in zip(build_ele.RadioGroupColorList.value, build_ele.RadioGroupRowColorList.value):
            model_ele_list.set_color(color)

            model_ele_list.append_geometry_2d(AllplanGeo.Line2D(x_start, y_start, x_start, y_end))

            model_ele_list.set_color(row_color)

            model_ele_list.append_geometry_2d(AllplanGeo.Line2D(x_start_row, y_start, x_start_row, y_end))

            x_start     += distance / 10
            x_start_row += distance / 10


        #----------------- create the lines with the different colors for the two dimensional lists

        y_start = length * 4
        y_end   = length * 5

        distance = length if build_ele.LengthRadioGroup.value == 0 else -length

        for column_colors, column_row_colors in zip(build_ele.RadioGroupColorList2Dim.value, build_ele.RadioGroupRowColorList2Dim.value):
            x_start     = build_ele.DistanceLeft.value if build_ele.LengthRadioGroup.value == 0 else -build_ele.DistanceRight.value
            x_start_row = x_start + distance

            for color, row_color in zip(column_colors, column_row_colors):
                model_ele_list.set_color(color)

                model_ele_list.append_geometry_2d(AllplanGeo.Line2D(x_start, y_start, x_start, y_end))

                model_ele_list.set_color(row_color)

                model_ele_list.append_geometry_2d(AllplanGeo.Line2D(x_start_row, y_start, x_start_row, y_end))

                x_start     += distance / 10
                x_start_row += distance / 10

            y_start += length * 1.5
            y_end    = y_start + length


        #------------------ Append for creation as new Allplan elements

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return pyp_util.create_pythonpart(build_ele)
