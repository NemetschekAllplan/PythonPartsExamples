""" Example script for IFW export and import
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.DwgExportBuildingElement import DwgExportBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load dwgExport.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : float) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element
        _version  : the current Allplan version

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

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\ExportImport\DwgExport.png"))


def create_element(build_ele: BuildingElement,
                   _doc: AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        _doc     : document of the Allplan drawing files

    Returns:
        created element result
    """
    build_ele.DwgExportConfigFileName.value = AllplanSettings.AllplanPaths.GetUsrPath() + \
        "\\nx_AllFT_AutoCad.cfg"
    build_ele.DwgImportConfigFileName.value = AllplanSettings.AllplanPaths.GetUsrPath() + \
        "\\nx_AutoCad_AllFT.cfg"
    return CreateElementResult()


def on_control_event(build_ele: BuildingElement,
                     event_id: int,
                     doc: AllplanEleAdapter.DocumentAdapter):
    """ On control event

    Args:
        build_ele: building element with the parameter properties
        event_id:  event id of the clicked button control
        doc:       document of the Allplan drawing files
    """

    export_import_service = AllplanBaseEle.ExportImportService()
    if event_id == build_ele.EXPORT_DWG:
        export_dwg(build_ele, doc, export_import_service)
    elif event_id == build_ele.IMPORT_DWG:
        import_dwg(build_ele, doc, export_import_service)


def export_dwg(build_ele: BuildingElement,
               doc: AllplanEleAdapter.DocumentAdapter,
               export_import_service: AllplanBaseEle.ExportImportService):
    """ export DWG

    Args:
        build_ele            : building element with the parameter properties
        doc                  : document of the Allplan drawing files
        export_import_service: An instance of ExportImort Service
    """

    export_import_service.ExportDWG(
        doc, build_ele.DwgDrawingFileName.value, build_ele.DwgExportConfigFileName.value, 0)


def import_dwg(build_ele: BuildingElement,
               doc: AllplanEleAdapter.DocumentAdapter,
               export_import_service: AllplanBaseEle.ExportImportService):
    """Import DWG

    Args:
        build_ele            : Building element with parameter properties
        doc                  : documetn of the Allplan drawing files
        export_import_service: An instance of ExportImort Service
    """

    export_import_service.ImportDWG(doc, build_ele.DwgDrawingFileName.value, build_ele.DwgImportConfigFileName.value, AllplanGeo.Point3D(
        build_ele.DrawingXOffset.value, build_ele.DrawingYOffset.value, build_ele.DrawingZOffset.value))
