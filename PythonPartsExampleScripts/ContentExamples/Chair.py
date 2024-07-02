"""
Script for Chair
"""
import hashlib

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

print('Load Chair.py')

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

    chair = Chair(build_ele.SeatWidth.value, build_ele.SeatDepth.value, build_ele.Height.value,
                  build_ele.SeatThickness.value, build_ele.SeatHeight.value, build_ele.LegWidth.value)
    if not chair.is_valid():
        return ([], [])

    handle_list = chair.create_handles()
    views = [View2D3D ([AllplanBasisElements.ModelElement3D(common_props, chair.create())])]

    pythonpart = PythonPart ("Chair",
                             parameter_list = build_ele.get_params_list(),
                             hash_value = build_ele.get_hash(),
                             python_file = build_ele.pyp_file_name,
                             views = views)

    model_elem_list = pythonpart.create()

    return (model_elem_list, handle_list)

class Chair():
    """
    Definition of class Chair
    """

    def __init__(self, seat_width = 450.0, seat_depth = 450.0, height = 1200.,
                 seat_thickness = 30.0, seat_height = 600.0, leg_width = 40.0):
        """
        Initialisation of class Chair
        """
        self.m_height = height
        self.m_seat_width = seat_width
        self.m_seat_depth = seat_depth
        self.m_seat_thickness = seat_thickness
        self.m_seat_height = seat_height
        self.m_leg_width = leg_width
        self.m_chair = None

    def get_params_list(self):
        """
        Append all parameters as parameter list

        Returns: param list
        """
        param_list = []
        param_list.append ("LegWidth = %s\n" % self.m_leg_width)
        param_list.append ("Height = %s\n" % self.m_height)
        param_list.append ("SeatWidth = %s\n" % self.m_seat_width)
        param_list.append ("SeatDepth = %s\n" % self.m_seat_depth)
        param_list.append ("SeatThickness = %s\n" % self.m_seat_thickness)
        param_list.append ("SeatHeight = %s\n" % self.m_seat_height)
        return param_list

    def __repr__(self):
        return 'Chair(leg_width=%s, height=%s, seat_width=%s, seat_depth=%s,' \
            'seat_thickness=%s, seat_height=%s)\n' \
            % (self.m_leg_width, self.m_height, self.m_seat_width, self.m_seat_depth,
               self.m_seat_thickness, self.m_seat_height)

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
        return "Chair.py"

    def is_valid(self):
        """
        Check for valid values
        """
        if self.m_seat_width == 0 or self.m_seat_depth == 0 or self.m_height == 0:
            return False

        if self.m_seat_thickness == 0 or self.m_seat_height == 0 or self.m_leg_width == 0:
            return False

        return True

    def volume(self):
        """
        Calculate the volume in m³

        Returns:
            Calculated volume
        """
        err, volume, _, _ = AllplanGeo.CalcMass(self.m_chair)
        if err:
            return 0.0
        return volume / 1000000000

    def create(self):
        """
        Creation of one Chair
        """

        #------------------ Create the board

        point1 = AllplanGeo.Point3D(0, 0, self.m_seat_height - self.m_seat_thickness)
        point2 = AllplanGeo.Point3D(self.m_seat_width, self.m_seat_depth, self.m_seat_height)

        board = AllplanGeo.Polyhedron3D.CreateCuboid(point1, point2)


        #------------------ Create the leg

        frontleg = AllplanGeo.Polyhedron3D.CreateCuboid(self.m_leg_width,
                                                        self.m_leg_width,
                                                        self.m_height)
        backleg = AllplanGeo.Polyhedron3D.CreateCuboid(self.m_leg_width,
                                                       self.m_leg_width,
                                                       self.m_seat_height)

        #------------------ Add the legs

        err, self.m_chair = AllplanGeo.MakeUnion(board, backleg)

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair, AllplanGeo.Move(
                frontleg, AllplanGeo.Vector3D(0, self.m_seat_depth - self.m_leg_width, 0)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair, AllplanGeo.Move(
                backleg, AllplanGeo.Vector3D(self.m_seat_width - self.m_leg_width, 0, 0)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair, AllplanGeo.Move(
                frontleg, AllplanGeo.Vector3D(self.m_seat_width - self.m_leg_width,
                                              self.m_seat_depth - self.m_leg_width, 0)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair


        #------------------ Add the stiffener at the back side

        stiffheight = 100.
        stiffthickness = 20.
        stiffener = AllplanGeo.Polyhedron3D.CreateCuboid(self.m_seat_width,
                                                         stiffthickness,
                                                         stiffheight)

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair,
            AllplanGeo.Move(
                stiffener,
                AllplanGeo.Vector3D(0,
                                    self.m_seat_depth - stiffthickness,
                                    self.m_height - stiffheight)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        deltay = (self.m_height - stiffheight * 2 - self.m_seat_height) / 2 + stiffheight

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair,
            AllplanGeo.Move(
                stiffener,
                AllplanGeo.Vector3D(0,
                                    self.m_seat_depth - stiffthickness,
                                    self.m_height - stiffheight - deltay)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair,
            AllplanGeo.Move(
                stiffener,
                AllplanGeo.Vector3D(0,
                                    self.m_seat_depth - stiffthickness,
                                    self.m_seat_height - stiffheight - self.m_seat_thickness)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair


        #------------------ Add the stiffener at the left and right side

        stiffener = AllplanGeo.Polyhedron3D.CreateCuboid(
            AllplanGeo.Point3D(),
            AllplanGeo.Point3D(stiffthickness, self.m_seat_depth, stiffheight))

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair,
            AllplanGeo.Move(
                stiffener,
                AllplanGeo.Vector3D(0,
                                    0,
                                    self.m_seat_height - stiffheight - self.m_seat_thickness)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        err, self.m_chair = AllplanGeo.MakeUnion(
            self.m_chair,
            AllplanGeo.Move(
                stiffener,
                AllplanGeo.Vector3D(self.m_seat_width - stiffthickness,
                                    0,
                                    self.m_seat_height - stiffheight - self.m_seat_thickness)))

        if not GeometryValidate.polyhedron(err):
            return self.m_chair

        return self.m_chair

    def create_handles(self):
        """
        Create handles

        Returns:
            List of HandleProperties
        """

        #------------------ Create the handle

        handle_list = [HandleProperties("SeatXYHandle",
                                        AllplanGeo.Point3D(self.m_seat_width, self.m_seat_depth, 0),
                                        AllplanGeo.Point3D(0, 0, 0),
                                        [("SeatWidth", HandleDirection.x_dir),
                                         ("SeatDepth", HandleDirection.y_dir)],
                                        HandleDirection.xy_dir),
                       HandleProperties("LegWidth",
                                        AllplanGeo.Point3D(self.m_leg_width, 0, 0),
                                        AllplanGeo.Point3D(0, 0, 0),
                                        [("LegWidth", HandleDirection.x_dir)],
                                        HandleDirection.x_dir),
                       HandleProperties("SeatThickness",
                                        AllplanGeo.Point3D(0, 0, self.m_seat_height - self.m_seat_thickness),
                                        AllplanGeo.Point3D(0, 0, self.m_seat_height),
                                        [("SeatThickness", HandleDirection.z_dir)],
                                        HandleDirection.z_dir),
                       HandleProperties("SeatHeight",
                                        AllplanGeo.Point3D(0, self.m_seat_depth, self.m_height),
                                        AllplanGeo.Point3D(0, self.m_seat_depth, 0),
                                        [("Height", HandleDirection.z_dir)],
                                        HandleDirection.z_dir)
                      ]

        return handle_list


    def get_seat_width(self):
        """
        Get property for seat width

        Returns:
            the seat width.
        """

        return self.m_seat_width
