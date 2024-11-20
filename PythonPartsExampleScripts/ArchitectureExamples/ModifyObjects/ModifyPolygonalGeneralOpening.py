""" Example Script for the general opening
"""

# pylint: disable=attribute-defined-outside-init

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData, OnCancelFunctionResult
from BuildingElementListService import BuildingElementListService
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from ParameterUtils.OpeningSillPropertiesParameterUtil import OpeningSillPropertiesParameterUtil

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator import HandleCreator
from Utils.HideElementsService import HideElementsService
from Utils.Architecture.OpeningModificationUtil import OpeningModificationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyPolygonalGeneralOpeningBuildingElement \
        import ModifyPolygonalGeneralOpeningBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ModifyPolygonalGeneralOpening.py')

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


def create_preview(build_ele: BuildingElement,
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(
                               fr"{build_ele.pyp_file_path}\ModifyPolygonalGeneralOpening.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifyPolygonalGeneralOpening(build_ele, script_object_data)


class ModifyPolygonalGeneralOpening(BaseScriptObject):
    """ Definition of class ModifyPolygonalGeneralOpening
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele           = build_ele
        self.general_opening_ele = AllplanArchEle.GeneralOpeningElement()
        self.placement_ele       = AllplanEleAdapter.BaseElementAdapter()
        self.opening_ele         = AllplanEleAdapter.BaseElementAdapter()
        self.opening_polygon     = AllplanGeo.Polygon2D()
        self.hide_ele            = HideElementsService()
        self.opening_sel_res     = SingleElementSelectResult()


    def start_input(self):
        """ start the input
        """

        self.script_object_interactor = SingleElementSelectInteractor(self.opening_sel_res,
                                                                      [AllplanEleAdapter.PolygonalNicheTier_TypeUUID,
                                                                       AllplanEleAdapter.PolygonalRecessTier_TypeUUID],
                                                                      "Select the niche/recess")

        self.build_ele.InputMode.value = self.build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None


        #----------------- get the data of the opening

        self.opening_ele = OpeningModificationUtil.get_opening_element(self.opening_sel_res.sel_element)

        self.placement_ele = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(self.opening_ele)

        self.general_opening_ele = cast(AllplanArchEle.GeneralOpeningElement, AllplanBaseEle.GetElement(self.opening_sel_res.sel_element))

        opening_prop = self.general_opening_ele.Properties

        build_ele.NicheType.value = "Niche" if opening_prop.OpeningType == AllplanArchEle.OpeningType.eNiche else "Recess"

        build_ele.IsVisibleInViewSection3D.value    = opening_prop.VisibleInViewSection3D
        build_ele.HasIndependent2DInteraction.value = opening_prop.Independent2DInteraction
        build_ele.HeightSettings.value              = opening_prop.PlaneReferences

        self.opening_polygon = self.general_opening_ele.GroundPlanePolygon

        OpeningSillPropertiesParameterUtil.set_parameter_values(build_ele, opening_prop.GetSillProperties(), "")

        self.hide_ele.hide_opening_parent_element(self.placement_ele, self.build_ele.HasIndependent2DInteraction.value)
        self.hide_ele.hide_element(self.opening_ele)

        build_ele.InputMode.value = build_ele.OPENING_INPUT


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        handle_placement_geo = self.hide_ele.get_hidden_geo_elements
        handle_placement_geo.append(self.opening_polygon)

        return CreateElementResult(self.modify_opening_element(), self.create_handles(),
                                   multi_placement      = True,
                                   placement_point      = AllplanGeo.Point3D(),
                                   handle_placement_geo = handle_placement_geo)


    def modify_opening_element(self) -> ModelEleList:
        """ create the opening element


        Returns:
            list with the elements
        """

        build_ele = self.build_ele


        #----------------- create the properties

        opening_prop = AllplanArchEle.GeneralOpeningProperties(
                            AllplanArchEle.OpeningType.eNiche if build_ele.NicheType.value == "Niche" else \
                            AllplanArchEle.OpeningType.eRecess)

        opening_prop.VisibleInViewSection3D   = build_ele.IsVisibleInViewSection3D.value
        opening_prop.Independent2DInteraction = build_ele.HasIndependent2DInteraction.value
        opening_prop.PlaneReferences          = build_ele.HeightSettings.value

        OpeningSillPropertiesParameterUtil.create_sill_properties(build_ele, "", opening_prop.GetSillProperties())


        #----------------- create the opening

        self.general_opening_ele.Properties         = opening_prop
        self.general_opening_ele.GroundPlanePolygon = self.opening_polygon

        model_ele_list = ModelEleList()

        model_ele_list.append(self.general_opening_ele)

        return model_ele_list


    def create_handles(self) -> list[HandleProperties]:
        """ create the handles

        Returns:
            created handles
        """

        handle_list = list[HandleProperties]()

        HandleCreator.point_list_2d(handle_list, "OpeningPolygon", self.opening_polygon.Points[:-1])

        return handle_list


    def move_handle(self,
                    handle_prop: HandleProperties,
                    input_pnt  : AllplanGeo.Point3D) -> CreateElementResult:
        """ Modify the element geometry by handles

        Args:
            handle_prop: handle properties
            input_pnt:   input point

        Returns:
            created element result
        """

        index = cast(int, handle_prop.parameter_data[0].list_index)

        self.opening_polygon[index] = AllplanGeo.Point2D(input_pnt)

        if index == 0:
            self.opening_polygon[ self.opening_polygon.Count() - 1] = AllplanGeo.Point2D(input_pnt)

        elif index == self.opening_polygon.Count() - 1:
            self.opening_polygon[0] = AllplanGeo.Point2D(input_pnt)

        return self.execute()


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        build_ele = self.build_ele

        BuildingElementListService.write_to_default_favorite_file([build_ele])

        if build_ele.InputMode.value == build_ele.ELEMENT_SELECT:
            return OnCancelFunctionResult.CANCEL_INPUT

        self.hide_ele.show_elements()

        AllplanIFW.HandleService().RemoveHandles()
        AllplanIFW.BuildingElementInputControls().CloseControls()

        AllplanBaseEle.ModifyElements(self.document, self.modify_opening_element())

        AllplanIFW.HandleService().RemoveHandles()

        return OnCancelFunctionResult.RESTART
