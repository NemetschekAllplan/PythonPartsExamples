""" Script for the sweep bar along path
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

from TypeCollections import Curve3DList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SweepBarAlongPathBuildingElement \
        import SweepBarAlongPathBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load SweepBarAlongPath.py')


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
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    element = SweepBarAlongPath()

    return element.create(build_ele)


class SweepBarAlongPath():
    """ Definition of class SweepBarAlongPath
    """

    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        ramp_radius        = build_ele.RampRadius.value
        ramp_height        = build_ele.RampHeight.value
        plate_width_bottom = build_ele.PlateWidthBottom.value
        plate_width_top    = build_ele.PlateWidthTop.value
        plate_height       = build_ele.PlateHeight.value
        outer_radius       = ramp_radius + (plate_width_bottom + plate_width_top) / 4
        inner_radius       = ramp_radius - (plate_width_bottom + plate_width_top) / 4


        #----------------- create the ramp ------------------------------------


        count = 30

        angle_delta       = math.pi / count
        ramp_height_delta = ramp_height / count


        #----------------- create the sweep paths

        axis_points = [AllplanGeo.Point3D(-ramp_radius + math.cos(angle_delta * index) * ramp_radius,
                                           math.sin(angle_delta * index) * ramp_radius, ramp_height_delta * index) \
                        for index in range(0, count + 1)]

        outer_points = [AllplanGeo.Point3D(-outer_radius + plate_width_bottom / 2 + math.cos(angle_delta * index) * outer_radius,
                                           math.sin(angle_delta * index) * outer_radius, ramp_height_delta * index) \
                        for index in range(0, count + 1)]

        inner_points = [AllplanGeo.Point3D(-inner_radius - plate_width_bottom / 2 + math.cos(angle_delta * index) * inner_radius,
                                           math.sin(angle_delta * index) * inner_radius, ramp_height_delta * index) \
                        for index in range(0, count + 1)]

        axis_spline = AllplanGeo.Spline3D(axis_points)
        outer_spline = AllplanGeo.Spline3D(outer_points)
        inner_spline = AllplanGeo.Spline3D(inner_points)

        def set_start_end_vector(spline: AllplanGeo.Spline3D,
                                 points: List[AllplanGeo.Point3D]):
            start_vec = AllplanGeo.Vector3D(points[0], points[1])
            end_vec   = AllplanGeo.Vector3D(points[-2], points[-1])

            start_vec.X = 0
            end_vec.X   = 0

            start_vec.Normalize()
            end_vec.Normalize()

            spline.SetStartVector(start_vec)
            spline.SetEndVector(end_vec)

        set_start_end_vector(axis_spline, axis_points)
        set_start_end_vector(outer_spline, outer_points)
        set_start_end_vector(inner_spline, inner_points)


        #----------------- create the bottom and top sweep polygon

        width_halve = plate_width_bottom / 2

        polyline1 = AllplanGeo.Polyline3D()
        polyline1 += AllplanGeo.Point3D(-width_halve, 0, 0)
        polyline1 += AllplanGeo.Point3D(width_halve, 0, 0)
        polyline1 += AllplanGeo.Point3D(width_halve, 0, plate_height)
        polyline1 += AllplanGeo.Point3D(-width_halve, 0, plate_height)
        polyline1 += AllplanGeo.Point3D(-width_halve, 0, 0)

        width_halve = plate_width_top / 2

        polyline2 = AllplanGeo.Polyline3D()
        polyline2 += AllplanGeo.Point3D(width_halve, 0, 0)
        polyline2 += AllplanGeo.Point3D(-width_halve, 0, 0)
        polyline2 += AllplanGeo.Point3D(-width_halve, 0, plate_height)
        polyline2 += AllplanGeo.Point3D(width_halve, 0, plate_height)
        polyline2 += AllplanGeo.Point3D(width_halve, 0, 0)

        polyline2 = AllplanGeo.Move(polyline2, AllplanGeo.Vector3D(-ramp_radius * 2, 0, ramp_height))


        #----------------- sweep the polygons

        err, extruded_ele, _ = AllplanGeo.CreateRailSweptBRep3D(Curve3DList([polyline1, polyline2]),
                                                                Curve3DList([inner_spline, outer_spline]), axis_spline,
                                                                 True, True, True, False)

        if err:
            AllplanUtil.ShowMessageBox("Not possible to extrude the geometry", AllplanUtil.MB_OK)

            return CreateElementResult()


        #-------------------- create the placement ----------------------------


        axis_path  = AllplanGeo.Path3D()
        inner_path = AllplanGeo.Path3D()
        outer_path = AllplanGeo.Path3D()

        axis_path  += axis_spline
        inner_path += inner_spline
        outer_path += outer_spline

        sweep_paths = AllplanGeo.Path3DList()
        sweep_paths.append(axis_path)
        sweep_paths.append(inner_path)
        sweep_paths.append(outer_path)

        edge_offset = [AllplanReinf.SweepBarPlacement.eEdgeOffsetType.eZeroAtStart,
                       AllplanReinf.SweepBarPlacement.eEdgeOffsetType.eMajorValueAtStart,
                       AllplanReinf.SweepBarPlacement.eEdgeOffsetType.eStartEqualEnd,
                       AllplanReinf.SweepBarPlacement.eEdgeOffsetType.eMajorValueAtEnd,
                       AllplanReinf.SweepBarPlacement.eEdgeOffsetType.eZeroAtEnd]

        placement = AllplanReinf.SweepBarPlacement(1, sweep_paths,
                                                   build_ele.Rotation.value, build_ele.FirstPathIsSweepPath.value,
                                                   build_ele.Interpolation.value, build_ele.InterpolationOfAllPoints.value,
                                                   build_ele.Distance.value,
                                                   build_ele.ConcreteCoverStart.value, build_ele.ConcreteCoverEnd.value,
                                                   edge_offset[build_ele.EdgeOffsetType.value],
                                                   build_ele.EdgeOffsetStart.value, build_ele.EdgeOffsetEnd.value,
                                                   build_ele.BarOffset.value, build_ele.BenchingLength.value,
                                                   build_ele.BenchingAngle.value)

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        com_prop.Color = build_ele.PreviewColor.value
        com_prop.Layer = build_ele.Layer.value

        placement.CommonProperties = com_prop

        for section in build_ele.Sections.value:
            placement.AddPlacementSection(AllplanReinf.BarPlacementSection(section.IsEnabled, section.Length, section.Distance))


        #----------------- create the reinforcement shapes at the start of the sweep

        concrete_cover = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        bending_roller = build_ele.BendingRoller.value
        steel_grade    = build_ele.SteelGrade.value

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller,
                                                         steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        bottom_shape = GeneralShapeBuilder.create_open_stirrup(plate_width_bottom, plate_height / 2, RotationAngles(90, 0, 0),
                                                               shape_props, concrete_cover_props, -1, -1)

        bottom_shape.Move(AllplanGeo.Vector3D(-plate_width_bottom / 2, 0, 0))

        top_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(plate_width_bottom, RotationAngles(0, 0, 0),
                                                                             shape_props, concrete_cover_props)

        top_shape.Rotate(RotationAngles(-90, 0, 0))
        top_shape.Move(AllplanGeo.Vector3D(-plate_width_bottom / 2, 0, plate_height))

        cross_bars_start = AllplanReinf.BendingShapeList()

        cross_bars_start.append(bottom_shape)
        cross_bars_start.append(top_shape)

        x_start = -build_ele.PlateWidthBottom.value / 2 + concrete_cover + diameter + bending_roller / 2 * diameter

        longi_bars_start = SweepBarAlongPath.create_longitudinal_bars(build_ele, x_start, -x_start, 0)

        placement.AddSectionBars(cross_bars_start, longi_bars_start,
                                 AllplanGeo.Plane3D(AllplanGeo.Point3D(0, 0, 0), AllplanGeo.Vector3D(0, 1, 0)))


        #----------------- create the reinforcement shapes at the end of the sweep (the point order must be mirrored)

        cross_bars_end = AllplanReinf.BendingShapeList()

        bottom_shape = GeneralShapeBuilder.create_open_stirrup(plate_width_top, plate_height / 2, RotationAngles(90, 0, 180),
                                                               shape_props, concrete_cover_props, -1, -1)

        top_shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(plate_width_top, RotationAngles(-90, 0, 180),
                                                                             shape_props, concrete_cover_props)

        top_shape.Move(AllplanGeo.Vector3D(0, 0, plate_height))

        bottom_shape.Move(AllplanGeo.Vector3D(-outer_radius * 2 + plate_width_bottom / 2 + plate_width_top, 0, ramp_height))
        top_shape.Move(AllplanGeo.Vector3D(-outer_radius * 2 + plate_width_bottom / 2 + plate_width_top, 0, ramp_height))

        cross_bars_end.append(bottom_shape)
        cross_bars_end.append(top_shape)

        x_start = -ramp_radius * 2 - build_ele.PlateWidthTop.value / 2 + concrete_cover + diameter + bending_roller / 2 * diameter
        x_end   = -ramp_radius * 2 + build_ele.PlateWidthTop.value / 2 - concrete_cover - diameter - bending_roller / 2 * diameter

        longi_bars_end = SweepBarAlongPath.create_longitudinal_bars(build_ele, x_end, x_start, ramp_height)

        placement.AddSectionBars(cross_bars_end, longi_bars_end,
                                 AllplanGeo.Plane3D(AllplanGeo.Point3D(-2 * ramp_radius, 0, ramp_height), AllplanGeo.Vector3D(0, 1, 0)))


        #----------------- create the edge offsets and sweep the placement

        build_ele.EdgeOffsetStart.value, build_ele.EdgeOffsetEnd.value = placement.GetEdgeOffsets()

        placement.Sweep()


        #----------------- Create PythonPart

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisEle.ModelElement3D(com_prop, extruded_ele))
        pyp_util.add_reinforcement_elements(placement)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    @staticmethod
    def create_longitudinal_bars(build_ele: BuildingElement,
                                 x_start  : float,
                                 x_end    : float,
                                 z_bottom : float) -> AllplanReinf.LongitudinalBarPropertiesList:
        """ Create the longitudinal bars

        Args:
            build_ele: building element
            x_start:   x-coordinate a start of the placement
            x_end:     x_coordinate a end of the placement
            z_bottom:  z-coordinate of the placement

        Returns:
            longitudinal bars
        """

        concrete_cover = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        longi_diameter = build_ele.LongitudinalDiameter.value
        steel_grade    = build_ele.LongitudinalSteelGrade.value

        bar_count = 10

        delta = (x_end - x_start) / (bar_count - 1)

        z_bar = z_bottom + concrete_cover + diameter + longi_diameter / 2

        delivery_shape_type = {"Straight": AllplanReinf.LongitudinalBarProperties.eDeliveryShapeType.eStraight,
                               "Round": AllplanReinf.LongitudinalBarProperties.eDeliveryShapeType.eRound}

        inside_bars_state = {"Exact": AllplanReinf.LongitudinalBarProperties.eInsideBarsState.eExact,
                             "Shortened": AllplanReinf.LongitudinalBarProperties.eInsideBarsState.eShortened,
                             "Overlapped": AllplanReinf.LongitudinalBarProperties.eInsideBarsState.eOverlapped}


        #---------------- create the bottom bars
        #                 The bending shape of the longitudinal bar is defined by a point at the placement position

        start_length = build_ele.StartLength.value

        section_longi_bars = AllplanReinf.LongitudinalBarPropertiesList()

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

            section_longi_bars.append(longi_bar)


        #---------------- create the top bars
        #                 The bending shape of the longitudinal bar is defined by a point at the placement position

        delta = x_end - x_start
        z_bar = z_bottom + build_ele.PlateHeight.value -  concrete_cover - diameter - longi_diameter / 2

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

            section_longi_bars.append(longi_bar)

        return section_longi_bars
