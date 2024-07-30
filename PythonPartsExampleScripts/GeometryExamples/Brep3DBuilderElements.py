"""
Script for the showing of the possible Brep3D builder elements
"""
import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from TypeCollections import Curve3DList

print('Load Brep3DBuilderElements.py')

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

    element = BRepBuilder(doc)
    return element.create(build_ele)


class BRepBuilder():
    """
    Definition of class BRepBuilder
    """

    def __init__(self, doc):
        """
        Initialisation of class BRepBuilder

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.com_prop_help1 = AllplanBaseElements.CommonProperties()
        self.com_prop_help1.GetGlobalProperties()
        self.com_prop_help1.Color = 6
        self.com_prop_help2 = AllplanBaseElements.CommonProperties()
        self.com_prop_help2.GetGlobalProperties()
        self.com_prop_help2.Color = 7
        self.show_elements = True

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.show_elements = build_ele.ShowElements.value

        if build_ele.RevolvedBreps.value:
            self.create_revolved_breps()

        if build_ele.RailSweptBreps.value:
            self.create_rail_swept_breps()

        if build_ele.SweptBreps.value:
            self.create_swept_breps()

        if build_ele.LoftedBreps.value:
            self.create_lofted_breps()

        if build_ele.PlanarBreps.value:
            self.create_planar_breps()

        return (self.model_ele_list, self.handle_list)

    def translate(self, element, trans_vector):
        """
        Translate element by translation vector
        """
        matrix = AllplanGeo.Matrix3D()
        matrix.Translate(trans_vector)
        return AllplanGeo.Transform(element, matrix)

    def create_elements(self, err, brep, translation, elem1, elem2, elem3, elem4, elem5, elem6):
        """
        Create Brep element and helper elements
        """
        if not err and brep.IsValid:
            brep = self.translate(brep, translation)
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, brep))
        if self.show_elements:
            if elem1:
                elem1 = self.translate(elem1, translation)
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_help1, elem1))
            if elem2:
                elem2 = self.translate(elem2, translation)
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_help1, elem2))
            if elem3:
                elem3 = self.translate(elem3, translation)
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_help1, elem3))
            if elem4:
                elem4 = self.translate(elem4, translation)
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_help2, elem4))
            if elem5:
                elem5 = self.translate(elem5, translation)
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_help2, elem5))
            if elem6:
                elem6 = self.translate(elem6, translation)
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_help2, elem6))


    def create_revolved_breps(self):
        """
        Create revolved breps
        """
        arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(1000.0, 0.0, 1000.0),
                               AllplanGeo.Vector3D(1., 0., 0.),
                               AllplanGeo.Vector3D(0., 0., 1.), 500.0, 500.0, 0.0, 2 * math.pi)
        profiles = Curve3DList([arc])

        axis_line = AllplanGeo.Line3D(AllplanGeo.Point3D(0.0, -550.0, 1000.0), AllplanGeo.Point3D(0., 550., 1000.))
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(math.pi / 2), True, 0)
        translation = AllplanGeo.Vector3D(0, 0, 0)
        self.create_elements(err, brep, translation, arc, None, None, axis_line, None, None)

        #------------------------ next brep

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(0.,   0., 500.)
        polyline += AllplanGeo.Point3D(500.,   0., 500.)
        polyline += AllplanGeo.Point3D(500., 500., 500.)
        polyline += AllplanGeo.Point3D(0., 500., 500.)
        polyline += AllplanGeo.Point3D(0.,   0., 500.)
        profiles = Curve3DList([polyline])

        axis_line = AllplanGeo.Line3D(AllplanGeo.Point3D(0.0, -50.0, 500.0), AllplanGeo.Point3D(0., 550., 500.))
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(math.pi / 2), True, 0)
        translation = AllplanGeo.Vector3D(2000, 0, 0)
        self.create_elements(err, brep, translation, polyline, None, None, axis_line, None, None)

        #------------------------ next brep
        arc = AllplanGeo.Arc3D(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, 0),
                                                          AllplanGeo.Vector3D(1, 0, 0),
                                                          AllplanGeo.Vector3D(0, 0, 1))
                               , 500., 500., 0., math.pi)
        profiles = Curve3DList([arc])

        axis_line = AllplanGeo.Line3D(arc.GetStartPoint(), arc.GetEndPoint())
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(math.pi + math.pi / 4), False, 0)
        translation = AllplanGeo.Vector3D(4000, 0, 0)
        self.create_elements(err, brep, translation, arc, None, None, axis_line, None, None)

        #------------------------ next brep
        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(0.,   0.,  0.)
        polyline += AllplanGeo.Point3D(300.,   0.,  0.)
        polyline += AllplanGeo.Point3D(300., 300.,  0.)
        polyline += AllplanGeo.Point3D(0., 300.,  0.)
        polyline += AllplanGeo.Point3D(0.,   0.,  0.)
        profiles = Curve3DList([polyline])

        axis_line = AllplanGeo.Line3D(500.0, -50.0, 0.0, 500.0, 350.0, 0.0)
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(2 * math.pi), False, 0)
        translation = AllplanGeo.Vector3D(6000, 0, 0)
        self.create_elements(err, brep, translation, polyline, None, None, axis_line, None, None)

        #------------------------ next brep
        line = AllplanGeo.Line3D(0., 0., 0., 500., 500., 1000.)
        profiles = Curve3DList([line])

        axis_line = AllplanGeo.Line3D(AllplanGeo.Point3D(0., 0., 0), AllplanGeo.Vector3D(0., 0., 1100.))
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(math.pi + math.pi / 2), False, 5)
        translation = AllplanGeo.Vector3D(8000, 0, 0)
        self.create_elements(err, brep, translation, line, None, None, axis_line, None, None)

        #------------------------ next brep

        spline = AllplanGeo.Spline3D()
        spline += AllplanGeo.Point3D(0,   0,   0)
        spline += AllplanGeo.Point3D(10.,  0,  50)
        spline += AllplanGeo.Point3D(30.,  0, 200)
        spline += AllplanGeo.Point3D(100.,  0, 280)
        spline += AllplanGeo.Point3D(210.,  0, 310)
        spline += AllplanGeo.Point3D(240.,  0, 355)
        spline += AllplanGeo.Point3D(240.,  0, 400)
        profiles = Curve3DList([spline])

        axis_line = AllplanGeo.Line3D(0, 0, 0, 0, 0, 500)
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(2 * math.pi), False, 0)
        translation = AllplanGeo.Vector3D(10000, 0, 0)
        self.create_elements(err, brep, translation, spline, None, None, axis_line, None, None)

    def create_rail_swept_breps(self):
        """
        Create rail swept breps
        """

        arc1 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 0., 0.), 400., 400., 0., math.pi)
        arc2 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 1000., 500.), 200., 600., 0., math.pi)
        line1 = AllplanGeo.Line3D(arc1.GetStartPoint(), arc2.GetStartPoint())
        line2 = AllplanGeo.Line3D(arc1.GetEndPoint(), arc2.GetEndPoint())
        profiles = Curve3DList([arc1, arc2])
        rails = Curve3DList([line1, line2])

        err, brep = AllplanGeo.CreateRailSweptBRep3D(profiles,rails, False, True, False)
        translation = AllplanGeo.Vector3D(0, 2000, 0)
        self.create_elements(err, brep, translation, arc1, arc2, None, line1, line2, None)

        #------------------------ next brep
        arc1 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 0., 0.),
                                AllplanGeo.Vector3D(1., 0., 0.),
                                AllplanGeo.Vector3D(0., -1., 0.),
                                400., 400., 0., 2 * math.pi)

        arc2 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 1000., 500.),
                                AllplanGeo.Vector3D(1., 0., 0.),
                                AllplanGeo.Vector3D(0., -1., 0.),
                                500., 700., 0., 2 * math.pi)

        line1 = AllplanGeo.Line3D(arc1.GetStartPoint(), arc2.GetStartPoint())

        profiles = Curve3DList([arc1, arc2])
        rails = Curve3DList([line1]) # closed arcs use only 1 rail

        err, brep = AllplanGeo.CreateRailSweptBRep3D(profiles,rails, False, True, False)
        translation = AllplanGeo.Vector3D(2000, 2000, 0)
        self.create_elements(err, brep, translation, arc1, arc2, None, line1, None, None)

        #------------------------ next brep
        arc1 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 0., 0.),
                                AllplanGeo.Vector3D(1., 0., 0.),
                                AllplanGeo.Vector3D(0., -1., 0.),
                                400., 400., 0., math.pi / 2)

        arc2 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 1000., 500.),
                                AllplanGeo.Vector3D(1., 0., 0.),
                                AllplanGeo.Vector3D(0., -1., 0.),
                                500., 700., 0., math.pi)

        line1 = AllplanGeo.Line3D(arc1.GetStartPoint(), arc2.GetStartPoint())

        profiles = Curve3DList([arc1, arc2])
        rails = Curve3DList([line1]) # closed arcs use only 1 rail

        err, brep = AllplanGeo.CreateRailSweptBRep3D(profiles,rails, False, True, False)
        translation = AllplanGeo.Vector3D(4000, 2000, 0)
        self.create_elements(err, brep, translation, arc1, arc2, None, line1, None, None)

        #------------------------ next brep
        profile1 = AllplanGeo.Line3D(0.000, 0., 0.00, 0.000, 500., 0.00)
        profile2 = AllplanGeo.Line3D(500.0, 0., 0.00, 500.0, 500., 200.)
        profile2 = AllplanGeo.Line3D(1000., 0., 100., 1000., 500., 400.)
        profile2 = AllplanGeo.Line3D(1500., 0., 200., 1500., 500., 600.)

        path = AllplanGeo.Polyline3D()
        path += profile1.GetStartPoint()
        path += profile2.GetStartPoint()

        profiles = Curve3DList([profile1, profile2])
        rails = Curve3DList([path])

        err, brep = AllplanGeo.CreateRailSweptBRep3D(profiles,rails, False, True, False)
        translation = AllplanGeo.Vector3D(6000, 2000, 0)
        self.create_elements(err, brep, translation, profile1, profile2, None, path, None, None)

        #------------------------ next brep
        profile1 = AllplanGeo.Polyline3D()
        profile1 += AllplanGeo.Point3D(0., 0., 0.)
        profile1 += AllplanGeo.Point3D(500., 0., 0.)
        profile1 += AllplanGeo.Point3D(500., 0., 500.)
        profile1 += AllplanGeo.Point3D(0., 0., 500.)
        profile1 += AllplanGeo.Point3D(0., 0., 0.)

        profile2 = AllplanGeo.Spline3D()
        profile2 += AllplanGeo.Point3D(0., 1000., 0.)
        profile2 += AllplanGeo.Point3D(500., 1000., 0.)
        profile2 += AllplanGeo.Point3D(500., 1000., 500.)
        profile2 += AllplanGeo.Point3D(0., 1000., 500.)
        profile2 += AllplanGeo.Point3D(0., 1000., 0.)

        path1 = AllplanGeo.Spline3D()
        path1 += profile1.GetStartPoint()
        path1 += profile2.GetStartPoint()

        path2 = AllplanGeo.Spline3D()
        path2 += profile1.GetPoint(2)
        path2 += profile2.GetPoint(2)

        profiles = Curve3DList([profile1, profile2])
        rails = Curve3DList([path1, path2])

        err, brep = AllplanGeo.CreateRailSweptBRep3D(profiles,rails, False, True, False)
        translation = AllplanGeo.Vector3D(8000, 2000, 0)
        self.create_elements(err, brep, translation, profile1, profile2, None, path1, path2, None)

    def create_swept_breps(self):
        """
        Create swept breps
        """

        path = AllplanGeo.Arc3D(AllplanGeo.Point3D(10., 0., 0.),
                                AllplanGeo.Vector3D(1., 0., 0.),
                                AllplanGeo.Vector3D(0., -1., 0.),
                                300., 300., 0.5, math.pi)

        line = AllplanGeo.Line3D(path.GetStartPoint(), AllplanGeo.Vector3D(150,0,0))
        profiles = [line]

        err, brep = AllplanGeo.CreateSweptBRep3D(profiles, path, False, True, None, 0)
        translation = AllplanGeo.Vector3D(0, 4000, 0)
        self.create_elements(err, brep, translation, line, None, None, path, None, None)

        #------------------------ next brep

        path = AllplanGeo.Arc3D(AllplanGeo.Point3D(10., 0., 0.),
                                AllplanGeo.Vector3D(1., 0., 0.),
                                AllplanGeo.Vector3D(0., -1., 0.),
                                300., 300., 0.5, math.pi)

        polyline = AllplanGeo.Polyline3D()
        polyline += path.GetStartPoint()
        polyline += polyline.GetLastPoint() + AllplanGeo.Vector3D(0,150,0)
        polyline += polyline.GetLastPoint() + AllplanGeo.Vector3D(150,0,0)
        polyline += polyline.GetLastPoint() + AllplanGeo.Vector3D(0,-150,0)
        profiles = [polyline]

        err, brep = AllplanGeo.CreateSweptBRep3D(profiles, path, False, True, None, 0)
        translation = AllplanGeo.Vector3D(2000, 4000, 0)
        self.create_elements(err, brep, translation, polyline, None, None, path, None, None)

        #------------------------ next brep (axis sweep)

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(100, 0, 0)
        polyline += polyline.GetLastPoint() + AllplanGeo.Vector3D(100, 0, 0)
        polyline += polyline.GetLastPoint() + AllplanGeo.Vector3D(100, 0, 50)
        polyline += polyline.GetLastPoint() + AllplanGeo.Vector3D(0, 0, 50)
        polyline += polyline.GetStartPoint()
        profile = polyline

        arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(0, 0, 0),
                               AllplanGeo.Vector3D(1, 0, 0),
                               AllplanGeo.Vector3D(0, 0, 1),
                               400, 400, 0, math.pi + math.pi / 2, True)
        path = AllplanGeo.BSpline3D.CreateArc3D(arc)

        axis_line = AllplanGeo.Line3D(0, 0, 0, 0, 0, 150)
        zaxis = AllplanGeo.Vector3D(0, 0, 1)

        err, brep = AllplanGeo.CreateSweptBRep3D(profile, path, False, zaxis)
        translation = AllplanGeo.Vector3D(4000, 4000, 0)
        self.create_elements(err, brep, translation, polyline, None, None, path, axis_line, None)

        #------------------------ next brep (axis sweep)

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(100, 0, 0)
        polyline += AllplanGeo.Point3D(200, 0, 0)
        polyline += AllplanGeo.Point3D(200, 0, 100)
        polyline += AllplanGeo.Point3D(100, 0, 100)
        polyline += AllplanGeo.Point3D(100, 0, 0)
        profile = polyline

        arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(0, 0, 0),
                               AllplanGeo.Vector3D(1, 0, 0),
                               AllplanGeo.Vector3D(0, 0, 1),
                               1000, 1000, 0, math.pi, True)
        bspline = AllplanGeo.BSpline3D.CreateArc3D(arc)

        count = bspline.Count()
        for index in range(1, count):
            point = bspline[index]
            point.Z = index  * 500 / (count - 1)
            bspline[index] = point

        axis_line = AllplanGeo.Line3D(0, 0, 0, 0, 0, 550)
        zaxis = AllplanGeo.Vector3D(0, 0, 1)

        err, brep = AllplanGeo.CreateSweptBRep3D(profile, bspline, False, zaxis)
        translation = AllplanGeo.Vector3D(6000, 4000, 0)
        self.create_elements(err, brep, translation, polyline, None, None, axis_line, None, None)

        #------------------------ next brep (axis sweep)
        err, brep = AllplanGeo.CreateSweptBRep3D(profile, bspline, True, zaxis)
        translation = AllplanGeo.Vector3D(8000, 4000, 0)
        self.create_elements(err, brep, translation, polyline, None, None, axis_line, None, None)

    def create_three_profiles (self):
        """
        Create three polylines as profiles for lofted brep
        """
        polyline1 = AllplanGeo.Polyline3D()
        polyline1 += AllplanGeo.Point3D(0., 0., 0.)
        polyline1 += AllplanGeo.Point3D(100., 0., 0.)
        polyline1 += AllplanGeo.Point3D(100., 0., 100.)
        polyline1 += AllplanGeo.Point3D(0., 0., 100.)
        polyline1 += AllplanGeo.Point3D(0., 0., 0.)

        polyline2 = AllplanGeo.Polyline3D()
        polyline2 += AllplanGeo.Point3D(-100., 200., 50.)
        polyline2 += AllplanGeo.Point3D(400., 200., 50.)
        polyline2 += AllplanGeo.Point3D(400., 200., 100.)
        polyline2 += AllplanGeo.Point3D(-100., 200., 100.)
        polyline2 += AllplanGeo.Point3D(-100., 200., 50.)

        polyline3 = AllplanGeo.Polyline3D()
        polyline3 += AllplanGeo.Point3D(0., 500., 0.)
        polyline3 += AllplanGeo.Point3D(100., 500., 0.)
        polyline3 += AllplanGeo.Point3D(100., 500., 100.)
        polyline3 += AllplanGeo.Point3D(0., 500., 100.)
        polyline3 += AllplanGeo.Point3D(0., 500., 0.)
        return polyline1, polyline2, polyline3

    def create_lofted_breps(self):
        """
        Create lofted breps
        """
        arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 0., 0.), 400., 400., 0., math.pi)

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(100., 10., 200.)
        polyline += AllplanGeo.Point3D(40., 100., 200.)
        polyline += AllplanGeo.Point3D(0., 100., 200.)
        polyline += AllplanGeo.Point3D(-70., 10., 200.)

        profiles = Curve3DList([arc, polyline])
        inner_profiles = Curve3DList()

        err, brep = AllplanGeo.CreateLoftedBRep3D(profiles, inner_profiles, False, False, True, False)
        translation = AllplanGeo.Vector3D(0, 6000, 0)
        self.create_elements(err, brep, translation, polyline, None, None, arc, None, None)

        #------------------------ next brep
        polyline1 = AllplanGeo.Polyline3D()
        polyline1 += AllplanGeo.Point3D(0., 0., 200.)
        polyline1 += AllplanGeo.Point3D(100., 100., 200.)
        polyline1 += AllplanGeo.Point3D(200., 100., 200.)
        polyline1 += AllplanGeo.Point3D(300., 0., 200.)

        polyline2 = AllplanGeo.Polyline3D()
        polyline2 += AllplanGeo.Point3D(-200., 100., 0.)
        polyline2 += AllplanGeo.Point3D(0., 300., 0.)
        polyline2 += AllplanGeo.Point3D(100., 500., 0.)
        polyline2 += AllplanGeo.Point3D(200., 500., 0.)
        polyline2 += AllplanGeo.Point3D(300., 300., 0.)
        polyline2 += AllplanGeo.Point3D(500., 100., 0.)

        profiles = Curve3DList([polyline1, polyline2])
        inner_profiles = Curve3DList()

        err, brep = AllplanGeo.CreateLoftedBRep3D(profiles, inner_profiles, False, False, True, False)
        translation = AllplanGeo.Vector3D(2000, 6000, 0)
        self.create_elements(err, brep, translation, polyline1, None, None, polyline2, None, None)

        #------------------------ next brep
        polyline1, polyline2, polyline3 = self.create_three_profiles()
        profiles = Curve3DList([polyline1, polyline2, polyline3])
        inner_profiles = Curve3DList()

        err, brep = AllplanGeo.CreateLoftedBRep3D(profiles, inner_profiles, True, True, False, False)
        translation = AllplanGeo.Vector3D(4000, 6000, 0)
        self.create_elements(err, brep, translation, polyline1, polyline3, None, polyline2, None, None)

        #------------------------ next brep
        arc = AllplanGeo.Arc3D(AllplanGeo.AxisPlacement3D(), 400., 400., 0., 2 * math.pi)

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(-200.,-200., 500.)
        polyline += AllplanGeo.Point3D(200.,-200., 500.)
        polyline += AllplanGeo.Point3D(200., 200., 500.)
        polyline += AllplanGeo.Point3D(-200., 200., 500.)
        polyline += AllplanGeo.Point3D(-200.,-200., 500.)

        profiles = Curve3DList([arc, polyline])
        inner_profiles = Curve3DList()

        err, brep = AllplanGeo.CreateLoftedBRep3D(profiles, inner_profiles, True, True, False, False)
        translation = AllplanGeo.Vector3D(6000, 6000, 0)
        self.create_elements(err, brep, translation, polyline1, None, None, arc, None, None)

        #------------------------ next brep
        arc1 = AllplanGeo.Arc3D(AllplanGeo.AxisPlacement3D(), 200., 500., 0.,2 * math.pi)
        arc2 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 0., 500.), 500., 200., 0., 2 * math.pi)

        profiles = Curve3DList([arc1, arc2])
        inner_profiles = Curve3DList()

        err, brep = AllplanGeo.CreateLoftedBRep3D(profiles, inner_profiles, True, True, False, False)
        translation = AllplanGeo.Vector3D(8000, 6000, 0)
        self.create_elements(err, brep, translation, arc1, None, None, arc2, None, None)

        #------------------------ next brep
        arc1 = AllplanGeo.Arc3D(AllplanGeo.Point3D(0., 0., 0.), 500., 500., 0., 2 * math.pi)
        arc1_hole = AllplanGeo.Arc3D(AllplanGeo.Point3D(100., 0., 0.), 300., 300., 0., 2 * math.pi)
        arc2 = AllplanGeo.Arc3D(AllplanGeo.Point3D(200., 0., 500.), 500., 500., 0., 2 * math.pi)
        arc2_hole = AllplanGeo.Arc3D(AllplanGeo.Point3D(100., 0., 500.), 300., 300., 0., 2 * math.pi)
        arc3 = AllplanGeo.Arc3D(AllplanGeo.Point3D(-100., -100., 1000.), 400., 400., 0., 2 * math.pi)
        arc3_hole = AllplanGeo.Arc3D(AllplanGeo.Point3D(-100., -100., 1000.), 300., 300., 0., 2 * math.pi)

        outerprofiles = Curve3DList([arc1, arc2, arc3])
        inner_profiles = Curve3DList([arc1_hole, arc2_hole, arc3_hole])

        err, brep = AllplanGeo.CreateLoftedBRep3D(outerprofiles, inner_profiles, True, True, False, False)
        translation = AllplanGeo.Vector3D(10000, 6000, 0)
        self.create_elements(err, brep, translation, arc1, arc2, arc3, arc1_hole, arc2_hole, arc3_hole)

        #------------------------ next brep
        err, brep = AllplanGeo.CreateLoftedBRep3D(outerprofiles, inner_profiles, False, True, False, False)
        translation = AllplanGeo.Vector3D(12000, 6000, 0)
        self.create_elements(err, brep, translation, arc1, arc2, arc3, arc1_hole, arc2_hole, arc3_hole)

    def create_planar_breps(self):
        """
        Create planar breps
        """
        #------------------------ rectangle brep
        curve = AllplanGeo.Polyline3D()
        curve += AllplanGeo.Point3D(-500.,-500., 500.)
        curve += AllplanGeo.Point3D(500.,-500., 500.)
        curve += AllplanGeo.Point3D(500., 500., 0.)
        curve += AllplanGeo.Point3D(-500., 500., 0.)
        curve += curve.GetStartPoint()

        err, brep = AllplanGeo.CreatePlanarBRep3D(curve)
        translation = AllplanGeo.Vector3D(0, 8000, 0)
        self.create_elements(err, brep, translation, curve, None, None, None, None, None)

        #------------------------ closed arc brep
        center = AllplanGeo.Point3D(0., 0., 0.)
        curve = AllplanGeo.Arc3D(center, 400., 600., 0., 2 * math.pi)

        err, brep = AllplanGeo.CreatePlanarBRep3D(curve)
        translation = AllplanGeo.Vector3D(2000, 8000, 0)
        self.create_elements(err, brep, translation, curve, None, None, None, None, None)

        #------------------------ closed ellipse with ellipse hole and polygon
        #inside ellipse hole
        outer_curve = AllplanGeo.Arc3D(center, 400., 600., 0., 2 * math.pi)
        inner_curve = AllplanGeo.Arc3D(center, 300., 400., 0., 2 * math.pi)
        curve = AllplanGeo.Polyline3D()
        curve += AllplanGeo.Point3D(-100.,-100., 0.)
        curve += AllplanGeo.Point3D(100.,-100., 0.)
        curve += AllplanGeo.Point3D(100., 100., 0.)
        curve += AllplanGeo.Point3D(-100., 100., 0.)
        curve += curve.GetStartPoint()

        profiles = Curve3DList([outer_curve, inner_curve, curve])

        err, brep = AllplanGeo.CreatePlanarBRep3D(profiles)
        translation = AllplanGeo.Vector3D(4000, 8000, 0)
        self.create_elements(err, brep, translation, outer_curve, None, None, inner_curve, None, None)

        #------------------------ three quarter arc (open arc closed by polyline)
        arc = AllplanGeo.Arc3D(center, 400., 600., 0., math.pi + math.pi / 2)

        polyline = AllplanGeo.Polyline3D()
        polyline += arc.GetStartPoint()
        polyline += center
        polyline += arc.GetEndPoint()

        path = AllplanGeo.Path3D()
        path += arc
        path += polyline

        err, brep = AllplanGeo.CreatePlanarBRep3D(path)
        translation = AllplanGeo.Vector3D(6000, 8000, 0)
        self.create_elements(err, brep, translation, arc, None, None, polyline, None, None)

        #------------------------ 2 touching ellipses
        center2 = AllplanGeo.Point3D(500., 0., 0.)
        arc1 = AllplanGeo.Arc3D(center, 400., 600., 0., 2 * math.pi)
        arc2 = AllplanGeo.Arc3D(center2, 300., 400., 0., 2 * math.pi)
        profiles = Curve3DList([arc1, arc2])

        err, brep = AllplanGeo.CreatePlanarBRep3D(profiles)
        translation = AllplanGeo.Vector3D(8000, 8000, 0)
        self.create_elements(err, brep, translation, arc1, None, None, arc2, None, None)

        #------------------------ bspline
        arc = AllplanGeo.Arc3D(center, 400., 600., 0., 2 * math.pi)
        bspline = AllplanGeo.BSpline3D.CreateArc3D(arc)

        err, brep = AllplanGeo.CreatePlanarBRep3D(bspline)
        translation = AllplanGeo.Vector3D(10000, 8000, 0)
        self.create_elements(err, brep, translation, arc, None, None, None, None, None)

        #------------------------ spline
        spline = AllplanGeo.Spline3D()
        spline += AllplanGeo.Point3D(-500, -500, 0)
        spline += AllplanGeo.Point3D(-568.158, 92.914, 0)
        spline += AllplanGeo.Point3D(-389.975, 423.827, 0)
        spline += AllplanGeo.Point3D(190.024, 423.827, 0)
        spline += AllplanGeo.Point3D(446.398, 471.100, 0)
        spline += AllplanGeo.Point3D(560.944, 302.007, 0)
        spline += AllplanGeo.Point3D(448.216, 14.731, 0)
        spline += AllplanGeo.Point3D(182.758, 134.733, 0)
        spline += AllplanGeo.Point3D(-104.517, 167.460, 0)
        spline += AllplanGeo.Point3D(-84.517, -65.269, 0)
        spline += AllplanGeo.Point3D(437.307, -83.451, 0)
        spline += AllplanGeo.Point3D(571.854, -365.272, 0)
        spline += AllplanGeo.Point3D(282.759, -547.092, 0)
        spline += AllplanGeo.Point3D(-33.607, -252.543, 0)
        spline += AllplanGeo.Point3D(-186.336, -283.453, 0)
        spline += AllplanGeo.Point3D(-69.971, -536.183, 0)
        spline += AllplanGeo.Point3D(-413.611, -587.093, 0)
        spline += AllplanGeo.Point3D(-490.765, -524.564, 0)
        spline += AllplanGeo.Point3D(-500, -500, 0)

        err, brep = AllplanGeo.CreatePlanarBRep3D(spline)
        translation = AllplanGeo.Vector3D(12000, 8000, 0)
        self.create_elements(err, brep, translation, spline, None, None, None, None, None)
