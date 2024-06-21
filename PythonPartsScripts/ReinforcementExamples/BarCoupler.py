"""
Script for the general reinforcement shape builder example
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.MeshPlacementBuilder as MeshPlacementBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles


print('Load BarCoupler.py')


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

    return ([], [])


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    print("create interactor !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    return BarCoupler(coord_input, pyp_path, str_table_service)


class BarCoupler():
    """
    Definition of class BarCoupler
    """

    def __init__(self,  coord_input, pyp_path, str_table_service):
        """
        Initialization of class BarCoupler

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service
        self.concrete_cover    = 20.

        self.longitudinal_shape()


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """
        return


    def process_mouse_msg(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        return False


    def longitudinal_shape(self):
        """
        Create the reinforcement and the bar coupler
        """

        model_angles = RotationAngles(0, 0 , 90)

        steel_grade = AllplanReinf.ReinforcementSettings.GetSteelGrade()

        shape_props = ReinforcementShapeProperties.rebar(40, 4, steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        concrete_cover_props = ConcreteCoverProperties.left_right_bottom(self.concrete_cover * 2,
                                                                         self.concrete_cover * 2,
                                                                         self.concrete_cover)

        shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(5000,
                                                                         model_angles,
                                                                         shape_props,
                                                                         concrete_cover_props, -1, -1)

        model_ele_list = [LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, shape,
                                                                                       AllplanGeo.Point3D(), AllplanGeo.Point3D(2000, 0, 0),
                                                                                       0, 0, 200)]

        doc = self.coord_input.GetInputViewDocument()

        created_elements = AllplanBaseElements.CreateElements(doc,AllplanGeo.Matrix3D(), model_ele_list, [], None)

        #AllplanBaseElements.CreateBarCoupler(doc, created_elements, "SAH\\SAS500", "SAH Muffenstäbe", "Standardmuffen T3003", "T3003-40", False)

        AllplanBaseElements.CreateBarCoupler(doc, created_elements, "Erico\\Erico 2013", "LENTON - Schraubmuffen",
                                                                    "Reduziermuffen A12N", "EL4034A12N", True)

        AllplanBaseElements.CreateBarCoupler(doc, created_elements, "Erico\\Erico 2013", "LENTON - Schraubmuffen",
                                                                    "Reduziermuffen P14LN", "EL4030P14LN", False)
