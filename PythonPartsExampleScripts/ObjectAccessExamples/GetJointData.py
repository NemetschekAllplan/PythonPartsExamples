""" Example Script for get joint data
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.ShapeGeometryPropertiesParameterUtil import ShapeGeometryPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HideElementsService import HideElementsService

from ArchitectureExamples.ModifyObjects.ModifyOpeningBase import ModifyOpeningBase

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GetJointDataBuildingElement import GetJointDataBuildingElement
else:
    GetJointDataBuildingElement = BuildingElement

print('Load GetJointData.py')

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

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\ObjectAccessExamples\GetJointData.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return GetJointData(build_ele, script_object_data)


class GetJointData(ModifyOpeningBase):
    """ Definition of class GetJointData
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(build_ele, script_object_data)

        self.joint_sel_result = SingleElementSelectResult()
        #self.polygon_result    = PolygonInteractorResult()

        self.build_ele = cast(GetJointDataBuildingElement, build_ele)

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

        self.placement_pnt        = AllplanGeo.Point3D()
        self.shape_polygon        = AllplanGeo.Polygon2D()
        self.shape_geo_param_util = ShapeGeometryPropertiesParameterUtil(build_ele, "")
        self.slab_plane_ref       = AllplanArchEle.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())
        self.hide_ele_service     = HideElementsService()
        self.joint_ele            = AllplanArchEle.JointElement()

    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.joint_sel_result,
                                                                      [AllplanEleAdapter.Joint_TypeUUID,
                                                                       AllplanEleAdapter.JointTier_TypeUUID],
                                                                      "Select the joint")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT

    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        last_input_mode = build_ele.InputMode.value

        build_ele.InputMode.value = build_ele.JOINT_INPUT

        self.script_object_interactor = None

        if last_input_mode == build_ele.JOINT_PLACEMENT:
            return

        #----------------- get the joint element
        self.joint_ele = cast(AllplanArchEle.JointElement, AllplanBaseEle.GetElement(self.joint_sel_result.sel_element))

        #----------------- get the properties

        joint_properties = self.joint_ele.Properties

        build_ele.Width.value                 = joint_properties.Width
        build_ele.Depth.value                 = joint_properties.Depth
        build_ele.StartPoint.value            = self.joint_ele.GetStartPoint()
        build_ele.EndPoint.value              = self.joint_ele.GetEndPoint()

        #----------------- start the joint modification

        self.placement_ele = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(self.joint_sel_result.sel_element)

    def modify_opening_element(self) -> ModelEleList:

        """ modify the joint element


        Returns:
            list with the elements
        """
        return []

    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        return[]