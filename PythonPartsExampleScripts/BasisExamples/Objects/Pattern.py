""" Example script for Pattern
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo

from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData, HandleParameterType
from HandleProperties import HandleProperties
from HandlePropertiesService import HandlePropertiesService
from PythonPartUtil import PythonPartUtil

from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PatternBuildingElement import PatternBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Pattern.py')


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


def create_preview(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    element = Pattern(doc)

    return element.create(build_ele)


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = Pattern(doc)

    return element.create(build_ele)


def move_handle(build_ele  : BuildingElement,
                handle_prop: HandleProperties,
                input_pnt  : AllplanGeo.Point3D,
                doc        : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Modify the element geometry by handles

    Args:
        build_ele:   building element with the parameter properties
        handle_prop: handle properties
        input_pnt:   input point
        doc:         document of the Allplan drawing files

    Returns:
        created element result
    """

    HandlePropertiesService.update_property_value(build_ele, handle_prop, input_pnt)

    return create_element(build_ele, doc)


class Pattern():
    """ Definition of class Pattern
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        model_ele_list = ModelEleList(build_ele.CommonProp.value)


        #----------------- create geometry

        length = build_ele.Size.value.X
        width  = build_ele.Size.value.Y

        if length < 1 or width < 1:
            return CreateElementResult()


        #------------------ Define the polygon

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(0,0)
        polygon += AllplanGeo.Point2D(length,0)
        polygon += AllplanGeo.Point2D(length,width)
        polygon += AllplanGeo.Point2D(0,width)
        polygon += AllplanGeo.Point2D(0,0)

        if build_ele.ShowPolygon.value:
            model_ele_list.append_geometry_2d(polygon)


        #------------------ Define pattern properties

        pattern_prop = AllplanBasisEle.PatternProperties()

        pattern_prop.PatternID          = build_ele.PatternId.value
        pattern_prop.XScalingFactor     = build_ele.XScalingFactor.value
        pattern_prop.YScalingFactor     = build_ele.YScalingFactor.value
        pattern_prop.IsScaleDependent   = build_ele.IsScaleDependent.value
        pattern_prop.RotationAngle      = AllplanGeo.Angle.FromDeg(build_ele.RotationAngle.value)
        pattern_prop.UseBackgroundColor = build_ele.DefineBackgroundColor.value
        pattern_prop.BackgroundColor    = AllplanBasisEle.ARGB(build_ele.BackgroundColor.value)
        pattern_prop.UseReferencePoint  = build_ele.DefineReferencePoint.value
        pattern_prop.ReferencePoint     = build_ele.ReferencePoint.value
        pattern_prop.PlacementType      = AllplanBasisEle.PlacementType.values[build_ele.PlacementType.value]


        #------------------ Append the pattern element

        model_ele_list.append(AllplanBasisEle.PatternElement(build_ele.CommonPropPattern.value, pattern_prop, polygon))


        #------------------ Handles

        handle1 = HandleProperties("UpperRightCorner",
                                   AllplanGeo.Point3D(length, width, 0), AllplanGeo.Point3D(),
                                   [HandleParameterData("Size.X", HandleParameterType.X_DISTANCE),
                                    HandleParameterData("Size.Y", HandleParameterType.Y_DISTANCE)],
                                   HandleDirection.xy_dir,
                                   True)

        handle_list = [handle1]


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele), handle_list)
