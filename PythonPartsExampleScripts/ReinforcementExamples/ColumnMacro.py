"""
Example Script for MacroPlacements
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.MeshPlacementBuilder as MeshPlacementBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles

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
    element = ColumnMacroExample(doc)

    return element.create(build_ele)


class ColumnMacroExample():
    """
    Definition of class ColumnMacroExample
    """

    def __init__(self, doc):
        """
        Initialisation of class ColumnMacroExample

        Args:
            doc: input document
        """
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        # define macro definition
        macro = self.create_macro(build_ele)

        self.model_ele_list.append(macro)

        # define placement
        self.model_ele_list.append(self.create_macro_placement(macro, AllplanGeo.Vector3D(0, 0, 0), build_ele))

        return (self.model_ele_list, self.handle_list)


    def create_macro_placement(self, macro, transvec, build_ele):
        """
        Create a macro placements referencing the macro definition

        Args:
            macro       macro element
            transvec:   the translation vector for macro placement matrix
            build_ele:  the building element.

        Returns:
            created macro placement.
        """

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()


        #------------------ Define macro placement referencing the macro definition

        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (transvec)
        mp_prop = AllplanBasisElements.MacroPlacementProperties()
        mp_prop.Matrix = matrix

        reinf_list = self.create_reinforcement(build_ele)

        macroplacement = AllplanBasisElements.MacroPlacementElement(com_prop, mp_prop, macro, reinf_list)

        return macroplacement


    def create_macro(self, build_ele):
        """
        Create the macro from the geometry

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        column_width     = build_ele.ColumnWidth.value
        column_thickness = build_ele.ColumnThickness.value
        column_height    = build_ele.ColumnHeight.value


        #------------------ Create the column

        column = AllplanGeo.Polyhedron3D.CreateCuboid(column_width, column_thickness, column_height)

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        ele_list = [AllplanBasisElements.ModelElement3D(com_prop, column)]

        slide = AllplanBasisElements.MacroSlideElement(AllplanBasisElements.MacroSlideProperties(),
                                                       ele_list)

        slide_list = [slide]


        #------------------ Define macro definition

        macro_prop = AllplanBasisElements.MacroProperties()
        macro_prop.Name = "ColumnMacro"
        macro_prop.CatalogName = "STD\\Library" # set to some useful value

        macro = AllplanBasisElements.MacroElement(macro_prop, slide_list)

        return macro

    def create_reinforcement(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #-----------------  Assign the parameter

        column_width = build_ele.ColumnWidth.value
        column_thickness = build_ele.ColumnThickness.value
        column_height = build_ele.ColumnHeight.value

        steel_grade      = 4
        diameter1        = 10
        bending_roller   = 4
        concrete_cover   = 25.
        stirrup_distance = 200.

        concrete_cover_props = ConcreteCoverProperties.all(concrete_cover)

        reinf_ele_list = []


        #----------------- Create the stirrups

        shape_props = ReinforcementShapeProperties.rebar(diameter1, bending_roller, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralShapeBuilder.create_stirrup(column_width, column_thickness,
                                                   RotationAngles(0, 0, 0),
                                                   shape_props, concrete_cover_props)

        if shape.IsValid():
            reinf_ele_list.append(
                LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                    1, shape, AllplanGeo.Point3D(),
                    AllplanGeo.Point3D(0, 0, 1000),
                    concrete_cover, concrete_cover, stirrup_distance))


        #----------------- mesh

        mesh_type        = AllplanReinf.ReinforcementSettings.GetMeshType()
        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        shape_props = ReinforcementShapeProperties.mesh(mesh_type, mesh_bending_dir,
                                                        bending_roller, -1,
                                                        AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralShapeBuilder.create_stirrup(column_width, column_thickness,
                                                   RotationAngles(0, 0, 0),
                                                   shape_props,
                                                   concrete_cover_props)

        if shape.IsValid():
            value_list = [(shape, 0)]

            MeshPlacementBuilder.create_mesh_placement_by_points(value_list,
                                                                 AllplanGeo.Point3D(0, 0, 1000),
                                                                 AllplanGeo.Point3D(0, 0, column_height),
                                                                 1,
                                                                 concrete_cover,
                                                                 concrete_cover,
                                                                 reinf_ele_list)

        return reinf_ele_list
