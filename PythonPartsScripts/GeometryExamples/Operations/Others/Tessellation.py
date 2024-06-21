"""Example script showing the implementation of CreatePolyhedron function and
the ApproximationsSettings class both used to tessellate a brep geometry into
a polyhedron geometry
"""
from typing import TYPE_CHECKING, Any, List, cast

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
    from __BuildingElementStubFiles.TessellationBuildingElement import TessellationBuildingElement
else:
    TessellationBuildingElement = BuildingElement


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

    return TessellationInteractor(coord_input,
                                  build_ele_list,
                                  build_ele_composite,
                                  control_props_list)


class TessellationInteractor(OperationExampleBaseInteractor):
    """Tessellation interactor showing an example implementation of CreatePolyhedron
    function and ApproximationSettings class, both in combination used to tessellate
    a brep geometry into a polyhedron. The interactor prompts for selecting one or
    multiple model elements, which contains a geometry of type BRep3D. Then, using
    the values from the property palette, calculates a new tessellated polyhedron
    geometry. Then deletes the selected elements from the model and creates new,
    with the tessellated geometry

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        elements_to_create:     elements with the resulting tessellated geometry
        elements_to_delete:     elements, whose tessellation was successful thus can be deleted
        post_element_selection: object containing selected elements after successful selection
        selected_elements:      elements selected by the user to perform the tessellation on
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

        # set initial values
        self.build_ele              = cast(TessellationBuildingElement, build_ele_list[0])
        self.elements_to_create     = ModelEleList()
        self.elements_to_delete     = AllplanElementAdapter.BaseElementAdapterList()
        self.post_element_selection = None
        self.selected_elements      = AllplanElementAdapter.BaseElementAdapterList()

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist = [AllplanGeometry.BRep3D]

        self.start_geometry_selection("Select breps to tessellate", self.whitelist)

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

            # do nothing, if no elements were selected
            if not self.selected_elements:
                return True

        # perform the tesselation
        self.tessellate(self.selected_elements)

        # create tessellated 3d solids in the drawing file, clear memory and restart selection
        self.create_and_delete_elements()
        self.selected_elements.clear()
        self.start_geometry_selection("Additional info in trace; Select breps to tessellate", self.whitelist)

        return True

    def tessellate(self, elements: AllplanElementAdapter.BaseElementAdapterList) -> None:
        """Tessellate the geometry of the given element using parameters set by the user
        in the property palette. The resulting error code is printed to the console.
        If the tessellation was successful, new geometry is appended to the list of elements,
        that can be created and the source element to the list of elements to be deleted

        Args:
            elements:   list of model elements containing a brep geometry to tessellate
        """

        print("\n--------------- Tessellation -------------------")

        for i, element in enumerate(elements, start=1):
            geometry: AllplanGeometry.BRep3D = element.GetGeometry()

            tesselation_settings = AllplanGeometry.ApproximationSettings()
            tesselation_settings.SetBRepTesselation(self.build_ele.Density.value,
                                                    AllplanGeometry.Angle.FromDeg(self.build_ele.MaxAngle.value),
                                                    self.build_ele.MinLength.value,
                                                    self.build_ele.MaxLength.value)

            error, polyhedron = AllplanGeometry.CreatePolyhedron(geometry,
                                                                 tesselation_settings)

            # print results to the console
            print(f"{i}. {element.GetDisplayName()}:",
                  f"   Tesselation result: {error}",
                  sep="\n")

            # if tessellation was successful, create the new geometry and delete one
            if error == AllplanGeometry.eOK:
                self.elements_to_create.append_geometry_3d(geo_ele  = polyhedron,
                                                           com_prop = element.GetCommonProperties())
                self.elements_to_delete.append(element)

        print("------------------------------------------------\n")

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
