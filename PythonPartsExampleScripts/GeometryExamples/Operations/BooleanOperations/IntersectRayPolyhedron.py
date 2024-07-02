""" Script for IntersectRayPolyhedron
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IntersectRayPolyhedronBuildingElement import \
        IntersectRayPolyhedronBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load IntersectRayPolyhedron.py')


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

    element = IntersectRayPolyhedron(doc)

    return element.create(build_ele)


class IntersectRayPolyhedron():
    """ Definition of class IntersectRayPolyhedron
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class IntersectRayPolyhedron

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

        preview_ele_list.set_stroke(2)


        #----------------- create the polyhedron

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.PolyhedSizes.value.Values())

        model_ele_list.append_geometry_3d(polyhed)


        #----------------- get the intersection point for the first ray

        line     = AllplanGeo.Line3D(build_ele.RayLine1.value)
        end_line = AllplanGeo.Line3D(line)

        error, result = AllplanGeo.IntersectRayPolyhedron(line.StartPoint, line.GetVector(), polyhed,
                                                          AllplanGeo.IntersectRayPolyhedronFlag.names[build_ele.IntersectFlag1.value])

        model_ele_list.set_color(build_ele.RayLine1Color.value)


        #----------------- add the part(s) of the ray

        if not error and result.RetCode:
            line.EndPoint = result.IntersectionPoint

            model_ele_list.append_geometry_3d(line)

            end_line.StartPoint = result.IntersectionPoint

            preview_ele_list.append_geometry_3d(end_line)

        else:
            model_ele_list.append_geometry_3d(line)


        #----------------- get the intersection point for the second ray

        line     = AllplanGeo.Line3D(build_ele.RayLine2.value)
        end_line = AllplanGeo.Line3D(line)

        face_list = AllplanUtil.VecIntList([build_ele.FaceIndex.value])

        error, result = AllplanGeo.IntersectRayPolyhedron(line.StartPoint, line.GetVector(), polyhed,
                                                          AllplanGeo.IntersectRayPolyhedronFlag.ePositiveOnly,
                                                          face_list)

        model_ele_list.set_color(build_ele.RayLine2Color.value)


        #----------------- add the part(s) of the ray

        if not error and result.RetCode:
            line.EndPoint = result.IntersectionPoint

            model_ele_list.append_geometry_3d(line)

            end_line.StartPoint = result.IntersectionPoint

            preview_ele_list.append_geometry_3d(end_line)

        else:
            model_ele_list.append_geometry_3d(line)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),
                                   preview_elements  = preview_ele_list)
