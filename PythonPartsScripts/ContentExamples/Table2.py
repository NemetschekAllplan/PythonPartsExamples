"""
Script for Table
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

from ContentExamples.Chair import Chair

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


print('Load Table2.py')


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


def create_element(build_ele, doc):
    """
    Create table element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    del doc


    #------------------ Set the values

    table_length_long = build_ele.TableLengthLong.value
    table_length_short = build_ele.TableLengthShort.value
    table_width_long = build_ele.TableWidthLong.value
    table_width_short = build_ele.TableWidthShort.value
    table_height = build_ele.TableHeight.value
    leg_width = build_ele.LegWidth.value
    excess_length = build_ele.ExcessLength.value

    if table_length_long == 0  or table_length_short == 0  or  table_width_long == 0  or  table_width_short == 0:
        return[]
    if table_height == 0  or  build_ele.BoardThickness.value == 0  or  leg_width == 0:
        return[]


    #------------------ Create the board

    point1 = AllplanGeo.Point3D(0, 0, table_height - build_ele.BoardThickness.value)
    point2 = AllplanGeo.Point3D(table_width_long, table_length_short, table_height)
    point3 = AllplanGeo.Point3D(table_width_short, table_length_long, table_height)

    board_part1 = AllplanGeo.Polyhedron3D.CreateCuboid(point1, point2)
    board_part2 = AllplanGeo.Polyhedron3D.CreateCuboid(point1, point3)

    err, board = AllplanGeo.MakeUnion(board_part1, board_part2)

    if not GeometryValidate.polyhedron(err):
        return []


    #------------------ Create the leg

    leg = AllplanGeo.Polyhedron3D.CreateCuboid(leg_width, leg_width, table_height)


    #------------------ Add the legs at the sides


    err, table = AllplanGeo.MakeUnion(
        board, AllplanGeo.Move(leg, AllplanGeo.Vector3D(excess_length, excess_length, 0)))

    if not GeometryValidate.polyhedron(err):
        return []

    err, table = AllplanGeo.MakeUnion(
        table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(excess_length,
                                                        table_length_long - excess_length - leg_width,
                                                        0)))

    if not GeometryValidate.polyhedron(err):
        return []

    err, table = AllplanGeo.MakeUnion(
        table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(table_width_long - excess_length - leg_width,
                                                        excess_length,
                                                        0)))

    if not GeometryValidate.polyhedron(err):
        return []

    err, table = AllplanGeo.MakeUnion(
        table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(table_width_short - excess_length - leg_width,
                                                        table_length_short - excess_length - leg_width,
                                                        0)))

    if not GeometryValidate.polyhedron(err):
        return []

    err, table = AllplanGeo.MakeUnion(
        table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(table_width_long - excess_length - leg_width,
                                                        table_length_short - excess_length - leg_width,
                                                        0)))

    if not GeometryValidate.polyhedron(err):
        return []

    err, table = AllplanGeo.MakeUnion(
        table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(table_width_short - excess_length - leg_width,
                                                        table_length_long - excess_length - leg_width,
                                                        0)))


    if not GeometryValidate.polyhedron(err):
        return []

    common_props = AllplanBaseElements.CommonProperties()
    common_props.GetGlobalProperties()
    model_elem_list = [AllplanBasisElements.ModelElement3D(common_props, table)]




    #------------------ Create the chairs for the front

    chair_element = Chair()

    chair_polyhedron = chair_element.create()

    rotation_angle = AllplanGeo.Angle()

    rotation_angle.SetDeg(180)

    rotation_matrix = AllplanGeo.Matrix3D()

    rotation_matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(),
                                               AllplanGeo.Point3D(0, 0, 1000)),
                             rotation_angle)

    trans_list = list()


    #------------------ Add the chairs at the front

    seat_size = chair_element.get_seat_width() + 400.

    chair_count = int(table_width_long / seat_size)

    if chair_count > 0:
        seat_size_real = table_width_long / chair_count

        deltax = (seat_size_real - chair_element.get_seat_width()) / 2.
        deltax1 = deltax + chair_element.get_seat_width()
        deltay = 200

        for _ in range(chair_count):
            trans_matrix = AllplanGeo.Matrix3D()

            trans_matrix = AllplanGeo.Matrix3D(rotation_matrix)
            trans_matrix.Translate(AllplanGeo.Vector3D(deltax1, -deltay, 0))

            trans_list.append(trans_matrix)

            deltax1 += seat_size_real




    #------------------ Transform the chair for the left

    rotation_angle.SetDeg(90)

    rotation_matrix = AllplanGeo.Matrix3D()

    rotation_matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(),
                                               AllplanGeo.Point3D(0, 0, 1000)),
                             rotation_angle)


    #------------------ Add the chairs at the left

    chair_count = int(table_length_long / seat_size)

    if chair_count > 0:
        seat_size_real = table_length_long / chair_count

        deltay = (seat_size_real - chair_element.get_seat_width()) / 2.
        deltax = 200

        for _ in range(chair_count):
            trans_matrix = AllplanGeo.Matrix3D(rotation_matrix)
            trans_matrix.Translate(AllplanGeo.Vector3D(-deltax, deltay, 0))

            trans_list.append(trans_matrix)

            deltay += seat_size_real

    model_element = AllplanBasisElements.ModelElement3D(common_props, chair_polyhedron)

    model_element.SetTransformationList(trans_list)

    model_elem_list.append(model_element)


    #------------------ Create the handles

    handle_list = [HandleProperties("TableXYHandle",
                                    AllplanGeo.Point3D(table_width_long, table_length_long, table_height),
                                    AllplanGeo.Point3D(0, 0, 0),
                                    [("TableLengthLong", HandleDirection.y_dir),
                                     ("TableWidthLong", HandleDirection.x_dir)],
                                    HandleDirection.xy_dir)
                  ]

    return (model_elem_list, handle_list)
