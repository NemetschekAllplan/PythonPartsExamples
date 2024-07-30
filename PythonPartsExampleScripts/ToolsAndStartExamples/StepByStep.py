"""
Step by step template
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf

import GeometryValidate as GeometryValidate

from PythonPart import View2D3D, PythonPart
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder

from StdReinfShapeBuilder.RotationAngles import RotationAngles
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
import StdReinfShapeBuilder.BarPlacementUtil as BarUtil


# Print some information
print('Load StepByStep.py')


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

    Returns:
            tuple  with created elements and handles
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
            tuple  with created elements and handles
    """

    return globals()[build_ele.Step.value](build_ele)


#==========================================================================================================================================


def EmptyScript(build_ele):
    """
    Empty function

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list = []
    handle_list    = []

    return (model_ele_list, handle_list)


#==========================================================================================================================================


def Polyhedron(build_ele):
    """
    Create a polyhedron

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list = []
    handle_list    = []

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(3000, 2000, 1000)

    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

    return (model_ele_list, handle_list)


#==========================================================================================================================================


def TwoPolyhedrons(build_ele):
    """
    Create two polyhedron

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list = []
    handle_list    = []

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(3000, 2000, 1000)
    polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(1200, 1200, 1000),
                                                    AllplanGeo.Point3D(1700, 1600, 2500))

    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed1))
    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed2))

    return (model_ele_list, handle_list)


#==========================================================================================================================================


def UnitePolyhedrons(build_ele):
    """
    Create two polyhedron and unite it

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list = []
    handle_list    = []

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(3000, 2000, 1000)
    polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(1200, 1200, 1000),
                                                    AllplanGeo.Point3D(1700, 1600, 2500))

    err, polyhed = AllplanGeo.MakeUnion(polyhed1, polyhed2)

    if not GeometryValidate.polyhedron(err):
        return

    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

    return (model_ele_list, handle_list)


#==========================================================================================================================================


def PythonPartFix(build_ele):
    """
    Create a PythonPart 

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list, handle_list = UnitePolyhedrons(build_ele)

    views = [View2D3D (model_ele_list)]

    pythonpart = PythonPart("StepByStep",
                            parameter_list = build_ele.get_params_list(),
                            hash_value     = build_ele.get_hash(),
                            python_file    = build_ele.pyp_file_name,
                            views          = views)

    return (pythonpart.create(), handle_list)


#==========================================================================================================================================


def PythonPartWithPalette(build_ele):
    """
    Create a PythonPart, use the properties from the palette

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list = []
    handle_list    = []

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.FoundationLength.value,
                                                    build_ele.FoundationWidth.value,
                                                    build_ele.FoundationHeight.value)

    ref_pnt = AllplanGeo.Point3D(build_ele.XOffset.value,
                                 build_ele.YOffset.value,
                                 build_ele.FoundationHeight.value)

    polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                    ref_pnt + AllplanGeo.Point3D(build_ele.ColumnLength.value,
                                                                                 build_ele.ColumnWidth.value,
                                                                                 build_ele.ColumnHeight.value))

    err, polyhed = AllplanGeo.MakeUnion(polyhed1, polyhed2)

    if not GeometryValidate.polyhedron(err):
        return

    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

    views = [View2D3D (model_ele_list)]

    pythonpart = PythonPart("StepByStep",
                            parameter_list = build_ele.get_params_list(),
                            hash_value     = build_ele.get_hash(),
                            python_file    = build_ele.pyp_file_name,
                            views          = views)

    return (pythonpart.create(), handle_list)


#==========================================================================================================================================


