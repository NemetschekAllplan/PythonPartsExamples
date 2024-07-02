"""Example script showing the implementation of CenterCalculus function
calculating the center point of curves
"""
from typing import TYPE_CHECKING, Any, List, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CenterCalculusBuildingElement import CenterCalculusBuildingElement
else:
    CenterCalculusBuildingElement = BuildingElement

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
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return CenterCalculusInteractor(coord_input,
                      build_ele_list,
                      build_ele_composite,
                      control_props_list)


class CenterCalculusInteractor(OperationExampleBaseInteractor):
    """ Center calculus Interactor showing the example implementation of CenterCalculus
    class capable of calculating the center point of curves and areas bounded by closed
    curves. Interactor prompts the user to select at least one object and perform the
    calculation directly after. The coordinates od the resulting point are printed in the
    console and (if te option was selected by the user) a point symbol representing
    the center point is created in the model

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      curves selected for the calculation
        post_element_selection: object containing selected elements after successful selection
        cg_symbol_common_props: common properties of the point symbol representing the center
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
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()
        self.build_ele              = cast(CenterCalculusBuildingElement, build_ele_list[0])
        self.cg_symbol_common_props = self.build_ele.CGSymbolCommonProp.value

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
                            AllplanGeometry.Path2D,
                            AllplanGeometry.Path3D,
                            AllplanGeometry.Polygon2D,
                            AllplanGeometry.Polygon3D,
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

            self.selected_elements = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            if self.selected_elements:

                self.calculate_center(self.selected_elements)

                # restart selection
                self.selected_elements.clear()
                self.start_geometry_selection("See result in trace or select next object", self.whitelist)

        return True

    def calculate_center(self, elements: AllplanElementAdapter.BaseElementAdapterList) -> None:
        """Calculate center point of each geometry element provided in the elements list
        considering options set in the property palette, and prints the result to the console.
        Optionally, creates the symbol representing the calculated center point in the model,
        if the corresponding option was selected in the palette.

        Args:
            elements: list with elements to calculate the center point
        """
        center_points = AllplanGeometry.Point3DList()

        print("\n------------- Quantity take-off ----------------")

        for i, element in enumerate(elements, start= 1):
            center_calculated = False
            center = AllplanGeometry.Point3D()

            geometry = element.GetGeometry()


            # implementation for lines

            if isinstance(geometry, (AllplanGeometry.Line2D,
                                     AllplanGeometry.Line3D)):

                center_calculated, center = AllplanGeometry.CenterCalculus.Calculate(geometry)


            # implementation for polylines

            elif isinstance(geometry,(AllplanGeometry.Polyline2D,
                                      AllplanGeometry.Polyline3D)):

                center_calculated, center = AllplanGeometry.CenterCalculus.Calculate(geometry,
                                                                                     edge = self.build_ele.EdgeNumber.value)


            # implementation for polygons

            elif isinstance(geometry, (AllplanGeometry.Polygon2D,
                                       AllplanGeometry.Polygon3D)):

                center_calculated, center = AllplanGeometry.CenterCalculus.Calculate(geometry,
                                                                                     bPlaneCenter = bool(self.build_ele.PlaneCenter.value),
                                                                                     edge         = self.build_ele.EdgeNumber.value)


            # implementation for arcs

            elif isinstance(geometry, (AllplanGeometry.Arc2D,
                                       AllplanGeometry.Arc3D)):

                center_calculated, center = AllplanGeometry.CenterCalculus.Calculate(geometry,
                                                                                     center = bool(self.build_ele.ArcCenter.value))


            # implementation for clothoids and splines (except for a 3D b-spline)

            elif isinstance(geometry, (AllplanGeometry.Spline2D,
                                       AllplanGeometry.Spline3D,
                                       AllplanGeometry.BSpline2D,
                                       AllplanGeometry.Clothoid2D)):

                center_calculated, center = AllplanGeometry.CenterCalculus.Calculate(geometry,
                                                                                     eps = self.build_ele.Precision.value)


            # implementation for a 3D b-spline and paths

            elif isinstance(geometry, (AllplanGeometry.BSpline3D,
                                       AllplanGeometry.Path2D,
                                       AllplanGeometry.Path3D)):

                center_calculated, center = AllplanGeometry.CenterCalculus.Calculate(geometry,
                                                                                     eps         = self.build_ele.Precision.value,
                                                                                     bAreaCenter = bool(self.build_ele.AreaCenter.value))


            # print results

            print(f"{i}. {element.GetDisplayName()}:",
                  f"   Geometry object type: {type(geometry).__name__}",
                  sep="\n")

            if center_calculated:
                print("   Center point:",
                      f"   X: {center.X}",
                      f"   Y: {center.Y}",
                      f"   Z: {center.Z}",
                      sep="\n")

                center_points.append(center)

            else:
                print("The center point could not be calculated")

            if self.build_ele.CreateCGPoint.value:
                self.create_cg_points(center_points)

        print("\n------------------------------------------------\n")


    def create_cg_points(self,
                         points: AllplanGeometry.Point3DList) -> None:
        """Creates 3D point symbols in given points to indicate the center of gravity

        Args:
            points: list with points, where to create symbols
        """

        symbol_props          = AllplanBasisElements.Symbol3DProperties()
        symbol_props.SymbolID = 1
        symbol_props.Height   = self.build_ele.CGSymbolSize.value
        symbol_props.Width    = self.build_ele.CGSymbolSize.value
        symbol_elements       = [AllplanBasisElements.Symbol3DElement(self.cg_symbol_common_props, symbol_props, point) for point in points]

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeometry.Matrix3D(),
                                           symbol_elements,
                                           modelUuidList = [],
                                           assoRefObj    = None)
