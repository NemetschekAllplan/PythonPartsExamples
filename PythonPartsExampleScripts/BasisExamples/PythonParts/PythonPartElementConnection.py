""" implementation of the example for the PythonPart - element connection"""

from typing import TYPE_CHECKING, cast

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil
from PythonPartTransaction import ConnectToElements

from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult

from TypeCollections.ModelEleList import ModelEleList
from TypeCollections.GeometryTyping import GeometryTyping

from Utils import LibraryBitmapPreview
from Utils.Geometry.ExtrudeByVectorUtil import ExtrudeByVectorUtil
from Utils.ElementFilter.CurvedGeometryElementFilter import CurvedGeometryElementFilter

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartElementConnectionBuildingElement import PythonPartElementConnectionBuildingElement
else:
    PythonPartElementConnectionBuildingElement = BuildingElement

print('Load PythonPartElementConnection.py')

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
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\BasisExamples\PythonParts\PythonPartElementConnection.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PythonPartElementConnection(build_ele, script_object_data)


class PythonPartElementConnection(BaseScriptObject):
    """ Definition of class PythonPartElementConnection
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

        build_ele = cast(PythonPartElementConnectionBuildingElement, build_ele)

        self.build_ele = build_ele

        self.sel_result = SingleElementSelectResult()


        #----------------- check for modification

        if not self.is_modification_mode:
            return

        python_part = self.modification_ele_list.get_base_element_adapter(self.document)

        geometry_uuid = AllplanEleAdapter.GUID.FromString(build_ele.GeometryElementUUID.value)

        model_ele = AllplanEleAdapter.BaseElementAdapter.FromGUID(geometry_uuid,
                                                                  self.coord_input.GetInputViewDocument())

        if str(python_part.GetModelElementUUID()) != build_ele.PythonPartUUID.value:
            AllplanUtil.ShowMessageBox("You are modifying a copied PythonPart!\n\n"
                                        "The original polygon is used",
                                        AllplanUtil.MB_OK)

            trans_mat = build_ele.get_insert_matrix().ReduceZDimension() \
                        if GeometryTyping.is_curve_2d(build_ele.GeometryElement.value) else build_ele.get_insert_matrix()

            build_ele.GeometryElement.value     = AllplanGeo.Transform(build_ele.GeometryElement.value, trans_mat)
            build_ele.GeometryElementUUID.value = str(AllplanEleAdapter.GUID())

        else:
            geo_ele = model_ele.GetGeometry()

            if isinstance(geo_ele, AllplanGeo.Polyline2D):
                geo_ele = AllplanGeo.Polygon2D(geo_ele.Points)

            build_ele.GeometryElement.value = geo_ele

        build_ele.InputMode.value = build_ele.PARAMETER_MODIFICATION


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        if self.is_only_update or self.is_modification_mode:
            return

        self.script_object_interactor = SingleElementSelectInteractor(self.sel_result,
                                                                      CurvedGeometryElementFilter(True, True),
                                                                      "Select the curve element")

        build_ele.InputMode.value = build_ele.ELEMENT_SELECT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        build_ele.InputMode.value = self.build_ele.PARAMETER_MODIFICATION

        build_ele.GeometryElement.value     = self.sel_result.sel_element.GetGeometry()
        build_ele.GeometryElementUUID.value = str(self.coord_input.GetSelectedElement().GetModelElementUUID())


    def execute(self) -> CreateElementResult:
        """  execute the script

        Returns:
            created result
        """

        build_ele = self.build_ele

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.extrude_geometry())


        #----------------- create the handle

        start_pnt = AllplanGeo.Point3D(self.build_ele.GeometryElement.value.StartPoint)

        handle_list = [HandleProperties("ExtrusionVector", start_pnt + build_ele.ExtrusionVector.value, start_pnt,
                                        [HandleParameterData("ExtrusionVector.X", HandleParameterType.X_DISTANCE, True),
                                         HandleParameterData("ExtrusionVector.Y", HandleParameterType.Y_DISTANCE, True),
                                         HandleParameterData("ExtrusionVector.Z", HandleParameterType.Z_DISTANCE, True)],
                                        HandleDirection.XYZ_DIR, False)]

        return CreateElementResult(pyp_util.create_pythonpart(build_ele), handle_list,
                                   placement_point = AllplanGeo.Point3D(),
                                   multi_placement = True,
                                   connect_to_ele = ConnectToElements([build_ele.GeometryElementUUID.value]),
                                   uuid_parameter_name = "PythonPartUUID")


    def extrude_geometry(self) -> ModelEleList:
        """ extrude the geometry

        Returns:
            created model elements
        """

        model_ele_list = ModelEleList()

        if (extruded_ele := ExtrudeByVectorUtil.extrude([self.build_ele.GeometryElement.value],
                                                        self.build_ele.ExtrusionVector.value, False, True)) is not None:
            model_ele_list.append_geometry_3d(extruded_ele)

        return model_ele_list
