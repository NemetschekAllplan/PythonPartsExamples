#pylint: disable=W1401
# Anomalous backslash in string

"""
Script for the Mesh Welding System Group

The script shows the creation of a MWS Group with 2 rebar Placements

"""

#pylint: enable=W1401
# Only disabled for comment part

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.BarPlacementUtil as BarUtil

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from StdReinfShapeBuilder.BarShapePlacementUtil import BarShapePlacementUtil
import NemAll_Python_Utility as AllplanUtil

from PythonPart import View2D3D, PythonPart

import NemAll_Python_Precast as AllplanPrecast


print('Load RebarPlacement.py')

def isEqual(val1, val2, tol = 0.001):
    if(val1 >= val2-tol and val1 <= val2+tol):
        return True
    else:
        return False


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

def write_attr(doc, attrid, attrval):
    """
    write_attr
    """
    AttributeType = AllplanBaseElements.AttributeService.AttributeType
    attrtype = AllplanBaseElements.AttributeService.GetAttributeType(doc, attrid)
    if attrtype == AttributeType.Integer:
        return AllplanBaseElements.AttributeInteger(attrid, int(attrval)) # Anzahl Stufen
    elif attrtype == AttributeType.Double:
        if attrid == 90 or attrid == 89:
            attrval = attrval / 10
        return AllplanBaseElements.AttributeDouble(attrid, float(attrval)) # Steigung
    elif attrtype == AttributeType.String:
        return AllplanBaseElements.AttributeString(attrid, str(attrval)) # Aufpreis Kellerfußsockel
    elif attrtype == AttributeType.StringVec:
        return AllplanBaseElements.AttributeStringVec(attrid, attrval) # Aufpreis Kellerfußsockel
    elif attrtype == AttributeType.Enum:
        return AllplanBaseElements.AttributeEnum(attrid, attrval) # Aufpreis Kellerfußsockel

def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = RebarPlacement(doc)

    return element.create(build_ele)


