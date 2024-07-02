"""Example script to cut a solid (polyhedron or brep) by a plane in two pieces
"""
from typing import TYPE_CHECKING, Any, List, Union, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService
from TypeCollections import ModelEleList

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CutSolidWithPlaneBuildingElement import CutSolidWithPlaneBuildingElement
else:
    CutSolidWithPlaneBuildingElement = BuildingElement


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

    return CutSolidWithPlaneInteractor(coord_input,
                                       build_ele_list,
                                       build_ele_composite,
                                       control_props_list)


class CutSolidWithPlaneInteractor(OperationExampleBaseInteractor):
    """ Cut solid with plane interactor showing the example implementation of two
    functions of the NemAll_Python_Geometry module: CutPolyhedronWithPlane and
    CutBRepWithPlane. Both of the perform a geometrical operation of cutting
    a solid into two pieces by a plane. The interactor prompts the user
    to select at least one solid. In the second step the user has to input 3 points
    to define the cutting plane. After that, the result is printed in the trace and
    (if the user selected that in the palette) the original solid is deleted, and
    two resulting solids are created in the model.

    Attributes:
        selected_elements:      model elements (solids) to cut
        build_ele:              contains, among others, parameter properties from the palette
        post_element_selection: object containing selected elements after successful selection
        input_mode:             current input mode: object selection or coordinate input
        plane_points:           list with points defining the cutting plane
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
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()
        self.build_ele              = cast(CutSolidWithPlaneBuildingElement, build_ele_list[0])
        self.post_element_selection = None
        self.input_mode             = self.InteractorInputMode.ELEMENT_SELECTION

        self.plane_points: List[AllplanGeometry.Point3D]= []

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist =   [AllplanGeometry.BRep3D,
                            AllplanGeometry.Polyhedron3D,
                            ]
        self.start_geometry_selection("Select objects to cut", self.whitelist)


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
        # solid selection mode
        if self.input_mode == self.InteractorInputMode.ELEMENT_SELECTION and self.post_element_selection:

            self.selected_elements = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            # do nothing, if nothing was selected
            if not self.selected_elements:
                self.start_geometry_selection("Select objects to cut", self.whitelist)
                return True

            # start point input
            self.start_point_input("Input first point of the cutting plane")
            self.input_mode = self.InteractorInputMode.COORDINATE_INPUT


        # coordinate input mode to define the points of cutting plane
        if self.input_mode == self.InteractorInputMode.COORDINATE_INPUT:

            coord_input_result = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info)

            # do nothing if no mouse click detected
            if self.coord_input.IsMouseMove(mouse_msg):
                return True

            # check if input point is different than already provided
            if not coord_input_result.GetPoint() in self.plane_points:
                self.plane_points.append(coord_input_result.GetPoint())


            # ask for second point, if only one defined
            if len(self.plane_points) == 1:
                self.start_point_input("Input second point of the cutting plane")
                return True

            # ask for third point, if only two defined
            if len(self.plane_points) == 2:
                self.start_point_input("Input third point of the cutting plane")
                return True

            # define cutting plane and cut the solid, if three points defined
            if len(self.plane_points) == 3:

                try:
                    cutting_plane = AllplanGeometry.Plane3D(*self.plane_points)
                except ValueError:
                    print("Couldn't create a cutting plane from provided points")
                else:
                    self.cut_solid(cutting_plane)

            # clear the memory and restart selection
            self.selected_elements.clear()
            self.plane_points.clear()
            self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
            self.start_geometry_selection("See result in trace or select next objects to cut", self.whitelist)

        return True


    def cut_solid(self, cutting_plane: AllplanGeometry.Plane3D) -> None:
        """Cut all the solids of the elements in the selected_elements list with the provided cutting plane
        and print the result in the console.
        Optionally, if the corresponding option in the palette is set, the resulting solids
        are created in the model and the originals are deleted

        Args:
            cutting_plane:  plane cutting the solids
        """

        print("\n------------- Cut solid with plane --------------\n")
        print("Cutting plane:")
        print(f"\tReference point: {cutting_plane.Point}")
        print(f"\tNormal vector: {cutting_plane.Vector}")

        solids_above = []
        solids_below = []

        for i, element in enumerate(self.selected_elements, start= 1):

            geometry = element.GetGeometry()

            # implementation for the polyhedron geometry
            if isinstance(geometry, AllplanGeometry.Polyhedron3D):
                is_cutting , solid_above, solid_below = AllplanGeometry.CutPolyhedronWithPlane(geometry, cutting_plane)

            # implementation for the brep geometry
            else:
                is_cutting , solid_above, solid_below = AllplanGeometry.CutBrepWithPlane(geometry, cutting_plane)

            # print the results to the console
            print(f"\n{i}. {element.GetDisplayName()} with geometry type of {type(geometry).__name__}:")

            print("\tPlane is cutting this solid" if is_cutting else "\tPlane is not cutting this solid")

            if is_cutting:
                print("\tResulting geometry above is " + ("valid" if solid_above.IsValid() else "invalid"))
                print("\tResulting geometry below is " + ("valid" if solid_below.IsValid() else "invalid"))

            solids_above.append(solid_above)
            solids_below.append(solid_below)


        # deleting the original object, if corresponding option is set in the palette

        if self.build_ele.DeleteOriginalObjects.value:
            AllplanBaseElements.DeleteElements(self.coord_input.GetInputViewDocument(),
                                               self.selected_elements)


        # creating the model elements, if corresponding option is set in the palette

        if self.build_ele.CreateSolidAbove.value:
            self.create_elements(solids_above)
        if self.build_ele.CreateSolidBelow.value:
            self.create_elements(solids_below)


    def create_elements(self, geometries: List[Union[AllplanGeometry.Polyhedron3D, AllplanGeometry.BRep3D]]) -> None:
        """Creates 3D objects in the model

        Args:
            geometries: list with geometries to create
        """
        common_props = self.build_ele.CommonProperties.value
        elements     = ModelEleList(common_props)

        for geometry in geometries:
            elements.append_geometry_3d(geometry)

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeometry.Matrix3D(),
                                           elements,
                                           modelUuidList= [],
                                           assoRefObj= [])
