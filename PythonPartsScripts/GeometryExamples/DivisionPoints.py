"""
Script for the usage of the DivisionPoints service
"""
import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load DivisionPoints.py')

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True

def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    element = DivisionPoints(doc)

    return element.create(build_ele)

class DivisionPoints():
    """
    Definition of class DivisionPoints
    """

    def __init__(self, doc):
        """
        Initialisation of class DivisionPoints

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        if build_ele.LineLineLine.value:
            path = self.create_line_line_line_path()
            self.create_division_points(build_ele, path)

        if build_ele.LineSplineLine.value:
            path = self.create_line_spline_line_path()
            self.create_division_points(build_ele, path)

        if build_ele.LineArcLine.value:
            path = self.create_line_arc_line_path()
            self.create_division_points(build_ele, path)

        return (self.model_ele_list, self.handle_list)

    def create_line_arc_line_path(self):
        """
        Create a line-arc-line path

        Returns:
            Path2D element
        """
        line1 = AllplanGeo.Line2D(0,1200, 1000, 1200)
        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(1000, 1000), 200, 200, 0, 0, math.pi/2, True)
        line2 = AllplanGeo.Line2D(1200, 1000, 1200, 0)

        path = AllplanGeo.Path2D()
        path += line1
        path += arc
        path += line2

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(com_prop, path))
        return path

    def create_line_line_line_path(self):
        """
        Create a line-line-line path

        Returns:
            Path2D element
        """
        line1 = AllplanGeo.Line2D(1500,0, 2500, 0)
        line2 = AllplanGeo.Line2D(2500, 0, 2500, 1000)
        line3 = AllplanGeo.Line2D(2500, 1000, 3500, 1000)

        path = AllplanGeo.Path2D()
        path += line1
        path += line2
        path += line3

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(com_prop, path))
        return path

    def create_line_spline_line_path(self):
        """
        Create a line-spline-line path

        Returns:
            Path2D element
        """
        line1 = AllplanGeo.Line2D(3000,0, 4000, 0)
        spline = AllplanGeo.Spline2D()
        spline += AllplanGeo.Point2D(4000, 0)
        spline += AllplanGeo.Point2D(4200, 200)
        spline += AllplanGeo.Point2D(4000, 1000)
        line3 = AllplanGeo.Line2D(4000, 1000, 5000, 1000)

        path = AllplanGeo.Path2D()
        path += line1
        path += spline
        path += line3

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(com_prop, path))
        return path

    def create_division_points(self, build_ele, path):
        """
        Create the division points for path

        Args:
            build_ele:  the building element.
        """

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Color = 5

        if build_ele.UseCountForDivision.value:
            division = AllplanGeo.DivisionPoints(path, build_ele.CountDivisions.value, build_ele.Epsilon.value)
        else:
            division = AllplanGeo.DivisionPoints(path, build_ele.LengthDivisions.value, build_ele.Epsilon.value)
        points = division.GetPoints()
        angles = division.GetPointAngles()

        for point, angle in zip(points, angles):
            divpointline = AllplanGeo.Line2D(point.X, point.Y-20, point.X, point.Y+20)
            matrix = AllplanGeo.Matrix2D()
            matrix.Rotation(AllplanGeo.Point2D(point.X, point.Y), angle)
            divpointline = AllplanGeo.Transform(divpointline , matrix)
            self.model_ele_list.append(AllplanBasisElements.ModelElement2D(com_prop, divpointline))


