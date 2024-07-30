"""Example script showing the implementation of CalcLength function
calculating the length of curves"""

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
    from __BuildingElementStubFiles.CalcLengthBuildingElement import CalcLengthBuildingElement
else:
    CalcLengthBuildingElement = BuildingElement

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


def create_interactor(coord_input:                 AllplanIFWInput.CoordinateInput,
                      _pyp_path:                   str,
                      _global_str_table_service:   StringTableService,
                      build_ele_list:              List[BuildingElement],
                      build_ele_composite:         BuildingElementComposite,
                      control_props_list:          List[ControlProperties],
                      _modify_uuid_list:           List[str]) -> Any:
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

    return CalcLengthInteractor(coord_input,
                                build_ele_list,
                                build_ele_composite,
                                control_props_list)


class CalcLengthInteractor(OperationExampleBaseInteractor):
    """ Calc Length Interactor showing the example implementation of the CalcLength function
    of the NemAll_Python_Geometry module, capable of calculating the length of linear geometry
    objects, such as splines or polylines, but also circumference of polygons. Interactor
    prompts the user for selecting one or more object(s) and the result is printed in the console.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        post_element_selection: object containing selected elements after successful selection
    """

    def __init__(self,
                 coord_input        : AllplanIFWInput.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[ControlProperties]):
        """ Constructor

        Args:
            coord_input:               coordinate input
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
        """

        #set initial values
        self.post_element_selection = None
        self.build_ele              = cast(CalcLengthBuildingElement, build_ele_list[0])

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        #start element selection
        self.whitelist =   [AllplanGeometry.Arc2D,
                            AllplanGeometry.Arc3D,
                            AllplanGeometry.BSpline3D,
                            AllplanGeometry.Clothoid2D,
                            AllplanGeometry.Line2D,
                            AllplanGeometry.Line3D,
                            AllplanGeometry.Path2D,
                            AllplanGeometry.Path3D,
                            AllplanGeometry.Polygon2D,
                            AllplanGeometry.Polygon3D,
                            AllplanGeometry.Polyhedron3D,
                            AllplanGeometry.Polyline2D,
                            AllplanGeometry.Polyline3D,
                            AllplanGeometry.Spline2D,
                            AllplanGeometry.Spline3D,
                            ]

        self.start_geometry_selection("Select an object", self.whitelist)


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
        self.on_preview_draw()

        if self.post_element_selection:

            selected_elements           = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            # do nothing, if nothing was selected
            if not selected_elements:
                return True

            print("\n------------- Length calculation ----------------")

            for i, element in enumerate(selected_elements, start= 1):

                geometry = element.GetGeometry()

                length = AllplanGeometry.CalcLength(geometry)

                print(f"{i}. {element.GetDisplayName()}:",
                      f"   Geometry object type: {type(geometry).__name__}",
                      f"   Length: {length} mm",
                      sep="\n")

            print("------------------------------------------------\n")

            # restart selection
            self.start_geometry_selection("See result in trace or select next object", self.whitelist)

        return True
