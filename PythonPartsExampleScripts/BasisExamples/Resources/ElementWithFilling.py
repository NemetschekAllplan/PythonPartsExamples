""" Example Script showing the creation of a 3D object with a hatching/pattern/filling
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from SectionFill import SectionFill
from TypeCollections.ModelEleList import ModelEleList
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ElementWithHatchingBuildingElement import \
        ElementWithHatchingBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

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
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of library preview

    Args:
        build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """
    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_element(build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created PythonPart with a surface element
    """

    # create the 3D object
    cube = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value,
                                                build_ele.Width.value,
                                                build_ele.Height.value)
    model_element_list = ModelEleList()
    model_element_list.append_geometry_3d(cube)

    # apply the surface element properties
    section_filling = SectionFill.from_surface_ele_properties(build_ele.SurfaceElementProperties.value)
    section_filling.apply_on_model_elements(model_element_list)

    # create as a 3D object
    if not build_ele.CreateAsPythonPart.value:
        return CreateElementResult(model_element_list)

    # create as a PythonPart
    pyp_util = PythonPartUtil()
    pyp_util.add_pythonpart_view_2d3d(model_element_list)

    return CreateElementResult(pyp_util.create_pythonpart(build_ele))
