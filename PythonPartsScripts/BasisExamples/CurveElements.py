"""
Example Script for CurveElements
"""

import math

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from HandleDirection import HandleDirection
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil

print('Load CurveElements.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        Object with the result data of the element creation
    """

    element = CurveElementsExample(doc)

    return element.create(build_ele)


def move_handle(build_ele  : BuildingElement,
                handle_prop: HandleProperties,
                input_pnt  : AllplanGeo.Point3D,
                doc        : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document

    Returns:
        Object with the result data of the element creation
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class CurveElementsExample():
    """
    Definition of class CurveElementsExample
    """

    def __init__(self, doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class CurveElementsExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = []
        self.document       = doc


    def create(self, build_ele: BuildingElement) -> CreateElementResult:
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            Object with the result data of the element creation
        """

        self.create_geometry(build_ele)

        if build_ele.CreatePythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d(self.model_ele_list)

            self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        return CreateElementResult(self.model_ele_list, self.handle_list,
                                   placement_point = build_ele.PlacementPoint.value if build_ele.GlobalPlacementPoint.value else None,
                                   multi_placement = build_ele.MultiPlacement.value)


    def create_geometry(self, build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette parameter values

        length = build_ele.Length.value
        width  = build_ele.Width.value


        #------------------ Define the curve elements

        line = AllplanGeo.Line2D(0, 0, 0, width/2)

        polyline = AllplanGeo.Polyline2D()
        polyline += AllplanGeo.Point2D(length / 2, 0)
        polyline += AllplanGeo.Point2D(length / 2 + length / 4, 0)
        polyline += AllplanGeo.Point2D(length / 2 + length / 4, width / 2)
        polyline += AllplanGeo.Point2D(length, width / 2)

        arc = AllplanGeo.Arc2D(AllplanGeo.Point2D(length /4, width / 2 + width / 4),
                               length / 4, width / 4, math.pi / 2, 0, math.pi, True)

        spline = AllplanGeo.Spline2D()
        spline += AllplanGeo.Point2D(length / 2, width / 2)
        spline += AllplanGeo.Point2D(length / 2 + length / 4, width / 2 + width / 4)
        spline += AllplanGeo.Point2D(length, width)

        spline.SetStartVector(AllplanGeo.Vector2D(1, 0))
        spline.SetEndVector(AllplanGeo.Vector2D(1, 0))


        #------------------ Define common properties, take global Allplan settings

        common_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


        #------------------ Define pattern curve properties

        patterncurve_prop = AllplanBasisElements.PatternCurveProperties()

        if build_ele.HasPatternCurve.value:
            patterncurve_prop.PatternID        = build_ele.PatternID.value
            patterncurve_prop.Height           = build_ele.PatternHeight.value
            patterncurve_prop.Width            = build_ele.PatternWidth.value
            patterncurve_prop.AlignmentType    = self.alignment_type_converter(build_ele.Alignment.value)
            patterncurve_prop.IntersectionType = self.intersection_type_converter(build_ele.Intersection.value)


        #------------------ Define end symbols properties

        endsymbols_prop = AllplanBasisElements.EndSymbolsProperties()

        if build_ele.HasStartSymbol.value:
            endsymbols_prop.StartID   = build_ele.StartSymbolID.value
            endsymbols_prop.StartSize = build_ele.StartSymbolSize.value

        if build_ele.HasEndSymbol.value:
            endsymbols_prop.EndID   = build_ele.EndSymbolID.value
            endsymbols_prop.EndSize = build_ele.EndSymbolSize.value


        #------------------ Append 2D line as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(common_prop, patterncurve_prop,
                                                                       endsymbols_prop, line))
        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(common_prop, patterncurve_prop,
                                                                       endsymbols_prop, polyline))
        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(common_prop, patterncurve_prop,
                                                                       endsymbols_prop, arc))
        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(common_prop, patterncurve_prop,
                                                                       endsymbols_prop, spline))

        #------------------ Handles

        origin = AllplanGeo.Point3D(0, 0, 0)
        corner = AllplanGeo.Point3D(length, width, 0)

        handle1 = HandleProperties("EndPoint", corner, origin,
                                   [HandleParameterData("Length", HandleParameterType.X_DISTANCE),
                                    HandleParameterData("Width", HandleParameterType.Y_DISTANCE)],
                                   HandleDirection.XY_DIR, True)

        self.handle_list.append(handle1)


    @staticmethod
    def alignment_type_converter(argument : str) ->AllplanBasisElements.PatternCurveAlignment:
        """Converter for alignment type

        Args:
            argument: Alignment as string

        Returns:
            Pattern curve alignment
        """
        switcher = {"Left"  : AllplanBasisElements.PatternCurveAlignment.eLeft,
                    "Center": AllplanBasisElements.PatternCurveAlignment.eCenter,
                    "Right" : AllplanBasisElements.PatternCurveAlignment.eRight}

        return switcher.get(argument, AllplanBasisElements.PatternCurveAlignment.eLeft)


    @staticmethod
    def intersection_type_converter(argument: str) -> AllplanBasisElements.PatternCurveIntersectionType:
        """ Converter for intersection type

        Args:
            argument: Intersection type as string

        Returns:
            Intersection type
        """

        switcher = {"Disabled": AllplanBasisElements.PatternCurveIntersectionType.eDisabled,
                    "Miter"   : AllplanBasisElements.PatternCurveIntersectionType.eMiter,
                    "Joint"   : AllplanBasisElements.PatternCurveIntersectionType.eJoint,
                    "Seamless": AllplanBasisElements.PatternCurveIntersectionType.eSeamless}

        return switcher.get(argument, AllplanBasisElements.PatternCurveIntersectionType.eDisabled)
