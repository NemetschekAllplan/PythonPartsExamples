"""Example script showing the implementation of the Comparison.DeterminePosition method
to determine the position of a point relative to a reference geometry object
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
    from __BuildingElementStubFiles.DeterminePositionBuildingElement import DeterminePositionBuildingElement
else:
    DeterminePositionBuildingElement = BuildingElement


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
        _pyp_path:                  path of the pyp file
        _global_str_table_service: global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return DeterminePositionInteractor(coord_input,
                                       build_ele_list,
                                       build_ele_composite,
                                       control_props_list)


class DeterminePositionInteractor(OperationExampleBaseInteractor):
    """ Determine Position Interactor showing the example implementation of the method
    Comparison.DeterminePosition of the NemAll_Python_Geometry module. In the first step
    the interactor prompts the user to select reference geometry object(s). In the second
    step the coordinate input is activated to let the user input a 3D point.
    With this input been made, the interactor uses the Comparison.DeterminePosition
    function to calculate the position of the point from the second step relative to the
    element(s) selected in the first step e.g., inside, outside, above, below or on element

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      selected elements used as reference for the calculation of the point's position
        post_element_selection: object containing selected elements after successful selection
    """

    def __init__(self,
                 coord_input        : AllplanIFWInput.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[ControlProperties]):
        """ Constructor

        Args:
            coord_input:                coordinate input
            build_ele_list:             list with the building elements containing parameter properties
            build_ele_composite:        building element composite
            control_props_list:         control properties list
        """
        self.post_element_selection=    None
        self.selected_elements=         AllplanElementAdapter.BaseElementAdapterList()
        self.build_ele=                 cast(DeterminePositionBuildingElement, build_ele_list[0])

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
        self.whitelist = [  AllplanGeometry.Arc2D,
                            AllplanGeometry.Arc3D,
                            AllplanGeometry.Axis2D,
                            AllplanGeometry.BSpline3D,
                            AllplanGeometry.BRep3D,
                            AllplanGeometry.Clothoid2D,
                            AllplanGeometry.Line2D,
                            AllplanGeometry.Line3D,
                            AllplanGeometry.Path3D,
                            AllplanGeometry.Polygon2D,
                            AllplanGeometry.Polyline2D,
                            AllplanGeometry.Polyline3D,
                            AllplanGeometry.Polyhedron3D,
                            AllplanGeometry.Spline2D,
                            AllplanGeometry.Spline3D,
                            ]

        self.start_geometry_selection("Select reference object", self.whitelist)


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeometry.Point2D,
                          msg_info : AllplanIFWInput.AddMsgInfo) -> bool:
        """ Called on each mouse message. A mouse message can be mouse movement, pressing a mouse button
        or releasing it.

        Args:
            mouse_msg:  the mouse message (e.g. 512 - mouse movement)
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """
        if self.input_mode == self.InteractorInputMode.ELEMENT_SELECTION and self.post_element_selection:

            self.selected_elements      = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            # do nothing, if nothing was selected
            if not self.selected_elements:
                return True

            # start
            self.start_point_input("Input point")
            self.input_mode = self.InteractorInputMode.COORDINATE_INPUT


        if self.input_mode == self.InteractorInputMode.COORDINATE_INPUT:

            coord_input_result = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info)

            # do nothing if no mouse click detected
            if self.coord_input.IsMouseMove(mouse_msg):
                return True

            # determine position of the point
            self.determine_position(coord_input_result.GetPoint())

            # clear the memory and restart selection
            self.selected_elements.clear()
            self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
            self.start_geometry_selection("See result in trace or select next object", self.whitelist)

        return True

    def determine_position(self, reference_point: AllplanGeometry.Point3D):
        """Determine position of the reference point in relation to all the geometries
        of the selected elements and print the results to the console

        Args:
            reference_point:    point to determine the position of
        """

        print("\n------------- Comparison result ----------------",
                "Input point:",
                f"\tX: {reference_point.X}",
                f"\tY: {reference_point.Y}",
                f"\tZ: {reference_point.Z}",
                "Position of the point in relation to the selected objects:",
                sep="\n")

        # determine position of reference point to each geometry element
        for i, element in enumerate(self.selected_elements, start= 1):
            geometry = element.GetGeometry()

            comparison_result = AllplanGeometry.Comparison.DeterminePosition(geometry,
                                                                             reference_point if element.Is3DElement() else AllplanGeometry.Point2D(reference_point),
                                                                             self.build_ele.Tolerance.value)

            print(f"\t{i}. {element.GetDisplayName()} ({type(geometry).__name__}): {comparison_result}" )

        print("------------------------------------------------\n")
