""" Script for MultiIndex
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.MultiIndexBuildingElement \
        import MultiIndexBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load MultiIndex.py')


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
                               r"Examples\PythonParts\PaletteExamples\BasicControls\MultiIndex.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = MultiIndex(doc)

    return element.create(build_ele)


class MultiIndex():
    """ Definition of class MultiIndex
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class MultiIndex

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


        #----------------- create the cubes

        x_cube = 0.
        y_cube = 0

        max_y = 0.

        for size, height in zip(build_ele.CubeSize.value, build_ele.CubeHeight.value):
            model_ele_list.append_geometry_3d(AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(x_cube, y_cube, 0),
                                                                                   AllplanGeo.Point3D(x_cube + size, y_cube + size, height)))

            x_cube += size + 500

            max_y = max(max_y, size)


        #----------------- create the spheres

        x_sphere = 0
        y_sphere = y_cube + max_y + 2000

        for radius in build_ele.SphereRadius.value:
            x_sphere += radius

            model_ele_list.append_geometry_3d(AllplanGeo.BRep3D.CreateSphere(
                AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x_sphere, y_sphere, 0)), radius))

            x_sphere += radius + 500


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
