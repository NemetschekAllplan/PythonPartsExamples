"""Example script showing the implementation of FilletCalculus3D
calculating fillet on solids and between two 3D lines
"""
from typing import TYPE_CHECKING, Any, List, Union, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
import NemAll_Python_Utility as AllplanUtil
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService
from TypeCollections.ModelEleList import ModelEleList

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.Fillet3DBuildingElement import Fillet3DBuildingElement
else:
    Fillet3DBuildingElement = BuildingElement

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

    return Fillet3DInteractor(coord_input,
                              build_ele_list,
                              build_ele_composite,
                              control_props_list)


class Fillet3DInteractor(OperationExampleBaseInteractor):
    """ Fillet 3D interactor showing the example implementation of the FilletCalculus3D
    class which is capable od calculating fillet of solid edges as well as fillet two
    3D lines. The interactor prompts the user to select 3D solid or a 3D line. If the
    user selects the first one, it performs the calculation. The result is printed
    in the console, the original solid is deleted in the model and the new solid with
    rounded edges is created.
    If the user selected a 3D line, he is prompt to select the second one. After that,
    a fillet arc is calulated and created in the model. If the originally selected
    lines were not parallel, they are getting deleted and trimmed 3D lines calculated
    by the FilletCalculus are created insted.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      selected solids or 3d lines
        elements_to_create:     lines/solids to create in the model after successful calculation
        elements_to_delete:     lines/solids to remove from the model after successful calculation
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
        self.build_ele          = cast(Fillet3DBuildingElement, build_ele_list[0])
        self.selected_elements  = AllplanElementAdapter.BaseElementAdapterList()
        self.elements_to_create = ModelEleList()
        self.elements_to_delete = AllplanElementAdapter.BaseElementAdapterList()

        self.post_element_selection: Union[AllplanIFWInput.PostElementSelection, None] = None

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist =   [AllplanGeometry.BRep3D,
                            AllplanGeometry.Polyhedron3D,
                            AllplanGeometry.Line3D,
                            ]
        self.start_geometry_selection("Select a solid or a 3D line", self.whitelist)


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

            self.selected_elements += self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None


            # if only one 3D line was selected, ask for the second one
            if len(self.selected_elements) == 1 and isinstance(self.selected_elements[0].GetGeometry(), AllplanGeometry.Line3D):
                self.start_geometry_selection("Select second 3D line", [AllplanGeometry.Line3D])
                return True


            # if two 3D lines selected, perform fillet them both
            if len(self.selected_elements) == 2 and all(isinstance(element.GetGeometry(), AllplanGeometry.Line3D) for element in self.selected_elements):
                error = self.fillet_3d_lines(*self.selected_elements)
                print(f"Fillet of 3D lines resulted in {error}")

            # if there were solids selected, the fillet is done on each of them
            for element in self.selected_elements:
                geometry = element.GetGeometry()


                #------ implementation of FilletCalculus for a brep

                if isinstance(geometry, AllplanGeometry.BRep3D):
                    error, fillet_brep = AllplanGeometry.FilletCalculus3D.Calculate(geometry,
                                                                                    self.build_ele.FilletRadius.value)


                #------ implementation of FilletCalculus for a polyhedron

                elif isinstance(geometry, AllplanGeometry.Polyhedron3D):
                    error, fillet_brep = AllplanGeometry.FilletCalculus3D.Calculate(geometry,
                                                                                    self.get_edges_to_fillet(geometry),
                                                                                    self.build_ele.FilletRadius.value,
                                                                                    self.build_ele.EdgePropagation.value)

                else:
                    continue


                # if fillet was successful, append the new geometry to the list for later element creation

                if error == AllplanGeometry.eFilletErrorCode.eNO_ERROR:
                    self.elements_to_delete.append(element)
                    self.elements_to_create.append_geometry_3d(fillet_brep)

                # print result to the console
                print(f"Fillet of {element.GetDisplayName()} resulted in {error}")

            # create new geometry in the model, clear the memory and restart selection
            self.create_and_delete_elements()
            self.selected_elements.clear()
            self.start_geometry_selection("Additional info in trace; select next solid or 3D lines", self.whitelist)

        return True


    def fillet_3d_lines(self,
                        first_line_element : AllplanElementAdapter.BaseElementAdapter,
                        second_line_element: AllplanElementAdapter.BaseElementAdapter) -> AllplanGeometry.eFilletErrorCode:
        """Fillets two 3D lines by getting the geometry from provided element adapters and
        applying the right FilletCalculus3D.Calculate method on them, depending on whether the
        two 3D lines are parallel to each other. If the fillet operation was successful,
        append the new geometry to the list for later element creation.

        Args:
            first_line_element:     element adapter of the first 3D line
            second_line_element:    element adapter of the second 3D line

        Returns:
            error code with fillet operation outcome
        """

        first_line : AllplanGeometry.Line3D = first_line_element.GetGeometry()
        second_line: AllplanGeometry.Line3D = second_line_element.GetGeometry()


        #------ implementation of FilletCalculus for two parallel 3D lines

        if AllplanGeometry.Comparison.IsParallel(first_line, second_line)[0] == AllplanGeometry.eParallel:

            error, fillet = AllplanGeometry.FilletCalculus3D.Calculate(first_line,
                                                                       second_line)

            if error == AllplanGeometry.eFilletErrorCode.eNO_ERROR:
                self.elements_to_create.append_geometry_3d(fillet)


        #------ implementation of FilletCalculus for two coplanar 3D lines

        else:
            error, trimmed_first_line, trimmed_second_line, fillet = \
                AllplanGeometry.FilletCalculus3D.Calculate(first_line,
                                                           second_line,
                                                           self.build_ele.FilletRadius.value)

            if error == AllplanGeometry.eFilletErrorCode.eNO_ERROR:
                self.elements_to_delete.append(first_line_element)
                self.elements_to_delete.append(second_line_element)
                self.elements_to_create.append_geometry_3d(trimmed_first_line)
                self.elements_to_create.append_geometry_3d(trimmed_second_line)
                self.elements_to_create.append_geometry_3d(fillet)

        return error


    def get_edges_to_fillet(self, polyhedron: AllplanGeometry.Polyhedron3D) -> AllplanUtil.VecSizeTList:
        """When a list of edges indices was specified in the property palette, create
        a VecSizeTList with the indices. If no edges were specified, create a list
        with all the edge indices of the given polyhedron

        Args:
            polyhedron: polyhedron, for which the list of edges should be created

        Returns:
            list with the edge indices to perform fillet on
        """

        if self.build_ele.EdgesToFillet.value == "":
            return AllplanUtil.VecSizeTList(list(range(polyhedron.GetEdgesCount())))

        return AllplanUtil.VecSizeTList([int(edge_idx) for edge_idx in self.build_ele.EdgesToFillet.value.split(',')])


    def create_and_delete_elements(self) -> AllplanElementAdapter.BaseElementAdapterList:
        """Create new model elements from the geometries in the elements_to_create list
        and delete the old elements in the elements_to_delete list from the current document.
        At the end clears both lists.

        Returns:
            list of element adapters of the created elements
        """
        if len(self.elements_to_delete) > 0:
            AllplanBaseElements.DeleteElements(self.coord_input.GetInputViewDocument(),
                                            self.elements_to_delete)
            self.elements_to_delete.clear()

        if len(self.elements_to_create) > 0:
            created_elements = AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                                                  AllplanGeometry.Matrix3D(),
                                                                  self.elements_to_create,
                                                                  [], None)
            self.elements_to_create.clear()
            return created_elements

        return AllplanElementAdapter.BaseElementAdapterList()
