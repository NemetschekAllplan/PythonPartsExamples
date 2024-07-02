"""
Script for Structural Framing Column creation M x N
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_ArchElements as AllplanArchElements


# Print some information
print('Load MxNStructuralColumn.py')


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

    common_props = AllplanBaseElements.CommonProperties()
    common_props.GetGlobalProperties()
    columnProps.SetCommonProperties(common_props)
    columnProps.SetMaterial(build_ele.Material.value)
    columnProps.SetPosition(0, 0, 0)

    columnProps.SetHeightProperties(doc, build_ele.ColumnPlaneReferences.value)

    model_elem_list = []
    spaceX = build_ele.Space_X.value
    spaceY = build_ele.Space_Y.value

    for x in range(build_ele.Number_X_Dir.value):
        for y in range(build_ele.Number_Y_Dir.value):
            columnProps.SetPosition(x * spaceX, y * spaceY, 0)
            column = AllplanArchElements.StructuralColumnElement(columnProps)
            model_elem_list.append(column)

    # Define the handles list
    handle_list = []
    # Return a tuple with elements list and handles list
    return (model_elem_list, handle_list)
