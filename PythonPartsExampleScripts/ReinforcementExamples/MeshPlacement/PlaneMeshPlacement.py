"""Script for the plane mesh placement
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_Utility as AllplanUtil

from CreateElementResult import CreateElementResult

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PlaneMeshPlacementBuildingElement \
        import PlaneMeshPlacementBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PlaneMeshPlacement.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
            version is supported state
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = PlaneMeshPlacement(doc)

    return element.create(build_ele)


class PlaneMeshPlacement():
    """ Definition of class PlaneMeshPlacement
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class PlaneMeshPlacement

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

        self.plane_mesh_placement(build_ele)

        return CreateElementResult(self.model_ele_list)


    def plane_mesh_placement(self,
                             build_ele: BuildingElement):
        """ Create the plane mesh placement

        Args:
            build_ele: building element with the parameter properties
        """

        mesh_polygon = AllplanGeo.Polygon3D()

        mesh_data = AllplanReinf.ReinforcementShapeBuilder.GetMeshData(build_ele.MeshType.value)

        self.model_ele_list = []

        if build_ele.Width.value > mesh_data.Width:
            AllplanUtil.ShowMessageBox("Width > Mesh width", AllplanUtil.MB_OK)
            return

        if build_ele.Length.value > mesh_data.Length:
            AllplanUtil.ShowMessageBox("Length > Mesh length", AllplanUtil.MB_OK)
            return

        if build_ele.CornerRecessLength.value and build_ele.CornerRecessWidth.value:
            mesh_polygon += AllplanGeo.Point3D(0, build_ele.CornerRecessWidth.value, 0)
            mesh_polygon += AllplanGeo.Point3D(build_ele.CornerRecessLength.value, build_ele.CornerRecessWidth.value, 0)
            mesh_polygon += AllplanGeo.Point3D(build_ele.CornerRecessLength.value, 0, 0)
        else:
            mesh_polygon += AllplanGeo.Point3D()

        mesh_polygon += AllplanGeo.Point3D(build_ele.Length.value, 0, 0)
        mesh_polygon += AllplanGeo.Point3D(build_ele.Length.value, build_ele.Width.value, 0)
        mesh_polygon += AllplanGeo.Point3D(0, build_ele.Width.value, 0)
        mesh_polygon += mesh_polygon.StartPoint

        plane_mesh_placement = AllplanReinf.PlaneMeshPlacement(1, mesh_data,
                                                               build_ele.Length.value, build_ele.Width.value,
                                                               mesh_polygon)

        reinf_com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        reinf_com_prop.Color = build_ele.PreviewColor.value

        plane_mesh_placement.CommonProperties = reinf_com_prop

        self.model_ele_list = [plane_mesh_placement]
