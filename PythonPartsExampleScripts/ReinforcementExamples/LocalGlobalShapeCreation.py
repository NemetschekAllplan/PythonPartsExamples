"""
Script for local / global bar creation example

The script shows the usage of the reinforcement shape builder. The shape builder needs
the geometry elements in a x/y-coordinate system for the shape calculation. To get this,
there a two possibilities:

- Create the shape by 2D points and lines. Transform the created shape to the model.

- Create the shape by 3D points and lines and a transformation matrix. The matrix is used
  to transform the 3D elements to the local x/y-coordinate system which is used for the
  shape calculation. After the calculation the shape is transformed back to the model
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.RotationAngles import RotationAngles


print('Load LocalGlobalBarCreation.py')


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
    element = LocalGlobalBarCreation(doc)

    return element.create(build_ele)


class LocalGlobalBarCreation():
    """
    Definition of class LocalGlobalBarCreation
    """

    def __init__(self, doc):
        """
        Initialisation of class LocalGlobalBarCreation

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

        self.local_bar_x0 = 1000
        self.local_bar_y0 = 1000

        self.global_bar_x0 = 6000
        self.global_bar_y0 = 1000


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        self.create_reinf_by_local_shape(build_ele)
        self.create_reinf_by_global_shape(build_ele)

        return (self.model_ele_list, self.handle_list)


    def create_polyhedron(self, build_ele, move_vec):
        """
        Create the reinforcement by using local shape creation

        Args:
            build_ele:  the building element.
            move_vec:   move vector
        """

        #----  Assign the parameter

        width = build_ele.Width.value
        length = build_ele.Length.value
        height = build_ele.Height.value
        angle_z = build_ele.AngleZ.value


        #----- Create the polyhedron

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, width, height)

        angle = AllplanGeo.Angle()
        angle.Deg = angle_z

        rot_mat = AllplanGeo.Matrix3D()
        rot_mat.SetRotation(AllplanGeo.Line3D(AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Point3D(0, 0, 1000)), angle)

        polyhed = AllplanGeo.Transform(polyhed, rot_mat)
        polyhed = AllplanGeo.Move(polyhed, move_vec)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

        return polyhed


    def create_reinf_by_local_shape(self, build_ele):
        """
        Create the reinforcement by using local shape creation

        Args:
            build_ele:  the building element.
        """

        #----  Assign the parameter

        width = build_ele.Width.value
        length = build_ele.Length.value
        height = build_ele.Height.value
        angle_z = build_ele.AngleZ.value

        concrete_cover = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        bending_roller = build_ele.BendingRoller.value
        steel_grade    = build_ele.SteelGrade.value
        concrete_grade = build_ele.ConcreteGrade.value
        distance       = build_ele.Distance.value


        #----- Create the polyhedron

        polyhed = self.create_polyhedron(build_ele, AllplanGeo.Vector3D(self.local_bar_x0, self.local_bar_y0, 0))


        #---- create the local shape for the x-z section

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        shape_builder.AddPoints([(AllplanGeo.Point2D(0, height), concrete_cover),
                                 (AllplanGeo.Point2D(0, 0), concrete_cover),
                                 (AllplanGeo.Point2D(length, 0), concrete_cover),
                                 (concrete_cover)])

        shape_builder.SetSideLengthStart(300.)
        shape_builder.SetAnchorageHookEnd(90)

        shape = shape_builder.CreateShape(diameter, bending_roller, steel_grade, concrete_grade,
                                          AllplanReinf.BendingShapeType.LongitudinalBar)

        if shape.IsValid() is False:
            return


        #---- rotate the shape orthogonal to the placement direction

        shape.Rotate(RotationAngles(90, 0, angle_z))


        #---- create the placement (move the shape to the start point of the placement by "global_move = True")

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                1, shape,
                polyhed[1],
                polyhed[0],
                concrete_cover, concrete_cover, distance,
                LinearBarBuilder.StartEndPlacementRule.AdditionalCover,
                True))


        #---- create the local shape for the y-z section (use AddSides for example)

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        shape_builder.AddSides(
            [(concrete_cover),
             (AllplanGeo.Line2D(AllplanGeo.Point2D(0, height), AllplanGeo.Point2D(0, 0)), concrete_cover),
             (AllplanGeo.Line2D(AllplanGeo.Point2D(0, 0), AllplanGeo.Point2D(width, 0)), concrete_cover + diameter),
             (concrete_cover)])

        shape_builder.SetSideLengthStart(300.)
        shape_builder.SetAnchorageHookEnd(90)

        shape = shape_builder.CreateShape(diameter, bending_roller, steel_grade, concrete_grade,
                                          AllplanReinf.BendingShapeType.LongitudinalBar)

        if shape.IsValid() is False:
            return


        #---- rotate the shape orthogonal to the placement direction

        shape.Rotate(RotationAngles(90, 0, angle_z + 90))


        #---- create the placement (move the shape to the start point of the placement by "global_move = True")

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                2, shape,
                polyhed[1],
                polyhed[2],
                concrete_cover, concrete_cover, distance,
                LinearBarBuilder.StartEndPlacementRule.AdditionalCover,
                True))

        return True



    def create_reinf_by_global_shape(self, build_ele):
        """
        Create the reinforcement by using local shape creation

        Args:
            build_ele:  the building element.
        """

        #----  Assign the parameter

        concrete_cover = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        bending_roller = build_ele.BendingRoller.value
        steel_grade    = build_ele.SteelGrade.value
        distance       = build_ele.Distance.value
        concrete_grade = build_ele.ConcreteGrade.value


        #----- Create the polyhedron

        polyhed = self.create_polyhedron(build_ele, AllplanGeo.Vector3D(self.global_bar_x0, self.global_bar_y0, 0))


        #---- create the global shape for the x-z section
        #                  rotate the points around the bottom front polyhedron edge
        #                  to get a local coordinate system for the shape builder

        angle_global_to_local     = AllplanGeo.Angle()
        angle_global_to_local.Deg = -90

        shape_mat = AllplanGeo.Matrix3D()
        shape_mat.SetRotation(AllplanGeo.Line3D(polyhed[1], polyhed[2]), angle_global_to_local)

        shape_builder = AllplanReinf.ReinforcementShapeBuilder(shape_mat)

        shape_builder.AddPoints([(polyhed[4], concrete_cover),
                                 (polyhed[1], concrete_cover),
                                 (polyhed[2], concrete_cover),
                                 (concrete_cover)])

        shape_builder.SetSideLengthStart(300.)
        shape_builder.SetAnchorageHookEnd(90)

        shape = shape_builder.CreateShape(diameter, bending_roller, steel_grade, concrete_grade,
                                          AllplanReinf.BendingShapeType.LongitudinalBar)

        if shape.IsValid() is False:
            return


        #---- create the placement (the shape has global coordinates, no move necessary by "global_move = False")

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                3, shape,
                polyhed[1],
                polyhed[0],
                concrete_cover, concrete_cover, distance,
                LinearBarBuilder.StartEndPlacementRule.AdditionalCover,
                False))


        #---- create the global shape for the y-z section (use AddSides for example)
        #     rotate the points around the bottom left polyhedron edge
        #     to get a local coordinate system for the shape builder

        shape_mat = AllplanGeo.Matrix3D()
        shape_mat.SetRotation(AllplanGeo.Line3D(polyhed[1], polyhed[0]), angle_global_to_local)

        shape_builder = AllplanReinf.ReinforcementShapeBuilder(shape_mat)

        shape_builder.AddSides([(concrete_cover),
                                (AllplanGeo.Line3D(polyhed[4], polyhed[1]), concrete_cover),
                                (AllplanGeo.Line3D(polyhed[1], polyhed[0]), concrete_cover + diameter),
                                (concrete_cover)])

        shape_builder.SetSideLengthStart(300.)
        shape_builder.SetAnchorageHookEnd(90)

        shape = shape_builder.CreateShape(diameter, bending_roller, steel_grade, concrete_grade,
                                          AllplanReinf.BendingShapeType.LongitudinalBar)

        if shape.IsValid() is False:
            return


        #---- create the placement (the shape has global coordinates, no move necessary by "global_move = False")

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                4, shape,
                polyhed[1],
                polyhed[2],
                concrete_cover, concrete_cover, distance,
                LinearBarBuilder.StartEndPlacementRule.AdditionalCover,
                False))

        return True

