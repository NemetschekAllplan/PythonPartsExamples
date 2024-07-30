""" Example script for include controls
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from ControlPropertiesUtil import ControlPropertiesUtil
from PythonPartUtil import PythonPartUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ValueListBuildingElement import ValueListBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ValueList.py')


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
                                  _doc          : AllplanEleAdapter.DocumentAdapter) -> None:
    """ initialize the control properties

    Args:
        build_ele     : building element
        ctrl_prop_util: control properties utility
        _doc          : document
    """

    #--------------------- use the enable function

    def item_enable(row: int) -> bool:
        """ enable function for the row

        Args:
            row: row index

        Returns:
            enable state of the row
        """
        return build_ele.EnableListRow.value != row

    ctrl_prop_util.set_enable_function("EnableVisibleItemsByFunction", item_enable)


    #--------------------- use the visible function

    def item_visible(row: int) -> bool:
        """ visible function for the row

        Args:
            row: row index

        Returns:
            visible state of the row
        """
        return build_ele.HideListRow.value != row

    ctrl_prop_util.set_visible_function("EnableVisibleItemsByFunction", item_visible)



def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        result of the created element
    """

    element = ValueList(doc)

    return element.create(build_ele)


def modify_element_property(build_ele: BuildingElement,
                            name     : str,
                            value    : Any) -> bool:
    """ Modify property of element

    Args:
        build_ele: building element with the parameter properties
        name:      name of the modified property
        value:     new value for property.

    Returns:
        update palette state
    """

    if name != build_ele.CubeCount.name:
        return False

    coordinates = build_ele.Coordinates.value

    for index in range(1, value):
        if coordinates[index][0] == coordinates[index - 1][0] and \
           coordinates[index][1] == coordinates[index - 1][1] and \
           coordinates[index][2] == coordinates[index - 1][2]:

            for index1 in range(index, value):
                for column in range(3):
                    coordinates[index1][column] += 2000 * (index1 - index + 1)

    return True


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

    if block_event_id == build_ele.BUTTON_GROUP_EVENT_ID:
        build_ele.ButtonEventID.value = str(block_event_id)
        build_ele.ButtonIndex.value   = str(block_row_index)
    else:
        build_ele.ButtonEventID2.value = str(block_event_id)
        build_ele.ButtonIndex2.value   = str(block_row_index)

    return True


class ValueList():
    """ Definition of class Visibility
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class Visibility

        Args:
            doc: document of the Allplan drawing files
        """

        self.model_ele_list = None
        self.document       = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            result of the created element
        """

        coordinates = build_ele.Coordinates.value
        coord_dim   = build_ele.CoordDimension3D.value + 2

        if build_ele.InitCoord.value:
            build_ele.InitCoord.value = False

            for i in range(build_ele.CubeCount.value):
                for j in range(coord_dim):
                    coordinates[i][j] = 2000 * i

        model_list = []

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        text_prop                  = AllplanBasisEle.TextProperties()
        text_prop.IsScaleDependent = True

        scaling_factor = self.document.GetScalingFactor()


        #----------------- create the cubes

        for coordinate, cube_dim, ref_loc, text_data in zip(build_ele.Coordinates.value,
                                                            build_ele.CubeDimensions.value,
                                                            build_ele.RefPointLocation.value,
                                                            build_ele.TextData.value):
            xref = coordinate[0]
            yref = coordinate[1]
            zref = 0 if coord_dim == 2 else coordinate[2]

            if ref_loc[0] == "Center":
                xref -= cube_dim / 2
            elif ref_loc[0] == "Right":
                xref -= cube_dim

            if ref_loc[1] == "Center":
                yref -= cube_dim / 2
            elif ref_loc[1] == "Top":
                yref -= cube_dim

            if cube_dim:
                polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(xref, yref, zref),
                                                               AllplanGeo.Point3D(xref + cube_dim, yref + cube_dim, zref + cube_dim))

                model_list.append(AllplanBasisEle.ModelElement3D(com_prop, polyhed))

            if len(text_data[1]):
                text_prop.Height = text_data[0]
                text_prop.Width  = text_prop.Height

                model_list.append(AllplanBasisEle.TextElement(com_prop, text_prop, text_data[1],
                                                                   AllplanGeo.Point2D(xref,
                                                                                      yref - text_prop.Height * scaling_factor * 1.5)))

        #----------------- sum the distances

        build_ele.Length.value  = sum(build_ele.Distance.value[:-1])
        build_ele.Length2.value = sum(build_ele.Distance2.value[:-1])


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d(model_list)

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(self.model_ele_list)
