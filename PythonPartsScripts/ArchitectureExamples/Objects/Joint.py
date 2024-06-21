""" Example Script for the joint
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator

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


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return Joint(build_ele, coord_input) # type: ignore


class Joint(OpeningBase):
    """ Definition of class Joint
    """

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

        self.create_opening_points()

        joint_ele = AllplanArchEle.JointElement(joint_prop, self.general_ele,
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

        opening_start_pnt = self.opening_start_pnt
        opening_end_pnt   = self.opening_end_pnt

        handle_list : list[HandleProperties] = []

        #----------------- width input controls

        HandleCreator.point_distance(handle_list, "Width", opening_end_pnt, opening_start_pnt,
                                     show_handles = False, input_field_above = False)

        x_start = AllplanGeo.TransformCoord.PointLocal(self.placement_ele, opening_start_pnt).X

        depth = build_ele.Depth.value or build_ele.ElementThickness.value

        #----------------- depth handle for the circular axis

        if self.general_ele == AllplanEleAdapter.CircularWall_TypeUUID:
            depth_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele, AllplanGeo.Point2D(x_start, depth))

            depth_ref_pnt = AllplanGeo.PerpendicularCalculus.Calculate(self.placement_ele, opening_start_pnt)[1]

            HandleCreator.point_distance(handle_list, "Depth", depth_pnt, depth_ref_pnt)

        #----------------- depth handle for the linear axis

        else:
            depth_pnt = AllplanGeo.TransformCoord.PointGlobal(self.placement_ele, AllplanGeo.Point2D(x_start, depth))

            HandleCreator.point_distance(handle_list, "Depth", depth_pnt, opening_start_pnt)

        self.create_opening_handles(handle_list)

        return handle_list
