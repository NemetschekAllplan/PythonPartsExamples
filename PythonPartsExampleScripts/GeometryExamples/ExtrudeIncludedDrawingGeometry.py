"""
Script for including geometry elements from the drawing
"""

# pylint: disable=line-too-long

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils.GeometryStringValueConverter import GeometryStringValueConverter

print('Load ExtrudeIncludedDrawingGeometry.py')


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
                   _doc     : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        _doc:      input document

    Returns:
        created element result
    """

    #--------------------- the geometry was selected by the tool "SelectDrawingGeometryForPythonPart" located in "ToolsAndStartExamples"

    geo_ele_strings = ["Arc2D(CenterPoint(47.5937737241,-15.5601526088)MinorRadius(25.000000000003009)MajorRadius(25.000000000003009)AxisAngle(0)StartAngle(3.2412684071712436)EndAngle(3.6729800524530098)IsCounterClockwise(1))",
                       "Line2D(22.71786163413708,-18.047922230507538,20.113127217726287,7.9975539243387175)",
                       "Arc2D(CenterPoint(15.1379447997,7.5)MinorRadius(4.9999999999992832)MajorRadius(4.9999999999992832)AxisAngle(0)StartAngle(0.099675753581647916)EndAngle(1.5707963267947382)IsCounterClockwise(1))",
                       "Line2D(15.137944799727848,12.5,-5.25,12.5)",
                       "Arc2D(CenterPoint(-5.25,9.5)MinorRadius(3)MajorRadius(3)AxisAngle(0)StartAngle(1.5707963267948966)EndAngle(3.1415926535897931)IsCounterClockwise(1))",
                       "Line2D(-8.25,9.5,-8.25,7.8702858422475401)",
                       "Arc2D(CenterPoint(-5.25,7.8702858422)MinorRadius(3.0000000000002451)MajorRadius(3.0000000000002451)AxisAngle(0)StartAngle(3.1415926535896119)EndAngle(3.9793506945458565)IsCounterClockwise(1))",
                       "Line2D(-7.2573918190792028,5.6408513658170705,6.5452481915417593,-6.7871015217351669)",
                       "Arc2D(CenterPoint(5.12,-8.37)MinorRadius(2.1299999999971653)MajorRadius(2.1299999999971653)AxisAngle(0)StartAngle(4.7123889803830199)EndAngle(7.1209433481389164)IsCounterClockwise(1))",
                       "Line2D(5.1199999999989814,-10.5,-0.15028409320439184,-10.5)",
                       "Arc2D(CenterPoint(-0.1502840932,9.5)MinorRadius(19.999999999996291)MajorRadius(19.999999999996291)AxisAngle(0)StartAngle(3.8491195760716641)EndAngle(4.7123889803846843)IsCounterClockwise(1))",
                       "Arc2D(CenterPoint(-7.75,3.0004370812)MinorRadius(10.00000000000094)MajorRadius(10.00000000000094)AxisAngle(0)StartAngle(3.1415926535899024)EndAngle(3.849119576071574)IsCounterClockwise(1))",
                       "Line2D(-17.75,3.0004370811584522,-17.75,10.5)",
                       "Arc2D(CenterPoint(-5.75,10.5)MinorRadius(12)MajorRadius(12)AxisAngle(0)StartAngle(1.5707963267948966)EndAngle(3.1415926535897931)IsCounterClockwise(1))",
                       "Line2D(-5.75,22.5,17.852888110777709,22.5)",
                       "Arc2D(CenterPoint(17.8528881108,10.5)MinorRadius(12.000000000000526)MajorRadius(12.000000000000526)AxisAngle(0)StartAngle(0.09967575358132974)EndAngle(1.570796326794945)IsCounterClockwise(1))",
                       "Line2D(29.793325913979061,11.694129418407101,32.394527916796505,-14.316025133855874)",
                       "Arc2D(CenterPoint(57.2704400068,-11.8282555122)MinorRadius(24.999999999998597)MajorRadius(24.999999999998597)AxisAngle(0)StartAngle(3.2412684071712046)EndAngle(3.6729800524530489)IsCounterClockwise(1))",
                       "Line2D(35.717818407825689,-24.496503307804232,123.30221273519783,-173.50474338689673)",
                       "Arc2D(CenterPoint(187.9600775321,-135.5)MinorRadius(74.999999999999858)MajorRadius(74.999999999999858)AxisAngle(0)StartAngle(3.672980052452993)EndAngle(4.7123889803846852)IsCounterClockwise(1))",
                       "Line2D(187.96007753211234,-210.5,562.03992246788766,-210.5)",
                       "Arc2D(CenterPoint(562.0399224679,-135.5)MinorRadius(74.999999999999858)MajorRadius(74.999999999999858)AxisAngle(0)StartAngle(4.7123889803846941)EndAngle(5.7517979083163864)IsCounterClockwise(1))",
                       "Line2D(626.69778726480217,-173.50474338689673,714.28218159217431,-24.496503307804232)",
                       "Arc2D(CenterPoint(692.7295599932,-11.8282555122)MinorRadius(24.999999999999105)MajorRadius(24.999999999999105)AxisAngle(0)StartAngle(5.7517979083166804)EndAngle(6.1835095535984692)IsCounterClockwise(1))",
                       "Line2D(717.60547208319986,-14.316025133855874,720.20667408602094,11.694129418407101)",
                       "Arc2D(CenterPoint(732.1471118892,10.5)MinorRadius(11.999999999998652)MajorRadius(11.999999999998652)AxisAngle(0)StartAngle(1.5707963267950125)EndAngle(3.0419169000086024)IsCounterClockwise(1))",
                       "Line2D(732.14711188921865,22.5,755.74999999999636,22.5)",
                       "Arc2D(CenterPoint(755.75,10.5)MinorRadius(12)MajorRadius(12)AxisAngle(0)StartAngle(0)EndAngle(1.5707963267948966)IsCounterClockwise(1))",
                       "Line2D(767.74999999999636,10.5,767.74999999999636,3.0004370811584522)",
                       "Arc2D(CenterPoint(757.75,3.0004370812)MinorRadius(10.000000000000909)MajorRadius(10.000000000000909)AxisAngle(0)StartAngle(5.5756583846978041)EndAngle(6.283185307179477)IsCounterClockwise(1))",
                       "Arc2D(CenterPoint(750.1502840932,9.5)MinorRadius(20.000000000000728)MajorRadius(20.000000000000728)AxisAngle(0)StartAngle(4.7123889803846151)EndAngle(5.575658384697614)IsCounterClockwise(1))",
                       "Line2D(750.15028409319711,-10.5,744.88000000000102,-10.5)",
                       "Arc2D(CenterPoint(744.88,-8.37)MinorRadius(2.1299999999971746)MajorRadius(2.1299999999971746)AxisAngle(0)StartAngle(2.3038346126304736)EndAngle(4.7123889803863444)IsCounterClockwise(1))",
                       "Line2D(743.45475180845824,-6.7871015217351669,757.25739181907193,5.6408513658170705)",
                       "Arc2D(CenterPoint(755.25,7.8702858423)MinorRadius(3.0000000000003433)MajorRadius(3.0000000000003433)AxisAngle(0)StartAngle(5.4454272662219054)EndAngle(6.2831853071786599)IsCounterClockwise(1))",
                       "Line2D(758.24999999999636,7.8702858422475401,758.24999999999636,9.5)",
                       "Arc2D(CenterPoint(755.25,9.5)MinorRadius(3)MajorRadius(3)AxisAngle(0)StartAngle(0)EndAngle(1.5707963267948966)IsCounterClockwise(1))",
                       "Line2D(755.24999999999636,12.5,734.86205520026488,12.5)",
                       "Arc2D(CenterPoint(734.8620552003,7.5)MinorRadius(4.9999999999992841)MajorRadius(4.9999999999992841)AxisAngle(0)StartAngle(1.5707963267950558)EndAngle(3.0419169000081459)IsCounterClockwise(1))",
                       "Line2D(729.88687278226644,7.9975539243387175,727.28213836586292,-18.047922230507538)",
                       "Arc2D(CenterPoint(702.4062262759,-15.5601526088)MinorRadius(24.999999999995197)MajorRadius(24.999999999995197)AxisAngle(0)StartAngle(5.7517979083163002)EndAngle(6.1835095535982036)IsCounterClockwise(1))",
                       "Line2D(723.95884787483374,-28.228400404455897,615.54838470168397,-212.66824779563467)",
                       "Arc2D(CenterPoint(593.9957631027,-200)MinorRadius(24.999999999999972)MajorRadius(24.999999999999972)AxisAngle(0)StartAngle(4.7123889803848318)EndAngle(5.7517979083162718)IsCounterClockwise(1))",
                       "Line2D(593.99576310271732,-225,156.00423689728268,-225)",
                       "Arc2D(CenterPoint(156.0042368973,-200)MinorRadius(25.000000000000057)MajorRadius(25.000000000000057)AxisAngle(0)StartAngle(3.6729800524531058)EndAngle(4.7123889803848362)IsCounterClockwise(1))",
                       "Line2D(134.45161529830875,-212.66824779563467,26.041152125166263,-28.228400404455897)"]

    geo_elements = GeometryStringValueConverter.get_elements(geo_ele_strings, True)

    start_pnt = geo_elements[0].StartPoint

    path = AllplanGeo.Polyline3D()

    path += start_pnt
    path += start_pnt + AllplanGeo.Point3D(0, 0, build_ele.Height.value)

    _, extruded_ele = AllplanGeo.CreateSweptBRep3D(geo_elements, path, True, False)


    #----------------- create the PythonPart

    com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    pyp_util = PythonPartUtil()

    pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, extruded_ele))

    return CreateElementResult(pyp_util.create_pythonpart(build_ele))
