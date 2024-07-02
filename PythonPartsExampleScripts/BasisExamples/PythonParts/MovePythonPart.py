""" Example script to show the possibility of moving or copying an already existing
PythonPart into a new location by modifying its placement matrix.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from TypeCollections import ModelEleList
from Utils import LibraryBitmapPreview, RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.MovePythonPartBuildingElement import MovePythonPartBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load MovePythonPart.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\ObjectCreation\PlaceExistingPythonPart.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return PlaceExistingPythonPart(build_ele, coord_input)


class PlaceExistingPythonPart(BaseScriptObject):
    """ Definition of a script object MovePythonPart

    This script object prompts the user to select a PythonPart (or smart symbol or SmartPart) and allows
    him to place it in a new location and with a different rotation by redefining the placement matrix
    of the MacroPlacement object representing the selected PythonPart.
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.build_ele = build_ele

        self.sel_result = SingleElementSelectResult()
        self.pnt_result = PointInteractorResult()

        self.sel_python_part = AllplanBasisEle.MacroPlacementElement()
        """Selected PythonPart represented by a macro placement"""


    def start_input(self):
        """ Start the selection of a PythonPart, SmartPart or smart symbol
        """

        build_ele = self.build_ele

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_result,
                                                                      [AllplanEleAdapter.PythonPart_TypeUUID,
                                                                       AllplanEleAdapter.SmartPart_TypeUUID,
                                                                       AllplanEleAdapter.SmartSymbol_TypeUUID,
                                                                       ],
                                                                      "Select a PythonPart, smart symbol or a SmartPart")
        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ Start the input of the new placement point
        """

        build_ele = self.build_ele


        #----------------- start the placement input

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            elements = AllplanBaseEle.GetElements(AllplanEleAdapter.BaseElementAdapterList([self.sel_result.sel_element]))

            self.sel_python_part = cast(AllplanBasisEle.MacroPlacementElement, elements[0])

            self.script_object_interactor = PointInteractor(self.pnt_result, True,
                                                            "Place the element", self.draw_preview)

            build_ele.InputMode.value = build_ele.ELEMENT_PLACEMENT

            return


        #----------------- create the PythonPart with new placement matrix
        match self.build_ele.MoveOrCopy.value:
            case "Move":
                self.modify_pyp_placement()
                self.start_input()
            case "Copy":
                AllplanBaseEle.CreateElements(self.document, AllplanGeo.Matrix3D(),
                                              self.create_pyp_placement(), [], None)

    def execute(self) -> CreateElementResult:
        """ Execute the script

        Returns:
            created element result
        """

        return CreateElementResult([])  # nothing to create, the scripts only modifies the object


    def draw_preview(self):
        """ draw the preview
        """

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeo.Matrix3D(),
                                          self.create_pyp_placement(), False, None)


    def create_pyp_placement(self) -> ModelEleList:
        """ Create a new PythonPart placement (MacroPlacement) referring to the same macro definition
        as of the selected PythonPart but with a new placement matrix

        Returns:
            list with the new placement
        """

        pyp_placement_prop        = self.sel_python_part.MacroPlacementProperties
        pyp_placement_prop.Matrix = self.placement_matrix
        model_ele_list            = ModelEleList()
        pyp_placement             = AllplanBasisEle.MacroPlacementElement(self.sel_python_part.CommonProperties,
                                                                          pyp_placement_prop,
                                                                          self.sel_python_part.GetMacro(),
                                                                          [])
        pyp_placement.Attributes = self.sel_python_part.Attributes

        model_ele_list.append(pyp_placement)

        return model_ele_list

    def modify_pyp_placement(self) -> None:
        """ Modifies the selected PythonPart placement (MacroPlacement) by changing its placement matrix
        """

        placement_props        = self.sel_python_part.GetMacroPlacementProperties()
        placement_props.Matrix = self.placement_matrix
        self.sel_python_part.SetMacroPlacementProperties(placement_props)

        AllplanBaseEle.ModifyElements(self.document, [self.sel_python_part])

    @property
    def placement_matrix(self) -> AllplanGeo.Matrix3D:
        """Property containing the new placement matrix

        The matrix describes rotations around X,Y and Z (angles are get from the property palette)
        and translation from the origin to the placement point picked by the user in the viewport,
        exactly in this order.

        Returns:
            placement matrix
        """
        translation = AllplanGeo.Matrix3D()
        translation.SetTranslation(AllplanGeo.Vector3D(self.pnt_result.input_point))

        rotation = RotationUtil(self.build_ele.AngleX.value,
                                self.build_ele.AngleY.value,
                                self.build_ele.AngleZ.value).get_rotation_matrix()

        return rotation * translation
