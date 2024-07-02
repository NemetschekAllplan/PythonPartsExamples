"""
Script for the area reinforcement example
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil

from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


print('Load AreaShapeCreation.py')


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    length = AllplanGeo.Vector3D(handle_prop.ref_point, input_pnt).GetLength()

    build_ele.bar_max_length[int(handle_prop.handle_id)] = length

    return create_element(build_ele, doc)


def expand_create_element(build_ele, expand_util, ref_pnt, view_proj, doc, last_expanded):
    """
    Expande the area

    Args:
        build_ele:      the building element.
        expand_util:    the util for expansion.
        ref_pnt:        reference point.
        view_proj:      view world projection.
        doc:            input document
        last_expanded:  the geometry of the current element is created by an expansion
                        (in case of False it's not necessary to create the original element geometry)
    """

    del last_expanded

    build_ele.bar_max_length = []
    build_ele.polyline       = AllplanGeo.Polyline2D()


    #----------------- reference line

    result, dir_line, build_ele.z_min, _, asso_ref_ele, _, view_id = expand_util.GetLineFromPoint(doc, ref_pnt, view_proj, True)

    if result is False:
        build_ele.polyline = None

        return (False, False, AllplanGeo.Point3D(), asso_ref_ele, create_element(build_ele, doc))


    #----------------- set the first line to th polyline

    build_ele.polyline += dir_line.EndPoint
    build_ele.polyline += dir_line.StartPoint

    pol_start_pnt = dir_line.EndPoint

    line = dir_line

    print(result, line)

    while True:
        ortho_pnt = AllplanGeo.TransformCoord.PointGlobal(line,AllplanGeo.Point2D(0,1000))

        dir_vec = AllplanGeo.Vector2D(AllplanGeo.Point2D(ortho_pnt), line.StartPoint)

        start_pnt = line.StartPoint

        result, line, _, _, _ = expand_util.GetLineAtPoint(start_pnt, dir_vec, True, 45)

        print(result, line)

        if result is False:
            dir_vec = dir_vec.Reverse()

            result, line, _, _, _ = expand_util.GetLineAtPoint(start_pnt, dir_vec, True, 45)

            print(result, line)

            if result is False:
                build_ele.polyline = None

                return (False, False, AllplanGeo.Point3D(), asso_ref_ele,
                        create_element(build_ele, doc))

        build_ele.polyline += line.StartPoint

        if line.StartPoint == pol_start_pnt:
            break

    return (True, True, AllplanGeo.Point3D(), asso_ref_ele,
            create_element(build_ele, doc))


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = AreaShapeCreation(doc)

    return element.create(build_ele)


def modify_element_property(build_ele, name, value):
    """
    Modify property of element

    Args:
        build_ele:  the building element.
        name:       the name of the property.
        value:      new value for property.

    Returns:
        True/False if palette refresh is necessary
    """

    if name != "Diameter":
        return False

    settings = AllplanReinf.ReinforcementSettings

    anchorage_service = AllplanReinf.AnchorageLengthService()

    anchorage_service.CalculateBar(settings.GetConcreteGrade(),settings.GetSteelGrade(),
                                   value, False, 0, 10.)

    build_ele.BarOverlap.value = anchorage_service.GetAnchorageLength()

    return True


class AreaShapeCreation():
    """
    Definition of class AreaShapeCreation
    """

    def __init__(self, doc):
        """
        Initialisation of class AreaShapeCreation

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = []
        self.preview_list   = []
        self.document       = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements, handles and reinforcement.
        """

        polyline = getattr(build_ele, "polyline", None)


        #----------------- create the preview

        if polyline is None:
            polyline = AllplanGeo.Polyline2D()

            polyline += AllplanGeo.Point2D(0,0)
            polyline += AllplanGeo.Point2D(0,5000)
            polyline += AllplanGeo.Point2D(2000,5000)
            polyline += AllplanGeo.Point2D(5000,6000)
            polyline += AllplanGeo.Point2D(5000,0)
            polyline += AllplanGeo.Point2D(0,0)

            build_ele.polyline       = polyline
            build_ele.bar_max_length = []
            build_ele.z_min          = 0

        diameter       = build_ele.Diameter.value
        concrete_cover = build_ele.ConcreteCover.value
        distance       = build_ele.Distance.value
        bending_roller = 4
        steel_grade    = build_ele.SteelGrade.value
        bar_max_length = build_ele.BarMaxLength.value
        overlap        = build_ele.BarOverlap.value

        if overlap == 0:
            settings = AllplanReinf.ReinforcementSettings

            anchorage_service = AllplanReinf.AnchorageLengthService()

            anchorage_service.CalculateBar(settings.GetConcreteGrade(),settings.GetSteelGrade(),
                                           diameter, False, 0, 10.)

            overlap = anchorage_service.GetAnchorageLength()

            build_ele.BarOverlap.value = overlap

        old_bar_max_length = getattr(build_ele, "old_bar_max_length", None)

        if old_bar_max_length != None  and  old_bar_max_length != bar_max_length:
            build_ele.bar_max_length = []

        build_ele.old_bar_max_length = bar_max_length


        #----------------- get the local coordinates of the polygon (base is the direction line)

        minmax = AllplanGeo.MinMax2D()

        dir_line = polyline.GetLine(0)

        loc_poly = AllplanGeo.Polyline2D()

        y_sections = []

        eps = 0.001

        for i in range(polyline.Count()):
            pnt = AllplanGeo.TransformCoord.PointLocal(dir_line, polyline.GetPoint(i))

            minmax   += pnt
            loc_poly += pnt

            insert = False

            for j in range(len(y_sections)):
                if abs(pnt.Y - y_sections[j]) < eps:
                    insert = True
                    break

                elif pnt.Y < y_sections[j]:
                    insert = True

                    y_sections.insert(j,pnt.Y)

                    break

            if not insert:
                y_sections.append(pnt.Y)

        x_start = minmax.GetMin().X
        x_end   = minmax.GetMax().X


        #----------------- calculate the placements

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        pos_nr = 1

        old_bar_max_length = []
        old_bar_max_length.extend(build_ele.bar_max_length)

        build_ele.bar_max_length.clear()

        max_length_index = 0

        self.preview_list = []

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        for i_sect in range(len(y_sections) - 1):
            y_start = y_sections[i_sect] + concrete_cover
            y_end = y_sections[i_sect + 1] - concrete_cover

            place_length = y_end - y_start


            #----------------- calculate the start end end bar line

            bar_lines = []

            while True:
                intersect_pnt = []

                intersect_line = AllplanGeo.Line2D(x_start, y_start, x_end, y_start)

                for i in range(loc_poly.Count() - 1):
                    result, inter_pnt = AllplanGeo.IntersectionCalculus(loc_poly.GetLine(i), intersect_line)

                    if result:
                        intersect_pnt.append(inter_pnt)

                if len(intersect_pnt) > 1:
                    bar_pnt1 = AllplanGeo.TransformCoord.PointGlobal(dir_line, intersect_pnt[0])
                    bar_pnt2 = AllplanGeo.TransformCoord.PointGlobal(dir_line, intersect_pnt[1])

                    bar_pnt1.Z = build_ele.z_min + concrete_cover + diameter / 2
                    bar_pnt2.Z = build_ele.z_min + concrete_cover + diameter / 2

                    bar_line = AllplanGeo.Line3D(bar_pnt1, bar_pnt2)
                    bar_line.TrimStart(concrete_cover)
                    bar_line.TrimEnd(concrete_cover)

                    bar_lines.append(bar_line)

                if y_start == y_end:
                    break

                y_start = y_end

            if len(bar_lines) == 2:
                place_vec_bottom = AllplanGeo.Vector3D(bar_lines[0].StartPoint, bar_lines[1].StartPoint)
                place_vec_top    = AllplanGeo.Vector3D(bar_lines[0].EndPoint, bar_lines[1].EndPoint)

                start_len = AllplanGeo.CalcLength(bar_lines[0])
                end_len   = AllplanGeo.CalcLength(bar_lines[1])

                max_length = bar_max_length if max_length_index >= len(old_bar_max_length) else \
                             old_bar_max_length[max_length_index]

                count = int(place_length / distance)


                #----------------- cut the placements

                while start_len > max_length  or  end_len > max_length:
                    count = int(place_length / distance)

                    if start_len < max_length:
                        bar_line1, bar_line2, delta_vec_bottom, delta_vec_top, poly_count = \
                            self.get_poly_bar_lines(bar_lines[0], bar_lines[1], max_length,
                                                    place_vec_bottom, place_vec_top, count, True)

                        self.append_polygonal_placement(bar_line1, bar_line2, shape_props, poly_count + 1, pos_nr)

                        bar_line2.StartPoint = bar_line2.StartPoint + delta_vec_bottom
                        bar_line2.EndPoint   = bar_line2.EndPoint + delta_vec_top

                        bar_lines[0] = bar_line2

                        start_len = AllplanGeo.CalcLength(bar_line2)

                        count -= poly_count - 1

                    elif end_len < max_length:
                        bar_line1, bar_line2, delta_vec_bottom, delta_vec_top, poly_count = \
                            self.get_poly_bar_lines(bar_lines[1], bar_lines[0], max_length,
                                                    place_vec_bottom, place_vec_top, count, False)

                        self.append_polygonal_placement(bar_line1, bar_line2, shape_props, poly_count + 1, pos_nr)

                        bar_line1.StartPoint = bar_line1.StartPoint - delta_vec_bottom
                        bar_line1.EndPoint   = bar_line1.EndPoint - delta_vec_top

                        bar_lines[1] = bar_line1

                        end_len = AllplanGeo.CalcLength(bar_line1)

                        count -= poly_count - 1


                    #----------------- create the handle for the max length

                    center1 = (bar_lines[0].StartPoint + bar_lines[1].StartPoint) / 2
                    center2 = (bar_lines[0].EndPoint + bar_lines[1].EndPoint) / 2

                    handle_line = AllplanGeo.Line3D(center1, center2)

                    handle_pnt = AllplanGeo.TransformCoord.PointGlobal(handle_line, max_length)

                    self.handle_list.append(
                        HandleProperties(str(max_length_index),
                                         handle_pnt, center1,
                                         [("MaxLengthHandle", HandleDirection.point_dir)],
                                         HandleDirection.point_dir))


                    #----------------- create the placement

                    place_start_pnt = bar_lines[0].StartPoint
                    place_end_pnt   = bar_lines[1].StartPoint

                    shape1, start_len = self.cut_shape_pol_from_bar_line(start_len, bar_lines[0],
                                                                         shape_props, max_length)

                    bar_lines[1].TrimStart(max_length)

                    end_len -= max_length

                    self.model_ele_list.append(
                        AllplanReinf.BarPlacement(pos_nr, count + 1, place_vec_bottom / count,
                                                  place_start_pnt, place_end_pnt, shape1))


                    self.preview_list.append(
                        AllplanBasisElements.ModelElement3D(com_prop, AllplanGeo.Line3D(bar_lines[0].StartPoint,
                                                                                        bar_lines[1].StartPoint)))

                    bar_lines[0].TrimStart(-overlap)
                    bar_lines[1].TrimStart(-overlap)

                    start_len += overlap
                    end_len   += overlap

                    self.preview_list.append(
                        AllplanBasisElements.ModelElement3D(com_prop, AllplanGeo.Line3D(bar_lines[0].StartPoint,
                                                                                        bar_lines[1].StartPoint)))


                    #----------------- next max length

                    build_ele.bar_max_length.append(max_length)

                    max_length_index += 1

                    max_length = bar_max_length if max_length_index >= len(old_bar_max_length) else \
                                 old_bar_max_length[max_length_index]


                #----------------- rest placement

                if abs(AllplanGeo.CalcLength(bar_lines[0]) - AllplanGeo.CalcLength(bar_lines[1])) > eps:
                    self.append_polygonal_placement(bar_lines[0], bar_lines[1], shape_props, count + 1, pos_nr)
                else:
                    place_start_pnt = bar_lines[0].StartPoint
                    place_end_pnt   = bar_lines[1].StartPoint

                    shape, _ = self.cut_shape_pol_from_bar_line(start_len, bar_lines[0],
                                                                shape_props, max_length)

                    self.model_ele_list.append(
                        AllplanReinf.BarPlacement(pos_nr, count + 1, place_vec_bottom / count,
                                                  place_start_pnt, place_end_pnt, shape))

        return (self.model_ele_list, self.handle_list, self.preview_list)


    def append_polygonal_placement(self, bar_line1, bar_line2, shape_props, count, pos_nr):
        """
        append the polygonal placement to the list

        Args:
            bar_line1:      first bar line
            bar_line2:      second bar line
            shape_props:    shape properties
            count:          bar count
            pos_nr:         position number
        """

        br_list = AllplanUtil.VecDoubleList()

        shape_pol1 = AllplanGeo.Polyline3D()
        shape_pol1 += bar_line1.StartPoint
        shape_pol1 += bar_line1.EndPoint

        shape_pol2 = AllplanGeo.Polyline3D()
        shape_pol2 += bar_line2.StartPoint
        shape_pol2 += bar_line2.EndPoint

        shape1 = AllplanReinf.BendingShape(shape_pol1, br_list, shape_props.diameter,
                                           shape_props.steel_grade, -1,
                                           AllplanReinf.BendingShapeType.LongitudinalBar)

        shape2 = AllplanReinf.BendingShape(shape_pol2, br_list, shape_props.diameter,
                                           shape_props.steel_grade, -1,
                                           AllplanReinf.BendingShapeType.LongitudinalBar)

        self.model_ele_list.append(
            AllplanReinf.BarPlacement(pos_nr, count, shape1, shape2))

        pos_nr += 1



    def cut_shape_pol_from_bar_line(self, bar_line_length, bar_line, shape_props, max_length):
        """
        cut the shape polyline from the bar line

        Args:
            bar_line_length: current length of the bar line
            bar_line:        bar line
            shape_props:     shape properties
            max_length:      max bar length
        """

        length = bar_line_length

        if length > max_length:
            length = max_length

        bar_line_length -= max_length

        br_list = AllplanUtil.VecDoubleList()

        shape_pol = AllplanGeo.Polyline3D()
        shape_pol += bar_line.StartPoint

        if bar_line_length > 0:
            bar_line.TrimStart(length)

            shape_pol += bar_line.StartPoint
        else:
            shape_pol += bar_line.EndPoint

        return (AllplanReinf.BendingShape(shape_pol, br_list, shape_props.diameter,
                                          shape_props.steel_grade, -1,
                                          AllplanReinf.BendingShapeType.LongitudinalBar),
                bar_line_length)


    def get_poly_bar_lines(self, bar_line, bar_line2, max_length,
                           place_vec_bottom, place_vec_top, count, is_start_line):
        """
        get the bar lines for the left and right side of a polygonal section

        Args:
            bar_line:           bar line with the mininmal length
            bar_line2:          bar line with the maximal length
            max_length:         max bar length
            place_vec_bottom:   placement vector at the bottom of the placement
            place_vec_top:      placement vector at the top of the placement
            count:              bar count
            is_start_line:      bar line with the minimal length is the start line: true/false
        """

        end_pnt_max_len1 = AllplanGeo.TransformCoord.PointGlobal(bar_line, max_length)
        end_pnt_max_len2 = AllplanGeo.TransformCoord.PointGlobal(bar_line2, max_length)

        line1 = AllplanGeo.Line3D(end_pnt_max_len1, end_pnt_max_len2)
        line2 = AllplanGeo.Line3D(bar_line.EndPoint, bar_line2.EndPoint)

        _, inter_pnt = AllplanGeo.IntersectionCalculus(line1, line2)

        delta_vec_bottom = place_vec_bottom / count
        delta_vec_top    = place_vec_top / count

        if is_start_line:
            pnt_max_len_vec = AllplanGeo.Vector3D(bar_line.EndPoint, inter_pnt)

            move_count = int(pnt_max_len_vec.GetLength() / delta_vec_top.GetLength())

            return (bar_line,
                    AllplanGeo.Line3D(bar_line.StartPoint + delta_vec_bottom * move_count,
                                      bar_line.EndPoint + delta_vec_top * move_count),
                    delta_vec_bottom,
                    delta_vec_top,
                    move_count)

        else:
            pnt_max_len_vec = AllplanGeo.Vector3D(inter_pnt, bar_line.EndPoint)

            move_count = int(pnt_max_len_vec.GetLength() / delta_vec_top.GetLength())

            return (AllplanGeo.Line3D(bar_line.StartPoint - delta_vec_bottom * move_count,
                                      bar_line.EndPoint - delta_vec_top * move_count),
                    bar_line,
                    delta_vec_bottom,
                    delta_vec_top,
                    move_count)
