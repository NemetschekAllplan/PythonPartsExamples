"""
Script for the usage of the BoolOp function
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart


print('Load BoolOp.py')


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

    element = BoolOp(doc)

    return element.create(build_ele)


def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class BoolOp():
    """
    Definition of class BoolOp
    """

    def __init__(self, doc):
        """
        Initialisation of class BoolOp

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
        self.make_union(build_ele)
        self.make_subtraction(build_ele)
        self.make_subtraction_brep_polyhedron(build_ele)

        views = [View2D3D (self.model_ele_list)]

        pythonpart = PythonPart ("BooleanOperation",
                                 parameter_list = build_ele.get_params_list(),
                                 hash_value     = build_ele.get_hash(),
                                 python_file    = build_ele.pyp_file_name,
                                 views          = views)

        self.model_ele_list = pythonpart.create()

        return (self.model_ele_list, self.handle_list)


    def make_union(self, build_ele):
        """
        Make union from polyhedrons

        Args:
            build_ele:  the building element.
        """

        #------------------ Define the handle reference point
        ref_point_1_x = build_ele.Ref1X_1.value
        ref_point_1_y = build_ele.Ref1Y_1.value
        ref_point_1_z = build_ele.Ref1Z_1.value
        handle1_point1 = AllplanGeo.Point3D(ref_point_1_x, ref_point_1_y, ref_point_1_z)
        handle1_point2 = AllplanGeo.Point3D(0, 0, 0)

        ref_point_2_x = build_ele.Ref1X_2.value
        ref_point_2_y = build_ele.Ref1Y_2.value
        ref_point_2_z = build_ele.Ref1Z_2.value
        handle2_point1 = AllplanGeo.Point3D(ref_point_2_x, ref_point_2_y, ref_point_2_z)
        handle2_point2 = AllplanGeo.Point3D(0, 0, 0)

        #------------------ Define base polyhedrons
        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length1_1.value,
                                                        build_ele.Width1_1.value,
                                                        build_ele.Thickness1_1.value)

        polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length1_2.value,
                                                        build_ele.Width1_2.value,
                                                        build_ele.Thickness1_2.value)

        #------------------ Define translation for second polyhedron - reaction to handle movement
        trans_to_ref_point_1 = AllplanGeo.Matrix3D()
        trans_to_ref_point_1.Translate(AllplanGeo.Vector3D(ref_point_1_x, ref_point_1_y, ref_point_1_z))
        polyhed1 = AllplanGeo.Transform(polyhed1, trans_to_ref_point_1)

        #------------------ Define translation for second polyhedron - reaction to handle movement
        trans_to_ref_point_2 = AllplanGeo.Matrix3D()
        trans_to_ref_point_2.Translate(AllplanGeo.Vector3D(ref_point_2_x, ref_point_2_y, ref_point_2_z))
        polyhed2 = AllplanGeo.Transform(polyhed2, trans_to_ref_point_2)

        #------------------ Draw original base bodies
        com_prop_base_bodies = AllplanBaseElements.CommonProperties()
        com_prop_base_bodies.GetGlobalProperties()
        com_prop_base_bodies.Stroke = 9 # dots
        com_prop_base_bodies.HelpConstruction = True # help construction color
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed1))
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed2))

        #------------------ Make union of polyhedrons
        err, polyhedron = AllplanGeo.MakeUnion(polyhed1, polyhed2)

        #------------------ Draw result body, if no error happens
        if GeometryValidate.polyhedron(err) and polyhedron.IsValid():
            com_prop = AllplanBaseElements.CommonProperties()
            com_prop.GetGlobalProperties()
            com_prop.Color = build_ele.Color1.value
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhedron))

        #------------------ Create a handle for the handle_point
        handle_elem1 = HandleProperties("UnionMoveHandleBody1",
                                        handle1_point1,
                                        handle1_point2,
                                        [("Ref1X_1", HandleDirection.x_dir),
                                         ("Ref1Y_1", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir,
                                        False)
        self.handle_list.append(handle_elem1)

        handle_elem2 = HandleProperties("UnionMoveHandleBody2",
                                        handle2_point1,
                                        handle2_point2,
                                        [("Ref1X_2", HandleDirection.x_dir),
                                         ("Ref1Y_2", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir,
                                        False)
        self.handle_list.append(handle_elem2)

    def make_subtraction(self, build_ele):
        """
        Create polyhedrons and subtract one from another

        Args:
            build_ele:  the building element.
        """

        delta = 4000

        #------------------ Define the handle reference point
        ref_point_1_x = build_ele.Ref2X_1.value
        ref_point_1_y = build_ele.Ref2Y_1.value
        ref_point_1_z = build_ele.Ref2Z_1.value
        handle1_point1 = AllplanGeo.Point3D(ref_point_1_x, ref_point_1_y, ref_point_1_z)
        handle1_point2 = AllplanGeo.Point3D(0, 0, 0)

        #------------------ Define common props for base geometry
        com_prop_base_bodies = AllplanBaseElements.CommonProperties()
        com_prop_base_bodies.GetGlobalProperties()
        com_prop_base_bodies.Stroke = 9 # dots
        com_prop_base_bodies.HelpConstruction = True # help construction color

        #------------------ Define base polyhedron
        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length2.value,
                                                        build_ele.Width2.value,
                                                        build_ele.Thickness2.value)

        #------------------ Translation in WCS
        trans_to_ref_point_1 = AllplanGeo.Matrix3D()
        trans_to_ref_point_1.Translate(AllplanGeo.Vector3D(ref_point_1_x, ref_point_1_y, ref_point_1_z))
        polyhed1 = AllplanGeo.Transform(polyhed1, trans_to_ref_point_1)

        #----------------- Define the second polyhedron by base polygon and height

        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_ele.BasePol2X1.value + delta,
                                       build_ele.BasePol2Y1.value,
                                       build_ele.BasePol2Z1.value)
        base_pol += AllplanGeo.Point3D(build_ele.BasePol2X2.value + delta,
                                       build_ele.BasePol2Y2.value,
                                       build_ele.BasePol2Z2.value)
        base_pol += AllplanGeo.Point3D(build_ele.BasePol2X3.value + delta,
                                       build_ele.BasePol2Y3.value,
                                       build_ele.BasePol2Z3.value)
        base_pol += AllplanGeo.Point3D(build_ele.BasePol2X4.value + delta,
                                       build_ele.BasePol2Y4.value,
                                       build_ele.BasePol2Z4.value)
        base_pol += AllplanGeo.Point3D(build_ele.BasePol2X1.value + delta,
                                       build_ele.BasePol2Y1.value,
                                       build_ele.BasePol2Z1.value)

        if not GeometryValidate.is_valid(base_pol):
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed1))
            return

        err, plane = base_pol.GetPlane()

        if not GeometryValidate.element_method(err):
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed1))
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, base_pol))
            return

        vector = plane.GetVector()

        height = build_ele.Height2.value

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_ele.BasePol2X1.value + delta,
                                   build_ele.BasePol2Y1.value,
                                   build_ele.BasePol2Z1.value)
        path += AllplanGeo.Point3D(build_ele.BasePol2X1.value + vector.X * height + delta,
                                   build_ele.BasePol2Y1.value + vector.Y * height,
                                   build_ele.BasePol2Z1.value + vector.Z * height)

        err, polyhed2 = AllplanGeo.CreatePolyhedron(base_pol, path)

        if not GeometryValidate.polyhedron(err):
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed1))
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, path))
            return

        #------------------ Draw original base bodies
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed1))
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, polyhed2))

        #------------------ Make subtraction of polyhedrons
        err, polyhedron = AllplanGeo.MakeSubtraction(polyhed1, polyhed2)

        #------------------ Draw result body, if no error happens
        if GeometryValidate.polyhedron(err) and polyhedron.IsValid():
            com_prop = AllplanBaseElements.CommonProperties()
            com_prop.GetGlobalProperties()
            com_prop.Color = build_ele.Color2.value
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhedron))

        #------------------ Create a handle for the handle_point
        handle_elem1 = HandleProperties("SubtractionMoveHandleBody1",
                                        handle1_point1,
                                        handle1_point2,
                                        [("Ref2X_1", HandleDirection.x_dir),
                                         ("Ref2Y_1", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir,
                                        False)
        self.handle_list.append(handle_elem1)

    def make_subtraction_brep_polyhedron(self, build_ele):
        """
        Make union from polyhedrons

        Args:
            build_ele:  the building element.
        """

        #------------------ Define the handle reference point
        ref_point_1_x = build_ele.Ref4X_1.value
        ref_point_1_y = build_ele.Ref4Y_1.value
        ref_point_1_z = build_ele.Ref4Z_1.value
        handle1_point1 = AllplanGeo.Point3D(ref_point_1_x, ref_point_1_y, ref_point_1_z)
        handle1_point2 = AllplanGeo.Point3D(0, 0, 0)

        ref_point_2_x = build_ele.Ref4X_2.value
        ref_point_2_y = build_ele.Ref4Y_2.value
        ref_point_2_z = build_ele.Ref4Z_2.value
        handle2_point1 = AllplanGeo.Point3D(ref_point_2_x, ref_point_2_y, ref_point_2_z)
        handle2_point2 = AllplanGeo.Point3D(0, 0, 0)

        #------------------ Define base polyhedrons
        polyhedron = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length4_1.value,
                                                          build_ele.Width4_1.value,
                                                          build_ele.Thickness4_1.value)

        cylinder = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(),
                                                    build_ele.Radius4.value,
                                                    build_ele.Height4.value)

        #------------------ Define translation for second polyhedron - reaction to handle movement
        trans_to_ref_point_1 = AllplanGeo.Matrix3D()
        trans_to_ref_point_1.Translate(AllplanGeo.Vector3D(ref_point_1_x, ref_point_1_y, ref_point_1_z))
        polyhedron = AllplanGeo.Transform(polyhedron, trans_to_ref_point_1)

        #------------------ Define translation for second polyhedron - reaction to handle movement
        trans_to_ref_point_2 = AllplanGeo.Matrix3D()
        trans_to_ref_point_2.Translate(AllplanGeo.Vector3D(ref_point_2_x, ref_point_2_y, ref_point_2_z))
        cylinder = AllplanGeo.Transform(cylinder, trans_to_ref_point_2)

        #------------------ Convert polyhedron to brep so Boolean op is possible
        _, cube = AllplanGeo.CreateBRep3D(polyhedron)

        #------------------ Draw original base bodies
        com_prop_base_bodies = AllplanBaseElements.CommonProperties()
        com_prop_base_bodies.GetGlobalProperties()
        com_prop_base_bodies.Stroke = 9 # dots
        com_prop_base_bodies.HelpConstruction = True # help construction color
        if cube.IsValid():
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, cube))
        if cylinder.IsValid():
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop_base_bodies, cylinder))

        #------------------ Make union of polyhedrons
        err, union = AllplanGeo.MakeSubtraction(cube, cylinder)

        #------------------ Draw result body, if no error happens
        if GeometryValidate.polyhedron(err) and union.IsValid():
            com_prop = AllplanBaseElements.CommonProperties()
            com_prop.GetGlobalProperties()
            com_prop.Color = build_ele.Color4.value
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, union))

        #------------------ Create a handle for the handle_point
        handle_elem1 = HandleProperties("UnionMoveHandleBody1",
                                        handle1_point1,
                                        handle1_point2,
                                        [("Ref4X_1", HandleDirection.x_dir),
                                         ("Ref4Y_1", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir,
                                        False)
        self.handle_list.append(handle_elem1)

        handle_elem2 = HandleProperties("UnionMoveHandleBody2",
                                        handle2_point1,
                                        handle2_point2,
                                        [("Ref4X_2", HandleDirection.x_dir),
                                         ("Ref4Y_2", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir,
                                        False)
        self.handle_list.append(handle_elem2)


