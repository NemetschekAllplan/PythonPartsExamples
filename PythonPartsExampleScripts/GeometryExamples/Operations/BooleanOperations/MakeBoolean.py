"""Example script showing the implementation of the MakeBoolean function
"""
from typing import TYPE_CHECKING, Any, List, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService
from TypeCollections.ModelEleList import ModelEleList

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.MakeBooleanBuildingElement import MakeBooleanBuildingElement
else:
    MakeBooleanBuildingElement = BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_interactor(coord_input              : AllplanIFWInput.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : List[ControlProperties],
                      _modify_uuid_list        : List[str]) -> Any       :
    """Function for the interactor creation, called when PythonPart is initialized.

    Args:
        coord_input:               coordinate input
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return MakeBooleanInteractor(coord_input,
                                 build_ele_list,
                                 build_ele_composite,
                                 control_props_list)


class MakeBooleanInteractor(OperationExampleBaseInteractor):
    """ Make boolean interactor showing the example implementation of the MakeBoolean function
    from the NemAll_Python_Geometry module. This interactor prompt the user for selecting
    two polyhedrons in the drawing file. Directly after that it calculates the intersection,
    union and subtraction solids, creates them in the drawing file and deletes source elements.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      elements selected by the user to perform the boolean operation on
        elements_to_create:     elements resulting from the boolean operations
        post_element_selection: object containing selected elements after successful selection
    """

    def __init__(self,
                 coord_input        : AllplanIFWInput.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[ControlProperties])       :
        """ Constructor

        Args:
            coord_input:               coordinate input
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
        """

        # set initial values
        self.build_ele              = cast(MakeBooleanBuildingElement, build_ele_list[0])
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()
        self.elements_to_create     = ModelEleList()
        self.post_element_selection = None

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # show palette and start element selection
        self.whitelist = [AllplanGeometry.Polyhedron3D]
        self.start_geometry_selection("Select first solid", self.whitelist)

    def process_mouse_msg(self,
                          _mouse_msg: int,
                          _pnt      : AllplanGeometry.Point2D,
                          _msg_info : AllplanIFWInput.AddMsgInfo) -> bool:
        """ Called on each mouse message. A mouse message can be mouse movement, pressing a mouse button
        or releasing it.

        Args:
            _mouse_msg:  the mouse message (e.g. 512 - mouse movement)
            _pnt:        the input point in view coordinates
            _msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        if self.post_element_selection:
            self.selected_elements      += self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection  = None

            # do nothing, if nothing was selected
            if not self.selected_elements:
                return True

            # prompt for selecting the second solid, if only one selected
            if len(self.selected_elements) == 1:
                self.start_geometry_selection("Select second solid", self.whitelist)

            # print a warning if more than two solids were selected
            if len(self.selected_elements) > 2:
                print("\nWARNING: Selected more than two solids! Only first two will be calculated.")

            # perform boolean operations
            if len(self.selected_elements) >= 2:
                self.calculate_boolean()

                # clear the memory and restart selection
                self.selected_elements.clear()
                self.start_geometry_selection("Additional info in trace; select first solid", self.whitelist)

        return True

    def calculate_boolean(self) -> None:
        """Perform boolean operations using MakeBoolean function on the first two elements in the
        list of selected elements, print the results to the console. Then, if the corresponding
        option was selected by the user in the palette, create the model elements representing
        the resulting solids and delete the source elements in the current drawing file.
        """

        first_geometry : AllplanGeometry.Polyhedron3D = self.selected_elements[0].GetGeometry()
        second_geometry: AllplanGeometry.Polyhedron3D = self.selected_elements[1].GetGeometry()

        # ---------- perform the boolean operation

        error, intersection, union, subtraction1, subtraction2 = AllplanGeometry.MakeBoolean(first_geometry, second_geometry)

        # if the operation was successful, and the resulting elements
        # are valid polyhedrons, create the 3d elements in the drawing file
        if error == AllplanGeometry.eOK:
            if self.build_ele.CreateIntersectionSolid.value and intersection.IsValid():
                self.elements_to_create.append_geometry_3d(intersection, self.build_ele.IntersectionCommonProp.value)

            if self.build_ele.CreateUnionSolid.value and union.IsValid():
                self.elements_to_create.append_geometry_3d(union, self.build_ele.UnionCommonProp.value)

            if self.build_ele.CreateSubtraction1Solid.value and subtraction1.IsValid():
                self.elements_to_create.append_geometry_3d(subtraction1, self.build_ele.Subtraction1CommonProp.value)

            if self.build_ele.CreateSubtraction2Solid.value and subtraction2.IsValid():
                self.elements_to_create.append_geometry_3d(subtraction2, self.build_ele.Subtraction2CommonProp.value)

        self.create_and_delete_elements()

        # print the result to the console
        print("\n------------- MakeBoolean result ----------------\n",
              f"Boolean operation resulted in: {error}",
              "\nResulting polyhedrons types:",
              f"Intersection:\t\t{intersection.Type}",
              f"Union:\t\t\t{union.Type}",
              f"First minus second:\t{subtraction1.Type}",
              f"Second minus first:\t{subtraction2.Type}",
              "------------------------------------------------\n",
              sep="\n")

    def create_and_delete_elements(self) -> AllplanElementAdapter.BaseElementAdapterList:
        """Create new model elements from the geometries in the elements_to_create list
        and delete the elements in the selected_elements list from the current document.
        At the end clear the elements to create list.

        Returns:
            list of element adapters of the created elements
        """
        if len(self.selected_elements) > 0 and self.build_ele.DeleteSourceElements.value:
            AllplanBaseElements.DeleteElements(self.coord_input.GetInputViewDocument(),
                                               self.selected_elements)

        if len(self.elements_to_create) > 0:
            created_elements = AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                                                  AllplanGeometry.Matrix3D(),
                                                                  self.elements_to_create,
                                                                  modelUuidList = [],
                                                                  assoRefObj    = None)
            self.elements_to_create.clear()
            return created_elements

        return AllplanElementAdapter.BaseElementAdapterList()
