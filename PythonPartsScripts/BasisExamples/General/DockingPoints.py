""" Example script for DockingPoints
"""

from __future__ import annotations

from typing import List, Any, Tuple, TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import DockingPointUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.DockingPointsBuildingElement import DockingPointsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load DockingPoints.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = DockingPoints(doc)

    return element.create(build_ele)


def create_docking_points(build_ele: BuildingElement,
                          doc      : AllplanElementAdapter.DocumentAdapter) -> Tuple[List[Tuple[str, AllplanGeo.Point3D]],
                                                                                     List[Tuple[str, AllplanGeo.Point3D]],
                                                                                     List[Tuple[str, AllplanGeo.Point3D]]]:
    """ Creation of the docking points

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created docking points
    """

    element = DockingPoints(doc)

    return element.create_docking_points(build_ele)


class DockingPoints():
    """ Definition of class DockingPoints
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """ Initialization

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc
        self.com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.create_fix_elements(build_ele) +
                                          self.create_multiple_elements(build_ele) +
                                          self.create_dynamic_elements(build_ele))

        model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(model_ele_list)


    def create_fix_elements(self,
                            build_ele: BuildingElement) -> List[Any]:
        """ Create the fix elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created elements
        """

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.PolyhedronLength.value,
                                                       build_ele.PolyhedronWidth.value,
                                                       build_ele.PolyhedronHeight.value)

        cylinder = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(build_ele.PolyhedronLength.value * 2,
                                                                                                  build_ele.CylinderRadius.value,
                                                                                                  0)),
                                                    build_ele.CylinderRadius.value,
                                                    build_ele.CylinderHeight.value)

        polyhed_ele  = AllplanBasisElements.ModelElement3D(self.com_prop, polyhed)
        cylinder_ele = AllplanBasisElements.ModelElement3D(self.com_prop, cylinder)

        polyhed_ele.SetDockingPointsKey("Polyhed")
        cylinder_ele.SetDockingPointsKey("Cylinder")

        return [polyhed_ele, cylinder_ele]


    def create_multiple_elements(self,
                                 build_ele: BuildingElement) -> List[Any]:
        """ Create the multiple elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created elements
        """

        multi_polyheds : List[AllplanBasisElements.AllplanElement] = []


        #----------------- set the x distance between the elements and the y distance from reference point of the PYP

        x_distance =  build_ele.MultiPolyhedronLength.value * 2
        y_distance = -build_ele.MultiPolyhedronWidth.value * 3

        multi_count = build_ele.Count.value


        #----------------- create the multiple elements

        for poly_index in range(multi_count):
            multi_polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.MultiPolyhedronLength.value,
                                                                 build_ele.MultiPolyhedronWidth.value,
                                                                 build_ele.MultiPolyhedronHeight.value)

            multi_polyhed = AllplanGeo.Move(multi_polyhed, AllplanGeo.Vector3D(x_distance * poly_index, y_distance, 0))

            multi_polyheds.append(AllplanBasisElements.ModelElement3D(self.com_prop, multi_polyhed))

            left_count = int((multi_count) / 2)

            poly_index_key = "L" + str(poly_index) if poly_index < left_count else "R" + str(multi_count - poly_index - 1)

            multi_polyheds[-1].SetDockingPointsKey(poly_index_key)

        return multi_polyheds


    def create_dynamic_elements(self,
                                build_ele: BuildingElement) -> List[Any]:
        """ Create the dynamic element

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created elements
        """

        ref_pnt = AllplanGeo.Point3D(0, -build_ele.MultiPolyhedronWidth.value * 3 - build_ele.DynamicWidth.value * 3, 0)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                       ref_pnt + AllplanGeo.Point3D(build_ele.DynamicLength.value,
                                                                                    build_ele.DynamicWidth.value,
                                                                                    build_ele.DynamicHeight.value))

        if build_ele.RecessLeft.value:
            recess = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                          ref_pnt + AllplanGeo.Point3D(build_ele.RecessLength.value,
                                                                                       build_ele.RecessWidth.value,
                                                                                       build_ele.DynamicHeight.value))

            _, polyhed = AllplanGeo.MakeSubtraction(polyhed, recess)

        if build_ele.RecessRight.value:
            ref_pnt += AllplanGeo.Point3D(build_ele.DynamicLength.value - build_ele.RecessLength.value, 0, 0)

            recess = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                          ref_pnt + AllplanGeo.Point3D(build_ele.RecessLength.value,
                                                                                       build_ele.RecessWidth.value,
                                                                                       build_ele.DynamicHeight.value))

            _, polyhed = AllplanGeo.MakeSubtraction(polyhed, recess)

        return [AllplanBasisElements.ModelElement3D(self.com_prop, polyhed)]


    @staticmethod
    def create_docking_points(build_ele: BuildingElement) -> Tuple[List[Tuple[str, AllplanGeo.Point3D]],
                                                                   List[Tuple[str, AllplanGeo.Point3D]],
                                                                   List[Tuple[str, AllplanGeo.Point3D]]]:
        """ Create the docking points

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created docking points
        """

        ref_pnt = AllplanGeo.Point3D(0, -build_ele.MultiPolyhedronWidth.value * 3 - build_ele.DynamicWidth.value * 3, 0)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                       ref_pnt + AllplanGeo.Point3D(build_ele.DynamicLength.value,
                                                                                    build_ele.DynamicWidth.value,
                                                                                    build_ele.DynamicHeight.value))

        polyhed_docking_points = DockingPointUtil.get_docking_points("DynPolyhed_", polyhed)

        docking_points = []
        docking_points.append(polyhed_docking_points[0])
        docking_points.append(polyhed_docking_points[3])
        docking_points.append(polyhed_docking_points[5])
        docking_points.append(polyhed_docking_points[6])


        #----------------- left recess

        if build_ele.RecessLeft.value:
            recess = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                          ref_pnt + AllplanGeo.Point3D(build_ele.RecessLength.value,
                                                                                       build_ele.RecessWidth.value,
                                                                                       build_ele.DynamicHeight.value))

            recess_docking_points = DockingPointUtil.get_docking_points("Recess_left_", recess)

            docking_points.append(recess_docking_points[0])
            docking_points.append(recess_docking_points[5])
            docking_points.append(("DynPolyhed_1", recess_docking_points[2][1]))
            docking_points.append(("DynPolyhed_4", recess_docking_points[7][1]))

        else:
            docking_points.append(polyhed_docking_points[1])
            docking_points.append(polyhed_docking_points[4])


        #----------------- right recess

        if build_ele.RecessRight.value:
            ref_pnt += AllplanGeo.Point3D(build_ele.DynamicLength.value - build_ele.RecessLength.value, 0, 0)

            recess = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                          ref_pnt + AllplanGeo.Point3D(build_ele.RecessLength.value,
                                                                                       build_ele.RecessWidth.value,
                                                                                       build_ele.DynamicHeight.value))

            recess_docking_points = DockingPointUtil.get_docking_points("Recess_right_", recess)

            docking_points.append(recess_docking_points[3])
            docking_points.append(recess_docking_points[6])
            docking_points.append(recess_docking_points[1])
            docking_points.append(recess_docking_points[4])
            docking_points.append(("DynPolyhed_2", recess_docking_points[1][1]))
            docking_points.append(("DynPolyhed_7", recess_docking_points[4][1]))

        else:
            docking_points.append(polyhed_docking_points[2])
            docking_points.append(polyhed_docking_points[7])

        return [], [], docking_points
