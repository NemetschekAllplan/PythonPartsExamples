""" Example Script for SurfaceDefinition
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SurfaceDefinitionBuildingElement \
        import SurfaceDefinitionBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load SurfaceDefinition.py')

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
    """ Creation of library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\Resources\SurfaceDefinition.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = SurfaceDefinitionExample(doc)

    return element.create(build_ele)


def on_control_event(build_ele: BuildingElement,
                     event_id : int,
                     doc      : AllplanEleAdapter.DocumentAdapter) -> bool:
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        event_id:  event id of the clicked button control
        doc:       document of the Allplan drawing files

    Returns:
        palette update state
    """

    #--------------------- create the surface

    if event_id == build_ele.CREATE_SURFACE:
        surface_def = AllplanBasisEle.SurfaceDefinition.Create()

        surface_def.RelativeName        = build_ele.RelativePathAndName.value
        surface_def.DiffuseColor        = AllplanBasisEle.ARGB(build_ele.DiffuseColor.value)
        surface_def.DiffuseReflectivity = build_ele.DiffuseReflectivity.value

        surface_def.Transparency        = build_ele.Transparency.value
        surface_def.Refraction          = build_ele.Refraction.value

        surface_def.Emission = build_ele.Emission.value

        surface_def.NormalMapStatus     = build_ele.NormalMapStatus.value
        surface_def.BumpAmplitude       = build_ele.BumpAmplitude.value
        surface_def.ParallaxOffset      = build_ele.ParallaxOffset.value
        surface_def.ParallaxSamples     = build_ele.ParallaxSamples.value

        surface_def.Roughness           = build_ele.Roughness.value

        surface_def.Reflection      = build_ele.Reflection.value
        surface_def.MultiToneFactor = build_ele.MultiToneFactor.value


        #----------------- add the bitmaps

        bitmaps: Dict[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID, AllplanBasisEle.BitmapDefinition] = {}

        if build_ele.DiffuseColorBitmap.value:
            bitmap_def = AllplanBasisEle.BitmapDefinition.Create(build_ele.DiffuseColorBitmap.value)

            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eDIFFUSE_SPRING] = bitmap_def
            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eDIFFUSE_SUMMER] = bitmap_def
            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eDIFFUSE_AUTUMN] = bitmap_def
            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eDIFFUSE_WINTER] = bitmap_def

        if build_ele.BumpBitmap.value:
            bitmap_def = AllplanBasisEle.BitmapDefinition.Create(build_ele.BumpBitmap.value)

            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eBUMP] = bitmap_def

        if build_ele.RoughnessBitmap.value:
            bitmap_def = AllplanBasisEle.BitmapDefinition.Create(build_ele.RoughnessBitmap.value)

            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eROUGHNESS] = bitmap_def

        if build_ele.ReflectionBitmap.value:
            bitmap_def = AllplanBasisEle.BitmapDefinition.Create(build_ele.ReflectionBitmap.value)

            bitmaps[AllplanBasisEle.SurfaceDefinition.eSurfaceTextureID.eREFLECTION] = bitmap_def


        #----------------- create the surface in Allplan

        surface_path = AllplanSettings.AllplanPaths.GetCurPrjPath() + "design"

        build_ele.Surface.value = AllplanBaseEle.DocumentResourceService.CreateSurface(doc, surface_path, surface_def.RelativeName,
                                                                                       surface_def, False, bitmaps)

        surface_def.Save(surface_path, bitmaps)

        return True


    #--------------------- delete the bitmaps

    if event_id == build_ele.DELETE_DIFFUSE_BITMAP:
        build_ele.DiffuseColorBitmap.value = ""

    elif event_id == build_ele.DELETE_BUMP_BITMAP:
        build_ele.BumpBitmap.value = ""

    elif event_id == build_ele.DELETE_ROUGHNESS_BITMAP:
        build_ele.RoughnessBitmap.value = ""

    else:
        build_ele.ReflectionBitmap.value = ""

    return True


class SurfaceDefinitionExample():
    """ Definition of class SurfaceDefinitionExample
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class SurfaceDefinitionExample

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

        #----------------- create the object

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value,
                                                       build_ele.Width.value,
                                                       build_ele.Height.value)

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        texture_def = AllplanBasisEle.TextureDefinition(build_ele.Surface.value)

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisEle.ModelElement3D(com_prop, texture_def, polyhed))

        return CreateElementResult(pyp_util.create_pythonpart(build_ele), multi_placement = True)
