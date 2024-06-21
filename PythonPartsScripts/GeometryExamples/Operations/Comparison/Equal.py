"""Example script showing the implementation of the Comparison.Equal method
comparing two geometries with tolerance
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
    from __BuildingElementStubFiles.EqualBuildingElement import EqualBuildingElement
else:
    EqualBuildingElement = BuildingElement


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

    return EqualInteractor(coord_input,
                      build_ele_list,
                      build_ele_composite,
                      control_props_list)


class EqualInteractor(OperationExampleBaseInteractor):
    """ Equal interactor showing the example implementation of the Comparison.Equal method
    from the NemAll_Python_Geometry module. This method determines, if two geometries are
    identical with a given tolerance. The Interactor prompts the user to select at least
    two objects. Both must be of the same type. After selection, the objects are compared.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      list of elements selected by the user
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
        self.post_element_selection = None
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()
        self.build_ele              = cast(EqualBuildingElement, build_ele_list[0])

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)


        # show palette and start element selection
        self.whitelist =   [AllplanGeometry.Arc2D,
                            AllplanGeometry.Arc3D,
                            AllplanGeometry.BSpline2D,
                            AllplanGeometry.BSpline3D,
                            AllplanGeometry.Clothoid2D,
                            AllplanGeometry.Line2D,
                            AllplanGeometry.Line3D,
                            AllplanGeometry.Path3D,
                            AllplanGeometry.Point2D,
                            AllplanGeometry.Point3D,
                            AllplanGeometry.Polyline3D,
                            AllplanGeometry.Spline2D,
                            AllplanGeometry.Spline3D,
                            ]


        self.start_geometry_selection("Select first object to compare", self.whitelist)

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
                self.start_geometry_selection("Select first object to compare",self.whitelist)
                return True


            # check, if all selected elements have the same type
            geo_types = [type(element.GetGeometry()) for element in self.selected_elements]


            # if two objects of different geometry type were selected, do nothing and restart the selection
            if len(set(geo_types)) > 1:
                print("\nBoth objects to compare must have the same geometry type!")
                self.selected_elements.clear()
                self.start_geometry_selection("See result in trace or select next objects to compare", self.whitelist)
                return True


            # prompt for selecting the second object, but with the same geometry type as the first one
            if len(self.selected_elements) == 1:
                self.start_geometry_selection(f"Select second {self.selected_elements[0].GetDisplayName()}",
                                              whitelist= [type(self.selected_elements[0].GetGeometry())])


            # print a warning if more than two objects were selected
            if len(self.selected_elements) > 2:
                print("\nWARNING: Selected more than two elements! Only first two are compared.")


            # when two or more elements are selected, compare geometries
            if len(self.selected_elements) >= 2:
                self.compare_geometries()

                # clear memory and restart selection
                self.selected_elements.clear()
                self.start_geometry_selection("See result in trace or select next objects to compare",
                                              whitelist= self.whitelist)

        return True


    def compare_geometries(self) -> None:
        """Compare the geometries of the first two elements in the list of selected elements
        using the Comparison.Equal method and print the results to the console
        """

        first_geometry  = self.selected_elements[0].GetGeometry()
        second_geometry = self.selected_elements[1].GetGeometry()

        are_equal = AllplanGeometry.Comparison.Equal(first_geometry,
                                                     second_geometry,
                                                     self.build_ele.Tolerance.value)

        print("\n------------- Comparison result ----------------\n",
              f"Compared geometries are of type {type(first_geometry).__name__}",
              "Result: geometries are " + ("EQUAL" if are_equal else "DIFFERENT"),
              f"Compared with tolerance of {self.build_ele.Tolerance.value} mm",
              "------------------------------------------------",
              sep="\n")
