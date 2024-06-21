"""Example script showing the functionality of the function Touching
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
    from __BuildingElementStubFiles.TouchingBuildingElement import TouchingBuildingElement
else:
    TouchingBuildingElement = BuildingElement


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

    return TouchingInteractor(coord_input,
                              build_ele_list,
                              build_ele_composite,
                              control_props_list)


class TouchingInteractor(OperationExampleBaseInteractor):
    """ Touching Interactor showing the example implementation of the function
    Touching from the NemAll_Python_Geometry module capable of telling whether
    two geometry objects comes in contact with each other. The interactor prompts
    the user to select at least two geometry objects of type accepted by the
    function and performs the calculation. The result (touching or not) is
    printed in the console. If calculation could not be done, the information
    is printed also.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      elements selected for the calculation
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
        self.build_ele              = cast(TouchingBuildingElement, build_ele_list[0])
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()
        self.post_element_selection = None

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist =   [AllplanGeometry.Line2D,
                            AllplanGeometry.Polygon2D,
                            AllplanGeometry.Polyline2D,
                            ]
        self.start_geometry_selection("Select first object", self.whitelist)


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
            self.selected_elements      += self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection  = None


            # do nothing, if nothing was selected
            if not self.selected_elements:
                self.start_geometry_selection("Select first object", self.whitelist)
                return True


            # prompt for second element, if only one selected
            if len(self.selected_elements) == 1:
                self.start_geometry_selection("Select second object", self.whitelist)
                return True


            # print a warning if more than two elements selected
            if len(self.selected_elements) > 2:
                print("Selected more than two elements! Only first will be taken for the calculation.\n")


            # perform the touching check
            self.find_if_touching()


            # clear the memory and restart the selection
            self.selected_elements.clear()
            self.start_geometry_selection("See result in trace or select first object", self.whitelist)

        return True

    def find_if_touching(self):
        """Find out, if the first two elements in the list of selected elements are touching using
        the Touching() function and print the results in the console
        """

        first_geometry  = self.selected_elements[0].GetGeometry()
        second_geometry = self.selected_elements[1].GetGeometry()

        print("\n------------- Touching calculation --------------\n")

        print("Calculating if following objects touch:\n")
        print(f"1. {self.selected_elements[0].GetDisplayName()} with geometry type of {type(first_geometry).__name__}")
        print("and")
        print(f"2. {self.selected_elements[1].GetDisplayName()} with geometry type of {type(second_geometry).__name__}")

        try:
            touching = AllplanGeometry.Touching(first_geometry, second_geometry)

        except TypeError:
            print("\nNot possible to determine, whether these objects touch using NemAll_Python_Geometry.Touching\n",
                  "Possible combinations:",
                  "\tLine2D     <->   Line2D",
                  "\tPolygon2D  <->   Polygon2D",
                  "\tPolyline2D <->   Polygon2D",
                  sep="\n")
        else:
            print("\nSelected geometries " +("" if touching else "do not ") + "touch")

        print("\n----------------------------------------------------\n")
