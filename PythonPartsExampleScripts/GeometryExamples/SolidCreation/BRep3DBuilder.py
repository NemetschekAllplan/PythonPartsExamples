"""An example script of using BRep3DBuilder to construct a cylinder
"""

import typing
import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil

from BuildingElement import BuildingElement
from ControlPropertiesUtil import ControlPropertiesUtil
from CreateElementResult import CreateElementResult

from TypeCollections.ModelEleList import ModelEleList

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


def modify_control_properties(build_ele     : BuildingElement,
                              _ctrl_prop_util: ControlPropertiesUtil,
                              value_name    : str,
                              _event_id      : int,
                              _doc           : AllplanElementAdapter.DocumentAdapter) -> bool:
    """Called after each change within the property palette

    Args:
        build_ele:      building element
        _ctrl_prop_util: control properties utility
        value_name:     name(s) of the modified value (multiple names are separated by ,)
        _event_id:       event ID
        _doc:            document

    Returns:
        True if an update of the property palette is necessary, False otherwise
    """

    if value_name == "OverrideKnots" and build_ele.OverrideKnots.value is False:
        build_ele.Knots.value = [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]
        return True

    return False


def create_element(build_ele: BuildingElement,
                   _doc     : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the cylinder

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result with cylinder brep if the creation was successful,
        or with just edge curves otherwise
    """

    # get common properties and construct list of model elements

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)


    # construct geometry objects (planed and edge curves) needed to build a brep

    # bottom surface

    bottom_surface = AllplanGeo.Plane3D(AllplanGeo.Point3D(),
                                        AllplanGeo.Vector3D(0, 0, 1))


    # top surface

    top_surface = AllplanGeo.Plane3D(bottom_surface)
    top_surface.Point = AllplanGeo.Point3D(0, 0, build_ele.Height.value)


    # lateral surface, top edge and bottom edge

    lateral_surface, top_edge_curve, bottom_edge_curve = create_cylindrical_surface(build_ele.Radius.value,
                                                                                    build_ele.Height.value,
                                                                                    build_ele.Knots.value)


    # line connecting the bottom and top edges curves

    side_edge_line = AllplanGeo.Line3D(bottom_edge_curve.EndPoint, top_edge_curve.StartPoint)


    # initialize the BRep builder

    builder = AllplanGeo.BRep3DBuilder()
    builder.Init(True) #initialise the builder to build a closed volume BRep

    loops_ok: typing.List[bool] = []


    # construction of top face

    top_face_idx = builder.AddFace(top_surface, True)
    top_loop_idx = builder.AddLoop(top_face_idx)

    top_edge_idx = builder.AddEdge(curve=           top_edge_curve,
                                   curveSense=      True,
                                   edgeSense=       True,
                                   loopIdx=         top_loop_idx,
                                   precision=       0.5)

    top_vertex_idx = builder.AddVertex(point=       top_edge_curve.StartPoint,
                                       edgeIdx=     top_edge_idx,
                                       precision=   0.5)

    loops_ok.append(builder.CheckLoop(top_loop_idx))


    # construction of bottom face

    bottom_face_idx = builder.AddFace(bottom_surface, False)
    bottom_loop_idx = builder.AddLoop(bottom_face_idx)

    bottom_edge_idx = builder.AddEdge(curve=            bottom_edge_curve,
                                      curveSense=       False,
                                      edgeSense=        True,
                                      loopIdx=          bottom_loop_idx,
                                      precision=        0.5)

    bottom_vertex_idx = builder.AddVertex(point=        bottom_edge_curve.StartPoint,
                                          edgeIdx=      bottom_edge_idx,
                                          precision=    0.5)

    loops_ok.append(builder.CheckLoop(bottom_loop_idx))


    # construction of lateral face

    lateral_face_idx = builder.AddFace(lateral_surface, True)
    lateral_loop_idx = builder.AddLoop(lateral_face_idx)

    side_edge_idx = builder.AddEdge(curve=           side_edge_line,
                                    curveSense=      True,
                                    edgeSense=       True,
                                    loopIdx=         lateral_loop_idx,
                                    precision=       0.5)

    builder.AddVertex(bottom_vertex_idx, side_edge_idx)
    builder.AddVertex(top_vertex_idx, side_edge_idx)

    builder.AddEdge(top_edge_idx, False, lateral_loop_idx)
    builder.AddEdge(side_edge_idx, False, lateral_loop_idx)
    builder.AddEdge(bottom_edge_idx, False, lateral_loop_idx)

    loops_ok.append(builder.CheckLoop(lateral_loop_idx))


    # check if all loops are ok and if so, build a brep

    if all(loops_ok):
        brep = builder.Complete()

        #check if the brep is valid and if so, create a model element

        if brep.IsValid():
            model_elements.append_geometry_3d(brep)


        # if the constructed BRep is not valid, create only the edge curves

        else:
            print("Brep is invalid")
            model_elements.append_geometry_3d(top_edge_curve)
            model_elements.append_geometry_3d(bottom_edge_curve)
            model_elements.append_geometry_3d(side_edge_line)

    else:
        print("Some of the loops are not OK")

    return CreateElementResult(model_elements)


def create_cylindrical_surface(radius: float,
                               height: float,
                               knots: typing.Union[typing.List[float], None] = None) -> typing.Tuple[AllplanGeo.BSplineSurface3D,
                                                                                                     AllplanGeo.BSpline3D,
                                                                                                     AllplanGeo.BSpline3D]:
    """Create a B-Spline surface (NURBS) representing the lateral face of a cylinder and
    the curves (b-splines) bounding the surface from top and bottom.
    Creation is based on radius and height.

    Args:
        radius: radius of the cylinder
        height: height of the cylinder
        knots:  list with knots. If not specified, values creating a cylindrical surface will be assumed

    Returns:
        B-Spline surface representing the lateral face of the cylinder
        B-Spline representing the top edge of the surface
        B-Spline representing the bottom edge of the surface
    """

    # define control points their weights and knots vector, if not specified

    control_points_and_weights = [  (AllplanGeo.Point3D( radius,      0,      0 ), 1),
                                    (AllplanGeo.Point3D( radius,      0, height ), 1),
                                    (AllplanGeo.Point3D( radius, radius,      0 ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D( radius, radius, height ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D(      0, radius,      0 ), 1),
                                    (AllplanGeo.Point3D(      0, radius, height ), 1),
                                    (AllplanGeo.Point3D(-radius, radius,      0 ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D(-radius, radius, height ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D(-radius,    0,        0 ), 1),
                                    (AllplanGeo.Point3D(-radius,    0,   height ), 1),
                                    (AllplanGeo.Point3D(-radius,-radius,      0 ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D(-radius,-radius, height ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D(      0,-radius,      0 ), 1),
                                    (AllplanGeo.Point3D(      0,-radius, height ), 1),
                                    (AllplanGeo.Point3D( radius,-radius,      0 ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D( radius,-radius, height ), math.sqrt(2)/2),
                                    (AllplanGeo.Point3D( radius,      0,      0 ), 1),
                                    (AllplanGeo.Point3D( radius,      0, height ), 1),
                                    ]

    if knots is None:
        knots = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]


    #-------- create surface


    # cast list of tuples containing control points and weights
    # into two individual objects: Point3DList and VecDoubleList

    lateral_surface_points = AllplanGeo.Point3DList()
    weights = AllplanUtil.VecDoubleList()

    for control_point, weight in control_points_and_weights:
        lateral_surface_points.append(control_point)
        weights.append(weight)

    lateral_surface = AllplanGeo.BSplineSurface3D(points=  lateral_surface_points,
                                                  weights= weights,
                                                  uknots=  AllplanUtil.VecDoubleList(knots),
                                                  vknots=  AllplanUtil.VecDoubleList([0, 0, 1, 1]),
                                                  udegree= 2,
                                                  vdegree= 1,
                                                  isUPeriodic= True,
                                                  isVPeriodic= False,
                                                  isUClosed= True,
                                                  isVClosed= False,
                                                  )


    #------- create spline of the bottom edge

    spline_points = AllplanGeo.Point3DList()
    weights = AllplanUtil.VecDoubleList()

    # get only the even points from the list, as they represent the bottom spline
    for control_point, weight in control_points_and_weights[::2]:
        spline_points.append(control_point)
        weights.append(weight)

    bottom_edge = AllplanGeo.BSpline3D(points=      spline_points,
                                       weights=     weights,
                                       knots=       AllplanUtil.VecDoubleList(knots),
                                       degree=      2,
                                       isPeriodic=  True)


    #------- create spline of the top edge

    spline_points = AllplanGeo.Point3DList()
    weights = AllplanUtil.VecDoubleList()

    # get only the odd points from the list, as they represent the top spline

    for control_point, weight in control_points_and_weights[1::2]:
        spline_points.append(control_point)
        weights.append(weight)

    top_edge = AllplanGeo.BSpline3D(points=     spline_points,
                                    weights=    weights,
                                    knots=      AllplanUtil.VecDoubleList(knots),
                                    degree=     2,
                                    isPeriodic= True)

    return lateral_surface, top_edge, bottom_edge
