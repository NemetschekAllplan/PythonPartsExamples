#pylint: disable=W1401
# Anomalous backslash in string

"""
Script for the Assembly Group

The script shows the creation of an Assembly Group, grouping:

- 2 Rebar placements

- 1 Library Fixture

- 1 Scripted Fixture

Connected to a PythonPart

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

import NemAll_Python_AllplanSettings as AllplanSettings

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from StdReinfShapeBuilder.BarShapePlacementUtil import BarShapePlacementUtil
from PythonPart import View2D3D, PythonPart

import NemAll_Python_Precast as AllplanPrecast
import NemAll_Python_Utility as AllplanUtil

import math as math
import hashlib as hashlib

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

def getAbsolutePath(filedir : str):
    """
    Get the absolute path from relative allplan path
    """
    path = filedir
    if path[:3] == "ETC":
        path = path.replace("ETC\\", AllplanSettings.AllplanPaths.GetEtcPath())
    if path[:3] == "STD":
        path = path.replace("STD\\", AllplanSettings.AllplanPaths.GetStdPath())
    if path[:3] == "PRJ":
        path = path.replace("PRJ\\", AllplanSettings.AllplanPaths.GetCurPrjPath())
    if path[:3] == "USR":
        path = path.replace("USR\\", AllplanSettings.AllplanPaths.GetUsrPath())
    return path

def getRelativePath(filedir : str):
    """
    Get the relative allplan path from absolute path
    """
    path = filedir
    if path.find(AllplanSettings.AllplanPaths.GetEtcPath())>-1:
        path = path.replace(AllplanSettings.AllplanPaths.GetEtcPath(), "ETC\\")
    if path.find(AllplanSettings.AllplanPaths.GetStdPath())>-1:
        path = path.replace(AllplanSettings.AllplanPaths.GetStdPath(), "STD\\")
    if path.find(AllplanSettings.AllplanPaths.GetCurPrjPath())>-1:
        path = path.replace(AllplanSettings.AllplanPaths.GetCurPrjPath(), "PRJ\\")
    if path.find(AllplanSettings.AllplanPaths.GetUsrPath())>-1:
        path = path.replace(AllplanSettings.AllplanPaths.GetUsrPath(), "USR\\")
    return path

def macro_hash (fix_macro):
    """
    Calculate hash value for script
    Returns:
        Hash string
    """
    param_string = fix_macro.__repr__()
    hash_val = hashlib.sha224(param_string.encode('utf-8')).hexdigest()
    return hash_val

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
        self.library_ele_list = []
        self.fixture_ele_list = []

        # Variables to fill the AssemblyGroupElement Class
        self.asg_Name = "ASG1_Python"
        self.asg_Number = 1


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
        self.model_ele_list.clear()

        # Init Class variables from build_ele
        # self.asg_Name --> Name of the Assembly Group
        # self.asg_Number --> Number of the Assembly Group
        self.asg_Name = build_ele.Name.value
        self.asg_Number = build_ele.Number.value
        # Init Class variables from build_ele

        #create LibraryElementList for AssemblyGroup
        self.library_ele_list = []
        placement_mat = RotationAngles(0,
                                       0,
                                       0).get_rotation_matrix()
        placement_mat.SetTranslation(AllplanGeo.Vector3D(build_ele.LibraryPlacePoint.value.X,
                                       build_ele.LibraryPlacePoint.value.Y,
                                       build_ele.LibraryPlacePoint.value.Z))

        path = getAbsolutePath(build_ele.Fixture_library.value)
        lib_ele_prop = AllplanBasisElements.LibraryElementProperties("",
                                                                     "",
                                                                     "",
                                                                     path,
                                                                     AllplanBasisElements.LibraryElementType.eFixtureSingleFile, placement_mat)
        self.library_ele_list.append(AllplanBasisElements.LibraryElement(lib_ele_prop))
        #create LibraryElementList for AssemblyGroup

        #create FixtureElementList for AssemblyGroup
        self.fixture_ele_list = []
        fixture = self.create_fixture_form_3D_element(build_ele)
        self.fixture_ele_list.append(fixture)
        #create FixtureElementList for AssemblyGroup

        #create Geometry of the Python and the Placements list for the AssemblyGroups
        self.create_geometry_and_placements(AllplanGeo.Point3D(0,0,0))
        #create Geometry of the Python and the Placements list for the AssemblyGroups

        # Fill the AssemblyGroupElement Class
        asg_element = AllplanPrecast.AssemblyGroupElement()
        asg_element.Name = self.asg_Name
        asg_element.Number = self.asg_Number
        asg_element.ReinforcementList = self.placement_list
        asg_element.LibraryElementsList = self.library_ele_list
        asg_element.FixtureElementsList = self.fixture_ele_list
        # Fill the AssemblyGroupElement Class

        # fill small Attribute list to write something on the Group
        self.attr_list = []
        self.attr_list.append(write_attr(self.document, 1444, "ASSEMBLYGROUP"))
        self.attr_list.append(write_attr(self.document, 684, "IfcElementAssembly"))

        attr_set_list = []
        attr_set_list.append(AllplanBaseElements.AttributeSet(self.attr_list))

        attributes = AllplanBaseElements.Attributes(attr_set_list)
        asg_element.SetAttributes(attributes)
        # fill small Attribute list to write something on the Group

        # fill AssemblbyGroup List for Pythonpart
        asg_list = []
        asg_list.append(asg_element)
        # fill AssemblbyGroup List for Pythonpart

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
                             attribute_list = self.attr_list,
                             fixture_elements = [],
                             assembly_elements = asg_list,
                             mws_elements = [])
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

        cross = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(2, self.shapes[1],
                                                                         ref_pnt,
                                                                         ref_pnt + AllplanGeo.Point3D(self.length, 0, 0),
                                                                         self.concrete_cover_shape1,
                                                                         self.concrete_cover_shape2 - self.diameter_shape2,
                                                                         self.distance_shape2)
        self.placement_list.append(longit)
        self.placement_list.append(cross)

        return self.shapes

    def create_fixture_form_3D_element(self, build_ele):
        # ----- ccreate Elements from Body
        self.FixtureGeometry = AllplanGeo.Polyhedron3D.CreateCuboid(
                                    AllplanGeo.Point3D(build_ele.FixturePlacePoint.value.X,
                                                       build_ele.FixturePlacePoint.value.Y,
                                                       build_ele.FixturePlacePoint.value.Z),
                                    AllplanGeo.Point3D(build_ele.FixturePlacePoint.value.X + build_ele.FixLength.value,
                                                       build_ele.FixturePlacePoint.value.Y + build_ele.FixWidth.value,
                                                       build_ele.FixturePlacePoint.value.Z + build_ele.FixHeight.value))

        if self.FixtureGeometry == None:
            return None

        self.com_prop_fix = AllplanBaseElements.CommonProperties()
        self.com_prop_fix.GetGlobalProperties()
        self.attr_list = []
        self.main_type = AllplanPrecast.MacroType.ePoint_Fixture
        self.sub_type = AllplanPrecast.MacroSubType.eUseNoSpecialSubType
        self.outline_type = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_NOTHING
        self.outline_shape_type = AllplanPrecast.OutlineShape.eBUILTIN_OUTLINE_SHAPE_RECTANGLE
        self.name = build_ele.Fixture_Name.value

        fix_body_3d = AllplanBasisElements.ModelElement3D(self.com_prop_fix, self.FixtureGeometry)
        fix_body_list_3d = [fix_body_3d]
        attr_set_list = []
        attr_set_list.append(AllplanBaseElements.AttributeSet(self.attr_list))

        attributes = AllplanBaseElements.Attributes(attr_set_list)

        #Slide 40
        slide_list = []

        slide_prop = AllplanPrecast.FixtureSlideProperties()
        slide_prop.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        slide = AllplanPrecast.FixtureSlideElement(slide_prop, fix_body_list_3d)
        slide_list.append(slide)

        # slide for Volume Body of Point Fixture
        slide_prop_2 = AllplanPrecast.FixtureSlideProperties()
        slide_prop_2.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW_OUTLINE_VOLUME
        slide_2 = AllplanPrecast.FixtureSlideElement(slide_prop_2, fix_body_list_3d)
        slide_list.append(slide_2)

        #Fixture definition 45
        fix_macro_prop = AllplanPrecast.FixtureProperties()

        fix_macro_prop.Type = self.main_type #MakroType
        fix_macro_prop.SubType = self.sub_type #SplitType
        fix_macro_prop.Name = self.name #Name
        fix_macro_prop.InsertionPoint = AllplanGeo.Point3D(build_ele.FixturePlacePoint.value)
        fix_macro = AllplanPrecast.FixtureElement(fix_macro_prop, slide_list)
        hash_code = macro_hash(fix_macro)
        fix_macro.SetHash(hash_code)

        #Fixture placement properties 50/53 - default Type and SubType is same as in macro
        fixture_pl_prop = AllplanPrecast.FixturePlacementProperties()
        fixture_pl_prop.Name = self.name #Name

        fixture_pl_prop.OutlineType = self.outline_type
        fixture_pl_prop.OutlineShape = self.outline_shape_type

        self.cat_ref = build_ele.CatRef.value
        if(self.cat_ref != ""):
            fixture_pl_prop.ConnectionToAIACatalog = True

        #Fixture1
        fixture = AllplanPrecast.FixturePlacementElement(self.com_prop_fix,fixture_pl_prop, fix_macro)

        attr_fix_list = []
        if(self.cat_ref != ""):
            attr_fix_list.append(AllplanBaseElements.AttributeString(1332, self.cat_ref))

            attr_set_list = []
            attr_set_list.append(AllplanBaseElements.AttributeSet(attr_fix_list))

            attributes = AllplanBaseElements.Attributes(attr_set_list)

            fixture.SetAttributes(attributes)

        return fixture
