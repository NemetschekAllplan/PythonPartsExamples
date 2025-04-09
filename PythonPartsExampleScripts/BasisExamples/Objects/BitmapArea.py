""" Example Script for BitmapArea
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData, HandleParameterType
from HandleProperties import HandleProperties

if TYPE_CHECKING:
    from __BuildingElementStubFiles.BitmapAreaBuildingElement import BitmapAreaBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load BitmapArea.py')


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
                   _doc:       AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Function for the creation of the library preview elements.

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        Preview elements. Only elements included in the property "elements" will be shown in the library preview
    """

    return CreateElementResult()


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return ScriptObject(build_ele, script_object_data)


class ScriptObject(BaseScriptObject):
    """ Implementation of the script object class
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ initialize

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        self.build_ele = build_ele

        super().__init__(script_object_data)


    def execute(self) -> CreateElementResult:
        """Execute element creation

        Returns:
            Result object with elements to create
        """

        return CreateElementResult([self.bitmap_element], self.handles)


    @property
    def bitmap_outline(self) -> AllplanGeo.Polygon2D:
        """Rectangle to use as the bitmap outline

        The rectangle dimensions are got from the values defined in the property palette

        Return:
            Bitmap outline as a rectangle
        """
        return AllplanGeo.Polygon2D.CreateRectangle(AllplanGeo.Point2D(0,0),
                                                    AllplanGeo.Point2D(self.build_ele.Length.value,
                                                                       self.build_ele.Width.value))


    @property
    def bitmap_element(self) -> AllplanBasisElements.BitmapAreaElement:
        """Bitmap element with properties based on the values from the property palette

        Returns:
            Bitmap element
        """

        #------------------ Define BitmapArea properties

        bitmaparea_prop                             = AllplanBasisElements.BitmapAreaProperties()

        bitmaparea_prop.BitmapName                  = self.build_ele.BitmapName.value
        bitmaparea_prop.XOffset                     = self.build_ele.Offset.value.X
        bitmaparea_prop.YOffset                     = self.build_ele.Offset.value.Y
        bitmaparea_prop.ReferencePoint              = self.build_ele.ReferencePoint.value
        bitmaparea_prop.RotationAngle               = AllplanGeo.Angle.FromDeg(self.build_ele.RotationAngle.value)
        bitmaparea_prop.XScalingFactor              = self.build_ele.XScalingFactor.value
        bitmaparea_prop.YScalingFactor              = self.build_ele.YScalingFactor.value
        bitmaparea_prop.UseMetricalValues           = self.build_ele.UseMetricalValues.value
        bitmaparea_prop.UseRepeatTile               = self.build_ele.UseRepeatTile.value
        bitmaparea_prop.UseDirectionToReferenceLine = self.build_ele.UseDirectionToReferenceLine.value
        bitmaparea_prop.UsePixelMask                = self.build_ele.UsePixelMask.value
        bitmaparea_prop.UseReferencePoint           = self.build_ele.UseReferencePoint.value

        transparent_color                         = AllplanBasisElements.ARGB(self.build_ele.ColorToMask.value)
        transparent_color.Alpha                   = self.build_ele.Transparency.value
        bitmaparea_prop.TransparentColor          = transparent_color
        bitmaparea_prop.TransparentColorTolerance = self.build_ele.TransparentColorTolerance.value

        if self.build_ele.DirectionToReferenceLine.value:
            bitmaparea_prop.DirectionToReferenceLine = self.build_ele.DirectionToReferenceLine.value

        #------------------ Define format properties

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        return AllplanBasisElements.BitmapAreaElement(com_prop, bitmaparea_prop, self.bitmap_outline)


    @property
    def handles(self) -> list[HandleProperties]:
        """Handles

        Returns:
            Handles
        """
        origin = AllplanGeo.Point3D()

        corner = AllplanGeo.Point3D(self.build_ele.Length.value,
                                    self.build_ele.Width.value,
                                    0)
        handle_parameter = [HandleParameterData("Length", HandleParameterType.X_DISTANCE),
                            HandleParameterData("Width", HandleParameterType.Y_DISTANCE)]

        return [HandleProperties("UpperRightCorner", corner, origin, handle_parameter, HandleDirection.xy_dir)]
