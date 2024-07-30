""" Script for IntersectBRepPolyhedron
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IntersectBRepPolyhedronBuildingElement \
        import IntersectBRepPolyhedronBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load IntersectBRepPolyhedron.py')


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

    element = IntersectBRepPolyhedron(doc)

    return element.create(build_ele)


class IntersectBRepPolyhedron():
    """ Definition of class IntersectBRepPolyhedron
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class IntersectBRepPolyhedron

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


        #----------------- create the cylinder as brep

        sizes = build_ele.CylinderSizes.value

        place_pnt = build_ele.PlacementPoint.value

        axis_mat = AllplanGeo.Plane3D(place_pnt, build_ele.AxisVector.value).GetTransformationMatrix()

        brep = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(place_pnt, axis_mat.GetVectorX(), axis_mat.GetVectorZ()),
                                                sizes.X, sizes.Y)


        #----------------- create the polyhedron

        sizes = build_ele.PolyhedSizes.value

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.PolyhedSizes.value.Values())


        #----------------- create the intersection

        intersecting, intersect_brep = AllplanGeo.Intersect(brep, polyhed)

        if intersecting == AllplanGeo.eOK and intersect_brep.IsValid():
            model_ele_list.append_geometry_3d(intersect_brep)


        #----------------- add the polyhedron and brep only for the preview

        preview_ele_list.set_stroke(2)

        preview_ele_list.set_color(build_ele.BRepColor.value)
        preview_ele_list.append_geometry_3d(brep)

        preview_ele_list.set_color(build_ele.PolyhedColor.value)
        preview_ele_list.append_geometry_3d(polyhed)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),
                                   preview_elements  = preview_ele_list)