class RebarPlacement():
    """
    Definition of class RebarPlacement
    """

    def __init__(self, doc):
        """
        Initialisation of class RebarPlacement

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc
        self.concrete_cover        = None
        self.diameter              = None
        self.diameter_longitudinal = None
        self.bending_roller        = None
        self.steel_grade           = None
        self.distance              = None
        self.mesh_type             = None
        self.length                = 500
        self.width                 = 1000
        self.height                = 200
        self.placement_list = []

        # Variables to fill the PrecastMWSElement Class
        self.basePlacementidx = -1
        self.segmentNumber = 0
        self.SegementPoints = []
        self.SegementVector = AllplanGeo.Point3D()
        self.Factory = "Werk1"
        self.MWSName = "MWS1_Python"
        self.MWSNumber = 1
        self.longitBarHeight = 1
        self.piecefactor = 1
        self.shapes = []


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.length = build_ele.Length.value
        self.width  = build_ele.Width.value
        self.height = build_ele.Height.value

        self.steel_grade           = build_ele.SteelGrade.value
        self.bending_roller        = build_ele.BendingRoller.value

        self.diameter_shape1              = build_ele.DiameterShape1.value
        self.concrete_cover_shape1        = build_ele.ConcreteCoverShape1.value
        self.distance_shape1              = build_ele.DistanceShape1.value
        self.diameter_shape2              = build_ele.DiameterShape2.value
        self.concrete_cover_shape2        = build_ele.ConcreteCoverShape2.value
        self.distance_shape2              = build_ele.DistanceShape2.value

        # fill small Attribute list to write something on the Group
        self.attr_list = []
        self.attr_list.append(write_attr(self.document, 1444, "MWSGROUP"))
        self.attr_list.append(write_attr(self.document, 684, "IfcElementAssembly"))
        # fill small Attribute list to write something on the Group

        # Init Class variables from build_ele
        # self.placement_list --> List of Placements which should be grouped
        # self.IndexLongitBar --> Which placement in list should be the longitudinal bar
        # self.segmentNumber --> Which segment of the base shape should be the Base segment
        # self.SegementPoints --> List of Point of the Base Placement,
        #                         Has to be transformed into insert_matrix
        # self.SegementVector --> Vector of the base segment (End Point - Start Point)
        # self.Factory --> Factory Catalogs reference
        # self.MWSName --> Name of the MWS Group
        # self.MWSNumber --> Number of the MWS Group
        # self.longitBarHeight --> Position of the Longitudinal Bar
        #                          1 = Position 1
        #                          2 = Position 2
        # self.piecefactor --> Piecefator of the MWS Group
        self.placement_list = []
        self.IndexLongitBar = -1
        if build_ele.longitSelect.value == "Shape1":
            self.IndexLongitBar = 0
        else:
            self.IndexLongitBar = 1
        self.segmentNumber = build_ele.SegmentNumber.value
        self.SegementPoints = []
        self.SegementVector = AllplanGeo.Point3D()
        self.Factory = build_ele.Factory.value
        self.MWSName = build_ele.Name.value
        self.MWSNumber = build_ele.Number.value
        if build_ele.longitBarHeightCombo.value == "Position1":
            self.longitBarHeight = 1
        else:
            self.longitBarHeight = 2
        self.piecefactor = build_ele.Piecefactor.value
        # Init Class variables from build_ele

        # create the Geometry and the Placements of the Pythonpart
        self.create_geometry_and_placements(AllplanGeo.Point3D(0,0,0))
        # create the Geometry and the Placements of the Pythonpart

        # Fill the PrecastMWSElement Class
        mws_element = AllplanPrecast.PrecastMWSElement(self.Factory,
                                                       self.MWSName,
                                                       self.MWSNumber,
                                                       self.piecefactor,
                                                       self.longitBarHeight,
                                                       self.segmentNumber,
                                                       self.SegementVector,
                                                       self.SegementPoints,
                                                       self.placement_list)
        # Fill the PrecastMWSElement Class

        # Get the Base Shape, the Pointslist of the Base Shape,
        # and the Segmentvector of BaseSegement of the Base Shape
        for k in range(self.shapes.__len__()):
            if k == self.IndexLongitBar:
                continue
            polyline_stirr = self.shapes[k].GetShapePolyline()
            lines_stirr = polyline_stirr.GetLines()
            self.SegementPoints = polyline_stirr.Points
            for i in range(lines_stirr.__len__()):
                if (i == self.segmentNumber-1):
                    self.SegementVector = lines_stirr[i].GetEndPoint()- lines_stirr[i].GetStartPoint()
        # Get the Base Shape, the Pointslist of the Base Shape,
        # and the Segmentvector of BaseSegement of the Base Shape

        # Refill the PrecastMWSElement Class with actual Values
        mws_element = AllplanPrecast.PrecastMWSElement()
        mws_element.SegmentPointList = self.SegementPoints
        mws_element.ReinforcementList = self.placement_list
        mws_element.Factory = self.Factory
        mws_element.Name = self.MWSName
        mws_element.Number = self.MWSNumber
        mws_element.Piecefactor = self.piecefactor
        mws_element.LongitBarHeight = self.longitBarHeight
        mws_element.IndexLongitBar = self.IndexLongitBar
        mws_element.SegmentVector = self.SegementVector
        mws_element.SegmentNumber = self.segmentNumber
        # Refill the PrecastMWSElement Class with actual Values

        # Set Attributes List to MWS Group
        attr_set_list = []
        attr_set_list.append(AllplanBaseElements.AttributeSet(self.attr_list))

        attributes = AllplanBaseElements.Attributes(attr_set_list)
        mws_element.SetAttributes(attributes)
        # Set Attributes List to MWS Group

        # fill MWS List for Pythonpart
        mws_list = []
        mws_list.append(mws_element)
        # fill MWS List for Pythonpart

        # Create the Pythonpart
        views = [View2D3D (self.model_ele_list)]
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        pythonpart = PythonPart ("FixtureModeller",
                             parameter_list = build_ele.get_params_list(),
                             hash_value     = build_ele.get_hash(),
                             python_file    = build_ele.pyp_file_name,
                             views          = views,
                             reinforcement  = [],
                             common_props   = com_prop,
                             library_elements = [],
                             attribute_list = [],
                             fixture_elements = [],
                             assembly_elements = [],
                             mws_elements = mws_list)
        self.model_ele_list = pythonpart.create()
        # Create the Pythonpart

        return (self.model_ele_list, self.handle_list)

    def create_geometry_and_placements(self, ref_pnt):
        """
        Create the geometry and a stirrup placement as base example data

        Args:
            build_ele:  the building element.
            ref_pnt:    reference point
        """

        size = AllplanGeo.Vector3D(self.length, self.width, self.height)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt, ref_pnt + size)

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed))


        #----------------- create the bars

        concrete_cover_props = ConcreteCoverProperties(self.concrete_cover_shape1, self.concrete_cover_shape1,
                                                       self.concrete_cover_shape1, self.concrete_cover_shape1)

        self.shapes = []

        shape_pol = AllplanGeo.Polyline3D()

        shape_pol += AllplanGeo.Point3D(0, 0, 0+concrete_cover_props.bottom+self.diameter_shape1/2)
        shape_pol += AllplanGeo.Point3D(self.length, 0, 0+concrete_cover_props.bottom+self.diameter_shape1/2)

        shape_props = ReinforcementShapeProperties.rebar(self.diameter_shape1, self.bending_roller, self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        self.shapes.append(AllplanReinf.BendingShape(shape_pol, AllplanUtil.VecDoubleList(),
                                      shape_props.diameter, shape_props.steel_grade,
                                      shape_props.concrete_grade,
                                      AllplanReinf.BendingShapeType.LongitudinalBar))

        concrete_cover_props = ConcreteCoverProperties(self.concrete_cover_shape2, self.concrete_cover_shape2,
                                                       self.concrete_cover_shape2, self.concrete_cover_shape2)

        shape_pol = AllplanGeo.Polyline3D()

        shape_pol += AllplanGeo.Point3D(0, 0, 0+concrete_cover_props.bottom+self.diameter_shape2/2)
        shape_pol += AllplanGeo.Point3D(0, self.width, 0+concrete_cover_props.bottom+self.diameter_shape2/2)

        shape_props = ReinforcementShapeProperties.rebar(self.diameter_shape2, self.bending_roller, self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        self.shapes.append(AllplanReinf.BendingShape(shape_pol, AllplanUtil.VecDoubleList(),
                                      shape_props.diameter, shape_props.steel_grade,
                                      shape_props.concrete_grade,
                                      AllplanReinf.BendingShapeType.LongitudinalBar))

        longit = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, self.shapes[0],
                                                                         ref_pnt,
                                                                         ref_pnt + AllplanGeo.Point3D(0, self.width, 0),
                                                                         self.concrete_cover_shape1,
                                                                         self.concrete_cover_shape1 - self.diameter_shape1,
                                                                         self.distance_shape1)

        cross = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, self.shapes[1],
                                                                         ref_pnt,
                                                                         ref_pnt + AllplanGeo.Point3D(self.length, 0, 0),
                                                                         self.concrete_cover_shape1,
                                                                         self.concrete_cover_shape2 - self.diameter_shape2,
                                                                         self.distance_shape2)
        self.placement_list.append(longit)
        self.placement_list.append(cross)

        return self.shapes
