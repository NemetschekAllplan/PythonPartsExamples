"""Example script showing the implementation of HiddenCalculus class used
to calculate 2d hidden view of a polyhedron geometry
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
    from __BuildingElementStubFiles.HiddenCalculusBuildingElement import HiddenCalculusBuildingElement
else:
    HiddenCalculusBuildingElement = BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
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
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return HiddenCalculationInteractor(coord_input,
                                       build_ele_list,
                                       build_ele_composite,
                                       control_props_list)


class HiddenCalculationInteractor(OperationExampleBaseInteractor):
    """Hidden calculation interactor showing the example implementation of the HiddenCalculus
    class. Prompts the user for selecting a model element containing a geometry of type Polyhedron3D
    and calculates 2d lines representing a hidden view of this element. The parameters for the
    calculation, such as view direction, angle for adjacent edges etc. are get from the
    property palette. At the end, the 2d lines are drawn in the model and the source 3d solid
    is deleted in the current drawing file.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        elements_to_create:     elements with the 2d lines resulting from hidden calculation
        elements_to_delete:     source 3d solids to be deleted
        post_element_selection: object containing selected elements after successful selection
        selected_elements:      3d solids selected by the user to perform the hidden calculation on
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

        # set initial values
        self.build_ele              = cast(HiddenCalculusBuildingElement, build_ele_list[0])
        self.elements_to_create     = ModelEleList()
        self.elements_to_delete     = AllplanElementAdapter.BaseElementAdapterList()
        self.post_element_selection = None
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist = [AllplanGeometry.Polyhedron3D]

        self.start_geometry_selection("Select polyhedrons to perform hidden calculation on", self.whitelist)

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

            self.selected_elements      = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            # do nothing, if no elements were selected
            if not self.selected_elements:
                return True

            # perform the hidden calculation
            self.calculate(self.selected_elements)

            # create 2d lines in the drawing file and clear memory
            self.create_and_delete_elements()
            self.selected_elements.clear()

        # restart selection
        self.start_geometry_selection("Additional info in trace; Select next polyhedrons", self.whitelist)

        return True

    def calculate(self, elements: AllplanElementAdapter.BaseElementAdapterList) -> None:
        """ Calculate a collection of 2D lines representing a hidden view of polyhedrons given in the element
        adapter list, using HiddenCalculus class of the geometry module. Calculation parameters are taken from
        the values specified in the property palette. Depending on selected option, visible or/and hidden lines
        are appended to the list of elements to create in the drawing file. Common properties of the created
        lines are taken from the 3d solid, they resulted from. The observer matrix and number of resulting
        lines is printed in the console

        Args:
            elements:   list of model elements containing polyhedrons to calculate 2d lines for
        """

        # setting the parameters of the hidden calculation
        calculation_parameters = AllplanGeometry.HiddenCalculationParameters()

        calculation_parameters.AdjacentEdgesMaxAngle = AllplanGeometry.Angle.FromDeg(self.build_ele.AdjacentEdgesAngle.value)
        calculation_parameters.GetHiddenLines        = self.build_ele.CreateHiddenLines.value

        # depending on the option set in the property palette, the observer matrix is obtained
        # either from the current viewport...
        if self.build_ele.GetObserverMatrixFrom.value == "CurrentView":
            view_world_projection = self.coord_input.GetViewWorldProjection()
            calculation_parameters.SetObserverMatrix(view_world_projection.GetEyePoint(),
                                                     view_world_projection.GetViewPoint())

        # ...or by eye and view point specified in the palette
        elif self.build_ele.GetObserverMatrixFrom.value == "ManualInput":
            calculation_parameters.SetObserverMatrix(self.build_ele.EyePoint.value,
                                                     self.build_ele.ViewPoint.value)

        # initialize hidden calculus and applying the settings
        hidden_calculus = AllplanGeometry.HiddenCalculus()
        hidden_calculus.Configure(calculation_parameters)

        # initialize the material object
        hidden_material             = AllplanGeometry.HiddenMaterial()
        hidden_material.ExtraSmooth = self.build_ele.ExtraSmooth.value

        # initialise a list with common properties of the source 3d solids
        common_props_list: list[AllplanBaseElements.CommonProperties] = []

        for i, element in enumerate(elements):
            geometry: AllplanGeometry.Polyhedron3D = element.GetGeometry()
            common_props_list.append(element.GetCommonProperties())

            # add each selected geometry to the hidden calculus tagging each element with an index
            hidden_calculus.AddElement(geometry, hidden_material, i)

        # performing the calculation
        hidden_calculus.Calculate()

        for line_idx in range(hidden_calculus.GetLinesCount()):
            line, result = hidden_calculus.GetResultLine(line_idx)

            # because each line is tagged by the index of the solid it resulted from,
            # the common properties of the source 3d solid are picked based on the tag
            common_properties = common_props_list[hidden_calculus.GetResultLineTag(line_idx)]

            # visible and hidden lines are appended to the list of elements to create only, if
            # the corresponding option in the palette to create them was selected
            if (result == AllplanGeometry.eHiddenCalculationResult.eVisible and self.build_ele.CreateVisibleLines.value) or \
                    (result == AllplanGeometry.eHiddenCalculationResult.eHidden and self.build_ele.CreateHiddenLines.value):
                self.elements_to_create.append_geometry_2d(AllplanGeometry.Line2D(line),    # convert resulting 3D line to 2D line
                                                           common_properties)               # apply common props picked from the list

        if self.build_ele.DeleteOriginalObjects.value:
            self.elements_to_delete += elements

        # print the result to the console
        print("\n--------------- Hidden calculation -------------------",
              "Observer matrix used for the calculation:",
              calculation_parameters.ObserverMatrix,
              f"\nCalculation resulted in {hidden_calculus.GetLinesCount()} lines",
              "----------------------------------------------------\n",
              sep="\n")

    def create_and_delete_elements(self) -> AllplanElementAdapter.BaseElementAdapterList:
        """Create new model elements from the geometries in the elements_to_create list
        and delete the elements in the elements_to_delete list from the current document.
        At the end, clear both lists.

        Returns:
            list of element adapters of the created elements
        """
        if self.elements_to_delete:
            AllplanBaseElements.DeleteElements(self.coord_input.GetInputViewDocument(),
                                               self.selected_elements)
            self.elements_to_delete.clear()

        if self.elements_to_create:
            created_elements = AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                                                  AllplanGeometry.Matrix3D(),
                                                                  self.elements_to_create,
                                                                  modelUuidList = [],
                                                                  assoRefObj    = None)
            self.elements_to_create.clear()
            return created_elements

        return AllplanElementAdapter.BaseElementAdapterList()
