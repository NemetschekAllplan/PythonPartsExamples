""" Script for the extrude bar along path
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ExtrudeBarAlongPathBuildingElement \
        import ExtrudeBarAlongPathBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ExtrudeBarAlongPath.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = ExtrudeBarAlongPath(doc)

    return element.create(build_ele)


class ExtrudeBarAlongPath():
    """ Definition of class ExtrudeBarAlongPath
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class ExtrudeBarAlongPath

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc

    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        ramp_radius  = build_ele.RampRadius.value
        ramp_height  = build_ele.RampHeight.value
        plate_width  = build_ele.PlateWidth.value
        plate_height = build_ele.PlateHeight.value


        #----------------- create the ramp ------------------------------------


        count = 30

        angle_delta       = math.pi / count
        ramp_height_delta = ramp_height / count

        points = [AllplanGeo.Point3D(-ramp_radius + math.cos(angle_delta * index) * ramp_radius,
                                     math.sin(angle_delta * index) * ramp_radius, ramp_height_delta * index) \
                  for index in range(0, count + 1)]

        spline = AllplanGeo.Spline3D(points)

        start_vec = AllplanGeo.Vector3D(points[0], points[1])
        end_vec   = AllplanGeo.Vector3D(points[-2], points[-1])

        start_vec.X = 0
        end_vec.X   = 0

        start_vec.Normalize()
        end_vec.Normalize()

        spline.SetStartVector(start_vec)
        spline.SetEndVector(end_vec)


        #----------------- create the extrusion polygon

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D()
        polyline += AllplanGeo.Point3D(plate_width, 0, 0)
        polyline += AllplanGeo.Point3D(plate_width, 0, plate_height)
        polyline += AllplanGeo.Point3D(0, 0, plate_height)
        polyline += AllplanGeo.Point3D()


        #----------------- extrude the polygon

        err, extruded_ele = AllplanGeo.CreateSweptBRep3D([polyline], spline, True, False,
                                                         AllplanGeo.Vector3D(0, 0, 1000), 0)

        if err:
            AllplanUtil.ShowMessageBox("Not possible to extrude the geometry", AllplanUtil.MB_OK)

            return CreateElementResult()


        #-------------------- create the placement ----------------------------


        path = AllplanGeo.Path3D()

        path += spline

        rotation = {"No rotation": AllplanReinf.ExtrudeBarPlacement.eProfileRotation.eNoRotation,
                    "Standard"   : AllplanReinf.ExtrudeBarPlacement.eProfileRotation.eStandard,
                    "Z-Axis"     : AllplanReinf.ExtrudeBarPlacement.eProfileRotation.eZ_Axis}[build_ele.ProfileRotation.value]

        edge_offset = [AllplanReinf.ExtrudeBarPlacement.eEdgeOffsetType.eZeroAtStart,
                       AllplanReinf.ExtrudeBarPlacement.eEdgeOffsetType.eMajorValueAtStart,
                       AllplanReinf.ExtrudeBarPlacement.eEdgeOffsetType.eStartEqualEnd,
                       AllplanReinf.ExtrudeBarPlacement.eEdgeOffsetType.eMajorValueAtEnd,
                       AllplanReinf.ExtrudeBarPlacement.eEdgeOffsetType.eZeroAtEnd]

        placement = AllplanReinf.ExtrudeBarPlacement(1, path, rotation,
                                                     build_ele.BreakElimination.value, build_ele.MaxBreakAngle.value,
                                                     build_ele.Distance.value,
                                                     build_ele.ConcreteCoverStart.value, build_ele.ConcreteCoverEnd.value,
                                                     edge_offset[build_ele.EdgeOffsetType.value],
                                                     build_ele.EdgeOffsetStart.value, build_ele.EdgeOffsetEnd.value,
                                                     build_ele.BarOffset.value, AllplanGeo.Vector3D(0, 1, 0))

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        com_prop.Color = build_ele.PreviewColor.value
        com_prop.Layer = build_ele.Layer.value

        placement.CommonProperties = com_prop

        for section in build_ele.Sections.value:
            placement.AddPlacementSection(AllplanReinf.BarPlacementSection(section.IsEnabled, section.Length, section.Distance))


        #----------------- create the cross reinforcement

        concrete_cover = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        bending_roller = build_ele.BendingRoller.value
        steel_grade    = build_ele.SteelGrade.value

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller,
                                                         steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        bottom_shape = GeneralShapeBuilder.create_open_stirrup(plate_width, plate_height / 2, RotationAngles(90, 0, 0),
                                                               shape_props, concrete_cover_props, -1, -1)

        top_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(plate_width, RotationAngles(0, 0, 0),
                                                                             shape_props, concrete_cover_props)

        top_shape.Rotate(RotationAngles(-90, 0, 0))
        top_shape.Move(AllplanGeo.Vector3D(0, 0, plate_height))

        placement.AddCrossBendingShape(bottom_shape)
        placement.AddCrossBendingShape(top_shape)


        #----------------- create the longitudinal bars

        ExtrudeBarAlongPath.create_longitudinal_bars(build_ele, placement)


        #----------------- create the edge offsets and extrude the placement

        build_ele.EdgeOffsetStart.value, build_ele.EdgeOffsetEnd.value = placement.GetEdgeOffsets()

        placement.Extrude()


        #----------------- add the attributes

        build_ele_attr_list = BuildingElementAttributeList()

        build_ele_attr_list.add_attributes_from_parameters(build_ele)

        build_ele_attr_list.set_attributes_to_element(placement)

        #----------------- Create PythonPart

        pyp_util = PythonPartUtil()

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisEle.ModelElement3D(com_prop, extruded_ele))
        pyp_util.add_reinforcement_elements(placement)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    @staticmethod
    def create_longitudinal_bars(build_ele: BuildingElement,
                                 placement: AllplanReinf.ExtrudeBarPlacement):
        """ Create the longitudinal bars

        Args:
            build_ele: building element with the parameter properties
            placement: placement
        """

        bending_roller = build_ele.BendingRoller.value
        concrete_cover = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        longi_diameter = build_ele.LongitudinalDiameter.value
        steel_grade    = build_ele.LongitudinalSteelGrade.value

        x_start = concrete_cover + diameter + bending_roller / 2 * diameter
        x_end   = build_ele.PlateWidth.value - x_start

        bar_count = 10

        delta = (x_end - x_start) / (bar_count - 1)

        z_bar = concrete_cover + diameter + longi_diameter / 2

        delivery_shape_type = {"Straight": AllplanReinf.LongitudinalBarProperties.eDeliveryShapeType.eStraight,
                               "Round": AllplanReinf.LongitudinalBarProperties.eDeliveryShapeType.eRound}

        inside_bars_state = {"Exact": AllplanReinf.LongitudinalBarProperties.eInsideBarsState.eExact,
                             "Shortened": AllplanReinf.LongitudinalBarProperties.eInsideBarsState.eShortened,
                             "Overlapped": AllplanReinf.LongitudinalBarProperties.eInsideBarsState.eOverlapped}


        #---------------- create the bottom bars
        #                 The bending shape of the longitudinal bar is defined by a point at the placement position

        start_length = build_ele.StartLength.value

        for index in range(bar_count):
            x_bar = x_start + delta * index

            shape = AllplanReinf.BendingShape(AllplanGeo.Point3D(x_bar, 0, z_bar), longi_diameter, steel_grade,  -1)

            longi_bar = AllplanReinf.LongitudinalBarProperties(shape,
                                                               build_ele.IsOverlappingAtStart.value,
                                                               build_ele.OverlappingAtStart.value,
                                                               build_ele.IsOverlappingAtEnd.value,
                                                               build_ele.OverlappingAtEnd.value,
                                                               build_ele.OverlappingLength.value,
                                                               0.,
                                                               delivery_shape_type[build_ele.DeliveryShapeType.value],
                                                               inside_bars_state[build_ele.InsideBarsState.value],
                                                               start_length if index % 2 else start_length / 2)

            placement.AddLongitudinalBarProp(longi_bar)


        #---------------- create the top bars
        #                 The bending shape of the longitudinal bar is defined by a point at the placement position

        delta = x_end - x_start
        z_bar = build_ele.PlateHeight.value - z_bar

        for index in range(2):
            x_bar = x_start + delta * index

            shape = AllplanReinf.BendingShape(AllplanGeo.Point3D(x_bar, 0, z_bar), longi_diameter, steel_grade,  -1)

            longi_bar = AllplanReinf.LongitudinalBarProperties(shape,
                                                               build_ele.IsOverlappingAtStart.value,
                                                               build_ele.OverlappingAtStart.value,
                                                               build_ele.IsOverlappingAtEnd.value,
                                                               build_ele.OverlappingAtEnd.value,
                                                               build_ele.OverlappingLength.value,
                                                               0.,
                                                               delivery_shape_type[build_ele.DeliveryShapeType.value],
                                                               inside_bars_state[build_ele.InsideBarsState.value],
                                                               build_ele.StartLength.value)

            placement.AddLongitudinalBarProp(longi_bar)
