""" Script for ReinfRearrange
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf

from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ReinfRearrangeBuildingElement \
        import ReinfRearrangeBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ReinfRearrange.py')


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
                               r"Examples\PythonParts\ReinforcementExamples\Utils\ReinfRearrange.png"))


def create_element(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult()


def on_control_event(build_ele: BuildingElement,
                     _event_id: int,
                     doc      : AllplanEleAdapter.DocumentAdapter):
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        _event_id: event id of the clicked button control
        doc:       document of the Allplan drawing files
    """

    AllplanReinf.ReinforcementUtil.Rearrange(doc,
                                             build_ele.FromBarPosition.value, build_ele.FromMeshPosition.value,
                                             build_ele.ToBarPosition.value, build_ele.ToMeshPosition.value,
                                             build_ele.AfterBarPosition.value, build_ele.AfterMeshPosition.value,
                                             build_ele.Tolerance.value, build_ele.RearrangedLock.value,
                                             build_ele.IdenticalShapes.value,
                                             build_ele.IdenticalPrefix.value)
