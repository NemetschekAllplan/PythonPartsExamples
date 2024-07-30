"""
Script for Scalable Table - Chair - Group
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from ContentExamples.Chair import Chair
from ContentExamples.TableScalable import TableScalable
from PythonPart import View2D3D, PythonPart, PythonPartGroup

print('Load TableChairGroupScalable.py')

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

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)

def create_element(build_ele, doc):
    """
    Create table element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    del doc

    common_props = AllplanBaseElements.CommonProperties()
    common_props.GetGlobalProperties()   

    #------------------ Set the values
    table = TableScalable(build_ele.Ref_x.value, build_ele.Ref_y.value, build_ele.Ref_z.value,
                  build_ele.BoardThickness.value, build_ele.LegWidth.value, build_ele.XExcessLength.value, build_ele.YExcessLength.value)
                  
    if not table.is_valid():
        return[]

    table_brep = table.create()
    table_attr_list = [AllplanBaseElements.AttributeDouble(AllplanBaseElements.ATTRNR_VOLUME, table.volume())]
    #ATTRNR_PYTHONPART_OBJECT is only for information in the placement scaling behaviour depends on the use of ref_x, ref_y, ref_z
    table_attr_list.append(AllplanBaseElements.AttributeString(AllplanBaseElements.ATTRNR_PYTHONPART_OBJECT, "MainObject"))
    
    table_views = [View2D3D ([AllplanBasisElements.ModelElement3D(common_props, table_brep)])]
    handle_list = table.create_handles()

    chair = Chair()
    chair_brep = chair.create()
    chair_attr_list = [AllplanBaseElements.AttributeDouble(AllplanBaseElements.ATTRNR_VOLUME, chair.volume())]
    #ATTRNR_PYTHONPART_OBJECT is only for information in the placement scaling behaviour depends on the use of ref_x, ref_y, ref_z
    chair_attr_list.append(AllplanBaseElements.AttributeString(AllplanBaseElements.ATTRNR_PYTHONPART_OBJECT, "SubObject"))
    chairs_views = [View2D3D ([AllplanBasisElements.ModelElement3D(common_props, chair_brep)])]

    trans_list = table.create_chair_positions(chair.get_seat_width())

    group_elems = [] # All elements of suite

    #Table without translate has to be the firsrt element because of group modification

    # Define python part for table
    main_part = (PythonPart ("TableScalable", parameter_list = table.get_params_list(),
                                   hash_value = table.hash(), python_file = table.filename(),
                                   views = table_views, attribute_list = table_attr_list))
    main_part.distortion_state(True)
    group_elems.append(main_part)

    # Define python parts for all chairs
    for matrix in trans_list:
        sub_part = (PythonPart ("Chair", parameter_list = chair.get_params_list(),
                                hash_value = chair.hash(), python_file = chair.filename(),
                                views = chairs_views, matrix = matrix, attribute_list = chair_attr_list))
        sub_part.distortion_state(True)
        group_elems.append(sub_part)

    # Define one python part group for this suite (1 table and (0..n) chairs)
    pythonpartgroup = PythonPartGroup ("TableChairGroup", build_ele.get_params_list(), build_ele.get_hash(),
                                       build_ele.pyp_file_name, group_elems)
    model_elem_list = pythonpartgroup.create()
    return (model_elem_list, handle_list)
