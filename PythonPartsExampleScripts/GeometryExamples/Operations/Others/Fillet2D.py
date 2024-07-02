"""Example script showing the implementation of FilletCalculus2D
calculating fillet between two 2D lines or arcs as an Interactor PythonPart
"""
from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService
from TypeCollections.ModelEleList import ModelEleList

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.Fillet2DBuildingElement import Fillet2DBuildingElement
else:
    Fillet2DBuildingElement = BuildingElement

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
                      build_ele_list           : list[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : list[ControlProperties],
                      _modify_uuid_list        : list[str]) -> Any       :
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

    return Fillet2DInteractor(coord_input,
                              build_ele_list,
                              build_ele_composite,
                              control_props_list)


class Fillet2DInteractor(OperationExampleBaseInteractor):
    """ Fillet 2D interactor showing a simple example implementation of the FilletCalculus2D

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      elements selected by the user to perform fillet operation on
        possible_fillets:       list with all possible fillet arcs, that can be calculated
        nearest_fillet:         the fillet arc nearest to the mouse pointer
        post_element_selection: object containing selected elements after successful selection
        fillet_calculus:        FilletCalculus2D object to perform the fillet calculation
    """

    def __init__(self,
                 coord_input        : AllplanIFWInput.CoordinateInput,
                 build_ele_list     : list[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : list[ControlProperties])       :
        """ Constructor

        Args:
            coord_input:               coordinate input
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
        """

        #set initial values
        self.build_ele          = cast(Fillet2DBuildingElement, build_ele_list[0])
        self.selected_elements  = AllplanElementAdapter.BaseElementAdapterList()
        self.possible_fillets   = AllplanGeometry.Arc2DList()
        self.nearest_fillet     = AllplanGeometry.Arc2D()

        self.post_element_selection: AllplanIFWInput.PostElementSelection | None = None
        self.fillet_calculus       : AllplanGeometry.FilletCalculus2D | None = None

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
        self.whitelist  = [AllplanGeometry.Line2D,
                           AllplanGeometry.Arc2D,
                           ]
        self.start_geometry_selection("Select a 2D line or arc", self.whitelist)


    def on_preview_draw(self) -> None:
        """Draw preview of all the possible fillet arcs and highlight the fillet arc nearest
        to the mouse pointer with a different color."""

        super().on_preview_draw()

        if len(self.possible_fillets) > 0:
            # create a ModelEleList with all the possible fillet arcs
            possible_fillets_common_props       = AllplanBaseElements.CommonProperties()
            possible_fillets_common_props.Color = 6

            possible_fillet_elements = ModelEleList(possible_fillets_common_props)

            for fillet_arc in self.possible_fillets:
                possible_fillet_elements.append_geometry_2d(fillet_arc)


            # create a ModelEleList with the fillet arc nearest to the mouse pointer
            nearest_fillet_common_props           = AllplanBaseElements.CommonProperties(possible_fillets_common_props)
            nearest_fillet_common_props.Color     = 7
            nearest_fillet_common_props.DrawOrder = 15

            nearest_fillet_element = ModelEleList(nearest_fillet_common_props)
            nearest_fillet_element.append_geometry_2d(self.nearest_fillet)


            # draw preview of all the arcs
            AllplanBaseElements.DrawElementPreview(self.coord_input.GetInputViewDocument(),
                                                   AllplanGeometry.Matrix3D(),
                                                   possible_fillet_elements + nearest_fillet_element,
                                                   False, [])

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any) -> None:
        """ Called after each property modification in the property palette.
        When fillet radius is modified in the palette after the lines to fillet are
        already selected, the FilletCalculus2D is constructed again with the new radius

        Args:
            page:   index of the page, beginning with 0
            name:   name of the modified property
            value:  new property value
        """

        super().modify_element_property(page, name, value)

        # if the fillet calculus has already been initialized, it has to be reinitialized
        # with the new fillet radius
        if self.fillet_calculus is not None and name == "FilletRadius":
            self.initiate_fillet_calculus(*self.selected_elements)


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeometry.Point2D,
                          msg_info : AllplanIFWInput.AddMsgInfo) -> bool:
        """ Called on each mouse message. A mouse message can be mouse movement, pressing a mouse button
        or releasing it.

        Args:
            mouse_msg: the mouse message (e.g. 512 - mouse movement)
            pnt:        the input point in view coordinates
            msg_info:  additional message info.

        Returns:
            True/False for success.
        """

        # select lines to fillet

        if self.input_mode == self.InteractorInputMode.ELEMENT_SELECTION and self.post_element_selection:
            self.selected_elements      += self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection  = None


            # if only one element (line or arc) selected, ask for the second one
            if len(self.selected_elements) == 1:
                self.start_geometry_selection("Select second 2D line or arc", self.whitelist)
                return True


            # if more than two elements selected, notify the user
            if len (self.selected_elements) > 2:
                print("Select only two lines or arcs!\nRestarting selection...")


            # if exactly two elements selected, perform fillet
            if len(self.selected_elements) == 2:
                # construct the FilletCalculus2D class and print the resulting fillet type to the console
                fillet_type = self.initiate_fillet_calculus(*self.selected_elements)
                print("Resulting fillet type between selected geometries:")
                print(fillet_type)
                print(f"Number of calculeted possible fillet arcs: {len(self.possible_fillets)}")


                # fillet types other than FT_LC_NO_INTERSECTION and FT_UNKNOWN result in one or more possible fillets
                # if that is the case, initialize the coordinate input for the user to select the desired fillet
                if fillet_type not in [AllplanGeometry.eFilletType.FT_LC_NO_INTERSECTION,
                                       AllplanGeometry.eFilletType.FT_UNKNOWN]:
                    self.input_mode = self.InteractorInputMode.COORDINATE_INPUT
                    self.start_point_input("Select the desired fillet")
                    self.on_preview_draw()
                    return True

                # otherwise only print a message and restart selection
                print("No fillet could be calculated")

            self.selected_elements.clear()
            self.start_geometry_selection("Additional info in trace; select next lines to fillet", self.whitelist)
            return True


        # if coordinate input is active, here with every mouse movement the fillet nearest to the
        # mouse point is determined and accordingly previewed

        if self.input_mode == self.InteractorInputMode.COORDINATE_INPUT and self.fillet_calculus is not None:
            input_point = AllplanGeometry.Point2D(self.coord_input.GetInputPoint(mouse_msg,pnt,msg_info).GetPoint())

            self.nearest_fillet = self.fillet_calculus.GetNearest(input_point)
            self.on_preview_draw()


        # if coordinate input is active and the user clicks in the viewport, the fillet arc nearest to the clicked
        # point is created in the model and the selection is restarted

        if self.input_mode == self.InteractorInputMode.COORDINATE_INPUT and not self.coord_input.IsMouseMove(mouse_msg):
            #get common properties for the fillet arc from the first selected element
            common_props = self.selected_elements[0].GetCommonProperties()

            fillet_to_create = ModelEleList(common_props)
            fillet_to_create.append_geometry_2d(self.nearest_fillet)

            AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                               AllplanGeometry.Matrix3D(),
                                               fillet_to_create, [],None)

            # clear the memory
            self.selected_elements.clear()
            self.possible_fillets = AllplanGeometry.Arc2DList()
            self.fillet_calculus  = None

            # restart selection
            self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
            self.start_geometry_selection("Additional info in trace; select next lines to fillet", self.whitelist)
        return True


    def initiate_fillet_calculus(self,
                                 first_element : AllplanElementAdapter.BaseElementAdapter,
                                 second_element: AllplanElementAdapter.BaseElementAdapter) -> AllplanGeometry.eFilletType:
        """Initiates fillet calculation from provided two element adapters representing 2D lines
        or arcs by constructing the FilletCalculus2D object, calculating all the possible fillets
        between them with the radius given by the user in the property palette and saving them
        in the class properties

        Args:
            first_element:  element adapter of the first 2d line or arc to calculate the fillet
            second_element: element adapter of the second 2d line or arc to calculate the fillet

        Returns:
            resulting fillet type
        """

        first_line  = first_element.GetGeometry()
        second_line = second_element.GetGeometry()

        # construct the FilletCalculus2D object
        self.fillet_calculus = AllplanGeometry.FilletCalculus2D(first_line,
                                                                second_line,
                                                                self.build_ele.FilletRadius.value)

        # calculate possible fillets
        self.possible_fillets = self.fillet_calculus.GetFillets()

        # determine the fillet type
        fillet_type = AllplanGeometry.FilletCalculus2D.GetFilletType(first_line, second_line)

        return fillet_type
