""" Script for BarLabelWithPointer
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PreviewSymbols import PreviewSymbols

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties

from TypeCollections.ModelEleList import ModelEleList

from Utils.RotationUtil import RotationUtil
from Utils.TextReferencePointPosition import TextReferencePointPosition

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BarLabelWithPointerBuildingElement import \
        BarLabelWithPointerBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load BarLabelWithPointer.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return BarLabelWithPointer(build_ele, script_object_data)


class BarLabelWithPointer(BaseScriptObject):
    """ Definition of class BarLabelWithPointer
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        stirrups = self.create_stirrups()
        label    = self.create_label()

        stirrups.SetLabel(label, AllplanElementAdapter.AssocViewElementAdapter())

        preview_symbols = self.create_preview_symbols(stirrups.GetBendingShape())

        return CreateElementResult(ModelEleList(element = stirrups),
                                   preview_symbols = preview_symbols)

    @staticmethod
    def create_stirrups() -> AllplanReinf.BarPlacement:
        """Create rectangular, closed stirrups:

        -   in XY plane
        -   500 mm long and 1000 mm wide
        -   8 mm diameter
        -   placed along Z+ axis
        -   with 200 mm spacing

        Returns:
            Linear placement of the stirrups
        """

        shape_props = ReinforcementShapeProperties.rebar(diameter           = 8,
                                                         bending_roller     = 4.0,
                                                         steel_grade        = -1,
                                                         concrete_grade     = -1,
                                                         bending_shape_type = AllplanReinf.BendingShapeType.Stirrup)

        stirrup_shape = GeneralShapeBuilder.create_stirrup(length               = 500,
                                                           width                = 1000,
                                                           model_angles         = RotationUtil(0, 0, 0),
                                                           shape_props          = shape_props,
                                                           concrete_cover_props = ConcreteCoverProperties.all(0),
                                                           stirrup_type         = AllplanReinf.StirrupType.Normal)

        return LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(position             = 1,
                                                                            shape                = stirrup_shape,
                                                                            from_point           = AllplanGeo.Point3D(),
                                                                            to_point             = AllplanGeo.Point3D(0, 0, 1000),
                                                                            concrete_cover_left  = 0,
                                                                            concrete_cover_right = 0,
                                                                            bar_distance         = 200)


    def create_label(self) -> AllplanReinf.BarLabel:
        """Create labels of the reinforcement based on the parameters in the property palette

        Returns:
            Reinforcement label
        """

        build_ele = self.build_ele


        # label properties
        label_props                    = AllplanReinf.ReinforcementLabelProperties()
        label_props.ShowPositionNumber = build_ele.ShowPositionNumber.value
        label_props.ShowBarDiameter    = build_ele.ShowBarDiameter.value
        label_props.ShowBarDistance    = build_ele.ShowBarDistance.value
        label_props.ShowBarCount       = build_ele.ShowBarCount.value
        label_props.ShowBendingShape   = build_ele.ShowBendingShape.value
        label_props.ShowBarPlace       = build_ele.ShowBarPlace.value
        label_props.ShowBarLength      = build_ele.ShowBarLength.value
        label_props.ShowSteelGrade     = build_ele.ShowSteelGrade.value
        label_props.ShowPositionAtEnd  = build_ele.ShowPositionAtEnd.value
        label_props.ShowTwoLineText    = build_ele.ShowTwoLineText.value

        # text properties
        text_props           = AllplanBasisEle.TextProperties()
        text_props.Alignment = AllplanBasisEle.TextAlignment.names[build_ele.TextAlignment.value]

        # place label by point
        if build_ele.LabelPositionDefinition.value == 1:    # LabelPositionDefinition.Point                                         # pylint: disable=consider-ternary-expression
            label = AllplanReinf.BarLabel(AllplanReinf.LabelType.LabelWithPointer, 1, label_props,
                                          build_ele.LabelPoint.value, AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

        # place label by shape leg and offset to it
        else:
            label = AllplanReinf.BarLabel(AllplanReinf.LabelType.LabelWithPointer, 1, label_props,
                                          build_ele.ShapeSide.value, build_ele.ShapeSideFactor.value,
                                          build_ele.LabelOffset.value, AllplanGeo.Angle.FromDeg(build_ele.Angle.value))

        # additional label properties

        if build_ele.SetPointerStartPoint.value:
            label.SetPointerStartPoint(build_ele.PointerStartPoint.value)

        if build_ele.SetAdditionalText.value:
            label.SetAdditionalText(build_ele.AdditionalText.value)

        label.TextProperties    = text_props
        label.ShowTextPointer   = build_ele.ShowTextPointer.value
        label.PointerProperties = build_ele.PointerProperties.value

        return label


    def create_preview_symbols(self,
                               bending_shape: AllplanReinf.BendingShape) -> PreviewSymbols:
        """Creates symbols for preview, depending on label placement option:

        -   Create label by point:                  a cross indicating placement point of the label is created
        -   Create label by shape leg and offset:   numbers indicating the legs indices are created

        Args:
            bending_shape:  labeled bending shape

        Returns:
            preview symbols object containing the cross/numbers
        """

        build_ele = self.build_ele

        preview_symbols = PreviewSymbols()

        if build_ele.LabelPositionDefinition.value == 1:
            preview_symbols.add_cross(AllplanGeo.Point3D(build_ele.LabelPoint.value),
                                    width = 40,
                                    color = 6)
        else:
            shape_lines = bending_shape.GetShapePolyline().GetLines()

            for idx, line in enumerate(shape_lines, start = 1):
                _, line_center = AllplanGeo.CenterCalculus.Calculate(line)

                preview_symbols.add_text(str(idx),
                                         line_center,
                                         TextReferencePointPosition.CENTER_CENTER,
                                         height         = 40,
                                         color          = 6,
                                         rotation_angle = AllplanGeo.Angle())
        return preview_symbols
