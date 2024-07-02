""" Script for IntersectBRepList
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IntersectBRepListBuildingElement \
        import IntersectBRepListBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load IntersectBRepList.py')


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

    element = IntersectBRepList(doc)

    return element.create(build_ele)


class IntersectBRepList():
    """ Definition of class IntersectBRepList
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class IntersectBRepList

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


        #----------------- create the cuboid as brep

        sizes = build_ele.CuboidSizes.value

        brep_cuboid = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(-sizes.X / 2, -sizes.Y / 2, 0)),
                                                     *sizes.Values())


        #----------------- create the cylinder as brep

        sizes = build_ele.CylinderSizes.value

        place_pnt = build_ele.PlacementPoint.value

        axis_mat = AllplanGeo.Plane3D(place_pnt, build_ele.AxisVector.value).GetTransformationMatrix()

        brep_cylinder = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(place_pnt, axis_mat.GetVectorX(),
                                                                                    axis_mat.GetVectorZ()),
                                                         sizes.X, sizes.Y)

        brep_cylinders = AllplanGeo.BRep3DList()

        brep_cylinders.append(brep_cylinder)
        brep_cylinders.append(AllplanGeo.Move(brep_cylinder, AllplanGeo.Vector3D(-2 * place_pnt.X, 0, 0)))
        brep_cylinders.append(AllplanGeo.Move(brep_cylinder, AllplanGeo.Vector3D(-place_pnt.X, place_pnt.X, 0)))
        brep_cylinders.append(AllplanGeo.Move(brep_cylinder, AllplanGeo.Vector3D(-place_pnt.X, -place_pnt.X, 0)))


        #----------------- create the intersection

        intersecting, intersect_brep = AllplanGeo.MakeIntersection(brep_cuboid, brep_cylinders)

        if intersecting == AllplanGeo.eOK and intersect_brep.IsValid():
            model_ele_list.append_geometry_3d(intersect_brep)


        #----------------- add the cuboid and cylinders only for the preview

        preview_ele_list.set_stroke(2)

        preview_ele_list.set_color(build_ele.BRepColor.value)
        preview_ele_list.append_geometry_3d(brep_cylinders)

        preview_ele_list.set_color(build_ele.CuboidColor.value)
        preview_ele_list.append_geometry_3d(brep_cuboid)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),
                                   preview_elements  = preview_ele_list)
