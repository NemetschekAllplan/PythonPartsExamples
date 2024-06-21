""" Example script for IFW export and import
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from BuildingElementTupleUtil import BuildingElementTupleUtil

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IfcExportImportBuildingElement import IfcExportImportBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load IfcExportImport.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Create the library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\ExportImport\IfcExportImport.png"))


def create_element(build_ele: BuildingElement,
                   _doc     : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result
    """

    #--------------------- create the file lists

    if not build_ele.FileList.value:
        if (file_list_tuple := BuildingElementTupleUtil.create_namedtuple_from_definition(build_ele.FileList)) is not None:
            build_ele.FileList.value = [  \
                file_list_tuple(AllplanEleAdapter.DocumentNameService.GetDocumentNameByFileNumber(index, True, False, "-"), True) \
                for index, _ in AllplanBaseEle.DrawingFileService().GetFileState()]


    #--------------------- create the import file selection

    if not build_ele.ImportFileSelection.value:
        if (file_list_tuple := BuildingElementTupleUtil.create_namedtuple_from_definition(build_ele.ImportFileSelection)) is not None:
            build_ele.ImportFileSelection.value = [  \
                file_list_tuple(AllplanEleAdapter.DocumentNameService.GetDocumentNameByFileNumber(number, True, False, "-"), number) \
                for index, (number, _) in enumerate(AllplanBaseEle.DrawingFileService().GetFileState())]

        build_ele.ImportFileNumber.value = AllplanBaseEle.DrawingFileService.GetActiveFileNumber()

    return CreateElementResult()


def on_control_event(build_ele: BuildingElement,
                     event_id : int,
                     doc      : AllplanEleAdapter.DocumentAdapter):
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        event_id:  event id of the clicked button control
        doc:       document of the Allplan drawing files
    """

    if event_id == build_ele.EXPORT_IFC:
        export_ifc(build_ele, doc)

    if event_id == build_ele.IMPORT_IFC:
        import_ifc(build_ele, doc)


def export_ifc(build_ele: BuildingElement,
               doc      : AllplanEleAdapter.DocumentAdapter):
    """ export IFC

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files
    """

    #--------------------- set the files indexes to export

    export_import_service = AllplanBaseEle.ExportImportService()

    if build_ele.FilesToExport.value == build_ele.ACTIVE_FILE:
        export_file_numbers = [AllplanBaseEle.DrawingFileService.GetActiveFileNumber()]

    elif build_ele.FilesToExport.value == build_ele.ALL_FILES:
        export_file_numbers = [file_index for file_index, _ in AllplanBaseEle.DrawingFileService().GetFileState()]

    else:
        export_file_numbers = [int(item.FileName.split("-", 1)[0]) for item in build_ele.FileList.value if item.ExportState]

    export_import_service.ExportIFC(doc, export_file_numbers,
                                    AllplanBaseEle.IFC_Version.names["Ifc_4"],
                                    build_ele.IfcExportPath.value,
                                    build_ele.IfcExportTheme.value)


def import_ifc(build_ele: BuildingElement,
               doc      : AllplanEleAdapter.DocumentAdapter):
    """ import IFC

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files
    """

    export_import_service = AllplanBaseEle.ExportImportService()

    imported_elements = export_import_service.ImportIFC(doc,
                                                        build_ele.ImportFileNumber.value,
                                                        build_ele.IfcImportPath.value)

    print("\n" * 3)
    print("======================================================================================")
    print ("IFC imported elements: \n")

    for imported_element in imported_elements:
        print("----------", imported_element.GetDisplayName(), "----------")
        print("Element adapter type:", imported_element.GetElementAdapterType().GetTypeName())
        print("Model element UUID:  ", imported_element.GetModelElementUUID())
        print("Is 3D element:       ", imported_element.Is3DElement())
        print("-----------------------------------\n")
