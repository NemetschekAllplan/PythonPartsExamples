"""Example script of creating a simple cuboid as brep or as polyhedron
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
from ControlPropertiesUtil import ControlPropertiesUtil
from CreateElementResult import CreateElementResult
from FileNameService import FileNameService

if TYPE_CHECKING:
    from __BuildingElementStubFiles.LibraryDialogsBuildingElement import LibraryDialogsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   str) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True

def modify_control_properties(build_ele:        BuildingElement,
                              _ctrl_prop_util:  ControlPropertiesUtil,
                              value_name:       str,
                              _event_id:        int,
                              _doc:             AllplanElementAdapter.DocumentAdapter) -> bool:
    """Called after each change within the property palette

    Args:
        build_ele:      building element
        _ctrl_prop_util: control properties utility
        value_name:     name(s) of the modified value (multiple names are separated by ,)
        _event_id:       event ID
        _doc:            document

    Returns:
        True if an update of the property palette is necessary, False otherwise
    """
    if value_name == "LibraryElementType" and build_ele.LibraryElementType.value == "OpeningSymbol":
        msg =  "Please note, that placing SmartParts is not implemented yet. Nothing will happen, when you "
        msg += "select a SmartPart from the library now. This feature will be available soon."
        AllplanUtil.ShowMessageBox(msg, AllplanUtil.MB_OK)

    return True


def create_element(build_ele:   BuildingElement,
                   _doc:        AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of the cuboid

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    # get the appropriate element from library
    match build_ele.LibraryElementType.value:
        case "Symbol":
            element_to_create = get_symbol_from_library(build_ele.SymbolPath.value)

        case "SmartSymbol":
            element_to_create = get_smart_symbol_from_library(build_ele.SmartSymbolPath.value)

        case "OpeningSymbol":
            element_to_create = get_opening_symbol_from_library(build_ele.OpeningSymbolPath.value)

        case "Fixture":
            element_to_create = get_fixture_from_library(build_ele.FixturePath.value)

        case _ :
            element_to_create = None

    return CreateElementResult([element_to_create],
                               multi_placement = True)

def get_symbol_from_library(symbol_path: str) -> AllplanBasisElements.LibraryElement:
    """Gets the library element representing a symbol

    Args:
        symbol_path:   full path to the symbol file (.sym)

    Returns:
        Library element representing the symbol.
    """

    lib_ele_prop = AllplanBasisElements.LibraryElementProperties(symbol_path,
                                                                 AllplanBasisElements.LibraryElementType.eSymbol,
                                                                 AllplanGeo.Matrix3D())

    return AllplanBasisElements.LibraryElement(lib_ele_prop)

def get_smart_symbol_from_library(smart_symbol_path: str) -> AllplanBasisElements.LibraryElement:
    """Gets the library element representing a smart symbol (macro)

    Args:
        smart_symbol_path:   full path to the smart symbol file (.nmk)

    Returns:
        Library element representing the smart symbol.
    """
    smart_symbol_path = FileNameService.get_global_standard_path(smart_symbol_path)

    lib_ele_prop = AllplanBasisElements.LibraryElementProperties(smart_symbol_path,
                                                                 AllplanBasisElements.LibraryElementType.eSmartSymbol,
                                                                 AllplanGeo.Matrix3D())

    return AllplanBasisElements.LibraryElement(lib_ele_prop)

def get_opening_symbol_from_library(opening_symbol_path: str) -> AllplanBasisElements.LibraryElement:
    """Gets the library element representing a smart symbol or a SmartPart

    Args:
        opening_symbol_path:   full path to the smart symbol (.nmk) or SmartPart (.smt) file

    Returns:
        Library element representing the smart symbol or SmartPart.
    """

    opening_symbol_path = FileNameService.get_global_standard_path(opening_symbol_path)

    if opening_symbol_path.lower().endswith(".smt"):
        # placing SmartPart is not implemented yet
        lib_ele_prop = AllplanBasisElements.LibraryElementProperties()

    elif opening_symbol_path.lower().endswith(".nmk"):
        lib_ele_prop = AllplanBasisElements.LibraryElementProperties(opening_symbol_path,
                                                                     AllplanBasisElements.LibraryElementType.eSmartSymbol,
                                                                     AllplanGeo.Matrix3D())
    else:
        lib_ele_prop = AllplanBasisElements.LibraryElementProperties()

    return AllplanBasisElements.LibraryElement(lib_ele_prop)

def get_fixture_from_library(fixture_path: str) -> AllplanBasisElements.LibraryElement:
    """Gets the library element representing a fixture

    Args:
        fixture_path:   full path to the fixture file (.lfx or .pxf)

    Returns:
        Library element representing the fixture. In case of line fixture: 1 meter long fixture
    """

    # replace the ETC/STD/USR keyword at the beginning of the path with the actual path
    fixture_path = FileNameService.get_global_standard_path(fixture_path)

    lib_ele_prop = AllplanBasisElements.LibraryElementProperties("", "", "", fixture_path,
                                                                 AllplanBasisElements.LibraryElementType.eFixtureSingleFile,
                                                                 AllplanGeo.Matrix3D())
    # apply a polyline in case of a line fixture
    if fixture_path.endswith('.lfx'):
        pnt_list = [AllplanGeo.Point3D(), AllplanGeo.Point3D(1000,0,0)]
        lib_ele_prop.SetPolyline(AllplanGeo.Polyline3D(pnt_list))

    return AllplanBasisElements.LibraryElement(lib_ele_prop)
