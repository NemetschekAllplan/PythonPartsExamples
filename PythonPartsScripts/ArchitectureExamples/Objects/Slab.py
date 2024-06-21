"""Example script showing the creation of an architectural beam"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult
from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SlabBuildingElement import SlabBuildingElement as BuildingElement  # type: ignore
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


def create_preview(_build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Create a simplified slab representation for library preview

    Args:
        _build_ele:   building element with the parameter properties
        _doc:        input document

    Returns:
        Preview elements
    """

    common_props = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    polygon = AllplanGeometry.Polygon3D()
    polygon += AllplanGeometry.Point3D()
    polygon += AllplanGeometry.Point3D(2500, 0, 0)
    polygon += AllplanGeometry.Point3D(2500, 800, 0)
    polygon += AllplanGeometry.Point3D(3500, 800, 0)
    polygon += AllplanGeometry.Point3D(3500, 2500, 0)
    polygon += AllplanGeometry.Point3D(   0, 2500, 0)
    polygon += AllplanGeometry.Point3D()
    polygon += polygon.Points[0]

    area  = AllplanGeometry.PolygonalArea3D()
    area += polygon

    extruded_solid = AllplanGeometry.ExtrudedAreaSolid3D()
    extruded_solid.SetDirection(AllplanGeometry.Vector3D(0,0,200))
    extruded_solid.SetRefPoint(polygon.Points[0])
    extruded_solid.SetExtrudedArea(area)    # type: ignore

    _, slab_geo = AllplanGeometry.CreatePolyhedron(extruded_solid)

    return CreateElementResult([AllplanBasisElements.ModelElement3D(common_props, slab_geo)])


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return SlabScript(build_ele, coord_input)


class SlabScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural slab

    This script objects prompts the user to input the outline by drawing a 2D-polygon and
    subsequently creates a slab

    Args:
        build_ele:      the building element with parameter properties from the property palette
        coord_input:    the object representing the coordinate input done by the user inside Allplan viewport
    """

    def __init__(self,
                 build_ele: BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):

        super().__init__(coord_input)

        self.doc                      = coord_input.GetInputViewDocument()
        self.outline_input_result     = PolygonInteractorResult()
        self.build_ele                = build_ele


    def start_input(self):
        """Starts the slab outline input at the beginning of the script runtime"""

        self.script_object_interactor = PolygonInteractor(self.outline_input_result,
                                                          z_coord_input       = False,
                                                          multi_polygon_input = False,
                                                          preview_function    = self.create_preview_elements)


    def start_next_input(self):
        """Terminate the outline input after successful input of a closed
        polygon consisting of at least 3 vertices
        """

        if self.outline_input_result != PolygonInteractorResult():
            self.script_object_interactor = None


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        _, outline = AllplanGeometry.ConvertTo2D(self.outline_input_result.input_polygon)

        return CreateElementResult([self.slab_element(outline)],
                                   placement_point = AllplanGeometry.Point2D())  # beam is already in the global coordinate system


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        if self.script_object_interactor:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    def modify_element_property(self,
                                name: str,
                                value: Any) -> bool:
        """ Handle the event of parameter modification (either in the palette or by a handle)

        Args:
            name:  name of the modified parameter
            value: new value of the parameter

        Returns:
            Should palette be updated
        """

        # enforce, that only hatch, pattern OR face style are selected as surface element

        if value and name in (params := ["UseHatch", "UsePattern", "UseFaceStyle"]):
            params.remove(name)

            for param_name in params:
                parameter_prop = getattr(self.build_ele, param_name)
                parameter_prop.value = False

            # additionally, prevent using filling, when using face style

            if name == "UseFaceStyle":
                self.build_ele.UseFilling.value = False

            return True

        # prevent using face style, when using filling

        if value and name == "UseFilling":
            self.build_ele.UseFaceStyle.value = False
            return True

        return False


    @property
    def slab_properties(self) -> AllplanArchElements.SlabProperties:
        """Properties of the beam element, based on the values from the property palette

        Returns:
            beam properties
        """

        slab_prop = AllplanArchElements.SlabProperties()

        #--------- Define properties specific to a slab

        slab_prop.PlaneReferences = self.build_ele.PlaneReferences.value

        #--------- Define standard architecture attributes

        slab_prop.CalculationMode = AllplanBaseElements.AttributeService.GetEnumIDFromValueString(120, self.build_ele.CalculationMode.value)
        slab_prop.Trade           = self.build_ele.Trade.value
        slab_prop.Priority        = self.build_ele.Priority.value
        slab_prop.Factor          = self.build_ele.Factor.value

        #--------- Define surface elements

        if self.build_ele.UseHatch.value:
            slab_prop.Hatch = self.build_ele.Hatch.value
        elif self.build_ele.UsePattern.value:
            slab_prop.Pattern = self.build_ele.Pattern.value

        if self.build_ele.UseFilling.value:
            if any({self.build_ele.UseHatch.value, self.build_ele.UsePattern.value}): # when using filling AND hatching or pattern,
                slab_prop.BackgroundColor = self.build_ele.Filling.value              # filling color must be defined in the BackgroundColor
            else:
                slab_prop.Filling = self.build_ele.Filling.value                      # otherwise it must be defined in Filling property

        slab_prop.SetShowAreaElementInGroundView(self.build_ele.ShowAreaElementInGroundView.value)

        #--------- Define format properties

        slab_prop.CommonProperties = self.build_ele.CommonProp.value

        if self.build_ele.Surface.value:
            slab_prop.Surface = self.build_ele.Surface.value

        return slab_prop


    def slab_element(self, outline: AllplanGeometry.Polygon2D) -> AllplanArchElements.SlabElement:
        """Creates a SlabElement based on outline polygon

        Args:
            outline: slab outline

        Returns:
            Slab element
        """

        if isinstance(outline, AllplanGeometry.Polygon3D):
            _, outline = AllplanGeometry.ConvertTo2D(outline)

        return AllplanArchElements.SlabElement(self.slab_properties, outline)


    def create_preview_elements(self, polygon: AllplanGeometry.Polygon3D) -> list:
        """Create the list of slab elements to preview based on 3d polygon

        Args:
            polygon: input 3d polygon

        Returns:
            list of elements to preview - one slab element
        """

        success, outline = AllplanGeometry.ConvertTo2D(polygon)

        return [self.slab_element(outline)] if success and outline.Count() > 2 else []
