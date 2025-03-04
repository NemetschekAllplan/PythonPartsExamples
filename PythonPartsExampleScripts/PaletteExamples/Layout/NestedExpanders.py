""" Example script for Nested Expanders
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult
from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.NestedExpandersBuildingElement import NestedExpandersBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load NestedExpanders.py')


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
                               r"Examples\PythonParts\PaletteExamples\Layout\NestedExpanders.png"))

def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return NestedExpanders(build_ele, script_object_data)

class NestedExpanders(BaseScriptObject):
    """ Definition of class NestedExpanders
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialize the NestedExpanders script object

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.general_ele = AllplanEleAdapter.BaseElementAdapter()
        self.pnt_result  = PointInteractorResult()
        self.build_ele   = build_ele

    def start_input(self):
        """Starts the point input at the beginning of the script runtime"""

        self.script_object_interactor = PointInteractor(self.pnt_result, True, "Place the elements", self.draw_preview)


    def start_next_input(self):
        """Terminate the input after successful input of start point"""

        if self.pnt_result != PointInteractorResult():
            self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        return CreateElementResult(self.create_elements(), placement_point = AllplanGeometry.Point2D())

    def draw_preview(self):
        """ draw the preview
        """

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeometry.Matrix3D(),
                                          self.create_elements(), False, None)

    def create_elements(self) -> ModelEleList:
        """ create the elements

        Returns:
            list with the elements
        """

        model_ele_list = ModelEleList()

        #----------------- bottom left column

        column_bottomleft_prop = self.create_column_properties_base()

        column_bottomleft_prop.Width = self.build_ele.Width1_1.value
        column_bottomleft_prop.Depth = self.build_ele.Depth1_1.value
        column_bottomleft_prop.SurfaceElementProperties = self.build_ele.SurfacePropBottomLeft.value

        column_bottomleft_ele = AllplanArchElements.ColumnElement(column_bottomleft_prop, self.pnt_result.input_point)

        model_ele_list.append(column_bottomleft_ele)

        #----------------- bottom right column

        column_bottomright_prop = self.create_column_properties_base()

        column_bottomright_prop.Width = self.build_ele.Width1_2.value
        column_bottomright_prop.Depth = self.build_ele.Depth1_2.value
        column_bottomright_prop.SurfaceElementProperties = self.build_ele.SurfacePropBottomRight.value

        column_bottomright_input = AllplanGeometry.Point3D(self.pnt_result.input_point)
        column_bottomright_input.X = column_bottomright_input.X + self.build_ele.Width1_1.value + 1000

        column_bottomright_ele = AllplanArchElements.ColumnElement(column_bottomright_prop, column_bottomright_input)

        model_ele_list.append(column_bottomright_ele)

        #----------------- top left column

        top_columns_y_offset = self.build_ele.Depth1_1.value + 1000

        if self.build_ele.Depth1_2.value > self.build_ele.Depth1_1.value:
            top_columns_y_offset = self.build_ele.Depth1_2.value + 1000

        column_topleft_prop = self.create_column_properties_base()

        column_topleft_prop.Width = self.build_ele.Width2.value
        column_topleft_prop.Depth = self.build_ele.Depth2.value
        column_topleft_prop.SurfaceElementProperties = self.build_ele.SurfacePropTop.value

        column_topleft_input = AllplanGeometry.Point3D(self.pnt_result.input_point)
        column_topleft_input.Y = column_topleft_input.Y + top_columns_y_offset

        column_topleft_ele = AllplanArchElements.ColumnElement(column_topleft_prop, column_topleft_input)

        model_ele_list.append(column_topleft_ele)

        #----------------- top right column

        column_topright_prop = self.create_column_properties_base()

        column_topright_prop.Width = self.build_ele.Width2.value
        column_topright_prop.Depth = self.build_ele.Depth2.value
        column_topright_prop.SurfaceElementProperties = self.build_ele.SurfacePropTop.value

        column_topright_input = AllplanGeometry.Point3D(self.pnt_result.input_point)
        column_topright_input.X = column_topright_input.X + self.build_ele.Width2.value + 1000
        column_topright_input.Y = column_topright_input.Y + top_columns_y_offset

        column_topright_ele = AllplanArchElements.ColumnElement(column_topright_prop, column_topright_input)

        model_ele_list.append(column_topright_ele)

        return model_ele_list

    def create_column_properties_base(self) -> AllplanArchElements.ColumnProperties:
        """Creates properties of the column element with base values set from the palette

        Returns:
            column properties
        """

        column_prop = AllplanArchElements.ColumnProperties()

        column_prop.PlaneReferences = AllplanArchElements.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())

        column_prop.CommonProperties = self.build_ele.CommonProp.value

        return column_prop
