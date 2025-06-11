""" Script for Hatch
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.PolygonInteractor import PolygonInteractor, PolygonInteractorResult

from TypeCollections.HandleList import HandleList
from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview
from Utils.HandleCreator.CurveHandlesCreator import CurveHandlesCreator

if TYPE_CHECKING:
    from __BuildingElementStubFiles.HatchBuildingElement import HatchBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Hatch.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Hatch(build_ele, script_object_data)


class Hatch(BaseScriptObject):
    """ Definition of class Hatch
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele              = build_ele
        self.poly_interactor_result = PolygonInteractorResult()
        self.model_ele_list         = ModelEleList()


    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def start_input(self):
        """ start the input
        """

        build_ele = self.build_ele

        self.script_object_interactor = PolygonInteractor(self.poly_interactor_result,
                                                          z_coord_input       = False,
                                                          multi_polygon_input = True,
                                                          preview_function    = self.draw_preview)

        build_ele.InputMode.value = build_ele.POLYGON_INPUT


    def start_next_input(self):
        """ start the next input
        """

        build_ele = self.build_ele

        self.script_object_interactor = None

        build_ele.InputMode.value = build_ele.PALETTE_INPUT


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        self.create_hatch(self.poly_interactor_result.input_polygon)


        #------------------ Handles

        handle_list = HandleList()

        CurveHandlesCreator.poly_curve(handle_list, "Polyyon", self.poly_interactor_result.input_polygon,
                                       True, delete_point = True)

        return CreateElementResult(self.model_ele_list, handle_list, placement_point = AllplanGeo.Point3D(), multi_placement = True)


    def draw_preview(self,
                     polygon: AllplanGeo.Polygon3D) -> ModelEleList:
        """ draw the preview

        Args:
            polygon: polygon

        Returns:
            created elements for the preview
        """

        return self.create_hatch(polygon)


    def create_hatch(self,
                     polygon: AllplanGeo.Polygon3D) -> ModelEleList:
        """ create the hatch

        Args:
            polygon: polygon

        Returns:
            created elements
        """

        build_ele = self.build_ele

        self.model_ele_list = ModelEleList()


        #------------------ Create the bounding polygon(s)

        valid, polygon_2d = AllplanGeo.ConvertTo2D(polygon)

        if not valid:
            return self.model_ele_list

        build_ele.PolygonSegmentCount.value = 0

        if build_ele.ShowPolygon.value:
            sub_poly = AllplanGeo.Polygon2D()

            for segment in polygon_2d.GetSegments()[1]:
                if not sub_poly.Count():
                    sub_poly += segment.StartPoint

                sub_poly += segment.EndPoint

                build_ele.PolygonSegmentCount.value += 1

                if AllplanGeo.Comparison.Equal(sub_poly.StartPoint, sub_poly.EndPoint):
                    self.model_ele_list.append_geometry_2d(sub_poly, build_ele.ComPropGeo.value)

                    sub_poly = AllplanGeo.Polygon2D()


        #------------------ Define hatching properties

        hatching_prop                          = AllplanBasisEle.HatchingProperties()
        hatching_prop.HatchID                  = build_ele.HatchId.value
        hatching_prop.IsScaleDependent         = build_ele.IsScaleDependent.value
        hatching_prop.DirectionToReferenceLine = build_ele.DirectionToReferenceLine.value
        hatching_prop.UseBackgroundColor       = build_ele.DefineBackgroundColor.value
        hatching_prop.BackgroundColor          = AllplanBasisEle.ARGB(build_ele.BackgroundColor.value)
        hatching_prop.UseReferencePoint        = build_ele.DefineReferencePoint.value
        hatching_prop.ReferencePoint           = build_ele.ReferencePoint.value
        hatching_prop.RotationAngle            = AllplanGeo.Angle.FromDeg(build_ele.RotationAngle.value)


        #------------------ Append the hatching element

        self.model_ele_list.append(AllplanBasisEle.HatchingElement(build_ele.ComPropHatch.value, hatching_prop, polygon_2d))

        return self.model_ele_list