def PythonPartWithHandles(build_ele):
    """
    Create a PythonPart with handles, use the properties from the palette

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list, handle_list = PythonPartWithPalette(build_ele)


    #----------------- create the handles

    found_length = build_ele.FoundationLength.value
    found_width  = build_ele.FoundationWidth.value

    ref_pnt = AllplanGeo.Point3D(build_ele.XOffset.value,
                                 build_ele.YOffset.value,
                                 build_ele.FoundationHeight.value)

    column_length = build_ele.ColumnLength.value
    column_width  = build_ele.ColumnWidth.value

    handle_list = [HandleProperties("FoundationLengthHandle",
                                    AllplanGeo.Point3D(found_length, found_width / 2, 0),
                                    AllplanGeo.Point3D(0           , found_width / 2, 0),
                                    [("FoundationLength", HandleDirection.x_dir)],
                                    HandleDirection.x_dir),
                   HandleProperties("FoundationWidthHandle",
                                    AllplanGeo.Point3D(found_length / 2, found_width, 0),
                                    AllplanGeo.Point3D(found_length / 2, 0          , 0),
                                    [("FoundationWidth", HandleDirection.y_dir)],
                                    HandleDirection.y_dir),
                   HandleProperties("FoundationHeightHandle",
                                    AllplanGeo.Point3D(found_length, found_width, build_ele.FoundationHeight.value),
                                    AllplanGeo.Point3D(found_length, found_width, 0),
                                    [("FoundationHeight", HandleDirection.z_dir)], HandleDirection.z_dir),
                   HandleProperties("ColumnLengthHandle",
                                    AllplanGeo.Point3D(ref_pnt.X + column_length, ref_pnt.Y + column_width / 2, ref_pnt.Z),
                                    AllplanGeo.Point3D(ref_pnt.X                , ref_pnt.Y + column_width / 2, ref_pnt.Z),
                                    [("ColumnLength", HandleDirection.x_dir)],
                                    HandleDirection.x_dir),
                   HandleProperties("ColumnWidthHandle",
                                    AllplanGeo.Point3D(ref_pnt.X + column_length / 2, ref_pnt.Y + column_width, ref_pnt.Z),
                                    AllplanGeo.Point3D(ref_pnt.X + column_length / 2, ref_pnt.Y               , ref_pnt.Z),
                                    [("ColumnWidth", HandleDirection.y_dir)],
                                    HandleDirection.y_dir),
                   HandleProperties("ColumnHeightHandle",
                                    AllplanGeo.Point3D(ref_pnt.X + column_length, ref_pnt.Y + column_width, ref_pnt.Z + build_ele.ColumnHeight.value),
                                    AllplanGeo.Point3D(ref_pnt.X + column_length, ref_pnt.Y + column_width, ref_pnt.Z),
                                    [("ColumnHeight", HandleDirection.z_dir)], HandleDirection.z_dir),
                   HandleProperties("XOffset",
                                    AllplanGeo.Point3D(build_ele.XOffset.value, build_ele.YOffset.value, ref_pnt.Z),
                                    AllplanGeo.Point3D(0, build_ele.YOffset.value, ref_pnt.Z),
                                    [("XOffset", HandleDirection.x_dir)],
                                    HandleDirection.x_dir),
                   HandleProperties("YOffset",
                                    AllplanGeo.Point3D(build_ele.XOffset.value, build_ele.YOffset.value, ref_pnt.Z),
                                    AllplanGeo.Point3D(build_ele.XOffset.value, 0 , ref_pnt.Z),
                                    [("YOffset", HandleDirection.y_dir)],
                                    HandleDirection.y_dir),
                  ]


    return (model_ele_list, handle_list)


#==========================================================================================================================================


def PythonPartWithReinforcement(build_ele):
    """
    Create a PythonPart with reinforcement

    Args:
        build_ele: the building element.

    Returns:
            tuple  with created elements and handles
    """

    model_ele_list = []
    handle_list    = []

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.FoundationLength.value,
                                                    build_ele.FoundationWidth.value,
                                                    build_ele.FoundationHeight.value)

    ref_pnt = AllplanGeo.Point3D(build_ele.XOffset.value,
                                 build_ele.YOffset.value,
                                 build_ele.FoundationHeight.value)

    polyhed2 = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt,
                                                    ref_pnt + AllplanGeo.Point3D(build_ele.ColumnLength.value,
                                                                                 build_ele.ColumnWidth.value,
                                                                                 build_ele.ColumnHeight.value))

    err, polyhed = AllplanGeo.MakeUnion(polyhed1, polyhed2)

    if not GeometryValidate.polyhedron(err):
        return

    model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))


    #----------------- create the reinforcement in the foundation by local x/y-coordinate system ----------------------


    steel_grade    = build_ele.SteelGrade.value
    concrete_cover = build_ele.ConcreteCover.value

    shape_builder = AllplanReinf.ReinforcementShapeBuilder()

    shape_builder.AddPoints([(AllplanGeo.Point2D(0, build_ele.FoundationHeight.value), concrete_cover),
                             (AllplanGeo.Point2D(0, 0), concrete_cover),
                             (AllplanGeo.Point2D(build_ele.FoundationLength.value, 0), concrete_cover),
                             (concrete_cover)])

    shape_builder.SetSideLengthStart(build_ele.SideLength1.value)
    shape_builder.SetAnchorageHookEnd(90)

    shape = shape_builder.CreateShape(build_ele.Diameter1.value, -1, steel_grade, -1,
                                      AllplanReinf.BendingShapeType.LongitudinalBar)

    if shape.IsValid() is False:
        return


    #---- rotate the shape orthogonal to the placement direction

    shape.Rotate(RotationAngles(90, 0, 0))


    #---- create the placement (move the shape to the start point of the placement by "global_move = True")

    reinf_list = [LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, shape,
                    AllplanGeo.Point3D(), AllplanGeo.Point3D(0, build_ele.FoundationWidth.value, 0),
                    concrete_cover, concrete_cover, build_ele.Spacing1.value,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance,
                    True)]


    #---- create the stirrup inside the column, use a library function ---------------------------------


    diameter_stirrup = build_ele.DiameterStirrup.value

    concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

    shape_props = ReinforcementShapeProperties.rebar(diameter_stirrup, -1, steel_grade, -1,
                                                     AllplanReinf.BendingShapeType.Stirrup)

    stirrup_shape = GeneralShapeBuilder.create_stirrup(build_ele.ColumnLength.value, build_ele.ColumnWidth.value,
                                                       RotationAngles(0, 0, 0),
                                                       shape_props, concrete_cover_props)

    if stirrup_shape.IsValid() is False:
        return

    reinf_list.append(
        LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, stirrup_shape,
                    polyhed2[1], polyhed2[4],
                    concrete_cover, concrete_cover, build_ele.SpacingStirrup.value,
                    LinearBarBuilder.StartEndPlacementRule.AdaptDistance,
                    True))


    #---- create the U-link inside the foundation and the column, use the global points ---------------------------------


    shape_builder = AllplanReinf.ReinforcementShapeBuilder(RotationAngles(-90, 0, 0).get_rotation_matrix())

    shape_builder.AddSides(
        [(concrete_cover),
         (AllplanGeo.Line3D(polyhed2[4], polyhed2[1]), concrete_cover + diameter_stirrup),
         (AllplanGeo.Line3D(polyhed1[1], polyhed1[2]), concrete_cover),
         (AllplanGeo.Line3D(polyhed2[2], polyhed2[7]), concrete_cover + diameter_stirrup),
         (concrete_cover)])

    shape_builder.SetSideLengthStart(build_ele.SideLengthULink.value)
    shape_builder.SetSideLengthEnd(build_ele.SideLengthULink.value)

    shape = shape_builder.CreateShape(build_ele.DiameterULink.value, -1, steel_grade, -1,
                                      AllplanReinf.BendingShapeType.OpenStirrup)

    if shape.IsValid() is False:
        return



    #---- create the placement (the shape has the global position, "global_move = False")

    cover_left = BarUtil.get_placement_start_from_bending_roller( \
                                stirrup_shape, 3,                # left side is number 3 (starting by hook side)
                                stirrup_shape.GetBendingRoller()[2],
                                AllplanGeo.Line2D(AllplanGeo.Point2D(), AllplanGeo.Point2D(0, build_ele.ColumnWidth.value)),
                                build_ele.DiameterULink.value,
                                RotationAngles(0, 0, 0))

    cover_right = BarUtil.get_placement_end_from_bending_roller( \
                                stirrup_shape, 3,                # left side is number 3 (starting by hook side)
                                stirrup_shape.GetBendingRoller()[1],
                                AllplanGeo.Line2D(AllplanGeo.Point2D(), AllplanGeo.Point2D(0, build_ele.ColumnWidth.value)),
                                build_ele.DiameterULink.value,
                                RotationAngles(0, 0, 0))

    reinf_list.append(
        LinearBarBuilder.create_linear_bar_placement_from_to_by_count(
            3, shape,
            polyhed2[1],
            polyhed2[0],
            cover_left, cover_right, build_ele.CountULink.value,
            False))


    #----------------- create the PythonPart

    views = [View2D3D (model_ele_list)]

    pythonpart = PythonPart("StepByStep",
                            parameter_list = build_ele.get_params_list(),
                            hash_value     = build_ele.get_hash(),
                            python_file    = build_ele.pyp_file_name,
                            views          = views,
                            reinforcement  = reinf_list)

    return (pythonpart.create(), handle_list)
