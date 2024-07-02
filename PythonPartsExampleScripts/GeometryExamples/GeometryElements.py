"""
Script for the showing of the possible geometry elements
"""

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

print('Load GeometryElements.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float):
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = GeometryElements(doc)

    return element.create(build_ele)


class GeometryElements():
    """
    Definition of class GeometryElements
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization

        Args:
            doc: input document
        """

        self.document = doc

        self.com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


    def create(self, build_ele: BuildingElement) -> CreateElementResult:
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            created element result
        """

        model_ele_list = []


        #----------------- 2D elements

        self.com_prop.Color = 5

        if build_ele.Line2D.value:
            model_ele_list.append(self.create_line2d())

        if build_ele.Polyline2D.value:
            model_ele_list.append(self.create_polyline2d())

        if build_ele.Polygon2D.value:
            model_ele_list.append(self.create_polygon2d())

        if build_ele.Arc2D.value:
            model_ele_list.append(self.create_arc2d())

        if build_ele.Spline2D.value:
            model_ele_list.append(self.create_spline2d())

        if build_ele.Path2D.value:
            model_ele_list.append(self.create_path2d())


        #----------------- 3D elements

        self.com_prop.Color = 1

        if build_ele.Line3D.value:
            model_ele_list.append(self.create_line3d())

        if build_ele.Polyline3D.value:
            model_ele_list.append(self.create_polyline3d())

        if build_ele.Polygon3D.value:
            model_ele_list.append(self.create_polygon3d())

        if build_ele.Arc3D.value:
            model_ele_list.append(self.create_arc3d())

        if build_ele.Spline3D.value:
            model_ele_list.append(self.create_spline3d())

        if build_ele.Polyhedron3D.value:
            model_ele_list.append(self.create_polyhedron3d())

        if build_ele.BRep3D.value:
            model_ele_list.append(self.create_brep3d())

        if build_ele.Ellipsoid3D.value:
            model_ele_list.append(self.create_ellipsoid3d())

        if build_ele.Cuboid3D.value:
            model_ele_list.append(self.create_cuboid3d())

        if build_ele.Cone3D.value:
            model_ele_list.append(self.create_cone3d())

        if build_ele.Cylinder3D.value:
            model_ele_list.append(self.create_cylinder3d())

        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(),
                                             build_ele.RotationAngleX.value,
                                             build_ele.RotationAngleY.value,
                                             build_ele.RotationAngleZ.value,
                                             model_ele_list)

        #----------------- create the PythonPart

        if build_ele.CreatePythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(model_ele_list)

            model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(model_ele_list)


    def create_line2d(self):
        """
        Create the 2D line
        """

        line = AllplanGeo.Line2D(AllplanGeo.Point2D(0,0),AllplanGeo.Point2D(1000,1000))

        return AllplanBasisElements.ModelElement2D(self.com_prop, line)


    def create_polyline2d(self):
        """
        Create the 2D polyline
        """

        polyline = AllplanGeo.Polyline2D()
        polyline += AllplanGeo.Point2D(2000,0)
        polyline += AllplanGeo.Point2D(2500,300)
        polyline += AllplanGeo.Point2D(2300,500)
        polyline += AllplanGeo.Point2D(3000,1000)

        return AllplanBasisElements.ModelElement2D(self.com_prop, polyline)


    def create_polygon2d(self):
        """
        Create the 2D polygon
        """

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(4000,0)
        polygon += AllplanGeo.Point2D(4500,300)
        polygon += AllplanGeo.Point2D(4300,500)
        polygon += AllplanGeo.Point2D(5000,1000)
        polygon += AllplanGeo.Point2D(4200,900)
        polygon += AllplanGeo.Point2D(4000,0)

        return AllplanBasisElements.ModelElement2D(self.com_prop, polygon)


    def create_arc2d(self):
        """
        Create the 2D arc
        """

        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(7000, 500), 1000, 500, math.pi / 2, 0, math.pi, True)

        return AllplanBasisElements.ModelElement2D(self.com_prop, arc)


    def create_spline2d(self):
        """
        Create the 2D spline
        """

        spline = AllplanGeo.Spline2D()
        spline += AllplanGeo.Point2D(8000, 0)
        spline += AllplanGeo.Point2D(8500, 500)
        spline += AllplanGeo.Point2D(9000, 1000)
        spline.SetStartVector(AllplanGeo.Vector2D(1, 0))
        spline.SetEndVector(AllplanGeo.Vector2D(1, 0))

        return AllplanBasisElements.ModelElement2D(self.com_prop, spline)


    def create_path2d(self):
        """
        Create the 2D path
        """

        path = AllplanGeo.Path2D()

        path += AllplanGeo.Line2D(AllplanGeo.Point2D(12000, 500), AllplanGeo.Point2D(10000, 1000))
        path += AllplanGeo.Arc2D(AllplanGeo.Point2D(10000, 500), 500, 500, math.pi / 2, 0, math.pi, True)

        polyline = AllplanGeo.Polyline2D()
        polyline += AllplanGeo.Point2D(10000, 0)
        polyline += AllplanGeo.Point2D(11000, -500)
        polyline += AllplanGeo.Point2D(12000, 500)

        path += polyline

        self.com_prop.Color = 6

        return AllplanBasisElements.ModelElement2D(self.com_prop, path)


    def create_line3d(self):
        """
        Create the 3D line
        """

        line = AllplanGeo.Line3D(AllplanGeo.Point3D(0,2000,0),AllplanGeo.Point3D(1000,3000,2000))

        return AllplanBasisElements.ModelElement3D(self.com_prop, line)


    def create_polyline3d(self):
        """
        Create the 3D polyline
        """

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(2000,2000,0)
        polyline += AllplanGeo.Point3D(2500,2300,500)
        polyline += AllplanGeo.Point3D(2300,2500,300)
        polyline += AllplanGeo.Point3D(3000,3000,1000)

        return AllplanBasisElements.ModelElement3D(self.com_prop, polyline)


    def create_polygon3d(self):
        """
        Create the 3D polygon
        """

        polygon = AllplanGeo.Polygon3D()
        polygon += AllplanGeo.Point3D(4500,2000,0)
        polygon += AllplanGeo.Point3D(5000,2500,500)
        polygon += AllplanGeo.Point3D(4500,3000,1000)
        polygon += AllplanGeo.Point3D(4000,2500,500)
        polygon += AllplanGeo.Point3D(4500,2000,0)

        return AllplanBasisElements.ModelElement3D(self.com_prop, polygon)


    def create_arc3d(self):
        """
        Create the 3D arc
        """

        arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(6500, 2500, 1000),
                               AllplanGeo.Vector3D(1, 0, 0),
                               AllplanGeo.Vector3D(0, 1, 1),
                               1000, 500, 0, math.pi, True)

        return AllplanBasisElements.ModelElement3D(self.com_prop, arc)


    def create_spline3d(self):
        """
        Create the 3D spline
        """

        spline = AllplanGeo.Spline3D()
        spline += AllplanGeo.Point3D(8000, 2000, 0)
        spline += AllplanGeo.Point3D(8500, 2500, 500)
        spline += AllplanGeo.Point3D(9000, 3000, 1000)

        spline.StartVector = AllplanGeo.Vector3D(1, 0, 0)
        spline.EndVector   = AllplanGeo.Vector3D(1, 0, 0)

        return AllplanBasisElements.ModelElement3D(self.com_prop, spline)


    def create_polyhedron3d(self):
        """
        Create the 3D polyhedron
        """

        point1 = AllplanGeo.Point3D(10000,2000,0)
        point2 = AllplanGeo.Point3D(11000,3000,2000)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(point1, point2)

        return AllplanBasisElements.ModelElement3D(self.com_prop, polyhed)


    def create_brep3d(self):
        """
        Create the 3D brep
        """

        brep = AllplanGeo.BRep3D.CreateCuboid(
            AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(12000, 2000, 0),
                                       AllplanGeo.Vector3D(1, 0, 0),
                                       AllplanGeo.Vector3D(0, 0, 1)),
            1000, 1000, 2000)

        return AllplanBasisElements.ModelElement3D(self.com_prop, brep)


    def create_ellipsoid3d(self):
        """
        Create the 3D ellipsoid
        """

        ellipsoid = AllplanGeo.Ellipsoid3D(
            AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(14500, 2500, 500),
                                       AllplanGeo.Vector3D(1, 0, 0),
                                       AllplanGeo.Vector3D(0, 0, 1)),
            500, 500, 500)

        return AllplanBasisElements.ModelElement3D(self.com_prop, ellipsoid)


    def create_cuboid3d(self):
        """
        Create the 3D cuboid
        """

        cuboid = AllplanGeo.Cuboid3D(AllplanGeo.Point3D(16500, 2000, 0),
                                     AllplanGeo.Point3D(0, 0, 0),
                                     AllplanGeo.Vector3D(500, 0, 500),
                                     AllplanGeo.Vector3D(0, 1000, 0),
                                     AllplanGeo.Vector3D(-500, 0, 500))

        return AllplanBasisElements.ModelElement3D(self.com_prop, cuboid)


    def create_cone3d(self):
        """
        Create the 3D cone
        """

        cone = AllplanGeo.Cone3D(
            AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(18500, 2500, 0),
                                       AllplanGeo.Vector3D(0, 1, 0),
                                       AllplanGeo.Vector3D(1, 0, 1)),
            1000, 200,
            AllplanGeo.Point3D(0, 0, 1000))

        return AllplanBasisElements.ModelElement3D(self.com_prop, cone)


    def create_cylinder3d(self):
        """
        Create the 3D cylinder
        """

        cylinder = AllplanGeo.Cylinder3D(
            AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(20500, 2500, 0),
                                       AllplanGeo.Vector3D(1, 0, 0),
                                       AllplanGeo.Vector3D(0, 1, 1)),
            500, 500,
            AllplanGeo.Point3D(0, 0, 1000))

        return AllplanBasisElements.ModelElement3D(self.com_prop, cylinder)
