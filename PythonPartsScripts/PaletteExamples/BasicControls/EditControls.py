""" Script for EditControls
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.EditControlsBuildingElement \
        import EditControlsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load EditControls.py')


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
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\PaletteExamples\BasicControls\EditControls.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = EditControls(doc)

    return element.create(build_ele)


class EditControls():
    """ Definition of class EditControls
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class EditControls

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        model_ele_list = ModelEleList(build_ele.CommonProp.value)


        #----------------- create the lines

        angle_cos = math.cos(math.radians(build_ele.Angle.value))
        angle_sin = math.sin(math.radians(build_ele.Angle.value))

        y_cube = 0.

        for length, coord in zip(build_ele.LineLength.value, build_ele.LineCoords.value):
            y_end = coord[1] + length * angle_sin

            model_ele_list.append_geometry_2d(AllplanGeo.Line2D(coord[0], coord[1], coord[0] + length * angle_cos, y_end))

            y_cube = max(y_cube, y_end)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
