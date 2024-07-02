"""
Example Script for Dimensioning
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load Dimensioning.py')


def check_allplan_version(_build_ele, _version):
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


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    element = DimensioningExample(doc)

    return element.create(build_ele)


class DimensioningExample():
    """
    Definition of class DimensioningExample
    """

    def __init__(self, doc):
        """
        Initialization of class DimensioningExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = []
        self.document       = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        #----------------- Extract palette parameter values

        length = build_ele.Length.value
        height = build_ele.Height.value


        #------------------ Define the elements

        dim_points = AllplanGeo.Point3DList()

        polyline = AllplanGeo.Polyline2D()
        polyline += AllplanGeo.Point2D()

        for i in range(1,5):
            polyline += AllplanGeo.Point2D(length * i,height * (i - 1))
            polyline += AllplanGeo.Point2D(length * i,height * i)

        for i in range(0,polyline.Count()):
            dim_points.append(AllplanGeo.Point3D(polyline[i]))


        #------------------ Define common properties, take global Allplan settings

        common_prop = AllplanBaseElements.CommonProperties()
        common_prop.GetGlobalProperties()

        dim_prop = AllplanBasisElements.DimensionProperties(self.document, AllplanBasisElements.Dimensioning.eDimensionLine)

        dim_prop.TextHeightDimensionNumber = 3
        dim_prop.FontIDDimensionNumber     = 3
        dim_prop.LeadingCharacter          = "lead "
        dim_prop.TailingCharacters         = " tail"
        dim_prop.TextLocation              = AllplanBasisElements.TextLocation.eBASIS_DIM_TOP_CENTER

        dim_line_x = AllplanBasisElements.DimensionLineElement(dim_points, AllplanGeo.Vector2D(0, -1500),
                                                               AllplanGeo.Vector2D(1000, 0), dim_prop)

        dim_prop.LeadingCharacter          = ""
        dim_prop.TailingCharacters         = ""

        dim_line_y = AllplanBasisElements.DimensionLineElement(dim_points, AllplanGeo.Vector2D(-1500, 0),
                                                               AllplanGeo.Vector2D(0, 1000), dim_prop)

        dim_line_x.SetCommonProperties(common_prop)
        dim_line_y.SetCommonProperties(common_prop)

        elevation_prop = AllplanBasisElements.DimensionProperties(self.document, AllplanBasisElements.Dimensioning.eElevation)

        elevation_prop.TextHeightDimensionNumber = 3
        elevation_prop.FontIDDimensionNumber     = 3
        elevation_prop.PointSymbol               = 1001
        elevation_prop.ElevationBaseOffset       = 5000
        elevation_prop.IsAbsoluteElevation       = False

        elevation_x = AllplanBasisElements.ElevationElement(dim_points, AllplanGeo.Vector2D(0, -500),
                                                            AllplanGeo.Vector2D(1000, 0), elevation_prop)

        elevation_prop.PointSymbol         = 1051
        elevation_prop.ElevationBaseOffset = 8000
        elevation_prop.TextOffset          = 2

        elevation_y = AllplanBasisElements.ElevationElement(dim_points, AllplanGeo.Vector2D(-500, 0),
                                                            AllplanGeo.Vector2D(0, 1000), elevation_prop)

        elevation_x.SetCommonProperties(common_prop)
        elevation_y.SetCommonProperties(common_prop)


        #------------------ Append 2D line as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.ModelElement2D(common_prop, polyline))
        self.model_ele_list.append(dim_line_x)
        self.model_ele_list.append(dim_line_y)
        self.model_ele_list.append(elevation_x)
        self.model_ele_list.append(elevation_y)

        return (self.model_ele_list, self.handle_list)
