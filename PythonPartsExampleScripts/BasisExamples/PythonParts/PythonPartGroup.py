"""Example script showing the creation of a PythonPartGroup
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from PythonPart.PythonPart import PythonPart
from PythonPart.PythonPartGroup import PythonPartGroup
from PythonPart.PythonPartAttributeTakeoverService import PythonPartAttributeTakeoverService

from Utils.PythonPart.PythonPartScriptObjectUtil import PythonPartScriptObjectUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartGroupBuildingElement import PythonPartGroupBuildingElement  # type: ignore
    from __BuildingElementStubFiles.PythonPartWithAttributesBuildingElement import PythonPartWithAttributesBuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

    PythonPartWithAttributesBuildingElement = BuildingElement

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


def create_script_object(build_ele         : PythonPartGroupBuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PythonPartGroupExample(build_ele, script_object_data)


class PythonPartGroupExample(BaseScriptObject):
    """ Definition of class PythonPartGroupExample
    """

    def __init__(self,
                 build_ele         : PythonPartGroupBuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def create_library_preview(self) -> CreateElementResult:
        """ create the library preview

        Returns:
            created elements for the preview
        """

        return self.execute()


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        script_obj_util = PythonPartScriptObjectUtil(self.coord_input,
                                                     r"Library\Examples\PythonParts\BasisExamples\PythonParts\PythonPartWithAttributes.pyp")

        if (script_obj := script_obj_util.create_script_object()) is None:
            return CreateElementResult()

        # cast the building element for better type checking
        sub_build_ele = cast(PythonPartWithAttributesBuildingElement, script_obj_util.build_ele_list[0])

        # construct an empty PythonPart group from a BuildingElement
        pythonpart_group = PythonPartGroup.from_build_ele(build_ele,
                                                          type_uuid = "bbd282f4-7fd8-4640-897e-6f49d8661b04",
                                                          type_display_name = "PythonPart group created from PythonPart with attributes")

        placement_matrix = AllplanGeo.Matrix3D()

        for i in range(build_ele.BoxCount.value):
            sub_pythonpart_key = f"Box {i + 1}"

            PythonPartAttributeTakeoverService.check_external_sub_pyp_attribute_modification([sub_build_ele], sub_pythonpart_key)

            # apply different dimensions to each cube
            sub_build_ele.Dimensions.value = build_ele.BoxDimensions.value[i]

            # other parameters should remain the same for each cube
            sub_build_ele.CommonProp.value     = build_ele.CommonProp.value
            sub_build_ele.LayerThickness.value = build_ele.LayerThickness.value

            # create PythonPart for each cube using function from the sub script and append it to the group
            box_pythonpart = cast(PythonPart, script_obj.create_pythonpart())                  # type: ignore

            box_pythonpart.placement_matrix   = AllplanGeo.Matrix3D(placement_matrix)
            box_pythonpart.sub_pythonpart_key = sub_pythonpart_key

            pythonpart_group.append(box_pythonpart)

            # modify the placement matrix by translating by box length + spacing
            placement_matrix.Translate(AllplanGeo.Vector3D(build_ele.BoxDimensions.value[i].X + build_ele.Spacing.value,0,0))

        return CreateElementResult(pythonpart_group.create())
