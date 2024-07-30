"""
Script for Structural Framing Column
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_ArchElements as AllplanArchElements

import NemAll_Python_Utility as AllplanUtil

# Print some information
print('Load StructuralColumn.py')


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
        columnProps = AllplanArchElements.StructuralColumnProperties()

        if build_ele.ColumType.value == 0:
            rectShape = AllplanArchElements.RectangularShape()
            rectShape.Width = build_ele.Width.value
            rectShape.Thickness = build_ele.Thickness.value

            columnProps.SetProfileShapeProperties(rectShape)

        elif build_ele.ColumType.value == 1:
            circleShape = AllplanArchElements.CircularShape()
            circleShape.Radius = build_ele.Radius.value

            columnProps.SetProfileShapeProperties(circleShape)
        else:
            profileShape = AllplanArchElements.ProfileShape()
            profileShape.ProfilePath = build_ele.SymbolDialog.value

            try:
                columnProps.SetProfileShapeProperties(profileShape)
            except:
                print("Invalid path to profile")
                return ([],[])

        # Set Angle
        angle = AllplanGeo.Angle()
        angle.Deg = build_ele.Angle.value
        columnProps.SetProfileAngle(angle)

        commonProps = AllplanBaseElements.CommonProperties()
        commonProps.GetGlobalProperties()
        columnProps.SetCommonProperties(commonProps)
        columnProps.SetMaterial(build_ele.Material.value)
        columnProps.SetPosition(0, 0, 0)

        columnProps.SetHeightProperties(doc, build_ele.ColumnPlaneReferences.value)

        anchor = 0
        local_str_table, global_str_table = build_ele.get_string_tables()
        anchor = __get_anchor_point_by_string__(build_ele.AnchorPoint.value, local_str_table)

        if anchor == 0:
            str_msg = 'No localisation available.\n'
            str_msg += 'This PythonPart can only run correct with a valid localisation file.\n'
            str_msg += 'No geometry will be created.'
            AllplanUtil.ShowMessageBox(str_msg, AllplanUtil.MB_OK)
            return ([],[])

        columnProps.SetAnchorPointProperties(anchor, build_ele.Offset.value)

        angleX = AllplanGeo.Angle()
        angleY = AllplanGeo.Angle()

        angleX.Deg = build_ele.StartAngleX.value
        angleY.Deg = build_ele.StartAngleY.value
        columnProps.SetAnglesAtStart(angleX, angleY)

        angleX.Deg = build_ele.EndAngleX.value
        angleY.Deg = build_ele.EndAngleY.value
        columnProps.SetAnglesAtEnd(angleX, angleY)

        column = AllplanArchElements.StructuralColumnElement(columnProps)
        column.SetAxisVisibility(build_ele.ShowAxis.value)

        model_elem_list = [column]
    except Exception as ex:
        msg_text = "Exception during creting of Structural element"
        print(msg_text)
        print(ex)

        AllplanUtil.ShowMessageBox(msg_text, AllplanUtil.MB_OK)


    # Define the handles list
    handle_list = []

    # Return a tuple with elements list and handles list
    return (model_elem_list, handle_list)

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
