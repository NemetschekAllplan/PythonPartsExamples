"""Example script showing the usage of the IntersectionCalculus function
"""
from typing import TYPE_CHECKING, Any, List, cast

import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IntersectionCalculusBuildingElement import IntersectionCalculusBuildingElement
else:
    IntersectionCalculusBuildingElement = BuildingElement


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

    return IntersectionCalculusInteractor(coord_input,
                                          build_ele_list,
                                          build_ele_composite,
                                          control_props_list)


class IntersectionCalculusInteractor(OperationExampleBaseInteractor):
    """ Intersection Calculus Interactor showing the example implementation
    of the function IntersectionCalculus from the NemAll_Python_Geometry module
    capable of finding intersection points between two geometry objects.
    The interactor prompts the user to select at least two geometry objects
    and directly after that performs the calculation and prints the result in the
    console. The function IntersectionCalculus accepts all types of geometries,
    but do not return result in every case. The purpose of this example is to
    offer a possibility to experiment and see, when the result is found.
    Therefore the selection is not filtered to any type of geometry.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        elements:               elements selected for the calculation
        post_element_selection: object containing selected elements after successful selection
    """

    def __init__(self,
                 coord_input:                AllplanIFWInput.CoordinateInput,
                 build_ele_list:             List[BuildingElement],
                 build_ele_composite:        BuildingElementComposite,
                 control_props_list:         List[ControlProperties]):
        """ Constructor

        Args:
            coord_input:               coordinate input
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
        """

        #set initial values
        self.build_ele              = cast(IntersectionCalculusBuildingElement, build_ele_list[0])
        self.post_element_selection = None
        self.elements               = AllplanElementAdapter.BaseElementAdapterList()

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.start_geometry_selection("Select first object")


    def process_mouse_msg(self,
                          _mouse_msg: int,
                          _pnt      : AllplanGeometry.Point2D,
                          _msg_info : AllplanIFWInput.AddMsgInfo) -> bool:
        """ Called on each mouse message. A mouse message can be mouse movement, pressing a mouse button
        or releasing it.

        Args:
            _mouse_msg: the mouse message (e.g. 512 - mouse movement)
            _pnt:       the input point in view coordinates
            _msg_info:  additional message info.

        Returns:
            True/False for success.
        """

        if self.post_element_selection:
            self.elements               += self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection  = None


            # do nothing, if nothing was selected
            if not self.elements:
                self.start_geometry_selection("Select first object")
                return True


            # prompt for selecting second element, if only one selected
            if len(self.elements) == 1:
                self.start_geometry_selection("Select second object")
                return True


            # print a warning, if more than two geometries were selected
            if len(self.elements) > 2:
                print("\nWARNING: More than two elements selected! Only first two are taken for the intersection calculation.\n")


            # calculate the intersection
            self.calculate_intersection()


            # clear the memory and restart the selection
            self.elements.clear()
            self.start_geometry_selection("See result in trace or select first object")

        return True

    def calculate_intersection(self) -> None:
        """Calculate the intersection between first two elements in the self.elements list
        using the IntersectionCalculus() and prints the result in the console
        """

        intersecting, points = AllplanGeometry.IntersectionCalculus(ele1         = self.elements[0].GetGeometry(),
                                                                    ele2         = self.elements[1].GetGeometry(),
                                                                    eps          = self.build_ele.Tolerance.value,
                                                                    maxSolutions = self.build_ele.MaxSolutionNumber.value)

        print("\n------------- Intersection calculation ----------------\n")

        print("Intersection between:",
              f"1. {self.elements[0].GetDisplayName()} with geometry type of {type(self.elements[0].GetGeometry()).__name__}",
              "and",
              f"2. {self.elements[1].GetDisplayName()} with geometry type of {type(self.elements[1].GetGeometry()).__name__}\n",
              "Result:",
              f"Found {len(points)} intersection(s) at:" if intersecting else "No intersection found",
              sep= "\n")

        for point in points:
            print(f"X: {round(point.X,2)}\tY: {round(point.Y,2)}\tZ {round(point.Z,2)}")

        print("-------------------------------------------------------\n")
