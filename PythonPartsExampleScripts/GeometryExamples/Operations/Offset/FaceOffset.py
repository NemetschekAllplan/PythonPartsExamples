"""Example script showing the implementation of FaceOffset calculating
offset faces and shells on solids and surfaces with a geometry type of
polyhedron as well as brep
"""
from typing import TYPE_CHECKING, Any, List, Tuple, Union, cast

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
    from __BuildingElementStubFiles.FaceOffsetBuildingElement import FaceOffsetBuildingElement
else:
    FaceOffsetBuildingElement = BuildingElement


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

    return FaceOffsetInteractor(coord_input,
                                build_ele_list,
                                build_ele_composite,
                                control_props_list)


class FaceOffsetInteractor(OperationExampleBaseInteractor):
    """ Face offset interactor showing the example implementation of the FaceOffset class
    from the NemAll_Python_Geometry module. This interactor prompt the user for selecting
    a 3D object (solid or surface) in the drawing file and directly after that calculates
    the offset face or shell based on the parameter from the property palette.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_elements:      3d objects selected by the user to perform offset operation on
        elements_to_create:     list with 3d objects resulting from the offset calculation
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

        # set initial values
        self.build_ele          = cast(FaceOffsetBuildingElement, build_ele_list[0])
        self.selected_elements  = AllplanElementAdapter.BaseElementAdapterList()
        self.elements_to_create = ModelEleList()

        self.post_element_selection: Union[AllplanIFWInput.PostElementSelection, None] = None

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.whitelist = [AllplanGeometry.BRep3D,
                          AllplanGeometry.Polyhedron3D,
                          ]
        self.start_geometry_selection("Select a solid or surface", self.whitelist)

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

            self.selected_elements      += self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection  = None

            print("\n\n--------------- Face offset results ---------------\n")

            for i, element in enumerate(self.selected_elements, 1):
                geometry = element.GetGeometry()

                # get common properties from the source element or from the palette, depending on the user's choice
                common_props = element.GetCommonProperties() if self.build_ele.CommonPropertiesFromSourceObject.value else self.build_ele.CommonProperties.value

                # calculate the offset geometries
                is_brep, error, geo_1, geo_2 = self.calculate_offset(geometry)

                # if offset was successful, append the new geometry to the list for later element creation
                if error == AllplanGeometry.eOK:
                    self.elements_to_create.append_geometry_3d(geo_1, common_props)

                    if geo_2 is not None:
                        self.elements_to_create.append_geometry_3d(geo_2, common_props)

                # print result to the console
                print(f"{i}. {element.GetDisplayName()} with {type(geometry).__name__} geometry:",
                      f"\tOffset calculation resulted in {error}",
                      "\tResulting geometry is a " +
                      ("brep" if is_brep else "polyhedron"),
                      sep="\n")

            print("\n---------------------------------------------------\n\n")

            # create new geometry in the model, clear the memory and restart selection
            self.create_elements()
            self.selected_elements.clear()
            self.start_geometry_selection("Additional info in trace; select next solid or surface", self.whitelist)

        return True

    def calculate_offset(self, solid: Union[AllplanGeometry.Polyhedron3D,
                                            AllplanGeometry.BRep3D]) -> Tuple[bool,AllplanGeometry.eGeometryErrorCode,Any,Any]:
        """Calculates offset or shell (depending on the option selected in the property palette)
        based on the given solid geometry and parameter values from the property palette
        using the FaceOffset class of the NemAll_Python_geometry module

        Args:
            solid:  solid to calculate offset/shell from

        Returns:
            true, if the resulting geometry will be a brep, false it will be a polyhedron
            error code resulting from the calculation (eOK if successful)
            first resulting geometry
            second resulting geometry; only in case of offset calculation and only if direction
                was set to BothSides; otherwise None is returned
        """

        if self.build_ele.OffsetSelectedFaces.value == 1:
            # convert string with face indices separated with coma into a VecSizeTList vector
            idx_vec = AllplanUtil.VecSizeTList(
                [int(edge_idx) for edge_idx in self.build_ele.FacesToOffset.value.split(',')])

            # construct the FaceOffset object by defining specific faces to offset
            face_offset = AllplanGeometry.FaceOffset(solid,
                                                     faceIndices = idx_vec)

        else:
            # construct the FaceOffset object by taking all faces into calculation
            face_offset = AllplanGeometry.FaceOffset(solid)

        is_brep = face_offset.IsResultBrep()

        # if punch direction was defined in the palette as zero vector, a None object is assigned
        punch_direction = self.build_ele.PunchDirection.value if self.build_ele.PunchDirection.value != AllplanGeometry.Vector3D() else None

        # when user selected option to calculate offset
        if self.build_ele.CalculationType.value == 0:
            result = face_offset.Offset(offsetDistance      = self.build_ele.OffsetDistance.value,
                                        direction           = AllplanGeometry.FaceOffset.eFaceOffsetDirection.names[self.build_ele.OffsetDirection.value],
                                        useOffsetStepPierce = bool(self.build_ele.UseOffsetStepPierce.value),
                                        useOrthoVXSplit     = bool(self.build_ele.UseOrthoVXSplit.value),
                                        punchDirection      = punch_direction)

            return (is_brep, *result)

        # when user selected option to calculate shell
        result = face_offset.Shell(offsetDistance      = self.build_ele.OffsetDistance.value,
                                   direction           = AllplanGeometry.FaceOffset.eFaceOffsetDirection.names[self.build_ele.OffsetDirection.value],
                                   useOffsetStepPierce = bool(self.build_ele.UseOffsetStepPierce.value),
                                   useOrthoVXSplit     = bool(self.build_ele.UseOrthoVXSplit.value),
                                   punchDirection      = punch_direction)

        return (is_brep, *result, None)

    def create_elements(self) -> AllplanElementAdapter.BaseElementAdapterList:
        """Create new model elements from the geometries saved in the property elements_to_create
        in the current document. Clears the property after creation.

        Returns:
            list of element adapters of the created elements
        """

        if len(self.elements_to_create) > 0:
            created_elements = AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                                                  AllplanGeometry.Matrix3D(),
                                                                  self.elements_to_create,
                                                                  modelUuidList = [],
                                                                  assoRefObj    = None)
            self.elements_to_create.clear()
            return created_elements

        return AllplanElementAdapter.BaseElementAdapterList()
