""" Example script for NamedTuple
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from ControlPropertiesUtil import ControlPropertiesUtil
from CreateElementResult import CreateElementResult

from PythonPartUtil import PythonPartUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.NamedTupleBuildingElement import NamedTupleBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load NamedTuple.py')


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


def initialize_control_properties(build_ele     : BuildingElement,
                                  ctrl_prop_util: ControlPropertiesUtil,
                                  _doc          : AllplanElementAdapter.DocumentAdapter) -> None:
    """ initialize the control properties

    Args:
        build_ele     : building element
        ctrl_prop_util: control properties utility
        _doc          : document
    """

    #--------------------- block

    def u_shape_ctrl_enable(field_name: str) -> bool:
        """ enable function for the u shape

        Args:
            field_name: field name of the tuple

        Returns:
            enable state
        """
        return build_ele.DisableBlockName.value != field_name

    ctrl_prop_util.set_enable_function("UShape", u_shape_ctrl_enable)


    #--------------------- row

    def l_shape_ctrl_visible(field_name: str) -> bool:
        """ visible function of the l shape

        Args:
            field_name: field name of the tuple

        Returns:
            visible state
        """
        return build_ele.HideRowName.value != field_name

    ctrl_prop_util.set_visible_function("LShape", l_shape_ctrl_visible)


    #--------------------- block list

    def u_shape_list_ctrl_visible(row        : int,
                                  _field_name: str) -> bool:
        """ visible function of the u shape list

        Args:
            row:         list row
            _field_name: field name of the tuple

        Returns:
            visible state of the row
        """
        return row + 1 != build_ele.HideRow.value

    def u_shape_list_ctrl_enable(_row      : int,
                                 field_name: str) -> bool:
        """ enable function of the u shape tuple field

        Args:
            _row:       list row
            field_name: field name of the tuple

        Returns:
            enable state of the tuple field
        """
        return build_ele.DisableColumn.value != field_name

    ctrl_prop_util.set_visible_function("UShapeList", u_shape_list_ctrl_visible)
    ctrl_prop_util.set_enable_function("UShapeList", u_shape_list_ctrl_enable)


    #--------------------- list

    def stirrup_list_column_visible(_row      : int,
                                    field_name: str) -> bool:
        """ visible function of the stirrup list tuple field

        Args:
            _row:       list row
            field_name: field name of the tuple

        Returns:
            visible state of the tuple field
        """
        return field_name != build_ele.HideColumn.value

    ctrl_prop_util.set_visible_function("StirrupList", stirrup_list_column_visible)


def modify_control_properties(_build_ele     : BuildingElement,
                              _ctrl_prop_util: ControlPropertiesUtil,
                              value_name     : str,
                              _event_id      : int,
                              _doc           : AllplanElementAdapter.DocumentAdapter) -> bool:
    """ modify the control properties

    Args:
        _build_ele:      building element with the parameter properties
        _ctrl_prop_util: control properties
        value_name:      name of the modified value
        _event_id:       event id of the clicked button control
        _doc:            document of the Allplan drawing files

    Returns:
        update the property palette
    """

    return value_name in {"HideRow", "DisableColumn"}


def on_control_event(build_ele: BuildingElement,
                     event_id : int) -> bool:
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        event_id:  event id of the clicked button control

    Returns:
        True/False if palette refresh is necessary
    """

    block_row_index = event_id >> 16
    block_event_id  = event_id - (block_row_index << 16)

    print("============================")
    print()
    print("Button clicked with EventId =", block_event_id, " in row =", block_row_index)
    print()

    build_ele.ButtonEventID.value = str(block_event_id)
    build_ele.ButtonIndex.value   = str(block_row_index)

    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        result of the created element
    """

    #--------------------- create the row text of the list

    stirrup_list = build_ele.StirrupList.value

    for i in range(1, build_ele.ItemCount.value - 1):
        stirrup_list[i] = stirrup_list[i]._replace(RowText = "Inside " + str(i))

    stirrup_list[0] = stirrup_list[0]._replace(RowText = "Top")

    if build_ele.ItemCount.value > 1:
        stirrup_list[-1] = stirrup_list[-1]._replace(RowText = "Bottom")


    #--------------------- create the text

    com_prop =  AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    text_prop = AllplanBasisElements.TextProperties()

    y_dist = -(text_prop.Height * 2 * doc.GetScalingFactor())

    u_shape = build_ele.UShape.value

    texts = [AllplanBasisElements.TextElement(com_prop, text_prop,
                                              "namedtuple(Picture,ReinfBarDiameter,...)", AllplanGeo.Point2D(0, 0)),
             AllplanBasisElements.TextElement(com_prop, text_prop,
                                              "UShape.Diameter = " + str(u_shape.Diameter), AllplanGeo.Point2D(0, y_dist)),
             AllplanBasisElements.TextElement(com_prop, text_prop,
                                              "UShape.ConcreteCover = " + str(u_shape.Cover), AllplanGeo.Point2D(0, y_dist * 2)),
             AllplanBasisElements.TextElement(com_prop, text_prop,
                                              "UShape.Length1 = " + str(u_shape.Length1), AllplanGeo.Point2D(0, y_dist * 3)),
             AllplanBasisElements.TextElement(com_prop, text_prop,
                                              "UShape.Length2 = " + str(u_shape.Length2), AllplanGeo.Point2D(0, y_dist * 4))]


    pyp_util = PythonPartUtil()

    pyp_util.add_pythonpart_view_2d(texts)

    return CreateElementResult(pyp_util.create_pythonpart(build_ele))
