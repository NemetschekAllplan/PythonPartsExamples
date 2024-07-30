""" Example script for showing a plane connection
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from HandleParameterType import HandleParameterType
from HandleParameterData import HandleParameterData

from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PlaneConnectionBuildingElement import PlaneConnectionBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
            version is supported state
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the library preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_libary_bitmap_preview( \
                                    AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                                    r"Examples\PythonParts\BasisExamples\PlaneConnection.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = PlaneConnection(doc)

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

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class PlaneConnection():
    """ Definition of class PlaneConnection
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class PlaneConnection

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        plane_ref = build_ele.PlaneReferences.value

        abs_bottom_elevation = plane_ref.GetAbsBottomElevation()
        abs_top_elevation    = plane_ref.GetAbsTopElevation()

        if (height := abs_top_elevation - abs_bottom_elevation) < 1:
            height = 1000

        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Width.value, build_ele.Depth.value, height)
        cuboid_geo = AllplanGeo.Move(cuboid_geo, AllplanGeo.Vector3D(0, 0, abs_bottom_elevation))

        com_prop = AllplanBaseEle.CommonProperties()
        com_prop.GetGlobalProperties()

        cuboid = AllplanBasisEle.ModelElement3D(com_prop, cuboid_geo)

        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(cuboid)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),
                                   self.create_handles(build_ele))


    def create_handles(self,
                       build_ele: BuildingElement) -> List[HandleProperties]:
        """ Create the column handles

        Args:
            build_ele: building element with the parameter properties

        Returns:
            list with the handles
        """

        abs_bottom_elevation = \
            AllplanArchElements.BottomTopPlaneService.GetAbsoluteBottomElevation(AllplanEleAdapter.BaseElementAdapter(),
                                                                                 self.document,
                                                                                 build_ele.PlaneReferences.value)

        ref_pnt    = AllplanGeo.Point3D(0, 0, abs_bottom_elevation)
        handle_pnt = AllplanGeo.Point3D(build_ele.Width.value, build_ele.Depth.value, abs_bottom_elevation)

        handle1 = HandleProperties("UpperRightCorner",
                                   handle_pnt, ref_pnt,
                                   [HandleParameterData("Width", HandleParameterType.X_DISTANCE),
                                    HandleParameterData("Depth", HandleParameterType.Y_DISTANCE)],
                                   HandleDirection.XY_DIR)

        return [handle1]
