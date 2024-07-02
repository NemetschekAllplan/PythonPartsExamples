"""Example script showing the functionality of the function Intersecting
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
    from __BuildingElementStubFiles.IntersectingBuildingElement import IntersectingBuildingElement
else:
    IntersectingBuildingElement = BuildingElement


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

    return IntersectingInteractor(coord_input,
                                  build_ele_list,
                                  build_ele_composite,
                                  control_props_list)


class IntersectingInteractor(OperationExampleBaseInteractor):
    """ Intersecting interactor showing the example implementation
    and possibilities of the Intersecting function of the NemAll_Python_Geometry
    module. This function is capable to only tell, if two geometry objects
    intersect with each other or not. The interactor prompts the user to select
    at least two objects and directly after prints the result in the trace

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      elements to check for intersection
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

        #set initial values
        self.build_ele              = cast(IntersectingBuildingElement, build_ele_list[0])
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()
        self.post_element_selection = None


        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)


        # start element selection
        self.whitelist = [AllplanGeometry.Arc3D,
                          AllplanGeometry.Line2D,
                          AllplanGeometry.Polygon2D,
                          AllplanGeometry.BRep3D,
                          AllplanGeometry.Polyhedron3D,
                          AllplanGeometry.BSpline3D,
                          AllplanGeometry.Spline3D,
                          ]

        self.start_geometry_selection("Select first object to calculate intersection", self.whitelist)


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
                self.start_geometry_selection("Select first object", self.whitelist)
                return True


            # prompt for selecting second element, if only one selected
            if len(self.selected_elements) == 1:
                self.start_geometry_selection("Select second object", self.whitelist)
                return True


            # print a warning, if more than two elements selected
            if len(self.selected_elements) > 2:
                print("Selected more than two elements! Only first will be taken for the calculation.\n")


            # perform the intersection search
            self.find_intersection()


            # clear the memory and restart the selection
            self.selected_elements.clear()
            self.start_geometry_selection("See result in trace or select first object", self.whitelist)

        return True


    def find_intersection(self) -> None:
        """Find the intersection point between the first and the second element in the selected_elements
        list using Intersecting() function and print the results to the console"""

        first_geometry  = self.selected_elements[0].GetGeometry()
        second_geometry = self.selected_elements[1].GetGeometry()

        # print the result to the console
        print("\n------------- Intersection calculation --------------\n",
              "Calculating intersection between:\n",
              f"1. {self.selected_elements[0].GetDisplayName()} with geometry type of {type(first_geometry).__name__}",
              "and",
              f"2. {self.selected_elements[1].GetDisplayName()} with geometry type of {type(second_geometry).__name__}",
              sep="\n")


        # implementation of Intersecting() for two 2D lines or two 2D polygons
        # in this case, the function requires an additional tolerance argument

        if isinstance(first_geometry, (AllplanGeometry.Line2D, AllplanGeometry.Polygon2D)) and type(first_geometry) is type(second_geometry):
            intersecting = AllplanGeometry.Intersecting(first_geometry,
                                                        second_geometry,
                                                        self.build_ele.Tolerance.value)

            print("\nSelected geometries " +("" if intersecting else "do not ") + "intersect")


        # implementation of Intersecting() for other cases

        else:
            try:
                intersecting = AllplanGeometry.Intersecting(second_geometry, first_geometry)    #type: ignore

            except TypeError:
                print("\nIt is not possible to calculate the intersection between these objects",
                      "using NemAll_Python_Geometry.Intersecting")

            else:
                print("\nSelected geometries " +("" if intersecting else "do not ") + "intersect")

        print("\n----------------------------------------------------\n")
