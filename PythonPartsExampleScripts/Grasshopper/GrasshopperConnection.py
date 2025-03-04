""" implementation of the Grasshopper connection
"""
# pylint: disable=import-error
# pylint: disable=broad-exception-caught
# pylint: disable=unused-import
from __future__ import annotations
import os
import signal
from pathlib import Path
from typing import TYPE_CHECKING

from threading import Thread

from System.Windows.Threading import DispatcherTimer        # type: ignore
from System import TimeSpan                                 # type: ignore

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from Utils import LibraryBitmapPreview

from .GrasshopperPythonHostHandler import GrasshopperPythonHostHandler
from .SocketConnection import run_server, init_app

print("Load GrasshopperConnection.py")

if TYPE_CHECKING:
    from .__BuildingElementStubFiles.GrasshopperConnectionBuildingElement import GrasshopperConnectionBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


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

    script_path = Path(_build_ele.pyp_file_path) / Path(_build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")
    preview = LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path))
    return CreateElementResult(preview)


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return GrasshopperConnection(build_ele, script_object_data)


class GrasshopperConnection(BaseScriptObject):
    """ Definition of class GrasshopperConnection
    """

    def __init__(self,
                 _build_ele        : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ initialize

        Args:
            _build_ele:         building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        #----------------- start http server

        self.app = init_app(GrasshopperPythonHostHandler(self.coord_input))

        self.thread = Thread(target = run_server, args=(self.app,))

        self.thread.daemon = True

        self.thread.start()

        print("Python Host is started")


        #----------------- this timer pushes python thread to process requests if user minimized main window

        self.timer           = DispatcherTimer()
        self.timer.Interval  = TimeSpan.FromMilliseconds(50)
        self.timer.Tick     += self.push_python_thread

        self.timer.Start()


    @staticmethod
    def push_python_thread(_sender: type,
                           _args  : type):
        """ push python thread

        Args:
            _sender: sender
            _args:   arguments
        """


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        return CreateElementResult(self.app.connection_handler.model_ele_list, placement_point = AllplanGeo.Point2D())


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True/False/None for success.
        """

        self.timer.Stop()
        os.kill(os.getpid(), signal.SIGINT)
        print("Python Host is stopped")

        return OnCancelFunctionResult.CANCEL_INPUT
