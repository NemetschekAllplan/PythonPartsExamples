""" Example script for using the general reinforcement creator that generates meshes
"""


from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult, ReinforcementRearrange
from PythonPartUtil import PythonPartUtil

from TypeCollections import ModelEleList

from Utils.RotationUtil import RotationUtil

from StdReinfShapeBuilder import GeneralReinfShapeBuilder
from StdReinfShapeBuilder import MeshPlacementBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties

if TYPE_CHECKING:
    from __BuildingElementStubFiles.GeneralMeshShapeCreationBuildingElement \
        import GeneralMeshShapeCreationBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


print('Load GeneralMeshShapeCreation.py')


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

    element = GeneralMeshShapeCreation(doc, build_ele)


    element = GeneralMeshShapeCreation(doc, build_ele)

    return element.create(build_ele)


class GeneralMeshShapeCreation():
    """ Definition of class GeneralMeshShapeCreation
    """

    def __init__(self,
                 doc      : AllplanEleAdapter.DocumentAdapter,
                 build_ele: BuildingElement):
        """ Initialization of class GeneralMeshShapeCreation

        Args:
            doc:       document of the Allplan drawing files
            build_ele: building element with the parameter properties
        """

        self.model_ele_list = ModelEleList()
        self.reinf_ele_list = ModelEleList()
        self.document       = doc

        self.concrete_cover         = build_ele.ConcreteCover.value
        self.concrete_grade         = build_ele.ConcreteGrade.value
        self.steel_grade            = build_ele.SteelGrade.value
        self.mesh_type              = build_ele.MeshType.value
        self.mesh_type_diamond      = build_ele.MeshTypeDiamond.value
        self.bending_roller         = build_ele.BendingRoller.value


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        self.mesh_stirrups()

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)
        pyp_util.add_reinforcement_elements(self.reinf_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele),
                                   reinf_rearrange = ReinforcementRearrange(build_ele.Rearrange.value))


    def mesh_stirrups(self):
        """ Create the reinforcement by using mesh stirrups
        """

        #------------------ Create the polyhedron

        width  = 8000
        length = 500
        height = 1000

        size = AllplanGeo.Vector3D(length, width, height)

        ref_pnt = AllplanGeo.Point3D(0, 0, 0)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt, ref_pnt + size)

        self.model_ele_list.append_geometry_3d(polyhed)


        #----------------- create the stirrups with mesh

        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        model_angles = RotationUtil(90, 0 , 0)

        concrete_cover_props = ConcreteCoverProperties.all(self.concrete_cover)

        shapes = []

        shape_props = ReinforcementShapeProperties.mesh(self.mesh_type, mesh_bending_dir,
                                                        self.bending_roller, self.concrete_grade,
                                                        AllplanReinf.BendingShapeType.Stirrup)

        shapes.append(GeneralReinfShapeBuilder.create_stirrup(length, height,model_angles,shape_props, concrete_cover_props,
                                                              AllplanReinf.StirrupType.Normal))

        shapes.append(GeneralReinfShapeBuilder.create_stirrup(length, height, model_angles, shape_props, concrete_cover_props,
                                                              AllplanReinf.StirrupType.Torsion))

        shape_props = ReinforcementShapeProperties.mesh(self.mesh_type_diamond, mesh_bending_dir,
                                                        self.bending_roller, self.concrete_grade,
                                                        AllplanReinf.BendingShapeType.Stirrup)

        shapes.append(GeneralReinfShapeBuilder.create_stirrup(length, height, model_angles, shape_props, concrete_cover_props,
                                                              AllplanReinf.StirrupType.Diamond))

        value_list = [(shapes[0], 3000),
                      (shapes[1], 2500),
                      (shapes[2], 0)]

        MeshPlacementBuilder.create_mesh_placement_by_points(value_list,
                                                             ref_pnt,
                                                             ref_pnt + AllplanGeo.Point3D(0, width, 0),
                                                             1,
                                                             self.concrete_cover,
                                                             self.concrete_cover,
                                                             self.reinf_ele_list)
