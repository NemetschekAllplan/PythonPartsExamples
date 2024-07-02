""" Script for CommonProperties
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CommonPropertiesUtil import CommonPropertiesUtil
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CommonPropertiesBuildingElement \
        import CommonPropertiesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load CommonProperties.py')


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
                               r"Examples\PythonParts\PaletteExamples\Properties\CommonProperties.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = CommonProperties(doc)

    return element.create(build_ele)


class CommonProperties():
    """ Definition of class CommonProperties
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class CommonProperties

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

        #----------------- Assign the single parameter

        model_ele_list = ModelEleList()

        length = build_ele.Length.value

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        if not build_ele.UseGlobalProperties.value:
            com_prop.HelpConstruction = build_ele.UseHelpConstruction.value

            CommonPropertiesUtil.assing_by_layer_check(com_prop,
                                                       build_ele.Color, build_ele.ColorByLayer,
                                                       build_ele.Pen, build_ele.PenByLayer,
                                                       build_ele.Stroke, build_ele.StrokeByLayer,
                                                       build_ele.Layer)

        model_ele_list.append_geometry_3d(polyhed1, com_prop)


        #----------------- use the CommonProperties parameter

        polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        polyhed2 = AllplanGeo.Move(polyhed2, AllplanGeo.Vector3D(length * 1.5, 0, 0))

        model_ele_list.append_geometry_3d(polyhed2, build_ele.CommonProp.value)

        polyhed3 = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        polyhed3 = AllplanGeo.Move(polyhed3, AllplanGeo.Vector3D(length * 3, 0, 0))

        model_ele_list.append_geometry_3d(polyhed3, build_ele.CommonPropCond.value)


        #----------------- from the list

        x_start = 0

        for com_prop in build_ele.CommonPropList.value:
            polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

            polyhed = AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_start, length * 2, 0))

            x_start += length * 1.5

            model_ele_list.append_geometry_3d(polyhed, com_prop)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
