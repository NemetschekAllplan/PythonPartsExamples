"""
Script for Beam1
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.IProfileReinfShapeBuilder as ProfileShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

import GeometryValidate as GeometryValidate

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


print('Load Beam1.py')


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

    element = Beam1(doc)

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

    element = Beam1(doc)

    return element.create(build_ele)


class Beam1():
    """
    Definition of class Beam1
    """

    def __init__(self, doc):
        """
        Initialisation of class Beam1

        Args:
            doc: Input document
        """

        self.model_ele_list = None
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

        self.create_geometry(build_ele)

        self.create_reinforcement(build_ele)

        return (self.model_ele_list, self.handle_list)


    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        length = build_ele.Length.value
        length_left = build_ele.LengthLeft.value

        height_left = build_ele.HeightLeft.value
        height_center = build_ele.HeightCenter.value
        height_right = build_ele.HeightRight.value

        offset_top_flange_left = build_ele.OffsetTopFlangeLeft.value
        offset_top_flange_right = build_ele.OffsetTopFlangeRight.value


        #-----------------  Get the I profile section polygons

        start_pol = self.create_iprofile_section_polygon(build_ele, offset_top_flange_left)
        center_pol = self.create_iprofile_section_polygon(build_ele, length_left, height_center)
        end_pol = self.create_iprofile_section_polygon(build_ele, length - offset_top_flange_right)


        #------------------ Create the polyhedron from the left and right I profile

        err, left_polyhed = AllplanGeo.CreatePolyhedron(start_pol, center_pol)

        if not GeometryValidate.polyhedron(err):
            return

        err, right_polyhed = AllplanGeo.CreatePolyhedron(center_pol, end_pol)

        if not GeometryValidate.polyhedron(err):
            return

        err, polyhed = AllplanGeo.MakeUnion(left_polyhed, right_polyhed)

        if not GeometryValidate.polyhedron(err):
            return


        #----------------- Add the full beam at the start and end

        length_full_beam_left = build_ele.LengthFullBeamLeft.value
        length_full_beam_right = build_ele.LengthFullBeamRight.value
        length_full_beam_web_left = build_ele.LengthFullBeamWebLeft.value
        length_full_beam_web_right = build_ele.LengthFullBeamWebRight.value

        if length_full_beam_left != 0.:
            pol1 = self.create_full_beam_polygon(build_ele, 0., height_left)
            pol2 = self.create_full_beam_polygon(build_ele, length_full_beam_left)
            pol3 = self.create_web_polygon(build_ele,
                                           length_full_beam_left + length_full_beam_web_left)

            err, full_beam_polyhed = AllplanGeo.CreatePolyhedron(pol1, pol2)

            if not GeometryValidate.polyhedron(err):
                return

            err, polyhed = AllplanGeo.MakeUnion(polyhed, full_beam_polyhed)

            if not GeometryValidate.polyhedron(err):
                return

            err, full_beam_polyhed = AllplanGeo.CreatePolyhedron(pol2, pol3)

            if not GeometryValidate.polyhedron(err):
                return

            err, polyhed = AllplanGeo.MakeUnion(polyhed, full_beam_polyhed)

            if not GeometryValidate.polyhedron(err):
                return

        if length_full_beam_right != 0.:
            pol1 = self.create_web_polygon(
                build_ele,
                length - length_full_beam_right - length_full_beam_web_right)
            pol2 = self.create_full_beam_polygon(build_ele, length - length_full_beam_right)
            pol3 = self.create_full_beam_polygon(build_ele, length, height_right)

            err, full_beam_polyhed = AllplanGeo.CreatePolyhedron(pol1, pol2)

            if not GeometryValidate.polyhedron(err):
                return

            err, polyhed = AllplanGeo.MakeUnion(polyhed, full_beam_polyhed)

            if not GeometryValidate.polyhedron(err):
                return

            err, full_beam_polyhed = AllplanGeo.CreatePolyhedron(pol2, pol3)

            if not GeometryValidate.polyhedron(err):
                return

            err, polyhed = AllplanGeo.MakeUnion(polyhed, full_beam_polyhed)

            if not GeometryValidate.polyhedron(err):
                return

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        self.model_ele_list = [AllplanBasisElements.ModelElement3D(com_prop, polyhed)]


        #------------------ Create the handles

        bottom_flange_width = build_ele.BottomFlangeWidth.value

        self.handle_list =[
            HandleProperties("HeightLeftHandle",
                             AllplanGeo.Point3D(0, bottom_flange_width / 2, height_left),
                             AllplanGeo.Point3D(0, bottom_flange_width / 2, 0),
                             [("HeightLeft", HandleDirection.z_dir)],
                             HandleDirection.z_dir),
            HandleProperties("HeightCenterHandle",
                             AllplanGeo.Point3D(length_left, bottom_flange_width / 2, height_center),
                             AllplanGeo.Point3D(length_left, bottom_flange_width / 2, 0),
                             [("HeightCenter", HandleDirection.z_dir)],
                             HandleDirection.z_dir),
            HandleProperties("HeightRightHandle",
                             AllplanGeo.Point3D(length, bottom_flange_width / 2, height_right),
                             AllplanGeo.Point3D(length, bottom_flange_width / 2, 0),
                             [("HeightRight", HandleDirection.z_dir)],
                             HandleDirection.z_dir),
            HandleProperties("LengthLeftHandle",
                             AllplanGeo.Point3D(length_left, 0, 0),
                             AllplanGeo.Point3D(0, 0, 0),
                             [("LengthLeft", HandleDirection.x_dir)],
                             HandleDirection.x_dir),
            HandleProperties("LengthHandle",
                             AllplanGeo.Point3D(length, 0, 0),
                             AllplanGeo.Point3D(0, 0, 0),
                             [("Length", HandleDirection.x_dir)],
                             HandleDirection.x_dir)
            ]


    def get_height(self, build_ele, x_coord):
        """
        Get the height at x_coord

        Args:
            build_ele:  the building element.
            x_coord:    the x coordinate.

        Returns:
            the height.
        """
        length = build_ele.Length.value
        length_left = build_ele.LengthLeft.value

        height_left = build_ele.HeightLeft.value
        height_center = build_ele.HeightCenter.value
        height_right = build_ele.HeightRight.value

        if x_coord < length_left:
            return height_left + (height_center - height_left) / length_left * x_coord
        else:
            return height_right + (height_center - height_right) / \
                (length - length_left) * (length - x_coord)


    def create_iprofile_section_polygon(self, build_ele, x_coord, height=0):
        """
        Create i profile section polygon

        Args:
            build_ele:  the building element.
            x_coord:    x coordinate.
            height:     the height.

        Returns:
            polygon for i profile section.
        """
        if height == 0:
            height = self.get_height(build_ele, x_coord)

        bottom_flange_width = build_ele.BottomFlangeWidth.value
        bottom_flange_height = build_ele.BottomFlangeHeight.value
        bottom_bevel_height = build_ele.BottomBevelHeight.value
        web_width = build_ele.WebWidth.value
        top_bevel_height = build_ele.TopBevelHeight.value
        top_flange_width = build_ele.TopFlangeWidth.value
        top_flange_height = build_ele.TopFlangeHeight.value


        #----------------- Calculate some help values

        z_top_bevel = height - top_flange_height - top_bevel_height
        z_bottom = bottom_flange_height + bottom_bevel_height
        dy_bottom = (bottom_flange_width - web_width) / 2.
        dy_top = (top_flange_width - web_width) / 2.


        #------------------ Create the points

        sect_pol = AllplanGeo.Polygon3D()

        sect_pol += AllplanGeo.Point3D(x_coord, 0, 0)
        sect_pol += AllplanGeo.Point3D(x_coord, 0, bottom_flange_height)
        sect_pol += AllplanGeo.Point3D(x_coord, dy_bottom, z_bottom)
        sect_pol += AllplanGeo.Point3D(x_coord, dy_bottom, z_top_bevel)

        delta_y = dy_bottom - dy_top

        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, height - top_flange_height)
        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, height)

        delta_y += top_flange_width

        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, height)
        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, height - top_flange_height)

        delta_y -= dy_top

        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, z_top_bevel)
        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, bottom_flange_height + bottom_bevel_height)

        delta_y += dy_bottom

        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, bottom_flange_height)
        sect_pol += AllplanGeo.Point3D(x_coord, delta_y, 0)
        sect_pol += AllplanGeo.Point3D(x_coord, 0, 0)

        return sect_pol


    def create_full_beam_polygon(self, build_ele, x_coord, height=0):
        """
        Create full beam polygon

        Args:
            build_ele:  the building element.
            x_coord:    x coordinate.
            height:     the height.

        Returns:
            polygon for full beam.
        """
        if height == 0:
            height = self.get_height(build_ele, x_coord)

        bottom_flange_width = build_ele.BottomFlangeWidth.value

        pol = AllplanGeo.Polygon3D()

        pol += AllplanGeo.Point3D(x_coord, 0, 0)
        pol += AllplanGeo.Point3D(x_coord, 0, height)
        pol += AllplanGeo.Point3D(x_coord, bottom_flange_width, height)
        pol += AllplanGeo.Point3D(x_coord, bottom_flange_width, 0)
        pol += AllplanGeo.Point3D(x_coord, 0, 0)

        return pol


    def create_web_polygon(self, build_ele, x_coord, height=0):
        """
        Create web polygon

        Args:
            build_ele:  the building element.
            x_coord:    x coordinate.
            height:     the height.

        Returns:
            polygon for web beam.
        """
        if height == 0:
            height = self.get_height(build_ele, x_coord)

        bottom_flange_width = build_ele.BottomFlangeWidth.value
        web_width = build_ele.WebWidth.value

        dy_bottom = (bottom_flange_width - web_width) / 2.

        pol = AllplanGeo.Polygon3D()

        pol += AllplanGeo.Point3D(x_coord, dy_bottom, 0)
        pol += AllplanGeo.Point3D(x_coord, dy_bottom, height)
        pol += AllplanGeo.Point3D(x_coord, dy_bottom + web_width, height)
        pol += AllplanGeo.Point3D(x_coord, dy_bottom + web_width, 0)
        pol += AllplanGeo.Point3D(x_coord, dy_bottom, 0)

        return pol


    def create_reinforcement(self, build_ele):
        """
        Create reinforcement elements

        Args:
            build_ele:  the building element.
        """

        #-----------------  Get the building element data

        length_left = build_ele.LengthLeft.value
        height_center = build_ele.HeightCenter.value

        offset_top_flange_left = build_ele.OffsetTopFlangeLeft.value

        length_full_beam_left = build_ele.LengthFullBeamLeft.value
        length_full_beam_web_left = build_ele.LengthFullBeamWebLeft.value

        shape_dist = 100.
        steel_grade = 4

        diameter1             = 12
        diameter2             = 12
        diameter3             = 12
        dia_full_beam_stirrup = 12
        diameter5             = 12
        diameter6             = 12
        diameter7             = 12
        diameter8             = 12

        concrete_cover = 25.

        bending_roller = 4


        #------------------ Rotation for the shape plane y/z to x/y

        rot_angle = AllplanGeo.Angle()

        rot_angle.SetDeg(-90)

        rot_mat = AllplanGeo.Matrix3D()

        rot_mat.Rotation(AllplanGeo.Line3D(
            AllplanGeo.Point3D(), AllplanGeo.Point3D(0, 0, 1000)), rot_angle)

        rot_angle.SetDeg(90)

        rot_mat.Rotation(AllplanGeo.Line3D(
            AllplanGeo.Point3D(), AllplanGeo.Point3D(1000, 0, 0)), rot_angle)


        #------------------ Create the shape in the bottom flange

        pol = self.create_iprofile_section_polygon(build_ele, length_full_beam_left)

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

        bar_props = ReinforcementShapeProperties.rebar(diameter1, bending_roller, steel_grade, -1,
                                                       AllplanReinf.BendingShapeType.Freeform)

        shape = ProfileShapeBuilder.create_bottom_flange_shape(pol, bar_props, concrete_cover_props)

        if shape.IsValid() is True:
            self.model_ele_list.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, shape,
                    AllplanGeo.Point3D(length_full_beam_left, 0, 0),
                    AllplanGeo.Point3D(length_left, 0, 0),
                    concrete_cover, concrete_cover, shape_dist,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance,
                    False))


        #------------------ Create the shape in the top flange

        pol = self.create_iprofile_section_polygon(build_ele, offset_top_flange_left)

        bar_props = ReinforcementShapeProperties.rebar(diameter2, bending_roller, steel_grade, -1,
                                                       AllplanReinf.BendingShapeType.Freeform)

        shape = ProfileShapeBuilder.create_top_flange_shape(pol, bar_props,concrete_cover_props)

        if shape.IsValid() is True:
            self.model_ele_list.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    2, shape,
                    AllplanGeo.Point3D(offset_top_flange_left, 0, 0),
                    AllplanGeo.Point3D(length_left,
                                       0,
                                       height_center - self.get_height(build_ele, offset_top_flange_left)),
                    concrete_cover, concrete_cover, shape_dist,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance,
                    False))


        #------------------ Create the stirrup in the web

        shape_props = ReinforcementShapeProperties.rebar(diameter3, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape1 = self.create_web_stirrup(build_ele,
                                         length_full_beam_left + length_full_beam_web_left,
                                         shape_props,
                                         concrete_cover_props)
        if shape1.IsValid() is True:
            shape2 = self.create_web_stirrup(build_ele, length_left - 25., shape_props, concrete_cover_props)

            if shape2.IsValid() is True:
                delta_x = length_left - offset_top_flange_left - 25.

                count = int(delta_x / shape_dist)

                self.model_ele_list.append(
                    AllplanReinf.BarPlacement(3, count + 1, shape1, shape2))


        #------------------ Create the stirrup in the support part of the full beam

        shape_props = ReinforcementShapeProperties.rebar(dia_full_beam_stirrup, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape1 = self.create_full_beam_stirrup(build_ele, rot_mat, 25., shape_props)

        if shape1.IsValid() is True:
            shape2 = self.create_full_beam_stirrup(build_ele, rot_mat, offset_top_flange_left, shape_props)

            if shape2.IsValid() is True:
                count = 3

                self.model_ele_list.append(
                    AllplanReinf.BarPlacement(4, count + 1, shape1, shape2))


        #------------------ Create the stirrup in the rest part of the full beam

        shape_props = ReinforcementShapeProperties.rebar(diameter5, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape1 = self.create_full_beam_stirrup(build_ele, rot_mat, offset_top_flange_left + shape_dist, shape_props)

        if shape1.IsValid() is True:
            shape2 = self.create_full_beam_stirrup(build_ele, rot_mat, length_full_beam_left, shape_props)

            if shape2.IsValid() is True:
                count = 10

                self.model_ele_list.append(AllplanReinf.BarPlacement(5, count + 1, shape1, shape2))


        #----------------- Create the stirrup in the section full beam - web

        shape_props = ReinforcementShapeProperties.rebar(diameter6, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape1 = self.create_full_beam_stirrup(build_ele, rot_mat, length_full_beam_left, shape_props)

        if shape1.IsValid() is True:
            shape2 = self.create_web_stirrup(build_ele, length_full_beam_left + length_full_beam_web_left,
                                             shape_props, concrete_cover_props)

            if shape2.IsValid() is True:
                count = int(length_full_beam_web_left / shape_dist)

                if count > 1:
                    poly1 = AllplanGeo.CreatePolyline3DFromIndex(shape1.GetShapePolyline(),shape2.GetShapePolyline(),
                                                                 1, count)

                    shape_start = AllplanReinf.BendingShape(poly1, shape1.GetBendingRoller(), diameter6,
                                                            steel_grade, -1,
                                                            AllplanReinf.BendingShapeType.Stirrup)

                    poly2 =  AllplanGeo.CreatePolyline3DFromIndex(shape1.GetShapePolyline(), shape2.GetShapePolyline(),
                                                                  count - 1, count)

                    shape_end = AllplanReinf.BendingShape(poly2, shape1.GetBendingRoller(), diameter6,
                                                          steel_grade, -1, AllplanReinf.BendingShapeType.Stirrup)

                    self.model_ele_list.append(
                        AllplanReinf.BarPlacement(6, count - 1, shape_start, shape_end))


        #----------------- Create the horizontal reinforcement in the support section

        self.create_horizontal_reinf_left(build_ele, diameter7, diameter8, dia_full_beam_stirrup,
                                          steel_grade, bending_roller)


    def create_horizontal_reinf_left(self, build_ele, diameter_bottom, diameter_top, dia_full_beam_stirrup,
                                     steel_grade, bending_roller):
        """
        Create left horizontal reinforcement

        Args:
            build_ele:        the building element.
            diameter_bottom:  the bottom diameter.
            diameter_top:     the top diameter.
            steel_grade:      the steel grade.
        """
        height_left         = build_ele.HeightLeft.value
        bottom_flange_width = build_ele.BottomFlangeWidth.value


        #----------------- links on the bottom side

        shape_props = ReinforcementShapeProperties.rebar(diameter_bottom, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.OpenStirrup)

        concrete_cover_props = ConcreteCoverProperties.left_right_bottom(25 + dia_full_beam_stirrup,
                                                                         25 + dia_full_beam_stirrup,
                                                                         25)

        shape = GeneralShapeBuilder.create_u_link(bottom_flange_width, 1000., RotationAngles(0, 0, -90),
                                                  shape_props, concrete_cover_props, -1)


        if shape.IsValid() is False:
            return

        z_cover_link = 50
        count        = 4
        link_dist    = 50

        from_point      = AllplanGeo.Point3D(0, bottom_flange_width, 0)
        direction_point = from_point + AllplanGeo.Point3D(0,0,1000.)

        placement = \
            LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(7, shape, from_point, direction_point,
                                                                            z_cover_link, link_dist, count)

        self.model_ele_list.append(placement)


        #----------------- links rest to the top

        shape_props = ReinforcementShapeProperties.rebar(diameter_top, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.OpenStirrup)

        shape = GeneralShapeBuilder.create_u_link(bottom_flange_width, 500., RotationAngles(0, 0, -90),
                                                  shape_props, concrete_cover_props, -1)

        if shape.IsValid() is False:
            return

        from_point = placement.GetEndPoint() + AllplanGeo.Point3D(0, 0, 100)
        to_point   = AllplanGeo.Point3D(0, bottom_flange_width, height_left)

        self.model_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_count(8, shape, from_point, to_point,
                                                                          0, z_cover_link, count))


    def create_full_beam_stirrup(self,
                                 build_ele,
                                 rot_mat,
                                 x_coord,
                                 shape_props):
        """
        Create full beam stirrup

        Args:
            build_ele:       the building element.
            rot_mat:         the rotation matrix.
            x_coord:         x coordinate.
            shape_props:     shape properties

        Returns:
            True/False for success.
        """
        pol = self.create_full_beam_polygon(build_ele, x_coord)

        shape_builder = AllplanReinf.ReinforcementShapeBuilder(rot_mat)

        shape_builder.AddPoints([(pol[1], 25.),
                                 (pol[2], 25.),
                                 (pol[3], 25.),
                                 (pol[4], 25.),
                                 (pol[1], 25.)])

        return shape_builder.CreateStirrup(shape_props, AllplanReinf.StirrupType.Normal)


    def create_web_stirrup(self,
                           build_ele,
                           x_coord,
                           shape_props,
                           concrete_cover_props):
        """
        Create web stirrup

        Args:
            build_ele:        the building element
            x_cooor´:         x coordinate
            shape_pros:       shape properties
            concrete_cover:   concrete cover

        Returns:
            the reinforcement shape.
        """
        pol = self.create_iprofile_section_polygon(build_ele, x_coord)

        return ProfileShapeBuilder.create_web_stirrup(pol, shape_props, concrete_cover_props)
