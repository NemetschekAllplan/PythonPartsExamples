"""Example script showing the implementation of CalcMass function
calculating volume, surface and center of gravity of a volumetric geometry objects
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
    from __BuildingElementStubFiles.CalcMassBuildingElement import CalcMassBuildingElement
else:
    CalcMassBuildingElement = BuildingElement

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
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

    return CalcMassInteractor(coord_input,
                              build_ele_list,
                              build_ele_composite,
                              control_props_list)


class CalcMassInteractor(OperationExampleBaseInteractor):
    """ Calc Mass Interactor showing the example implementation of the CalcMass function
    of the NemAll_Python_Geometry module, capable of calculating the surface, volumen and
    center of gravity of volumetric objects such as polyhedrons or BReps. Interactor prompts
    the user for selecting one or more solids. The calculation results are printed in the console.
    If the option was selected, a point symbol representing the center of gravity is drawn in
    the model.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      solids selected for the calculation
        post_element_selection: object containing selected elements after successful selection
        cg_symbol_common_props: common properties of the point symbol representing the center of gravity
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
        self.build_ele              = cast(CalcMassBuildingElement, build_ele_list[0])
        self.cg_symbol_common_props = self.build_ele.CGSymbolCommonProp.value

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist = [AllplanGeometry.BRep3D,
                          AllplanGeometry.Polyhedron3D]

        self.start_geometry_selection("Select a solid or surface", self.whitelist)

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

            self.selected_elements      = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            if self.selected_elements:
                self.calculate_qty_takeoff(self.selected_elements)

                # restart selection
                self.selected_elements.clear()

            self.start_geometry_selection("See result in trace or select next solid", self.whitelist)

        return True

    def calculate_qty_takeoff(self, elements: AllplanElementAdapter.BaseElementAdapterList) -> None:
        """Perform quantity take-off (volume, surface and center of gravity) from each of the
        elements using CalcMass(), print the result in the console and optionally create
        a point symbol for CG if a corresponding option in the palette is selected

        Args:
            elements: list with elements, for which quantity take-off should be done
        """

        cg_points = AllplanGeometry.Point3DList()

        print("\n------------- Quantity take-off ----------------")

        for i, element in enumerate(elements, start= 1):
            geometry = element.GetGeometry()

            err, volume, surface, center_of_gravity = AllplanGeometry.CalcMass(geometry)

                # print results to the console
            print(f"{i}. {element.GetDisplayName()}:")

            if err == AllplanGeometry.eOK:
                print(f"   Geometry object type: {type(geometry).__name__}",
                      f"   Volume: {volume / 1e6} m³",
                      f"   Surface: {surface / 1e6} m³",
                      "   Center of gravity:",
                      f"\tX: {center_of_gravity.X}",
                      f"\tY: {center_of_gravity.Y}",
                      f"\tZ: {center_of_gravity.Z}",
                      sep="\n")

                cg_points.append(center_of_gravity)

            else:
                print(err)

        print("------------------------------------------------\n")

        # create the point symbol if option selected in the palette
        if self.build_ele.CreateCGPoint.value:
            self.create_cg_points(cg_points)


    def create_cg_points(self, points: AllplanGeometry.Point3DList) -> None:
        """Creates 3D point symbols (terrain point) in given points in the model to indicate
        the center of gravity

        Args:
            points: list with points, where to create symbols
        """

        symbol_props          = AllplanBasisElements.Symbol3DProperties()
        symbol_props.SymbolID = 1
        symbol_props.Height   = self.build_ele.CGSymbolSize.value
        symbol_props.Width    = self.build_ele.CGSymbolSize.value
        symbol_elements       = [AllplanBasisElements.Symbol3DElement(self.cg_symbol_common_props, symbol_props, point) for point in points]

        AllplanBaseElements.CreateElements( self.coord_input.GetInputViewDocument(),
                                            AllplanGeometry.Matrix3D(),
                                            symbol_elements,
                                            modelUuidList= [],
                                            assoRefObj=    None)
