"""
Script for the usage of the Chamfer function
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate


print('Load Chamfer.py')


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

    element = Chamfer(doc)

    return element.create(build_ele)


class Chamfer():
    """
    Definition of class Chamfer
    """

    def __init__(self, doc):
        """
        Initialisation of class Chamfer

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

        #self.line2d_chamfer(build_ele)
        #self.line3d_chamfer(build_ele)
        #self.polyline_chamfer(build_ele)
        self.phed_chamfer(build_ele)
        self.brep_chamfer(build_ele)

        return (self.model_ele_list, self.handle_list)


    def line3d_chamfer(self, build_ele):
        """
        Create the 2 lines 3d and chamfer them

        Args:
            build_ele:  the building element.
        """

        line1 = AllplanGeo.Line3D(build_ele.Line1X1_2.value, build_ele.Line1Y1_2.value,
                                  build_ele.Line1X2_2.value, build_ele.Line1Y2_2.value,
                                  build_ele.Line1Z2_2.value, build_ele.Line1Z2_2.value)

        line2 = AllplanGeo.Line3D(build_ele.Line2X1_2.value, build_ele.Line2Y1_2.value,
                                  build_ele.Line2X2_2.value, build_ele.Line2Y2_2.value,
                                  build_ele.Line2Z2_2.value, build_ele.Line2Z2_2.value)

        input_pnt = AllplanGeo.Point3D(build_ele.PointX_2.value,
                                       build_ele.PointY_2.value,
                                       build_ele.PointZ_2.value)

        result, intersect_pnt = AllplanGeo.IntersectionCalculus(line1, line2)

        if not GeometryValidate.intersection(result):
            return

        plane = AllplanGeo.Plane3D(line1.GetStartPoint(),
                                   line1.GetEndPoint(),
                                   line2.GetEndPoint())

        chamfer_line = AllplanGeo.ChamferCalculus.CalculateChamferLine(
            line1, line2, plane, intersect_pnt, input_pnt)

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = build_ele.Color2.value

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, line1))
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, line2))
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, chamfer_line))


    def phed_chamfer(self, build_ele):
        """
        Create the polyhedron and chamfer it

        Args:
            build_ele:  the building element.
        """

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length4.value,
                                                       build_ele.Width4.value,
                                                       build_ele.Thickness4.value)

        chamfer_width = build_ele.ChamferWidth4.value

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = build_ele.Color4.value

        if chamfer_width > 0:

            ori_edges = build_ele.Edges4.value.split(",")

            edges = AllplanUtil.VecSizeTList()
            for edge in ori_edges:
                edges.append(int(edge))

            err, polyhed = AllplanGeo.ChamferCalculus.Calculate(polyhed, edges, chamfer_width, False)

            if not GeometryValidate.polyhedron(err):
                return

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))


    def brep_chamfer(self, build_ele):
        """
        Create the brep and chamfer it

        Args:
            build_ele:  the building element.
        """

        brep = AllplanGeo.BRep3D.CreateCuboid(
            AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(3000, 0, 0),
                                       AllplanGeo.Vector3D(1, 0, 0),
                                       AllplanGeo.Vector3D(0, 0, 1)),
            build_ele.Length5.value,
            build_ele.Width5.value,
            build_ele.Thickness5.value)

        chamfer_width = build_ele.ChamferWidth5.value

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = build_ele.Color5.value

        if chamfer_width > 0:

            ori_edges = build_ele.Edges5.value.split(",")

            edges = AllplanUtil.VecSizeTList()
            for edge in ori_edges:
                edges.append(int(edge))

            err, brep = AllplanGeo.ChamferCalculus.Calculate(brep, edges, chamfer_width, False)

            if not GeometryValidate.polyhedron(err):
                return

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, brep))
