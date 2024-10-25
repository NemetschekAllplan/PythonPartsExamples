"""Example script showing the creation of an architectural beam"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return SlabScript(build_ele, script_object_data)


class SlabScript(BaseScriptObject):
    """Script object that realizes the creation of an architectural slab

    This script objects prompts the user to input the outline by drawing a 2D-polygon and
    subsequently creates a slab
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ function description

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.outline_input_result     = PolygonInteractorResult()
        self.build_ele                = build_ele
        self.slab_element             = AllplanArchElements.SlabElement()


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

        return CreateElementResult([self.create_slab_element(outline)],
                                   placement_point = AllplanGeometry.Point2D())  # beam is already in the global coordinate system


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """Handles the event of hitting the ESC button

        Returns:
            What to do after hitting the ESC button
        """

        if self.script_object_interactor:
            return self.script_object_interactor.on_cancel_function()

        return OnCancelFunctionResult.CREATE_ELEMENTS


    @property
    def slab_properties(self) -> AllplanArchElements.SlabProperties:
        """Properties of the beam element, based on the values from the property palette

        Returns:
            beam properties
        """

        slab_prop = AllplanArchElements.SlabProperties()

        #--------- Define properties specific to a slab

        slab_prop.PlaneReferences = self.build_ele.PlaneReferences.value
        slab_prop.TierCount       = self.build_ele.TierCount.value
        slab_prop.VariableTier    = self.build_ele.VariableTier.value

        calc_modes = ["m³","m²","m","Pcs","kg"]

        for tier_index in range(slab_prop.TierCount):

            slab_tier_prop                 = slab_prop.GetSlabTierProperties(tier_index)
            slab_tier_prop.Priority        = self.build_ele.Priority.value[tier_index]
            slab_tier_prop.Trade           = self.build_ele.Trade.value[tier_index]
            slab_tier_prop.Factor          = self.build_ele.Factor.value[tier_index]
            slab_tier_prop.CalculationMode = calc_modes.index(self.build_ele.CalculationMode.value[tier_index])
            slab_tier_prop.Thickness       = self.build_ele.Thickness.value[tier_index]

            slab_tier_prop.CommonProperties         = self.build_ele.CommonProp.value[tier_index]
            slab_tier_prop.SurfaceElementProperties = self.build_ele.SurfaceElemProp.value[tier_index]


            if self.build_ele.IsSurface.value[tier_index]:
                slab_tier_prop.Surface = self.build_ele.SurfaceName.value[tier_index]

        return slab_prop


    def create_slab_element(self, outline: AllplanGeometry.Polygon2D) -> AllplanArchElements.SlabElement:
        """Creates a SlabElement based on outline polygon

        Args:
            outline: slab outline

        Returns:
            Slab element
        """

        if isinstance(outline, AllplanGeometry.Polygon3D):
            _, outline = AllplanGeometry.ConvertTo2D(outline)

        self.slab_element = AllplanArchElements.SlabElement(self.slab_properties, outline)

        return self.slab_element


    def create_preview_elements(self, polygon: AllplanGeometry.Polygon3D) -> list:
        """Create the list of slab elements to preview based on 3d polygon

        Args:
            polygon: input 3d polygon

        Returns:
            list of elements to preview - one slab element
        """

        success, outline = AllplanGeometry.ConvertTo2D(polygon)

        return [self.create_slab_element(outline)] if success and outline.Count() > 2 else []

    def modify_element_property(self,
                                name : str,
                                value: Any) -> bool:
        """ modify the element property

        Args:
            name:  name
            value: value

        Returns:
            update palette state
        """
        match name:
            case "TierCount":

                slab_props = AllplanArchElements.SlabProperties()
                slab_props.PlaneReferences = self.build_ele.PlaneReferences.value

                height = 0.0

                for tier in range(value):
                    height = height + self.build_ele.Thickness.value[tier]

                plane_ref = slab_props.GetPlaneReferences()
                plane_ref.SetHeight(height)

                self.build_ele.PlaneReferences.value = plane_ref

                return True
            
            case "VariableTier":

                old_variable_tier = self.slab_element.GetProperties().GetVariableTier() -1
                old_thickness    = self.build_ele.Thickness.value[value-1]

                self.build_ele.Thickness.value[value-1] = self.build_ele.Thickness.value[old_variable_tier]
                self.build_ele.Thickness.value[old_variable_tier] = old_thickness
                return True
              
            case "PlaneReferences.Height":

                height = 0.0
                variable_tier = self.build_ele.VariableTier.value
                tier_count = self.build_ele.TierCount.value

                for tier in range(tier_count):
                    if tier != variable_tier:
                        height = height + self.build_ele.Thickness.value[tier]
                        
                self.build_ele.Thickness.value[variable_tier-1] = value - height

                return True

            case s if s.startswith('Thickness'):

                height = 0.0

                slab_props = AllplanArchElements.SlabProperties()
                slab_props.PlaneReferences = self.build_ele.PlaneReferences.value

                tier_count = self.build_ele.TierCount.value

                for tier in range(tier_count):
                    height = height + self.build_ele.Thickness.value[tier]

                plane_ref = slab_props.GetPlaneReferences()
                plane_ref.SetHeight(height)

                self.build_ele.PlaneReferences.value = plane_ref

        return False
