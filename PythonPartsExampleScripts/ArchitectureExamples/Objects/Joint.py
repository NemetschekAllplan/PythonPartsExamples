""" Example Script for the joint
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ScriptObjectInteractors.ArchPointInteractor import ArchPointInteractor

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.Architecture.OpeningPointsUtil import OpeningPointsUtil
from Utils.Architecture.OpeningHandlesUtil import OpeningHandlesUtil
from Utils.ElementFilter.ArchitectureElementsQueryUtil import ArchitectureElementsQueryUtil

from .OpeningBase import OpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.JointBuildingElement import JointBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Joint.py')

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


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ArchitectureExamples\Objects\Joint.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Joint(build_ele, script_object_data) # type: ignore


class Joint(OpeningBase):
    """ Definition of class Joint
    """

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = ArchPointInteractor(self.arch_pnt_result,
                                                            ArchitectureElementsQueryUtil.create_arch_general_opening_elements_query(),
                                                            "Set properties or click a component line",
                                                            self.draw_placement_preview)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def create_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = cast(BuildingElement, self.build_ele)

        #----------------- create the properties

        joint_prop = AllplanArchEle.JointProperties()
        joint_prop.Width = build_ele.Width.value
        joint_prop.Depth = build_ele.Depth.value

        #----------------- create the joint

        self.opening_end_pnt = OpeningPointsUtil.create_opening_end_point_for_axis_element(self.opening_start_pnt.To2D,
                                                                                           build_ele.Width.value,
                                                                                           self.placement_ele_axis,
                                                                                           self.placement_ele_geo,
                                                                                           self.placement_line).To3D

        joint_ele = AllplanArchEle.JointElement(joint_prop, self.placement_ele,
                                                self.opening_start_pnt.To2D,
                                                self.opening_end_pnt.To2D,
                                                build_ele.InputMode.value == build_ele.ELEMENT_SELECT)

        model_ele_list = ModelEleList()
        model_ele_list.append(joint_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        build_ele = self.build_ele

        handle_list : list[HandleProperties] = []

        bottom_pnt = AllplanGeo.Point3D()

        depth = build_ele.Depth.value or build_ele.ElementThickness.value

        OpeningHandlesUtil.create_opening_depth_handle(self.opening_start_pnt.To2D, self.placement_ele_axis,
                                                       self.placement_ele_geo, self.placement_line,
                                                       self.placement_arc, bottom_pnt, depth, handle_list)

        OpeningHandlesUtil.create_opening_handles(self.opening_start_pnt.To2D, self.opening_end_pnt.To2D,
                                                  self.offset_start_pnt, self.offset_end_pnt,
                                                  self.placement_ele_axis, self.placement_arc, self.input_field_above, bottom_pnt,
                                                  handle_list)

        return handle_list
