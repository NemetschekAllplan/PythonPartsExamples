"""
Script for Structural Framing Brace
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_ArchElements as AllplanArchElements

import NemAll_Python_Utility as AllplanUtil

# Print some information
print('Load StructuralBrace.py')


# Method for checking the supported versions
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


# Method for element creation
def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
            tuple  with created elements, handles and (otional) reinforcement.
    """

    #----------------- create the element
    model_elem_list = []

    try:
        braceProps = AllplanArchElements.StructuralBraceProperties()

        if build_ele.BraceType.value == 0:
            rectShape = AllplanArchElements.RectangularShape()
            rectShape.Width = build_ele.Width.value 
            rectShape.Thickness = build_ele.Thickness.value 
    
            braceProps.SetProfileShapeProperties(rectShape)
        else:
            profileShape = AllplanArchElements.ProfileShape()
            profileShape.ProfilePath = build_ele.SymbolDialog.value 
        
            try:
                braceProps.SetProfileShapeProperties(profileShape)
            except:
                print("Invalid path to profile")
                return ([],[])

        # Set Angel
        angle = AllplanGeo.Angle()
        angle.Deg = build_ele.Angle.value
        braceProps.SetProfileAngle(angle)

        commonProps = AllplanBaseElements.CommonProperties()
        commonProps.GetGlobalProperties()
        braceProps.SetCommonProperties(commonProps)
        braceProps.SetMaterial(build_ele.Material.value)

        braceProps.SetStartPoint(0, 0, 0)
        braceProps.SetEndPoint(2500, 0, 0)
    
        braceProps.SetHeightProperties(doc, build_ele.BracePlaneReferences.value)
        
        local_str_table, global_str_table = build_ele.get_string_tables()
        
        if (build_ele.TwoAnchorPoints.value == False):
            anchor = __get_anchor_point_by_string__(build_ele.AnchorPoint.value, local_str_table)
            if anchor == 0:
                str_msg = 'No localisation available.\n'
                str_msg += 'This PythonPart can only run correct with a valid localisation file.\n'
                str_msg += 'No geometry will be created.'
                AllplanUtil.ShowMessageBox(str_msg, AllplanUtil.MB_OK)
                return ([],[])
            braceProps.SetAnchorPointProperties(anchor, build_ele.Offset.value, anchor, build_ele.Offset.value, build_ele.TwoAnchorPoints.value)
        elif (build_ele.TwoAnchorPoints.value == True):
            anchorStart = __get_anchor_point_by_string__(build_ele.AnchorPointStart.value, local_str_table)
            if anchorStart == 0:
                str_msg = 'No localisation available.\n'
                str_msg += 'This PythonPart can only run correct with a valid localisation file.\n'
                str_msg += 'No geometry will be created.'
                AllplanUtil.ShowMessageBox(str_msg, AllplanUtil.MB_OK)
                return ([],[])
                
            anchorEnd = __get_anchor_point_by_string__(build_ele.AnchorPointEnd.value, local_str_table)
            if anchorEnd == 0:
                str_msg = 'No localisation available.\n'
                str_msg += 'This PythonPart can only run correct with a valid localisation file.\n'
                str_msg += 'No geometry will be created.'
                AllplanUtil.ShowMessageBox(str_msg, AllplanUtil.MB_OK)
                return ([],[])
        
            braceProps.SetAnchorPointProperties(anchorStart, build_ele.OffsetStart.value, anchorEnd, build_ele.OffsetEnd.value, build_ele.TwoAnchorPoints.value)

        angleX = AllplanGeo.Angle()
        angleY = AllplanGeo.Angle()
        
        angleX.Deg = build_ele.StartAngleX.value
        angleY.Deg = build_ele.StartAngleY.value        
        braceProps.SetAnglesAtStart(angleX, angleY)
        
        angleX.Deg = build_ele.EndAngleX.value
        angleY.Deg = build_ele.EndAngleY.value    
        braceProps.SetAnglesAtEnd(angleX, angleY)
        
        brace = AllplanArchElements.StructuralBraceElement(braceProps)

        model_elem_list = [brace]
    except Exception as ex:
        msg_text = "Exception during creting of Structural element"
        print()
        print(msg_text)
        
        print(ex)

        AllplanUtil.ShowMessageBox(msg_text, AllplanUtil.MB_OK)


    # Define the handles list
    handle_list = []

    # Return a tuple with elements list and handles list
    return (model_elem_list, handle_list)

def modify_element_property(build_ele_index_list, name, value):
    """
    Modify property of element

    Args:
        build_ele_index_list:   Building elements index list
        name:                   the name of the property.
        value:                  new value for property.
    """

    build_ele = build_ele_index_list
    
    if name == "TwoAnchorPoints":
        if (value == True):
            build_ele.AnchorPointStart.value = build_ele.AnchorPoint.value
            build_ele.OffsetStart.value = build_ele.Offset.value
        else:
            build_ele.AnchorPoint.value = build_ele.AnchorPointStart.value
            build_ele.Offset.value = build_ele.OffsetStart.value

def __get_anchor_point_by_string__(anchor_point, local_str_table):
    """
    Calcutates the depending on inputvalue and the content of string tables

    Args:
         anchor_point           : localised string value
         local_str_table        : local string table

    Returns:
        int value for anchor point
    """
    
    box_point = 0
    #<ValueList>top left|left in middle|left down|top in middle|in middle|in middle down|top right|right in middle|right down|in center of gravity</ValueList>
    #<ValueList_TextIds>1102|1103|1104|1105|1106|1107|1108|1109|1110|1111</ValueList_TextIds>
    text_id_possible = [1102,1103,1104,1105,1106,1107,1108,1109,1110,1111]

    text_id_used = 0

    for elem in text_id_possible:
        try:
            res_str, res  = local_str_table.get_entry(str(elem))
        except:
            print("String table was not found.")
            return (0)
            
        if res is True:
            if res_str == anchor_point:
                text_id_used = elem
                break

    # uses \\Interfaces\NemAll_Elements\NemAll_ElementsArchitecture\Skeleton\BoxPointEnum.h
    if text_id_used == 1102:
        box_point = 4 # 1102 stands for "top left"
    elif text_id_used == 1103:
        box_point = 9 # 1103 stands for "left in middle"
    elif text_id_used == 1104:
        box_point = 1 # 1104 stands for "left down"
    elif text_id_used == 1105:
        box_point = 8 # 1105 stands for "top in middle"
    elif text_id_used == 1106:
        box_point = 5 # 1106 stands for "in middle"
    elif text_id_used == 1107:
        box_point = 6 # 1107 stands for "in middle down"
    elif text_id_used == 1108:
        box_point = 3 # 1108 stands for "top right"
    elif text_id_used == 1109:
        box_point = 7 # 1109 stands for "right in middle"
    elif text_id_used == 1110:
        box_point = 2 # 1110 stands for "right down"
    elif text_id_used == 1111:
        box_point = 10 # 1111 stands for "in center of gravity"
    else:
        text_id_used = 0

    return box_point