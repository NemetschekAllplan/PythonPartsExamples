""" Script for ModifyLine2D
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties

from TypeCollections import ModelEleList

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from Utils import LibraryBitmapPreview
from Utils.HandleCreator.CurveHandlesCreator import CurveHandlesCreator

from Utils.HideElementsService import HideElementsService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyLine2DBuildingElement import ModifyLine2DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ModifyLine2D.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ModifyLine2D(build_ele, script_object_data)


class ModifyLine2D(BaseScriptObject):
    """ Definition of class ModifyLine2D
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele             = build_ele
        self.sel_interactor_result = SingleElementSelectResult()
        self.model_ele_list        = ModelEleList()
        self.hide_ele_service      = HideElementsService()
        self.line_element          = AllplanBasisEle.ModelElement2D()

    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        self.hide_ele_service.show_elements()

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_interactor_result,
                                                                      [AllplanEleAdapter.Line2D_TypeUUID], "Select line")

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        build_ele.InputMode.value = build_ele.ELEMENT_MODIFY

        self.script_object_interactor = None

        self.hide_ele_service.hide_element(self.sel_interactor_result.sel_element)


        #----------------- get the line element

        self.line_element = cast(AllplanBasisEle.ModelElement2D, AllplanBaseEle.GetElement(self.sel_interactor_result.sel_element))

        geo_ele = cast(AllplanGeo.Line2D, self.line_element.GetGeometryObject())

        build_ele.CommonProp.value = self.line_element.GetCommonProperties()
        build_ele.Line.value       = geo_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList()

        self.line_element.SetCommonProperties(build_ele.CommonProp.value)
        self.line_element.SetGeometryObject(build_ele.Line.value)

        model_ele_list.append(self.line_element)


        #----------------- create the handles

        handle_list = list[HandleProperties]()

        CurveHandlesCreator.line(handle_list, "Line", build_ele.Line.value, owner_element = self.line_element.GetBaseElementAdapter())

        return CreateElementResult(model_ele_list, handle_list, multi_placement = True)
