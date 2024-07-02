"""
Script for the showing of the possible geometry elements
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load Arc3D.py')

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

    element = Arc3D(doc)

    return element.create(build_ele)

class Arc3D():
    """
    Definition of class Arc3D
    """

    def __init__(self, doc):
        """
        Initialisation of class Arc3D

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

        self.startangle = AllplanGeo.Angle()
        self.deltaangle = AllplanGeo.Angle()
        self.ccw = True
        self.minor = 500
        self.major = 1000

        self.showxaxis = True
        self.showzaxis = True
        self.createplanarbreps = True

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.startangle.Deg = build_ele.StartAngle.value
        self.deltaangle.Deg = build_ele.DeltaAngle.value
        self.ccw = build_ele.CCW.value
        self.minor = build_ele.Minor.value
        self.major = build_ele.Major.value
        self.showzaxis = build_ele.ShowZAxis.value
        self.showxaxis = build_ele.ShowXAxis.value
        self.createplanarbreps = build_ele.CreatePlanarBReps.value

        # Z axis normal
        self.create_arc3d(AllplanGeo.Point3D(0, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(-1500, 0, 0))

        self.create_arc3d(AllplanGeo.Point3D(2000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(-1500, -1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(4000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(0, -1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(6000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(1500, 0, 0))

        self.create_arc3d(AllplanGeo.Point3D(8000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(1500, 1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(10000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(0, 1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(12000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1000),
                          AllplanGeo.Vector3D(-1500, 1500, 0))

        # X axis normal
        self.create_arc3d(AllplanGeo.Point3D(0, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, -1500))

        self.create_arc3d(AllplanGeo.Point3D(2000, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, -1500, -1500))

        self.create_arc3d(AllplanGeo.Point3D(4000, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, -1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(6000, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, 0, 1500))

        self.create_arc3d(AllplanGeo.Point3D(8000, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, 1500, 1500))

        self.create_arc3d(AllplanGeo.Point3D(10000, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, 1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(12000, 2000, 0),
                          AllplanGeo.Vector3D(1000, 0, 0),
                          AllplanGeo.Vector3D(0, 1500, -1500))

        # Y axis normal
        self.create_arc3d(AllplanGeo.Point3D(0, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(0, 0, -1500))

        self.create_arc3d(AllplanGeo.Point3D(2000, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(-1500, 0, -1500))

        self.create_arc3d(AllplanGeo.Point3D(4000, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(-1500, 0, 0))

        self.create_arc3d(AllplanGeo.Point3D(6000, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(0, 0, 1500))

        self.create_arc3d(AllplanGeo.Point3D(8000, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(1500, 0, 1500))

        self.create_arc3d(AllplanGeo.Point3D(10000, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(1500, 0, 0))

        self.create_arc3d(AllplanGeo.Point3D(12000, 4000, 0),
                          AllplanGeo.Vector3D(0, 1000, 0),
                          AllplanGeo.Vector3D(1500, 0, -1500))

        # ZX axis normal
        self.create_arc3d(AllplanGeo.Point3D(0, 6000, 0),
                          AllplanGeo.Vector3D(1000, 0, 1000),
                          AllplanGeo.Vector3D(-1500, 0, 1500))

        self.create_arc3d(AllplanGeo.Point3D(2000, 6000, 0),
                          AllplanGeo.Vector3D(1000, 0, 1000),
                          AllplanGeo.Vector3D(1500, 0, -1500))

        vector = AllplanGeo.Vector3D(1000, 0, 1000) * AllplanGeo.Vector3D(-1500, 0, 1500)
        vector.Normalize(1500)
        self.create_arc3d(AllplanGeo.Point3D(4000, 6000, 0),
                          AllplanGeo.Vector3D(1000, 0, 1000),
                          vector)

        vector = AllplanGeo.Vector3D(1000, 0, 1000) * AllplanGeo.Vector3D(1500, 0, -1500)
        vector.Normalize(1500)
        self.create_arc3d(AllplanGeo.Point3D(6000, 6000, 0),
                          AllplanGeo.Vector3D(1000, 0, 1000),
                          vector)

        # ZY axis normal
        self.create_arc3d(AllplanGeo.Point3D(0, 8000, 0),
                          AllplanGeo.Vector3D(0, 1000, 1000),
                          AllplanGeo.Vector3D(0, -1500, 1500))

        self.create_arc3d(AllplanGeo.Point3D(2000, 8000, 0),
                          AllplanGeo.Vector3D(0, 1000, 1000),
                          AllplanGeo.Vector3D(0, 1500, -1500))

        vector = AllplanGeo.Vector3D(0, 1000, 1000) * AllplanGeo.Vector3D(0, -1500, 1500)
        vector.Normalize(1500)
        self.create_arc3d(AllplanGeo.Point3D(4000, 8000, 0),
                          AllplanGeo.Vector3D(0, 1000, 1000),
                          vector)

        vector = AllplanGeo.Vector3D(0, 1000, 1000) * AllplanGeo.Vector3D(0, 1500, -1500)
        vector.Normalize(1500)
        self.create_arc3d(AllplanGeo.Point3D(6000, 8000, 0),
                          AllplanGeo.Vector3D(0, 1000, 1000),
                          vector)

        # XY axis normal
        self.create_arc3d(AllplanGeo.Point3D(0, 10000, 0),
                          AllplanGeo.Vector3D(1000, 1000, 0),
                          AllplanGeo.Vector3D(1500, -1500, 0))

        self.create_arc3d(AllplanGeo.Point3D(2000, 10000, 0),
                          AllplanGeo.Vector3D(1000, 1000, 0),
                          AllplanGeo.Vector3D(-1500, 1500, 0))

        vector = AllplanGeo.Vector3D(1000, 1000, 0) * AllplanGeo.Vector3D(1500, -1500, 0)
        vector.Normalize(1500)
        self.create_arc3d(AllplanGeo.Point3D(4000, 10000, 0),
                          AllplanGeo.Vector3D(1000, 1000, 0),
                          vector)

        vector = AllplanGeo.Vector3D(1000, 1000, 0) * AllplanGeo.Vector3D(-1500, 1500, 0)
        vector.Normalize(1500)
        self.create_arc3d(AllplanGeo.Point3D(6000, 10000, 0),
                          AllplanGeo.Vector3D(1000, 1000, 0),
                          vector)

        return (self.model_ele_list, self.handle_list)

    def create_arc3d(self, centerpoint, normalvec, majoraxisvec):
        """
        Create the 3D arc
        """
        com_prop_element = AllplanBaseElements.CommonProperties()
        com_prop_element.GetGlobalProperties()
        com_prop_element.Color = 1

        arc = AllplanGeo.Arc3D(
            centerpoint,            # center
            majoraxisvec,           # major axis
            normalvec,              # normal
            self.minor,             # minor
            self.major,             # major
            self.startangle.Rad,    # start angle
            self.deltaangle.Rad,    # delta angle
            self.ccw)               # clockwise

        polyline = AllplanGeo.Polyline3D()
        polyline += arc.GetStartPoint()
        polyline += centerpoint
        polyline += arc.GetEndPoint()

        if self.createplanarbreps:
            path = AllplanGeo.Path3D()
            path += arc
            if self.deltaangle.Deg - self.startangle.Deg < 360:
                path += polyline

            err, brep = AllplanGeo.CreatePlanarBRep3D(path)
            if not err and brep.IsValid:
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_element, brep))
        else:
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_element, arc))
            #define lines to close arc
            if self.deltaangle.Deg - self.startangle.Deg < 360:
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_element, polyline))

        if self.showxaxis:
            com_prop_major_axis = AllplanBaseElements.CommonProperties()
            com_prop_major_axis.GetGlobalProperties()
            com_prop_major_axis.Color = 6 # red

            major_axis = majoraxisvec
            trans_major_axis = AllplanGeo.Matrix3D()
            trans_major_axis.Translate(major_axis)
            point3 = AllplanGeo.Transform(centerpoint, trans_major_axis)

            self.model_ele_list.append(
                AllplanBasisElements.ModelElement3D(com_prop_major_axis, AllplanGeo.Line3D(centerpoint, point3)))

        if self.showzaxis:
            com_prop_normal = AllplanBaseElements.CommonProperties()
            com_prop_normal.GetGlobalProperties()
            com_prop_normal.Color = 7 # blue

            normal = normalvec
            trans_normal = AllplanGeo.Matrix3D()
            trans_normal.Translate(normal)
            point2 = AllplanGeo.Transform(centerpoint, trans_normal)

            self.model_ele_list.append(
                AllplanBasisElements.ModelElement3D(com_prop_normal, AllplanGeo.Line3D(centerpoint, point2)))


