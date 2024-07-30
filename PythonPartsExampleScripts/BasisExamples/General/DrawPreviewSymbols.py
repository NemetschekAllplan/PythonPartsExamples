""" Example script for DrawPreviewSymbols
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import math

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from CreateElementResult import CreateElementResult
from PreviewSymbols import PreviewSymbols
from PythonPartUtil import PythonPartUtil

from Utils import TextReferencePointPosition

if TYPE_CHECKING:
    from __BuildingElementStubFiles.DrawPreviewSymbolsBuildingElement \
        import DrawPreviewSymbolsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load DrawPreviewSymbols.py')


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


def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = DrawPreviewSymbols(doc)

    return element.create(build_ele)


class DrawPreviewSymbols():
    """ Definition of class Visibility
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """ Initialization of class Visibility

        Args:
            doc: document of the Allplan drawing files
        """

        self.model_ele_list = []
        self.document       = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(3000, 2000, 1000)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)


        #----------------- create the preview symbols

        preview_symbols = PreviewSymbols()

        polyline = AllplanGeo.Polyline2D([AllplanGeo.Point2D(-10, -10),
                                          AllplanGeo.Point2D(10, -10),
                                          AllplanGeo.Point2D(10, 10),
                                          AllplanGeo.Point2D(-10, 10),
                                          AllplanGeo.Point2D(-10, -10)])

        color = AllplanBasisElements.ARGB(build_ele.ColorID.value)

        print(build_ele.ColorID.value)

        if build_ele.PreviewSymbol.value == "Circle":
            preview_symbols.add_circle(AllplanGeo.Point3D(3000, 2000, 1000),
                                       build_ele.Radius.value, color)

        elif build_ele.PreviewSymbol.value == "Polyline":
            preview_symbols.add_polyline(AllplanGeo.Point3D(3000, 2000, 1000), polyline, color, 0xffff)

        elif build_ele.PreviewSymbol.value == "Cross":
            preview_symbols.add_cross(AllplanGeo.Point3D(3000, 2000, 1000), build_ele.CrossSize.value, color)

        elif build_ele.PreviewSymbol.value == "Mark":
            preview_symbols.add_mark(AllplanGeo.Point3D(3000, 2000, 1000), build_ele.MarkSize.value, color)

        elif build_ele.PreviewSymbol.value == "Coordinate cross":
            preview_symbols.add_coord_cross(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(1500, 1000, 500),
                                                                       AllplanGeo.Vector3D(100, 0, 0),
                                                                       AllplanGeo.Vector3D(0, 0, 100)),
                                            build_ele.ArmSize.value)

        elif build_ele.PreviewSymbol.value == "Text":
            preview_symbols.add_text("Text", AllplanGeo.Point3D(3000, 2000, 1000),
                                     TextReferencePointPosition.CENTER_CENTER,
                                     build_ele.TextHeight.value, color,
                                     AllplanGeo.Angle(math.radians(build_ele.RotationAngle.value)))

        elif build_ele.PreviewSymbol.value == "Arrow":
            preview_symbols.add_arrow(AllplanGeo.Point3D(3000, 2000, 1000),
                                      build_ele.ArrowSize.value, color,
                                      AllplanGeo.Angle(math.radians(build_ele.RotationAngle.value)))

        elif build_ele.PreviewSymbol.value == "Filled rectangle":
            preview_symbols.add_filled_rectangle(AllplanGeo.Point3D(3000, 2000, 1000),
                                                 build_ele.RectSize.value, color,
                                                 AllplanGeo.Angle(math.radians(build_ele.RotationAngle.value)))


        #----------------- return the result

        return CreateElementResult(self.model_ele_list, preview_symbols = preview_symbols)
