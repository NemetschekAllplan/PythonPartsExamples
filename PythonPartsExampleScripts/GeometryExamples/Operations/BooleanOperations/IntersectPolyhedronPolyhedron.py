""" Script for IntersectPolyhedronPolyhedron
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IntersectPolyhedronPolyhedronBuildingElement \
        import IntersectPolyhedronPolyhedronBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load IntersectPolyhedronPolyhedron.py')


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

    return create_element(build_ele, doc)


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = IntersectPolyhedronPolyhedron(doc)

    return element.create(build_ele)


class IntersectPolyhedronPolyhedron():
    """ Definition of class IntersectPolyhedronPolyhedron
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class IntersectPolyhedronPolyhedron

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

        model_ele_list   = ModelEleList(build_ele.CommonProp.value)
        preview_ele_list = ModelEleList(build_ele.CommonProp.value)


        #----------------- create the polyhedrons

        sizes = build_ele.PolyhedSizes1.value

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(sizes.X, sizes.Y, sizes.Z)

        polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.PlacementPoint.value,
                                                        build_ele.PlacementPoint.value + build_ele.PolyhedSizes2.value)

        #----------------- create the intersection

        intersecting, intersect_polyhed = AllplanGeo.Intersect(polyhed1, polyhed2)

        if intersecting:
            model_ele_list.append_geometry_3d(intersect_polyhed)


        #----------------- add the polyhedron only for the preview

        preview_ele_list.set_stroke(2)

        preview_ele_list.set_color(build_ele.PolyhedColor1.value)
        preview_ele_list.append_geometry_3d(polyhed1)

        preview_ele_list.set_color(build_ele.PolyhedColor2.value)
        preview_ele_list.append_geometry_3d(polyhed2)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),
                                   preview_elements  = preview_ele_list)
