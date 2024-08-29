"""Example script showing the creation of a Block Foundation"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo


from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.PointInteractor import PointInteractor, PointInteractorResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

from Utils import LibraryBitmapPreview
from pathlib import Path


if TYPE_CHECKING:
    from __BuildingElementStubFiles.BlockFoundationBuildingElement import BlockFoundationBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_preview(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a simplified block foundation representation for library preview

    Args:
        build_ele:   building element with the parameter properties
        _doc:        input document

    Returns:
        Preview elements
    """

    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
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

    return BlockFoundationScript(build_ele, script_object_data)


class BlockFoundationScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural Block Foundation"""


    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialize the Block Foundation script object

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.pnt_result  = PointInteractorResult()
        self.build_ele   = build_ele


    def start_input(self):
        """Starts the Block Foundation point input at the beginning of the script runtime"""

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

        return CreateElementResult([self.block_foundation_element()], placement_point = AllplanGeometry.Point2D())


    def draw_preview(self):
        """ draw the preview
        """

        AllplanBaseEle.DrawElementPreview(self.document, AllplanGeometry.Matrix3D(),
                                          [self.block_foundation_element()], False, None)


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        if self.script_object_interactor:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def create_block_foundation_properties(self) -> AllplanArchElements.BlockFoundationProperties:
        """Properties of the block foundation element, based on the values from the property palette

        Returns:
            block Foundation properties
        """

        props = AllplanArchElements.BlockFoundationProperties()


        #--------- Define properties specific to a block foundation
        if (self.build_ele.ShapeType.value == "eRectangular"):
            props.ShapeType = AllplanArchElements.ShapeType.eRectangular
        if (self.build_ele.ShapeType.value == "eCircular"):
            props.ShapeType = AllplanArchElements.ShapeType.eCircular
        if (self.build_ele.ShapeType.value == "ePolygonal"):
            props.ShapeType = AllplanArchElements.ShapeType.ePolygonal

        if (self.build_ele.ShapeType.value == "eConical"):
            props.ShapeType = AllplanArchElements.ShapeType.eConical

        profilePoints = self.build_ele.ProfilePoints.value
        polygon = AllplanGeo.Polygon2D(profilePoints)
        props.SetShapePolygon(polygon)
        props.VouteBack = self.build_ele.VouteBack.value
        props.VouteFront = self.build_ele.VouteFront.value
        props.VouteLeft = self.build_ele.VouteLeft.value
        props.VouteRight = self.build_ele.VouteRight.value
        props.SetPlaneReferences(self.build_ele.WallPlaneRef.value)
        props.Width = self.build_ele.Width.value
        props.Depth = self.build_ele.Depth.value
        props.Radius = self.build_ele.Radius.value
        props.SetCircleDivision(100)

        #--------- Define format and texture properties
        props.SetCommonProperties(self.build_ele.CommonProp.value)

        if self.build_ele.IsSurface.value:
            props.Surface = self.build_ele.SurfaceName.value

        #--------- Define surface elements
        props.SurfaceElementProperties = self.build_ele.SurfaceElemProp.value

        #--------- Define standard architecture attributes
        props.CalculationMode = AllplanBaseEle.AttributeService.GetEnumIDFromValueString(120, self.build_ele.CalculationMode.value)
        props.Trade = self.build_ele.Trade.value
        props.Priority = self.build_ele.Priority.value
        props.Factor = self.build_ele.Factor.value

        return props


    def block_foundation_element(self) -> AllplanArchElements.BlockFoundationElement:
        """Creates a block foundation element based on selection point

        Returns:
            block foundation element
        """

        return AllplanArchElements.BlockFoundationElement(self.create_block_foundation_properties(), self.pnt_result.input_point)
