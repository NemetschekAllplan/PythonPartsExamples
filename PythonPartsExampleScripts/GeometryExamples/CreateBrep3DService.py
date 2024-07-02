"""
Script for the usage of the CreateBRep3D service
"""
import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil

from TypeCollections import Curve3DList

print('Load CreateBRep3DService.py')

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

    element = CreateBRep3DService(doc)
    return element.create(build_ele)

class CreateBRep3DService():
    """
    Definition of class CreateBRep3DService
    """

    def __init__(self, doc):
        """
        Initialisation of class CreateBRep3DService

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc
        self.offset_factor = 2
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.com_prop_faces = AllplanBaseElements.CommonProperties()
        self.com_prop_faces.GetGlobalProperties()
        self.com_prop_faces.Color = 5

    def transform(self, element, translation):
        """
        Translate element

        Returns
            Translated element
        """
        matrix = AllplanGeo.Matrix3D()
        matrix.Translate(translation)
        return AllplanGeo.Transform(element, matrix)

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.offset_factor = build_ele.OffsetFactor.value

        self.create_brep_faces(self.create_brep1())
        self.create_brep_faces(self.create_brep2())
        self.create_brep_faces(self.create_brep3())

        return (self.model_ele_list, self.handle_list)

    def create_brep1(self):
        """
        Create BRep3D element (quarter arc tube)
        """
        arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(1000.0, 0.0, 1000.0),
                               AllplanGeo.Vector3D(1., 0., 0.),
                               AllplanGeo.Vector3D(0., 0., 1.), 200.0, 200.0, 0.0, 2 * math.pi)
        profiles = Curve3DList([arc])

        axis_line = AllplanGeo.Line3D(AllplanGeo.Point3D(0.0, -550.0, 1000.0), AllplanGeo.Point3D(0., 550., 1000.))
        axis = AllplanGeo.Axis3D(axis_line)

        err, brep = AllplanGeo.CreateRevolvedBRep3D(profiles, axis, AllplanGeo.Angle(math.pi / 2), True, 0)
        if not err and brep.IsValid:
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, brep))
            return brep
        return None

    def create_brep2(self):
        """
        Create BRep3D element (three joined cylinders)
        """
        origin1 = AllplanGeo.Point3D(0, 0, -500)
        origin2 = AllplanGeo.Point3D(-500, 0, 0)
        origin3 = AllplanGeo.Point3D(0, -500, 0)
        xaxis =  AllplanGeo.Vector3D(1, 0, 0)
        yaxis =  AllplanGeo.Vector3D(0, 1, 0)
        zaxis =  AllplanGeo.Vector3D(0, 0, 1)
        axispl1 = AllplanGeo.AxisPlacement3D(origin1, xaxis, zaxis)
        axispl2 = AllplanGeo.AxisPlacement3D(origin2, yaxis, xaxis)
        axispl3 = AllplanGeo.AxisPlacement3D(origin3, zaxis, yaxis)

        cylinder1 = AllplanGeo.BRep3D.CreateCylinder(axispl1, 100, 1000)
        cylinder2 = AllplanGeo.BRep3D.CreateCylinder(axispl2, 100, 1000)
        cylinder3 = AllplanGeo.BRep3D.CreateCylinder(axispl3, 100, 1000)

        err, brep = AllplanGeo.MakeUnion(cylinder1, cylinder2)
        err, brep = AllplanGeo.MakeUnion(brep, cylinder3)
        if not err and brep.IsValid:
            brep = self.transform(brep, AllplanGeo.Vector3D(5000, 0, 0))
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, brep))
            return brep
        return None

    def create_brep3(self):
        """
        Create BRep3D element (fillet)
        """
        brep = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(), 1500, 2000, 1000)

        fillet_radius = 200

        edges = AllplanUtil.VecSizeTList()
        edges[:] = [4, 5, 6, 7]

        err, brep = AllplanGeo.FilletCalculus3D.Calculate(brep, edges, fillet_radius, False)
        if not err and brep.IsValid:
            brep = self.transform(brep, AllplanGeo.Vector3D(10000, 0, 0))
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, brep))
            return brep
        return None

    def gravity_point(self, brep):
        """
        Extract gravity point of brep

        Returns
            Point3D gravity point
        """
        err, _, _, gravitypoint = AllplanGeo.CalcMass(brep)
        if not err:
            return gravitypoint
        return None

    def create_brep_faces(self, brep):
        """
        Create for every BRep3D face a new BRep3D
        """
        if brep.IsValid:
            gravity_all = self.gravity_point(brep)
            for i in range (1, brep.GetFaceCount()+1):
                err, brepface = AllplanGeo.CreateBRep3D(brep, i-1)
                if not err and brepface.IsValid:

                    # translate faces for exploration
                    gravity_part = self.gravity_point(brepface)
                    translation = AllplanGeo.Vector3D(gravity_all, gravity_part)
                    length = translation.GetLength()
                    translation.Normalize()
                    translation *= self.offset_factor * length
                    brepface2 = self.transform(brepface, translation)

                    self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop_faces, brepface2))

