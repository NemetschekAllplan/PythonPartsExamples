""" Script for ImprintProfileOnFaces
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Utility as AllplanUtil

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ImprintProfileOnFacesBuildingElement \
        import ImprintProfileOnFacesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ImprintProfileOnFaces.py')


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

    return create_element(build_ele, doc)


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = ImprintProfileOnFaces(doc)

    return element.create(build_ele)


class ImprintProfileOnFaces():
    """ Definition of class ImprintProfileOnFaces
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class ImprintProfileOnFaces

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

        cuboid_sizes = build_ele.Cuboid.value

        brep = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(), *cuboid_sizes.Values())


        #----------------- rectangle imprint on the bottom

        x_left = (cuboid_sizes.X - build_ele.Rectangle.value.X) / 2
        y_left = (cuboid_sizes.Y - build_ele.Rectangle.value.Y) / 2

        rect_2d = AllplanGeo.Polygon2D.CreateRectangle(AllplanGeo.Point2D(x_left, y_left),
                                                       AllplanGeo.Point2D(x_left + build_ele.Rectangle.value.X,
                                                                          y_left + build_ele.Rectangle.value.Y))

        result, rect_3d = AllplanGeo.ConvertTo3D(rect_2d)

        if result:
            result, imprint_brep, _faces = AllplanGeo.ImprintProfileOnFaces(brep, AllplanUtil.VecUIntList([4]), rect_3d)

            if result == AllplanGeo.eOK:
                brep = imprint_brep


        #----------------- arc imprint on the top

        result, circle_3d = AllplanGeo.ConvertTo3D(build_ele.Circle.value)

        if result:
            circle_3d = AllplanGeo.Move(circle_3d, AllplanGeo.Vector3D(0, 0, cuboid_sizes.Z))

            result, imprint_brep, _faces = AllplanGeo.ImprintProfileOnFaces(brep, AllplanUtil.VecUIntList([1]), circle_3d)

            if result == AllplanGeo.eOK:
                brep = imprint_brep


        #----------------- polyline imprint on the left

        circle_3d = AllplanGeo.Move(circle_3d, AllplanGeo.Vector3D(0, 0, cuboid_sizes.Z))

        result, imprint_brep, _faces = AllplanGeo.ImprintProfileOnFaces(brep, [4], build_ele.Polyline.value)

        if result == AllplanGeo.eOK:
            brep = imprint_brep

        model_ele_list.append_geometry_3d(brep)


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
