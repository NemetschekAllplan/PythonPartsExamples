"""Example script showing the creation of a PythonPartGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
from BuildingElementService import BuildingElementService
from CreateElementResult import CreateElementResult
from PythonPart import PythonPart, PythonPartGroup

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartGroupBuildingElement import PythonPartGroupBuildingElement  # type: ignore
    from __BuildingElementStubFiles.PythonPartWithAttributesBuildingElement import PythonPartWithAttributesBuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PythonPartGroup.py')

def check_allplan_version(_build_ele: PythonPartGroupBuildingElement,
                          _version: float) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True

def create_element(build_ele:   PythonPartGroupBuildingElement,
                   _doc:        AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create the python part group

    Args:
        build_ele: the building element.
        _doc:       input document

    Returns:
        Result of the element creation
    """

    # get the building element of the subordinate PythonPart from its .pyp file
    etc_path = AllplanSettings.AllplanPaths.GetEtcPath()
    result, sub_script, sub_build_ele = BuildingElementService.read_build_ele_from_pyp(
        file_name = etc_path + r"\Examples\PythonParts\BasisExamples\PythonParts\PythonPartWithAttributes.pyp")

    if not result or not sub_script:
        return CreateElementResult()

    # cast the building element for better type checking
    if TYPE_CHECKING:
        sub_build_ele = cast(PythonPartWithAttributesBuildingElement, sub_build_ele)

    # construct an empty PythonPart group from a BuildingElement
    pythonpart_group = PythonPartGroup.from_build_ele(build_ele,
                                                      type_uuid = "bbd282f4-7fd8-4640-897e-6f49d8661b04",
                                                      type_display_name = "PythonPart group created from PythonPart with attributes")

    placement_matrix = AllplanGeo.Matrix3D()

    for i in range(build_ele.BoxCount.value):
        # apply different dimensions to each cube
        sub_build_ele.Dimensions.value = build_ele.BoxDimensions.value[i]

        # other parameters should remain the same for each cube
        sub_build_ele.CommonProp.value = build_ele.CommonProp.value
        sub_build_ele.LayerThickness.value = build_ele.LayerThickness.value

        # create PythonPart for each cube using function from the sub script and append it to the group
        box_pythonpart = cast(PythonPart, sub_script.create_pythonpart(sub_build_ele))
        box_pythonpart.placement_matrix = AllplanGeo.Matrix3D(placement_matrix)
        pythonpart_group.append(box_pythonpart)

        # modify the placement matrix by translating by box length + spacing
        placement_matrix.Translate(AllplanGeo.Vector3D(build_ele.BoxDimensions.value[i].X + build_ele.Spacing.value,0,0))

    return CreateElementResult(pythonpart_group.create())
