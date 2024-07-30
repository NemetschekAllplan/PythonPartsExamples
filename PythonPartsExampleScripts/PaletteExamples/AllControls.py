""" Example script for AllControls
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.AllControlsBuildingElement import AllControlsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load AllControls.py')


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


def set_active_palette_page_index(active_page_index: int):
    """ set the active page index

    Args:
        active_page_index: active page index
    """

    print()
    print("Active page index: ", active_page_index)


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = AllControls(doc)

    return element.create(build_ele)


def modify_element_property(build_ele: BuildingElement,
                            name     : str,
                            value    : Any) -> bool:
    """ Modify property of element

    Args:
        build_ele: the building element.
        name:      the name of the property.
        value:     new value for property.

    Returns:
        True/False if palette refresh is necessary
    """

    if name == build_ele.Length.name:
        build_ele.Area.value   = cast(float, value * value * 6)
        build_ele.Volume.value = cast(float, value * value * value)

    elif name == build_ele.RefPointId.name:
        build_ele.RefPointId.value = cast(int, value)

    return True


def on_control_event(build_ele: BuildingElement,
                     event_id : int) -> bool:
    """ On control event

    Args:
        build_ele: the building element.
        event_id:  event id of control.

    Returns:
        True/False if palette refresh is necessary
    """

    if event_id == build_ele.CENTER_OF_GRAVITY:
        build_ele.RefPointId.value = 0

    elif event_id == build_ele.CENTER_OF_GRAVITY_SELECTED:
        build_ele.RefPointId.value = 5

    return True


class AllControls():
    """ Definition of class Visibility
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """ Initialization of class Visibility

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.document       = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: the building element.

        Returns:
            created element result
        """

        length = build_ele.Length.value

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        x_offset = 0
        y_offset = 0

        if build_ele.RefPointId.value in {2, 5, 8}:
            x_offset = -length / 2

        elif build_ele.RefPointId.value in {3, 6, 9}:
            x_offset = -length

        if build_ele.RefPointId.value in {1, 2, 3}:
            y_offset = -length

        elif build_ele.RefPointId.value in {4, 5, 6}:
            y_offset = -length / 2

        polyhed = AllplanGeo.Move(polyhed, AllplanGeo.Vector3D(x_offset, y_offset, 0))


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(build_ele.CommonProp.value, polyhed))

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(self.model_ele_list)
