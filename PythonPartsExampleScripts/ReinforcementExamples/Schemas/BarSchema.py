""" Script for BarSchema
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.LinearBarPlacementBuilder import StartEndPlacementRule
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from TypeCollections.ModelEleList import ModelEleList

from Utils.RotationUtil import RotationUtil


from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BarSchemaBuildingElement import BarSchemaBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load BarSchema.py')


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

    return BarSchema(build_ele, script_object_data)


class BarSchema(BaseScriptObject):
    """ Definition of class BarSchema
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

        # determine the bending rollers based on the norm
        self.bending_roller_stirrup = AllplanReinf.BendingRollerService.GetBendingRollerFactor(build_ele.DiameterStirrup.value,
                                                                                               build_ele.SteelGrade.value,
                                                                                               -1, True)

        self.bending_roller_longitudinal = AllplanReinf.BendingRollerService.GetBendingRollerFactor(build_ele.DiameterLongitudinal.value,
                                                                                                    build_ele.SteelGrade.value,
                                                                                                    -1, False)


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

        build_ele = self.build_ele

         # create the geometry of the bounding box

        model_ele_list = ModelEleList(self.build_ele.CommonProp.value)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.Sizes.value.Values())

        model_ele_list.append_geometry_3d(polyhed)
        model_ele_list.append_geometry_3d(AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(2000, 0, 0)))


        # create the reinforcement placements

        reinf_ele_list = self.create_stirrups()

        reinf_ele_list += self.create_longitudinal()

        reinf_ele_list.append(self.create_bar_schema(1, AllplanGeo.Point2D(4000, build_ele.Sizes.value.Y + 1000)))

        reinf_ele_list.append(self.create_bar_schema(3, AllplanGeo.Point2D(3000, 0)))


        # create the PythonPart, if the option was selected in the palette

        if self.build_ele.IsPythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(model_ele_list)
            pyp_util.add_reinforcement_elements(reinf_ele_list)

            return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))

        return CreateElementResult(elements= model_ele_list + reinf_ele_list)


    def create_stirrups(self) -> ModelEleList:
        """ Create the stirrup placement

        Returns:
            stirrup placements
        """

        build_ele = self.build_ele

        # rotation angles to transform the stirrup shape from its local to the global coordinate system
        local_to_global = RotationUtil(90, 0 , 0)

        # define the bending shape and its properties
        shape_props = ReinforcementShapeProperties.rebar(build_ele.DiameterStirrup.value,
                                                         self.bending_roller_stirrup,
                                                         build_ele.SteelGrade.value,
                                                         -1,                # get the concrete grade from current Allplan settings
                                                         AllplanReinf.BendingShapeType.Stirrup)

        concrete_cover_props = ConcreteCoverProperties.all(build_ele.ConcreteCover.value)

        shape = GeneralShapeBuilder.create_stirrup(build_ele.Sizes.value.X,
                                                   build_ele.Sizes.value.Z,
                                                   local_to_global,
                                                   shape_props,
                                                   concrete_cover_props)

        # define the stirrup placement
        from_pnt = AllplanGeo.Point3D()
        to_point = from_pnt + AllplanGeo.Point3D(0, build_ele.Sizes.value.Y, 0)

        placement = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                            1, shape, from_pnt, to_point,
                            build_ele.ConcreteCover.value,
                            build_ele.ConcreteCover.value - build_ele.DiameterStirrup.value,
                            build_ele.DistanceStirrup.value,
                            StartEndPlacementRule[build_ele.PlacementRuleStirrup.value])

        # if selected in the palette, set placement type to per linear meter and the length factor
        placement.PlacePerLinearMeter = self.build_ele.PlacePerLinearMeter.value

        if self.build_ele.PlacePerLinearMeter.value:
            placement.LengthFactor = self.build_ele.LengthFactor.value

        placement.SetPartialSchema(self.create_bar_schema(1, AllplanGeo.Point2D(0, build_ele.Sizes.value.Y + 1000)))

        model_ele_list = ModelEleList()
        model_ele_list.append(placement)

        trans_mat = AllplanGeo.Matrix3D()
        trans_mat.SetTranslation(AllplanGeo.Vector3D(2000, 0, 0))

        placement = AllplanReinf.BarPlacement(placement)

        placement.Transform(trans_mat)

        placement.SetPartialSchema(self.create_bar_schema(1, AllplanGeo.Point2D(2000, build_ele.Sizes.value.Y + 1000)))

        model_ele_list.append(placement)

        return model_ele_list


    def create_longitudinal(self) -> ModelEleList:
        """ Create the longitudinal bar placement

        Returns:
            list with both placements: top and bottom longitudinal bars
        """

        build_ele = self.build_ele

        # define the bending shape properties for both top and bottom longitudinal bar shapes
        cover_side = build_ele.ConcreteCover.value + (1 + self.bending_roller_stirrup * build_ele.DiameterStirrup.value) / 2

        shape_props = ReinforcementShapeProperties.rebar(build_ele.DiameterLongitudinal.value,
                                                         self.bending_roller_longitudinal,
                                                         build_ele.SteelGrade.value, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        concrete_cover = build_ele.ConcreteCover.value

        cover_props = ConcreteCoverProperties.left_right_bottom(concrete_cover, concrete_cover,
                                                                concrete_cover + build_ele.DiameterStirrup.value)

        # define the bottom shape
        bottom_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(build_ele.Sizes.value.Y,
                                                                                RotationUtil(90, 0 , 90),
                                                                                shape_props,
                                                                                cover_props)

        # define the top shape by rotating and moving the bottom one
        top_shape = AllplanReinf.BendingShape(bottom_shape)
        top_shape.Rotate(RotationUtil(0, 180, 0))                   # rotate the bottom shape around the global Y axis
        top_shape.Move(AllplanGeo.Vector3D(0, 0, build_ele.Sizes.value.Z))      # move the rotated shape to the top of the cube

        # define the start and end points for the placement
        from_pnt = AllplanGeo.Point3D(0, 0, 0)
        to_pnt   = from_pnt + AllplanGeo.Point3D(build_ele.Sizes.value.X, 0, 0)

        # create list with both placements
        longitudinal_bar_placements = ModelEleList()

        trans_mat = AllplanGeo.Matrix3D()
        trans_mat.SetTranslation(AllplanGeo.Vector3D(2000, 0, 0))

        for mark_nr, shape in enumerate([top_shape, bottom_shape], start= 3):
            placement = LinearBarBuilder.create_linear_bar_placement_from_to_by_count(mark_nr, shape, from_pnt, to_pnt,
                                                                                      cover_side, cover_side,
                                                                                      build_ele.BarCountLongitudinal.value)
            # if selected in the palette, set placement type to per linear meter and the length factor
            placement.PlacePerLinearMeter = self.build_ele.PlacePerLinearMeterLongitudinal.value

            if self.build_ele.PlacePerLinearMeterLongitudinal.value:
                placement.LengthFactor = self.build_ele.LengthFactorLongitudinal.value

            longitudinal_bar_placements.append(placement)

            placement = AllplanReinf.BarPlacement(placement)

            placement.Transform(trans_mat)

            longitudinal_bar_placements.append(placement)

        return longitudinal_bar_placements


    def create_bar_schema(self,
                          postion_number : int,
                          placement_point: AllplanGeo.Point2D) -> AllplanReinf.BarSchema:
        """ Create the bar schema

        Args:
            postion_number:  position number of the bar schema
            placement_point: placement point of the bar schema

        Returns:
            created bar schema
        """

        build_ele = self.build_ele

        schema = AllplanReinf.BarSchema(postion_number, placement_point)

        schema.AngleDimensioning   = build_ele.AngleDimensioning.value
        schema.BendingDimensioning = build_ele.BendingDimensioning.value
        schema.Dimensioning        = build_ele.Dimensioning.value
        schema.SegmentDimensioning = build_ele.SegmentDimensioning.value
        schema.ToScale             = build_ele.ToScale.value
        schema.Mirroring           = build_ele.Mirroring.value
        schema.RotationAngle       = build_ele.RotationAngle.value
        schema.StirrupUnfold       = build_ele.StirrupUnfold.value

        return schema
