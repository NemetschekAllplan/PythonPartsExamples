"""Foo"""
from __future__ import annotations

import uuid

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
import PreviewSymbols

from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService
from PythonPartUtil import PythonPartUtil, View2D3D
from TypeCollections.ModelEleList import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.StructuredPythonPartBuildingElement import StructuredPythonPartBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def move_handle(build_ele  : BuildingElement,
                handle_prop: HandleProperties,
                input_pnt  : AllplanGeometry.Point3D,
                doc        : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop:handle properties
        input_pnt:  input point
        doc:        input document

    Returns:
        result of the element creation
    """
    HandlePropertiesService.update_property_value(build_ele, handle_prop, input_pnt)

    return create_element(build_ele, doc)


def create_element(build_ele:   BuildingElement,
                   _doc:        AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Function for the element creation

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        created element result
    """
    structured_pythonpart = StructuredPythonPart(build_ele)

    return CreateElementResult(structured_pythonpart.create_pythonpart(),
                               structured_pythonpart.handles,
                               preview_symbols= structured_pythonpart.create_preview_texts())


class StructuredPythonPart():
    """Representation of a structured PythonPart containing several boxes

    Each box is an individual element inside the PythonPart container with it's own attributes and common properties.
    The number of the boxes can be changed without losing the attributes of existing boxes.
    The structure of the PythonPart is flat; the PythonPart itself is the parent element for all the boxes.

    Args:
        build_ele:  the building element containing the parameter and their values
                    input by the user in the property palette
    """
    def __init__(self, build_ele: BuildingElement):
        """Initialize"""

        self.build_ele = build_ele

        # generate the base points for the boxes along the X axis based on count and spacing
        base_pnts = [AllplanGeometry.Point3D(build_ele.Spacing.value * i, 0.0, 0.0) for i in range(build_ele.BoxCount.value)]

        # create a list of boxes
        self.boxes = BoxList(map(Box,
                                 range(build_ele.BoxCount.value),
                                 build_ele.Length.value,
                                 build_ele.Width.value,
                                 build_ele.Height.value,
                                 base_pnts,
                                 build_ele.CommonProps.value))

        # create nested structure
        if self.build_ele.CreateNestedHierarchy.value:
            self.create_nested_hierarchy()

            if self.has_circular_reference():   # check for circular reference
                self.build_ele.ParentElements.value = ["None"]*3
                AllplanUtil.ShowMessageBox("You just created a circular hierarchy. Please define different parent <-> child relationships.",
                                           AllplanUtil.MB_OK)

        # create list containing handles of only the selected boxes
        self.handles: list[HandleProperties] = []

        for box in self.boxes:
            if box.id in set(i for rng in self.build_ele.BoxIndex.value for i in range(rng[0]-1, rng[1])):  # type: ignore
                self.handles.extend(box.handles)

        # define attributes of the container as a whole
        self.attributes = BuildingElementAttributeList()
        self.attributes.add_attribute(507, "Structured PythonPart")   # name


    def create_bounding_box(self) -> ModelEleList:
        """Create a bounding box, bounding all the individual boxes

        Returns:
            list containing the bounding box
        """
        min_max = AllplanGeometry.MinMax3D()

        for box in self.boxes:
            for vertex in box.geometry.GetVertices():
                AllplanGeometry.AddToMinMax(min_max, vertex)

        min_max_cube = AllplanGeometry.Polyhedron3D.CreateCuboid(min_max)

        model_ele_list = ModelEleList()
        model_ele_list.append_geometry_3d(min_max_cube)

        return model_ele_list

    def create_pythonpart(self) -> list:
        """Create the PythonPart as a structured container

        Returns:
            list of model elements representing a PythonPart
        """
        if not self.boxes:
            return []

        pyp_util = PythonPartUtil()

        #------- attributes
        pyp_util.add_attribute_list(self.attributes)    # append container-related attributes to the whole container

        for box in self.boxes:
            pyp_util.add_attribute_list_to_sub_element_in_structured_container(box.attributes, box.uuid)  # append box-related attributes to each box

        #------- PythonPart views
        # when option "create simplified geometry" is checked, create two views: one with all the boxes, one with only bounding box
        if self.build_ele.CreateBoundingBox.value:
            pyp_util.add_view(View2D3D([box.element_node for box in self.boxes], end_scale = self.build_ele.BoundingBoxFromScale.value))
            pyp_util.add_view(View2D3D(self.create_bounding_box(), start_scale = self.build_ele.BoundingBoxFromScale.value))
        else:
            pyp_util.add_pythonpart_view_2d3d([box.element_node for box in self.boxes])

        return pyp_util.create_pythonpart(self.build_ele)

    def create_nested_hierarchy(self):
        """Organize the boxes in a nested hierarchy based on the relationships set by the user
        in the property palette
        """
        for box in self.boxes:
            if (parent_box_id := eval(self.build_ele.ParentElements.value[box.id].replace("Box ", ""))) is None:
                continue

            box.set_parent_box(self.boxes[parent_box_id])

    def create_preview_texts(self) -> PreviewSymbols.PreviewSymbols:
        """Create preview texts showing the Box id in the middle of the box for a better identification

        Returns:
            Preview texts
        """
        preview_symbols = PreviewSymbols.PreviewSymbols()
        for box in self.boxes:
            _, _, _, reference_pnt = AllplanGeometry.CalcMass(box.geometry)
            preview_symbols.add_text(text           = str(box.id),
                                    reference_point = reference_pnt,
                                    ref_pnt_pos     = PreviewSymbols.TextReferencePointPosition.CENTER_CENTER,
                                    height          = 50.0,
                                    color           = 6,
                                    rotation_angle  = AllplanGeometry.Angle())
        return preview_symbols

    def has_circular_reference(self) -> bool:
        """Check if there is a circular reference in the hierarchy of elements

        Returns:
            True if there is a circular reference, False otherwise
        """
        visited: set[Box] = set()  # track of visited elements to detect cycles

        for current_box in self.boxes:
            while current_box is not None:
                if current_box in visited:
                    # Circular hierarchy found
                    return True

                visited.add(current_box)

                # Move up to the parent
                try:
                    parent_uuid = current_box.element_node.GetParentID()
                    current_box = self.boxes.get_by_uuid(parent_uuid)
                except KeyError:
                    current_box = None

            visited.clear()

        # If we reach here, there is no circular hierarchy
        return False



class Box():
    """Representation of a box

    Args:
        box_id:         identification number of the box
        length:         X-dimension
        width:          Y-dimension
        height:         Z-dimension
        base_pnt:       bottom-left point of the box in global coordinate system
        common_props:   common properties (pen, stroke, color, etc...)
    """

    def __init__(self,
                 box_id      : int,
                 length      : float,
                 width       : float,
                 height      : float,
                 base_pnt    : AllplanGeometry.Point3D,
                 common_props: AllplanBaseElements.CommonProperties = AllplanBaseElements.CommonProperties() ):
        """Initialize"""

        self.length       = length
        self.width        = width
        self.height       = height
        self.base_pnt     = base_pnt
        self.id           = box_id
        self.common_props  = common_props

        #------- geometry
        self.geometry = AllplanGeometry.Polyhedron3D.CreateCuboid(AllplanGeometry.AxisPlacement3D(self.base_pnt),
                                                                  self.length,
                                                                  self.width,
                                                                  self.height)

        #------- attributes
        _err, volume, surface, _cg_point = AllplanGeometry.CalcMass(self.geometry)

        self.attributes = BuildingElementAttributeList()
        self.attributes.add_attribute(507, f"Box_{self.id}")
        self.attributes.add_attribute(220, self.length / 1e3)
        self.attributes.add_attribute(221, self.width / 1e3)
        self.attributes.add_attribute(222, self.height / 1e3)
        self.attributes.add_attribute(722, surface / 1e6)
        self.attributes.add_attribute(223, volume / 1e9)

        #------- handles
        self.handles = [
            # handle for controlling the X-dimension
            HandleProperties(f"Length_{self.id}",
                             AllplanGeometry.Point3D(self.length,0,0) + self.base_pnt,
                             self.base_pnt,
                             [HandleParameterData("Length", HandleParameterType.X_DISTANCE, list_index = self.id )],
                             HandleDirection.X_DIR),

            # handle for controlling the Y-dimension
            HandleProperties(f"Width_{self.id}",
                             AllplanGeometry.Point3D(0, self.width,0) + self.base_pnt,
                             self.base_pnt,
                             [HandleParameterData("Width", HandleParameterType.Y_DISTANCE, list_index = self.id)],
                             HandleDirection.Y_DIR),

            # handle for controlling the Z-dimension
            HandleProperties(f"Height_{self.id}",
                             AllplanGeometry.Point3D(0,0, self.height) + self.base_pnt,
                             self.base_pnt,
                             [HandleParameterData("Height", HandleParameterType.Z_DISTANCE, list_index = self.id)],
                             HandleDirection.Z_DIR),

            # handle for controlling all three dimensions
            HandleProperties(f"XYZ_{self.id}", AllplanGeometry.Point3D(self.length, self.width, self.height) + self.base_pnt,
                             self.base_pnt,
                             [HandleParameterData("Length", HandleParameterType.X_DISTANCE, False, list_index = self.id),
                              HandleParameterData("Width",  HandleParameterType.Y_DISTANCE, False, list_index = self.id),
                              HandleParameterData("Height", HandleParameterType.Z_DISTANCE, False, list_index = self.id)],
                             HandleDirection.XYZ_DIR),
        ]

        #------- model elements
        self.model_elements = ModelEleList(self.common_props)
        self.model_elements.append_geometry_3d(self.geometry)

        #------- element node
        self.element_node = AllplanBasisElements.ElementNodeElement(self.common_props,
                                                                    self.uuid,                    # type: ignore
                                                                    self.model_elements)

    def set_parent_box(self, parent_box: Box):
        """Set another box as a parent element of this box

        Args:
            parent_box: box to be set as parent of this box
        """
        self.element_node.SetParentID(parent_box.uuid)

    @property
    def uuid(self) -> uuid.UUID:
        """Property with UUID of the box

        The UUID is generated based on a namespace and a string e.g., 'Box_1' deterministically.
        This means, that the UUID for 'Box_1' will always be the same, each time the script is executed.

        Returns:
            UUID of the box
        """
        return uuid.uuid5(uuid.NAMESPACE_OID, f'Box_{self.id}')

class BoxList(list):
    """List of boxes with additional methods for easier access to the boxes"""

    def get_by_uuid(self, box_uuid: uuid.UUID) -> Box:
        """Get the box with the given UUID

        Args:
            box_uuid: UUID of the box

        Returns:
            Box with the given UUID

        Raises:
            KeyError: if the box with the given UUID is not found
        """
        for box in self:
            if box.uuid == box_uuid:
                return box

        raise KeyError(f"Box with UUID {box_uuid} not found")
