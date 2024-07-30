""" Example script for material button
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.MaterialButtonsBuildingElement \
        import ButtonBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load MaterialButtons.py')


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
                               r"Examples\PythonParts\PaletteExamples\ButtonControls\MaterialButtons.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return MaterialButtons(build_ele, script_object_data)


class MaterialButtons(BaseScriptObject):
    """ Definition of class MaterialButtons
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


        #----------------- Extract palette parameter values

        length   = build_ele.Length1.value
        surface1 = build_ele.Surface1.value
        surface2 = build_ele.Surface2.value
        surface3 = build_ele.Surface3.value


        #------------------ Define the cube polyhedrons

        solid1 = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)
        solid2 = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(), length, length, length)

        solid3 = AllplanGeo.Polygon3D()
        solid3 += AllplanGeo.Point3D(0,0,1)
        solid3 += AllplanGeo.Point3D(length,0,1)
        solid3 += AllplanGeo.Point3D(length,length,1)
        solid3 += AllplanGeo.Point3D(0,length,1)
        solid3 += AllplanGeo.Point3D(0,0,1)


        #------------------ Translation of second cube in WCS

        translate_matrix = AllplanGeo.Matrix3D()
        translate_matrix.Translate(AllplanGeo.Vector3D(length + 1000, 0, 0))

        solid2 = AllplanGeo.Transform(solid2, translate_matrix)

        translate_matrix.Translate(AllplanGeo.Vector3D(length + 1000, 0, 0))

        solid3 = AllplanGeo.Transform(solid3, translate_matrix)


        #------------------ Define texture definition

        texturedef1 = AllplanBasisEle.TextureDefinition(surface1)
        texturedef2 = AllplanBasisEle.TextureDefinition(surface2)
        texturedef3 = AllplanBasisEle.TextureDefinition(surface3)


        #------------------ Append for creation as new Allplan elements

        model_ele_list = ModelEleList()
        model_ele_list.append_geometry_3d_with_texture(solid1, texturedef1)
        model_ele_list.append_geometry_3d_with_texture(solid2, texturedef2)
        model_ele_list.append_geometry_3d_with_texture(solid3, texturedef3)

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
