""" Script for LabelBarPlacement
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementService import BuildingElementListService
from CreateElementResult import CreateElementResult
from PythonPartPreview import PythonPartPreview

from ParameterUtils.Reinforcement.DimensionLinePropertiesParameterUtil import DimensionLinePropertiesParameterUtil
from ParameterUtils.Reinforcement.LabelPropertiesParameterUtil import LabelPropertiesParameterUtil
from ParameterUtils.Reinforcement.TextPointerPropertiesParameterUtil import TextPointerPropertiesParameterUtil

from Utils import LibraryBitmapPreview
from Utils.ElementFilter.ReinforcementElementsQueryUtil import ReinforcementElementsQueryUtil
from Utils.Reinforcement.LabelingUtil import LabelingUtil

from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LabelBarPlacementBuildingElement \
        import LabelBarPlacementBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load LabelBarPlacement.py')


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
                               r"Examples\PythonParts\ReinforcementExamples\Labels\LabelBarPlacement.png"))


def create_script_object(build_ele  : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return LabelBarPlacement(build_ele, script_object_data)


class LabelBarPlacement(BaseScriptObject):
    """ Definition of class LabelBarPlacement
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele

        self.sel_result    = MultiElementSelectInteractorResult()
        self.placement_elements = list[AllplanReinf.BarPlacement]()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = MultiElementSelectInteractor(self.sel_result,
                                                                     ReinforcementElementsQueryUtil.create_linear_bar_placement_query(),
                                                                     "Select the bar represetation(s)")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        self.placement_elements = AllplanBaseEle.GetElements(self.sel_result.sel_elements)

        if not self.placement_elements:
            return

        self.script_object_interactor = None

        self.build_ele.InputMode.value = self.build_ele.LABEL_INPUT


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        for placement in self.placement_elements:
            label = self.create_dim_line_label(placement.PositionNumber)    \
                        if LabelingUtil.is_placement_labeling(placement.GetRepresentation()) else \
                    self.create_pointer_label(placement.PositionNumber)

            placement.SetLabel(label, AllplanEleAdapter.AssocViewElementAdapter())

        PythonPartPreview.draw_reinforcement_labeling_preview(self.document, self.placement_elements, True)

        return CreateElementResult([])


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
           On cancel function result
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        PythonPartPreview.close()

        undo_redo = AllplanIFW.UndoRedoService(self.document)

        AllplanReinf.CreateReinforcementLabeling(self.document, AllplanGeo.Matrix3D(), self.placement_elements,
                                                 self.coord_input.GetViewWorldProjection(), undo_redo)

        undo_redo.CreateUndoStep()

        return OnCancelFunctionResult.RESTART


    def create_dim_line_label(self,
                              position_number: int) -> AllplanReinf.ReinforcementLabel:
        """ Create a dimension line label

        Args:
            position_number: position number of the bar placement

        Returns:
            Reinforcement label
        """

        build_ele = self.build_ele

        label_props = LabelPropertiesParameterUtil.create_label_properties(build_ele, "DimLine")

        text_props           = AllplanBasisEle.TextProperties()
        text_props.Alignment = AllplanBasisEle.TextAlignment.names[build_ele.TextAlignmentDimLine.value]

        label = AllplanReinf.ReinforcementLabel(reinforcementType    = AllplanReinf.ReinforcementType.Bar,
                                                type                 = AllplanReinf.LabelType.LabelWithDimensionLine,
                                                positionNumber       = position_number,
                                                labelProp            = label_props,
                                                bDimLineAtShapeStart = build_ele.DimLineAtShapeStart.value,
                                                dimLineOffset        = build_ele.DimLineOffset.value)

        DimensionLinePropertiesParameterUtil.create_dim_line_properties(build_ele, label, "DimLine")

        label.SetTextProperties(text_props)

        return label


    def create_pointer_label(self,
                                 position_number: int) -> AllplanReinf.ReinforcementLabel:
        """ Create a text pointer label

        Args:
            position_number: position number of the bar placement

        Returns:
            Reinforcement label
        """

        build_ele = self.build_ele

        label_props = LabelPropertiesParameterUtil.create_label_properties(build_ele, "DimLine")

        text_props           = AllplanBasisEle.TextProperties()
        text_props.Alignment = AllplanBasisEle.TextAlignment.names[build_ele.TextAlignmentDimLine.value]

        if build_ele.LabelPositionDefinition.value == build_ele.LABEL_POSITION_BY_POINT:        # pylint: disable=consider-ternary-expression
            label = AllplanReinf.ReinforcementLabel(reinforcementType = AllplanReinf.ReinforcementType.Bar,
                                                    type              = AllplanReinf.LabelType.LabelWithPointer,
                                                    positionNumber    = position_number,
                                                    labelProp         = label_props,
                                                    labelPoint        = build_ele.LabelPoint.value,
                                                    angle             = AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

        else:
            label = AllplanReinf.ReinforcementLabel(reinforcementType = AllplanReinf.ReinforcementType.Bar,
                                                    type              = AllplanReinf.LabelType.LabelWithPointer,
                                                    positionNumber    = position_number,
                                                    labelProp         = label_props,
                                                    shapeSide         = build_ele.ShapeSide.value,
                                                    shapeSideFactor   = build_ele.ShapeSideFactor.value,
                                                    labelOffset       = build_ele.LabelOffset.value,
                                                    angle             = AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

        TextPointerPropertiesParameterUtil.create_text_pointer_properties(build_ele, label, "")

        label.SetTextProperties(text_props)

        return label
