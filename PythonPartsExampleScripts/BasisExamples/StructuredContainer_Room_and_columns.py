"""
Example Script for StructuredContainer
"""

import uuid

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElementAttributeList import BuildingElementAttributeList
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil

from Utilities.AttributeIdEnums import AttributeIdEnums

print('Load StructuredContainer_Room_and_columns.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        Object with the result data of the element creation
    """

    element = StructuredContainerExampleRoomColumns(doc)

    return element.create(build_ele)


def move_handle(build_ele  : BuildingElement,
                handle_prop: HandleProperties,
                input_pnt  : AllplanGeo.Point3D,
                doc        : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document

    Returns:
        Object with the result data of the element creation
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class StructuredContainerExampleRoomColumns():
    """
    Definition of class StructuredContainerExampleRoomColumns
    """

    obj_room_uuid = uuid.uuid5(uuid.NAMESPACE_OID, 'room')

    def __init__(self, doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class StructuredContainerExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = []
        self.structured_container_attrs = {}
        self.document       = doc


    @staticmethod
    def __create_cube3d(location: AllplanGeo.Point2D,
                        size    : float,
                        height  : float):
        """ Create the 3D cube

        Args:
            location: Rectangle global location
            size:     Size in X / Y direction
        """

        cube_3d = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(location.X, location.Y, 0), AllplanGeo.Point3D(location.X + size, location.Y + size, height))

        return cube_3d

    def create(self, build_ele: BuildingElement) -> CreateElementResult:
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            Object with the result data of the element creation
        """

        self.create_geometry(build_ele)

        pyp_util = PythonPartUtil()

        for key, attr_list in self.structured_container_attrs.items():
            pyp_util.add_attribute_list_to_sub_element_in_structured_container(attr_list, key) # <- Set attributes for sub element in StructuredContainer

        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(self.model_ele_list, self.handle_list)

    def create_column(self, com_prop, point, side_length, height):
        pnt1 = AllplanGeo.Point3D(point.X, point.Y, 0)
        pnt2 = AllplanGeo.Point3D(point.X + side_length, point.Y + side_length, height)

        column = AllplanGeo.Polyhedron3D.CreateCuboid(pnt1, pnt2)

        element = AllplanBasisElements.ModelElement3D(com_prop, column)
        return element

    def create_columns(self, com_prop, count, side_length, height):
        padding = 10

        for ind in range (0, count):
            column = self.create_column(com_prop,
                                        AllplanGeo.Point2D((side_length + padding) * ind + 10, (side_length + padding) * ind + 10),
                                        side_length,
                                        height)

            # creating an UUID for every column.
            # Note: on every update operation the UUID must be the same, for that purpose you can use UUID5
            name = 'column_' + str(ind)
            obj_uuid = uuid.uuid5(uuid.NAMESPACE_OID, name)

            ele = AllplanBasisElements.ElementNodeElement(com_prop, obj_uuid, [column])
            ele.SetParentID(StructuredContainerExampleRoomColumns.obj_room_uuid) # <-- every column has parent (obj_room_uuid)

            sub_element_attr_list = BuildingElementAttributeList()
            sub_element_attr_list.add_attribute(AttributeIdEnums.NAME, name)
            sub_element_attr_list.add_attribute(AttributeIdEnums.MATERIAL, name + " Material ")

            self.structured_container_attrs[obj_uuid] = sub_element_attr_list

            self.model_ele_list.append(ele)


    def create_room(self, com_prop, length, height):
        path = self.__create_cube3d(AllplanGeo.Point2D(0, 0), length, height)
        room_ele = AllplanBasisElements.ModelElement3D(com_prop, path)

        sub_element_attr_list = BuildingElementAttributeList()
        sub_element_attr_list.add_attribute(AttributeIdEnums.NAME, "Room")

        self.structured_container_attrs[StructuredContainerExampleRoomColumns.obj_room_uuid] = sub_element_attr_list

        ele = AllplanBasisElements.ElementNodeElement(
            com_prop,
            StructuredContainerExampleRoomColumns.obj_room_uuid, # <-- setting object id (obj_room_uuid) to the room.
            [ room_ele ])
        self.model_ele_list.append(ele)

    def create_geometry(self, build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #----------------- Extract palette parameter values

        width = float(build_ele.ColumnWidth.value)
        count = int(build_ele.NrColumns.value)
        room_height = int(build_ele.RoomHeight.value)

        padding = 10 * (count + 1)

        self.create_room(com_prop, width * count + padding, room_height)
        self.create_columns(com_prop, count, width, 1000)
