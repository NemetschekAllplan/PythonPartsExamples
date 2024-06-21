"""
Script for Table
"""
import hashlib

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart


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
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    del doc # param not needed

    common_props = AllplanBaseElements.CommonProperties()
    common_props.GetGlobalProperties()

    table = Table(build_ele.TableLength.value, build_ele.TableWidth.value, build_ele.TableHeight.value,
                  build_ele.BoardThickness.value, build_ele.LegWidth.value, build_ele.XExcessLength.value, build_ele.YExcessLength.value)
    if not table.is_valid():
        return ([], [])

    handle_list = table.create_handles()
    table_views = [View2D3D ([AllplanBasisElements.ModelElement3D(common_props, table.create())])]

    pythonpart = PythonPart ("Table",
                             parameter_list = build_ele.get_params_list(),
                             hash_value = build_ele.get_hash(),
                             python_file = build_ele.pyp_file_name,
                             views = table_views)

    model_elem_list = pythonpart.create()

    return (model_elem_list, handle_list)


class Table():
    """
    Definition of class Table
    """

    def __init__(self, length = 1000.0, width = 500.0, height = 100.0,
                 board_thickness = 20.0, leg_width = 40.0,
                 x_excess_length = 100.0, y_excess_length = 100.0):
        """
        Initialisation of class Table
        """
        self.length = length
        self.width = width
        self.height = height
        self.board_thickness = board_thickness
        self.leg_width = leg_width
        self.x_excess_length = x_excess_length
        self.y_excess_length = y_excess_length
        self.table = None

    def get_params_list(self):
        """
        Append all parameters as parameter list

        Returns: param list
        """
        param_list = []
        param_list.append ("Length = %s\n" % self.length)
        param_list.append ("Width = %s\n" % self.width)
        param_list.append ("Height = %s\n" % self.height)
        param_list.append ("BoardThickness = %s\n" % self.board_thickness)
        param_list.append ("LegWidth = %s\n" % self.leg_width)
        param_list.append ("XExcessLength = %s\n" % self.x_excess_length)
        param_list.append ("YExcessLength = %s\n" % self.y_excess_length)
        return param_list

    def __repr__(self):
        return 'Table(length=%s, width=%s, height=%s, board_thickness=%s,' \
            'leg_width=%s, x_excess_length=%s, y_excess_length=%s)\n' \
            % (self.length, self.width, self.height, self.board_thickness,
               self.leg_width, self.x_excess_length, self.y_excess_length)

    def hash (self):
        """
        Calculate hash value for script

        Returns:
            Hash string
        """
        param_string = self.__repr__()
        hash_val = hashlib.sha224(param_string.encode('utf-8')).hexdigest()
        return hash_val

    def filename(self):
        """
        Python script filename

        Returns:
            Script filename
        """
        return "Table.py"

    def is_valid(self):
        """
        Check for valid values
        """
        if self.length == 0 or self.width == 0 or self.height == 0:
            return False

        if self.board_thickness == 0 or self.leg_width == 0:
            return False

        return True

    def volume(self):
        """
        Calculate the volume in m³

        Returns:
            Calculated volume
        """
        err, volume, _, _ = AllplanGeo.CalcMass(self.table)
        if err:
            return 0.0
        return volume / 1000000000

    def create(self):
        """
        Create a Table
        """
        if not self.is_valid():
            return []


        #------------------ Create the board
        point1 = AllplanGeo.Point3D(0, 0, self.height - self.board_thickness)
        point2 = AllplanGeo.Point3D(self.length, self.width, self.height)
        board = AllplanGeo.Polyhedron3D.CreateCuboid(point1, point2)

        #------------------ Create the leg
        leg = AllplanGeo.Polyhedron3D.CreateCuboid(self.leg_width, self.leg_width, self.height)

        #------------------ Add the legs
        err, table = AllplanGeo.MakeUnion(
            board, AllplanGeo.Move(leg, AllplanGeo.Vector3D(self.x_excess_length, self.y_excess_length, 0)))

        if not GeometryValidate.polyhedron(err):
            return []

        err, table = AllplanGeo.MakeUnion(
            table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(self.x_excess_length,
                                                            self.width - self.y_excess_length - self.leg_width,
                                                            0)))

        if not GeometryValidate.polyhedron(err):
            return []

        err, table = AllplanGeo.MakeUnion(
            table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(self.length - self.x_excess_length - self.leg_width,
                                                            self.y_excess_length,
                                                            0)))

        if not GeometryValidate.polyhedron(err):
            return []

        err, table = AllplanGeo.MakeUnion(
            table, AllplanGeo.Move(leg, AllplanGeo.Vector3D(self.length - self.x_excess_length - self.leg_width,
                                                            self.width - self.y_excess_length - self.leg_width,
                                                            0)))

        if not GeometryValidate.polyhedron(err):
            return []

        common_props = AllplanBaseElements.CommonProperties()
        common_props.GetGlobalProperties()

        self.table = table
        return self.table

    def create_handles(self):
        """
        Create handles

        Returns:
            List of HandleProperties
        """

        #------------------ Create the handle

        handle_list = [HandleProperties("TableXYHandle",
                                        AllplanGeo.Point3D(self.length, self.width, self.height),
                                        AllplanGeo.Point3D(0, 0, 0),
                                        [("TableLength", HandleDirection.x_dir),
                                         ("TableWidth", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir),
                       HandleProperties("LegWidth",
                                        AllplanGeo.Point3D(self.x_excess_length + self.leg_width, self.y_excess_length, 0),
                                        AllplanGeo.Point3D(self.x_excess_length, self.y_excess_length, 0),
                                        [("LegWidth", HandleDirection.x_dir)],
                                        HandleDirection.x_dir),
                       HandleProperties("BoardThickness",
                                        AllplanGeo.Point3D(0, 0, self.height - self.board_thickness),
                                        AllplanGeo.Point3D(0, 0, self.height),
                                        [("BoardThickness", HandleDirection.z_dir)],
                                        HandleDirection.z_dir),
                       HandleProperties("XExcessLength",
                                        AllplanGeo.Point3D(self.x_excess_length, 0, 0),
                                        AllplanGeo.Point3D(0, 0, 0),
                                        [("XExcessLength", HandleDirection.x_dir)],
                                        HandleDirection.x_dir),
                       HandleProperties("YExcessLength",
                                        AllplanGeo.Point3D(0, self.y_excess_length, 0),
                                        AllplanGeo.Point3D(0, 0, 0),
                                        [("YExcessLength", HandleDirection.y_dir)],
                                        HandleDirection.y_dir),
                      ]

        return handle_list

    def create_chair_positions(self, chair_seat_width = 450.):
        """
        Create a list of transformations to position all chairs around the table

        Returns:
            List of Matrix3D transformations
        """

        trans_list = list()

        #------------------ Create the chairs for the front

        rotation_angle = AllplanGeo.Angle()
        rotation_angle.SetDeg(180)
        rotation_matrix = AllplanGeo.Matrix3D()
        rotation_matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(),
                                                   AllplanGeo.Point3D(0, 0, 1000)),
                                 rotation_angle)

        #------------------ Add the chairs at the front and back

        seat_size = chair_seat_width + 400.

        chair_count = int(self.length / seat_size)

        if chair_count > 0:
            seat_size_real = self.length / chair_count

            deltax = (seat_size_real - chair_seat_width) / 2.
            deltax1 = deltax + chair_seat_width
            deltay = 200

            for _ in range(chair_count):
                trans_matrix = AllplanGeo.Matrix3D()
                trans_matrix.Translate(AllplanGeo.Vector3D(deltax, self.width + deltay, 0))

                trans_list.append(trans_matrix)

                trans_matrix = AllplanGeo.Matrix3D(rotation_matrix)
                trans_matrix.Translate(AllplanGeo.Vector3D(deltax1, -deltay, 0))

                trans_list.append(trans_matrix)

                deltax += seat_size_real
                deltax1 += seat_size_real


        #------------------ Transform the chair for the left and right

        rotation_angle.SetDeg(90)

        rotation_matrix = AllplanGeo.Matrix3D()

        rotation_matrix.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(),
                                                   AllplanGeo.Point3D(0, 0, 1000)),
                                 rotation_angle)

        rotation_angle.SetDeg(-90)

        rotation_matrix1 = AllplanGeo.Matrix3D()

        rotation_matrix1.Rotation(AllplanGeo.Line3D(AllplanGeo.Point3D(),
                                                    AllplanGeo.Point3D(0, 0, 1000)),
                                  rotation_angle)


        #------------------ Add the chair at the left and right table

        chair_count = int(self.width / seat_size)

        if chair_count > 0:
            seat_size_real = self.width / chair_count

            deltay = (seat_size_real - chair_seat_width) / 2.
            deltay1 = deltay + chair_seat_width
            deltax = 200

            for _ in range(chair_count):
                trans_matrix = AllplanGeo.Matrix3D(rotation_matrix)
                trans_matrix.Translate(AllplanGeo.Vector3D(-deltax, deltay, 0))

                trans_list.append(trans_matrix)

                trans_matrix = AllplanGeo.Matrix3D(rotation_matrix1)
                trans_matrix.Translate(AllplanGeo.Vector3D(self.length + deltax, deltay1, 0))

                trans_list.append(trans_matrix)

                deltay += seat_size_real
                deltay1 += seat_size_real

        return trans_list
