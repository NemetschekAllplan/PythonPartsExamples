""" Script for SymbolLibraryElement
"""

# pylint: disable=no-self-use

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SymbolLibraryElementBuildingElement \
        import SymbolLibraryElementBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load SymbolLibraryElement.py')


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


def create_preview(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    element = SymbolLibraryElement(doc)

    return element.create(build_ele)


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = SymbolLibraryElement(doc)

    return element.create(build_ele)


class SymbolLibraryElement():
    """ Definition of class SymbolLibraryElement
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class SymbolLibraryElement

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
            created element result
        """


        #----------------- create the library element for the symbol

        placement_mat = RotationUtil(build_ele.SymbolRotationAngleX.value,
                                     build_ele.SymbolRotationAngleY.value,
                                     build_ele.SymbolRotationAngleZ.value).get_rotation_matrix()

        placement_mat.SetTranslation(AllplanGeo.Vector3D(build_ele.SymbolPlacement.value))

        lib_ele_prop = AllplanBasisEle.LibraryElementProperties(build_ele.SymbolName.value,
                                                                AllplanBasisEle.LibraryElementType.eSymbol, placement_mat)

        lib_ele = AllplanBasisEle.LibraryElement(lib_ele_prop)

        pyp_util = PythonPartUtil()

        pyp_util.add_library_elements(lib_ele)


        #----------------- create a help construction element as PythonPart selector from the min/max box

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        com_prop.HelpConstruction = True

        min_max = lib_ele.GetMinMax(self.document)

        if min_max.GetSizeZ() < 1.:
            polygon = AllplanGeo.Polygon2D.CreateRectangle(AllplanGeo.Point2D(min_max.GetMin()),
                                                           AllplanGeo.Point2D(min_max.GetMax()))

            pyp_util.add_pythonpart_view_2d3d(
                AllplanBasisEle.ModelElement2D(com_prop, AllplanGeo.Transform(polygon, placement_mat.ReduceZDimension())))
        else:
            polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(min_max)

            pyp_util.add_pythonpart_view_2d3d(AllplanBasisEle.ModelElement3D(com_prop, polyhed))


        #----------------- return the result

        return CreateElementResult(pyp_util.create_pythonpart(build_ele), multi_placement = True)
