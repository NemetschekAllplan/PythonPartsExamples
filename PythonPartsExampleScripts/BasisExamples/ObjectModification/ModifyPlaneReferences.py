""" Example Script for modification of reference planes
"""

from __future__ import annotations
from typing import TYPE_CHECKING, cast

from pathlib import Path

import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.MultiElementSelectInteractor import MultiElementSelectInteractor, MultiElementSelectInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ModifyPlaneReferencesBuildingElement import \
        ModifyPlaneReferencesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load ModifyPlaneReferences.py')

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


def create_preview(build_ele : BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele:  building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PlaneReferencesModify(build_ele, script_object_data)


class PlaneReferencesModify(BaseScriptObject):
    """ Script for modifying the plane references of architectural components,
    such as walls, beams, columns and slabs.
    """

    elements_whitelist = [AllplanEleAdapter.WallTier_TypeUUID,
                          AllplanEleAdapter.Column_TypeUUID,
                          AllplanEleAdapter.Beam_TypeUUID,
                          AllplanEleAdapter.Slab_TypeUUID]
    """Types of architectural components accepted for modification"""

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele          = build_ele
        self.placement_pnt      = AllplanGeo.Point2D()
        self.selection_results  = MultiElementSelectInteractorResult()


    def start_input(self):
        """ start the input
        """
        prompt = "Set up the plane references in the property palette, then apply them on an architecture component"

        self.script_object_interactor = MultiElementSelectInteractor(self.selection_results,
                                                                     self.elements_whitelist,
                                                                     prompt_msg = prompt)

    def start_next_input(self):
        """ Start the next input

        Get the selection results and perform modification of plane references.
        Once done, restart selection.
        """

        # group the wall tiers into a dictionary and modify them
        if (grouped_wall_tiers := self.group_wall_tiers(self.selection_results.sel_elements)):
            self.modify_wall_plane_references(grouped_wall_tiers)

        # modify elements other than walls
        self.modify_plane_references(self.selection_results.sel_elements)

        self.start_input()

    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """
        return CreateElementResult() # nothing to create, the script just modifies

    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event.

        This event is triggered by hitting ESC during the runtime of a PythonPart.
        In this case, the selection is terminated as well as the PythonPart itself

        Returns:
            Always cancel the input and terminate PythonPart
        """

        self.script_object_interactor = None    # terminate the selection interactor
        return OnCancelFunctionResult.CANCEL_INPUT


    def modify_plane_references(self,
                                element_adapter_list: AllplanEleAdapter.BaseElementAdapterList):
        """ Modify the plane references of architectural components: columns, beams and slabs

        Args:
            element_adapter_list:   list of element adapters representing components to modify
        """

        valid_element_types = self.elements_whitelist.copy()
        valid_element_types.remove(AllplanEleAdapter.WallTier_TypeUUID)     # this method should not modify the wall tiers!

        adapters_without_wall_tiers = AllplanEleAdapter.BaseElementAdapterList(
            [element for element in element_adapter_list if element.GetElementAdapterType().GetGuid() in valid_element_types])

        if not (arch_elements := AllplanBaseEle.GetElements(adapters_without_wall_tiers)):
            return

        for arch_element in arch_elements:
            arch_properties = cast(AllplanArchElements.ArchBaseProperties, arch_element.Properties)     # get the properties
            arch_properties.PlaneReferences = self.build_ele.PlaneReferences.value                      # set new plane references
            arch_element.Properties         = arch_properties                                           # apply references to the element

        AllplanBaseEle.ModifyElements(self.document, arch_elements)                                     # write into database

    def modify_wall_plane_references(self,
                                     grouped_tiers: dict[AllplanEleAdapter.GUID, list[AllplanEleAdapter.BaseElementAdapter]]):
        """ Modify the plane references of wall tiers

        Because each tier has its own plane references, but modification must be done
        on the wall as a whole, tiers must be grouped into a dictionary.

        Args:
            grouped_tiers:  Dictionary containing lists of tiers to modify.
                            Key of each list is a GUID of the wall element it belongs to
        """
        walls_to_modify: list[AllplanArchElements.WallElement] = []

        for wall_uuid, tier_adapters in grouped_tiers.items():
            wall_adapter = AllplanEleAdapter.BaseElementAdapter.FromGUID(wall_uuid, self.document)                  # get wall adapter
            wall_element = AllplanBaseEle.GetElements(AllplanEleAdapter.BaseElementAdapterList([wall_adapter]))[0]  # get wall element
            wall_properties = wall_element.Properties                                                               # get wall properties

            for tier_adapter in tier_adapters:
                tier_number = AllplanEleAdapter.BaseElementAdapterChildElementsService.GetTierNumber(tier_adapter)
                tier_properties = wall_properties.GetWallTierProperties(tier_number)
                tier_properties.PlaneReferences = self.build_ele.PlaneReferences.value      # set plane references to each wall tier

            wall_element.SetProperties(wall_properties)                                     # set wall properties to whole wall
            walls_to_modify.append(wall_element)

        AllplanBaseEle.ModifyElements(self.document, walls_to_modify)                       # write into database


    @staticmethod
    def group_wall_tiers(wall_tier_adapters: AllplanEleAdapter.BaseElementAdapterList) -> dict[AllplanEleAdapter.GUID,
                                                                                               list[AllplanEleAdapter.BaseElementAdapter]]:
        """Group wall tiers into a dictionary

        Args:
            wall_tier_adapters: unsorted list of element adapters representing wall tiers

        Returns:
            Dictionary with wall tiers. Keys are the UUID of the whole wall. Items are lists with
                wall tiers (as element adapter), that belongs to the wall with UUID in the key.
        """
        wall_tiers_dict: dict[AllplanEleAdapter.GUID, list[AllplanEleAdapter.BaseElementAdapter]] = {}

        for wall_tier in wall_tier_adapters:
            if wall_tier.GetElementAdapterType().GetGuid() != AllplanEleAdapter.WallTier_TypeUUID:
                continue

            # get the wall, to which the tier belongs
            wall = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(wall_tier)

            # if the wall UUID is exists in the dict, append the tier to this item
            if (wall_uuid := wall.GetElementUUID()) in wall_tiers_dict:
                wall_tiers_dict[wall_uuid].append(wall_tier)

            # else, add a new UUID to the dictionary keys and put the tier in a list
            else:
                wall_tiers_dict[wall_uuid] = [wall_tier]

        return wall_tiers_dict
