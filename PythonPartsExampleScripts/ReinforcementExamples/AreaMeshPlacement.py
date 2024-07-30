"""
Script for the general reinforcement shape builder example
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPart import View2D3D, PythonPart

print('Load AreaMeshPlacement.py')


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = AreaMeshPlacement(doc)

    return element.create(build_ele)


class AreaMeshPlacement():
    """
    Definition of class AreaMeshPlacement
    """

    def __init__(self, doc):
        """
        Initialisation of class AreaMeshPlacement

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

        self.area_mesh_placement(build_ele)

        return (self.model_ele_list, self.handle_list)


    def area_mesh_placement(self, build_ele):
        """
        Create the plane mesh placement
        """

        outer_polygon = AllplanGeo.Polygon3D()

        if build_ele.CornerRecessLength.value and build_ele.CornerRecessWidth.value:
            outer_polygon += AllplanGeo.Point3D(0, build_ele.CornerRecessWidth.value, 0)
            outer_polygon += AllplanGeo.Point3D(build_ele.CornerRecessLength.value, build_ele.CornerRecessWidth.value, 0)
            outer_polygon += AllplanGeo.Point3D(build_ele.CornerRecessLength.value, 0, 0)
        else:
            outer_polygon += AllplanGeo.Point3D()

        outer_polygon += AllplanGeo.Point3D(build_ele.Length.value, 0, 0)
        outer_polygon += AllplanGeo.Point3D(build_ele.Length.value, build_ele.Width.value, 0)
        outer_polygon += AllplanGeo.Point3D(0, build_ele.Width.value, 0)
        outer_polygon += outer_polygon.StartPoint

        pnt = build_ele.OpeningPosition.value

        opening_polygon = AllplanGeo.Polygon3D()

        opening_polygon += pnt
        opening_polygon += pnt + AllplanGeo.Point3D(build_ele.OpeningLength.value, 0, 0)
        opening_polygon += pnt + AllplanGeo.Point3D(build_ele.OpeningLength.value, build_ele.OpeningWidth.value, 0)
        opening_polygon += pnt + AllplanGeo.Point3D(0, build_ele.OpeningWidth.value, 0)
        opening_polygon += pnt
        
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.HelpConstruction = True

        views = [View2D3D([AllplanBasisElements.ModelElement3D(com_prop, outer_polygon),
                           AllplanBasisElements.ModelElement3D(com_prop, opening_polygon)])]


        #----------------- create the placement

        area_props                       = AllplanReinf.MeshAreaPlacementProperties()
        area_props.StartLength           = build_ele.StartLength.value
        area_props.StartWidth            = build_ele.StartWidth.value
        area_props.OverlapLongitudinal   = build_ele.OverlapLongitudinal.value
        area_props.OverlapCross          = build_ele.OverlapCross.value
        area_props.MeshSizeRound         = build_ele.MeshSizeRound.value
        area_props.PlacementEndJustified = build_ele.PlacementEndJustified.value
        area_props.PlacementStartChange  = build_ele.PlacementStartChange.value
        area_props.LapJointOffset        = build_ele.LapJointOffset.value
        area_props.PlacementDirection    = AllplanReinf.MeshAreaPlacementProperties.MeshPlacementDirection.Cross if build_ele.PlacementDirection.value == 1 else \
                                           AllplanReinf.MeshAreaPlacementProperties.MeshPlacementDirection.Longitudinal

        area_mesh_placement = AllplanReinf.MeshAreaPlacementService()
        area_mesh_placement.SetOuterPolygon(outer_polygon, build_ele.ConcreteCoverBorder.value)

        if build_ele.OpeningLength.value and build_ele.OpeningWidth.value:
            area_mesh_placement.AddOpeningPolygon(opening_polygon, build_ele.OpeningConcreteCover.value)

        placement_angle = AllplanGeo.Angle()
        placement_angle.SetDeg(build_ele.PlacementAngle.value)

        placement_vec = AllplanGeo.Rotate(AllplanGeo.Vector2D(1000, 0), placement_angle);

        mesh_data = AllplanReinf.ReinforcementShapeBuilder.GetMeshData(build_ele.MeshType.value)

        placement_axis = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(), AllplanGeo.Vector3D(placement_vec), AllplanGeo.Vector3D(0, 0, 1000))

        reinf_ele_list = area_mesh_placement.Calculate(self.document, mesh_data, area_props, placement_axis.GetTransformationMatrix(),
                                                       1, build_ele.ConcreteCoverZDir.value)


        pythonpart = PythonPart("AreaMeshPlacement",
                                parameter_list = build_ele.get_params_list(),
                                hash_value     = build_ele.get_hash(),
                                python_file    = build_ele.pyp_file_name,
                                views          = views,
                                reinforcement  = reinf_ele_list)

        self.model_ele_list = pythonpart.create()
