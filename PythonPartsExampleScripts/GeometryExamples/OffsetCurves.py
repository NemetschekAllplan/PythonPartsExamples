"""
Script for the usage of the Offset service
"""
import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load OffsetCurves.py')

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

    element = OffsetCurves(doc)

    return element.create(build_ele)

class OffsetCurves():
    """
    Definition of class OffsetCurves
    """

    def __init__(self, doc):
        """
        Initialisation of class OffsetCurves

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()

    def translate(self, vector, elem):
        """
        Translate the geometry elements

        Args:
            vector:  Vector2D translation
        """
        matrix = AllplanGeo.Matrix2D()
        matrix.Translate(vector)
        elem = AllplanGeo.Transform(elem , matrix)
        return elem

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.create_offset_curves(build_ele, self.create_path1())
        self.create_offset_curves(build_ele, self.create_path2())
        self.create_offset_curves(build_ele, self.create_path3())
        self.create_offset_curves(build_ele, self.create_path4())
        self.create_offset_curves(build_ele, self.create_path5())
        self.create_offset_curves(build_ele, self.create_path6())
        self.create_offset_curves(build_ele, self.create_path7())
        self.create_offset_curves(build_ele, self.create_path8())
        self.create_offset_curves(build_ele, self.create_path9())
        self.create_offset_curves(build_ele, self.create_path10())
        self.create_offset_curves(build_ele, self.create_path11())
        self.create_offset_curves(build_ele, self.create_path12())

        return (self.model_ele_list, self.handle_list)

    def create_path1(self):
        """
        Create path

        Returns:
            Path2D element
        """
        path = AllplanGeo.Path2D()
        path += AllplanGeo.Line2D(0,0, 1000, 0)
        path += AllplanGeo.Line2D(1000, 0, 1000, 1000)
        path += AllplanGeo.Line2D(1000, 1000, 2000, 1000)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path2(self):
        """
        Create path

        Returns:
            Path2D element
        """
        path = AllplanGeo.Path2D()
        path += AllplanGeo.Line2D(0,0, 1000, 0)
        path += AllplanGeo.Line2D(1000, 0, 1500, 1000)
        path += AllplanGeo.Line2D(1500, 1000, 2000, 1000)
        path = self.translate(AllplanGeo.Vector2D(3000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path3(self):
        """
        Create path

        Returns:
            Path2D element
        """
        spline = AllplanGeo.Spline2D()
        spline += AllplanGeo.Point2D(0, 0)
        spline += AllplanGeo.Point2D(1000, 100)
        spline += AllplanGeo.Point2D(1500, 200)
        spline += AllplanGeo.Point2D(2000, 1000)

        path = AllplanGeo.Path2D()
        path += spline
        #path += AllplanGeo.Line2D(2000, 1000, 2500, 1000)
        #path += AllplanGeo.Line2D(2500, 1000, 3500, 1000)
        path = self.translate(AllplanGeo.Vector2D(6000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path4(self):
        """
        Create path

        Returns:
            Path2D element
        """
        path = AllplanGeo.Path2D()
        path += AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), 1000, 1000, 0, 0, math.pi, True)
        path = self.translate(AllplanGeo.Vector2D(10000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path5(self):
        """
        Create path

        Returns:
            Path2D element
        """
        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), 500, 500, 0, 0, math.pi, True)

        path = AllplanGeo.Path2D()
        path += arc
        path += AllplanGeo.Line2D(arc.GetStartPoint(), AllplanGeo.Point2D (arc.GetStartPoint().X + 500, 0))
        path = self.translate(AllplanGeo.Vector2D(13000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path6(self):
        """
        Create path

        Returns:
            Path2D element
        """
        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), 500, 500, 0, 0, math.pi, True)

        path = AllplanGeo.Path2D()
        path += arc
        path += AllplanGeo.Line2D(arc.GetStartPoint(), AllplanGeo.Point2D (arc.GetStartPoint().X + 100, -1000))
        path = self.translate(AllplanGeo.Vector2D(16000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path7(self):
        """
        Create path

        Returns:
            Path2D element
        """
        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), 500, 500, 0, 0, math.pi, True)

        path = AllplanGeo.Path2D()
        path += arc
        path += AllplanGeo.Line2D(arc.GetStartPoint(), AllplanGeo.Point2D (arc.GetStartPoint().X +1, -1000))
        path = self.translate(AllplanGeo.Vector2D(19000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path8(self):
        """
        Create path

        Returns:
            Path2D element
        """
        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), 500, 500, 0, 0, math.pi, True)

        path = AllplanGeo.Path2D()
        path += arc
        path += AllplanGeo.Line2D(arc.GetStartPoint(), AllplanGeo.Point2D (arc.GetStartPoint().X , -1000))
        path = self.translate(AllplanGeo.Vector2D(22000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path9(self):
        """
        Create path

        Returns:
            Path2D element
        """
        spline = AllplanGeo.Spline2D()
        spline += AllplanGeo.Point2D(0, 0)
        spline += AllplanGeo.Point2D(1000, 100)
        spline += AllplanGeo.Point2D(1500, 200)
        spline += AllplanGeo.Point2D(2000, 1000)

        path = AllplanGeo.Path2D()
        path += spline
        path += AllplanGeo.Line2D(2000, 1000, 2500, 1000)
        path = self.translate(AllplanGeo.Vector2D(25000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path10(self):
        """
        Create path

        Returns:
            Path2D element
        """
        spline = AllplanGeo.Spline2D()
        spline += AllplanGeo.Point2D(0, 0)
        spline += AllplanGeo.Point2D(1000, 100)
        spline += AllplanGeo.Point2D(1500, 200)
        spline += AllplanGeo.Point2D(2000, 1000)

        path = AllplanGeo.Path2D()
        path += spline
        path += AllplanGeo.Line2D(2000, 1000, 2500, 2000)
        path = self.translate(AllplanGeo.Vector2D(28000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path11(self):
        """
        Create path

        Returns:
            Path2D element
        """
        poly = AllplanGeo.Polyline2D()
        poly += AllplanGeo.Point2D(0, 0)
        poly += AllplanGeo.Point2D(1000, 0)
        poly += AllplanGeo.Point2D(1500, 1200)
        poly += AllplanGeo.Point2D(0, 1500)

        path = AllplanGeo.Path2D()
        path += poly
        path = self.translate(AllplanGeo.Vector2D(31000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_path12(self):
        """
        Create path

        Returns:
            Path2D element
        """
        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(0, 0), 500, 1000, 0, 0, math.pi, True)

        path = AllplanGeo.Path2D()
        path += arc
        path += AllplanGeo.Line2D(arc.GetStartPoint(), AllplanGeo.Point2D (arc.GetStartPoint().X + 100, -1000))
        path = self.translate(AllplanGeo.Vector2D(34000, 0), path)

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(self.com_prop, path))
        return path

    def create_offset_curves(self, build_ele, path):
        """
        Create the offset curves for path

        Args:
            build_ele:  the building element.
            path:       the path element for which the offset curves are calculated.
        """

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        com_prop.Color = 5
        for i in range (1, build_ele.CountOffsetCurves.value+1):
            err, offset_curve = AllplanGeo.Offset(i * +build_ele.OffsetCurveDistance.value, path, False)
            if not err:
                self.model_ele_list.append(AllplanBasisElements.ModelElement2D(com_prop, offset_curve))

        com_prop.Color = 4
        for i in range (1, build_ele.CountOffsetCurves.value+1):
            err, offset_curve = AllplanGeo.Offset(i * -build_ele.OffsetCurveDistance.value, path, False)
            if not err:
                self.model_ele_list.append(AllplanBasisElements.ModelElement2D(com_prop, offset_curve))

