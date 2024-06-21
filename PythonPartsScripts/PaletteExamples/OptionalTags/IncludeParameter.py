""" Example script for include controls
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.IncludeParameterBuildingElement \
        import IncludeParameterBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load IncludeParameter.py')


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
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = IncludeParameter(doc)

    return element.create(build_ele)


class IncludeParameter():
    """ Definition of class Visibility
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class Visibility

        Args:
            doc: document of the Allplan drawing files
        """
        self.document       = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            tuple  with created elements and handles.
        """

        if build_ele.InitCoord.value:
            build_ele.InitCoord.value = False

            for i in range(1, 21):
                getattr(build_ele, f"XCoord{i}").value = 2000 * (i + 1)
                getattr(build_ele, f"YCoord{i}").value = 2000 * (i + 1)

        model_list = ModelEleList()

        xref = 0.
        xref = self.create_polyhedron(model_list, xref,
                                      build_ele.LengthLeft.value, build_ele.WidthLeft.value, build_ele.HeightLeft.value)
        xref = self.create_polyhedron(model_list, xref,
                                      build_ele.Length2.value, build_ele.Width2.value, build_ele.Height2.value)
        xref = self.create_polyhedron(model_list, xref,
                                      build_ele.Length3.value, build_ele.Width3.value, build_ele.Height3.value)
        xref = self.create_polyhedron(model_list, xref,
                                      build_ele.Length4.value, build_ele.Width4.value, build_ele.Height4.value)
        xref = self.create_polyhedron(model_list, xref,
                                      build_ele.LengthRight.value, build_ele.WidthRight.value, build_ele.HeightRight.value)


        #----------------- create the polyhedron by count

        for i in range(1, build_ele.CoordCount.value + 1):
            xref = getattr(build_ele, f"XCoord{i}").value
            yref = getattr(build_ele, f"YCoord{i}").value

            polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(xref, yref, 0),
                                                           AllplanGeo.Point3D(xref + build_ele.LengthRight.value,
                                                                              yref + build_ele.WidthRight.value,
                                                                              build_ele.HeightRight.value))

            model_list.append_geometry_3d(polyhed)


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    @staticmethod
    def create_polyhedron(model_list: ModelEleList,
                          xref      : float,
                          length    : float,
                          width     : float,
                          height    : float) -> float:
        """ Create the polyhedron

        Args:
            model_list: model element list
            xref:       x reference point
            length:     length
            width:      width
            height:     height

        Returns:
            new x reference point
        """

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(xref, 0, 0),
                                                       AllplanGeo.Point3D(xref + length, width, height))

        model_list.append_geometry_3d(polyhed)

        return xref + length + 1000.
