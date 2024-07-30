""" Script for SurfaceElementProperties
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
    from __BuildingElementStubFiles.SurfaceElementPropertiesBuildingElement \
        import SurfaceElementPropertiesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load SurfaceElementProperties.py')


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
                               r"Examples\PythonParts\PaletteExamples\Properties\SurfaceElementProperties.png"))

def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return SurfaceElementProperties(build_ele, script_object_data)

class SurfaceElementProperties(BaseScriptObject):
    """ Definition of class SurfaceElementProperties
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialize the SurfaceElementProperties script object

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

        self.script_object_interactor = PointInteractor(self.pnt_result, True, "Place the element", self.draw_preview)


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
        """ create the opening element


        Returns:
            list with the elements
        """

        model_ele_list = ModelEleList()

        #----------------- use the SurfaceElementProperties parameter for the first column

        column_ele_1_prop = self.create_column_properties_base()
        column_ele_1_prop.SurfaceElementProperties = self.build_ele.SurfaceElementProp.value

        column_ele_1 = AllplanArchElements.ColumnElement(column_ele_1_prop, self.pnt_result.input_point)

        model_ele_list.append(column_ele_1)

        #----------------- use the properties with condition for the second column

        column_ele_2_prop = self.create_column_properties_base()
        column_ele_2_prop.SurfaceElementProperties = self.build_ele.SurfaceElementPropCond.value

        column_ele_2_input = AllplanGeometry.Point3D(self.pnt_result.input_point)
        column_ele_2_input.X = column_ele_2_input.X + self.build_ele.Width.value*2

        column_ele_2 = AllplanArchElements.ColumnElement(column_ele_2_prop, column_ele_2_input)

        model_ele_list.append(column_ele_2)

        #----------------- use the single parameters for the third column

        column_ele_3_prop = self.create_column_properties_base()
        surface_elem_prop = AllplanArchElements.SurfaceElementProperties()

        # fill in the single properties from the palette

        surface_elem_prop.UseAreaInGroundplan = self.build_ele.UseAreaInGroundplan.value
        surface_elem_prop.HatchSelected       = self.build_ele.IsHatch.value
        surface_elem_prop.HatchID             = self.build_ele.HatchId.value
        surface_elem_prop.PatternSelected     = self.build_ele.IsPattern.value
        surface_elem_prop.PatternID           = self.build_ele.PatternId.value
        surface_elem_prop.FillingSelected     = self.build_ele.IsFilling.value
        surface_elem_prop.FillingID           = self.build_ele.FillingId.value
        surface_elem_prop.FaceStyleSelected   = self.build_ele.IsFaceStyle.value
        surface_elem_prop.FaceStyleID         = self.build_ele.FaceStyleId.value
        surface_elem_prop.BitmapSelected      = self.build_ele.IsBitmap.value
        surface_elem_prop.BitmapID            = self.build_ele.BitmapName.value

        # assign the properties

        column_ele_3_prop.SurfaceElementProperties = surface_elem_prop

        column_ele_3_input = AllplanGeometry.Point3D(self.pnt_result.input_point)
        column_ele_3_input.X = column_ele_3_input.X + self.build_ele.Width.value*4

        column_ele_3 = AllplanArchElements.ColumnElement(column_ele_3_prop, column_ele_3_input)
        model_ele_list.append(column_ele_3)

        #----------------- use properties from the list for the second row of columns

        column_ele_list_item_input = AllplanGeometry.Point3D(self.pnt_result.input_point)
        column_ele_list_item_input.Y = column_ele_list_item_input.Y + self.build_ele.Width.value*2

        for surface_elem_prop in self.build_ele.SurfaceElemPropList.value:
            column_ele_list_item_prop = self.create_column_properties_base()
            column_ele_list_item_prop.SurfaceElementProperties = surface_elem_prop

            point_input = AllplanGeometry.Point3D(column_ele_list_item_input)
            column_ele_list_item = AllplanArchElements.ColumnElement(column_ele_list_item_prop, point_input)
            model_ele_list.append(column_ele_list_item)

            column_ele_list_item_input.X += self.build_ele.Width.value*2

        return model_ele_list

    def create_column_properties_base(self) -> AllplanArchElements.ColumnProperties:
        """Creates properties of the column element with base values set from the palette

        Returns:
            column properties
        """

        column_prop = AllplanArchElements.ColumnProperties()

        column_prop.Width = self.build_ele.Width.value
        column_prop.Depth = self.build_ele.Width.value

        column_prop.PlaneReferences = AllplanArchElements.PlaneReferences(self.document, AllplanEleAdapter.BaseElementAdapter())

        column_prop.CommonProperties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        return column_prop
