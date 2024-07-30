"""
Fixture group example
"""

import hashlib as hashlib

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Precast as AllplanPrecast

from BuildingElement import BuildingElement

# Print some information
print('Load FixtureGroup.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    del _build_ele
    del _version

    # Support all versions
    return True

def macro_hash (fix_macro) -> str:
    """
    Calculate hash value for script

    Returns:
        Hash string
    """

    param_string = fix_macro.__repr__()
    hash_val = hashlib.sha224(param_string.encode('utf-8')).hexdigest()
    return hash_val

def create_element(build_ele: BuildingElement,
                   _doc     : AllplanElementAdapter.DocumentAdapter) -> tuple:
    """
    Creation of element

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
            created fixture group tuple with elements and handles.
    """

    groupFixture = GroupFixture(build_ele, _doc)

    return groupFixture.create_element()

class GroupFixture:
    def __init__(self, build_ele, document) -> None:
        """
        Initialization

        Args:
            build_ele:  the building element.
            document:   input document
        """

        del document

        self.build_ele = build_ele

        self.model_elem_list = []
        self.handle_list = []
        self.common_props = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()
        self.Name = "Fixture group 1"
        self.Dynamic = False
        self.GroupLeading = False
        self.ReferencePoint = AllplanGeo.Point3D(125, 0, 0)

    def create_element(self) -> tuple:
        """
        Creation of element

        Args:
            build_ele: the building element.
            doc:       input document

        Returns:
                tuple with created elements and handles.
        """

        fixture_list = []

        self.name = "Fixture 1"                               # x, y, z,   l,   w,   h
        fixture_list.append(self.create_fixture_form_3D_element(0, 0, 0, 100, 100, 100))

        self.name = "Fixture 2"                               #   x, y, z,  l,  w,  h
        fixture_list.append(self.create_fixture_form_3D_element(150, 0, 0, 50, 50, 50))

        fixture_grp_prop = AllplanPrecast.FixtureGroupProperties()

        # Name
        fixture_grp_prop.Name = self.build_ele.Name.value

        # Type
        if self.build_ele.Dynamic.value == True:
            fixture_grp_prop.Type = AllplanPrecast.MacroGroupType.eGroupType_DynamicGroup
        elif self.build_ele.GroupLeading.value == True:
            fixture_grp_prop.Type = AllplanPrecast.MacroGroupType.eGroupType_LeadingGroup

            # leading point
            fixture_grp_prop.LeadingPoint = self.build_ele.ReferencePoint.value
        else:
            fixture_grp_prop.Type = AllplanPrecast.MacroGroupType.eGroupType_GeneralGroup

        fixture_group = AllplanPrecast.FixtureGroupElement(fixture_grp_prop, fixture_list)

        self.model_elem_list = [fixture_group]

        return (self.model_elem_list, self.handle_list)


    def create_fixture_form_3D_element(self, x, y, z, l, w, h) -> AllplanPrecast.FixturePlacementElement:
        """
        Creation of fixture from 3D element

        Args:
            x, y, z -> Start point
            l, w, h -> Dimensions

        Returns:
                FixturePlacementElement
        """

        # ----- create Elements from Body
        self.FixtureGeometry = AllplanGeo.Polyhedron3D.CreateCuboid(
                                    AllplanGeo.Point3D(x, y, z),
                                    AllplanGeo.Point3D(x + l,
                                                       y + w,
                                                       z + h))

        if self.FixtureGeometry == None:
            return None

        self.com_prop_fix = AllplanBaseElements.CommonProperties()
        self.com_prop_fix.GetGlobalProperties()
        self.attr_list = []
        self.main_type = AllplanPrecast.MacroType.ePoint_Fixture
        self.sub_type = AllplanPrecast.MacroSubType.eUseNoSpecialSubType
        self.outline_type = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_NOTHING
        self.outline_shape_type = AllplanPrecast.OutlineShape.eBUILTIN_OUTLINE_SHAPE_RECTANGLE

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

        fix_macro_prop.Type = self.main_type   #MakroType
        fix_macro_prop.SubType = self.sub_type #SplitType
        fix_macro_prop.Name = self.name        #Name
        fix_macro_prop.InsertionPoint = AllplanGeo.Point3D(x, y, z)
        fix_macro = AllplanPrecast.FixtureElement(fix_macro_prop, slide_list)
        hash_code = macro_hash(fix_macro)
        fix_macro.SetHash(hash_code)

        #Fixture placement properties 50/53 - default Type and SubType is same as in macro
        fixture_pl_prop = AllplanPrecast.FixturePlacementProperties()
        fixture_pl_prop.Name = self.name #Name

        fixture_pl_prop.OutlineType = self.outline_type
        fixture_pl_prop.OutlineShape = self.outline_shape_type

        self.cat_ref = "E-Dose"
        if(self.cat_ref != ""):
            fixture_pl_prop.ConnectionToAIACatalog = True

        #Fixture
        fixture = AllplanPrecast.FixturePlacementElement(self.com_prop_fix,fixture_pl_prop, fix_macro)

        attr_fix_list = []
        if(self.cat_ref != ""):
            attr_fix_list.append(AllplanBaseElements.AttributeString(1332, self.cat_ref))

            attr_set_list = []
            attr_set_list.append(AllplanBaseElements.AttributeSet(attr_fix_list))

            attributes = AllplanBaseElements.Attributes(attr_set_list)

            fixture.SetAttributes(attributes)

        return fixture
