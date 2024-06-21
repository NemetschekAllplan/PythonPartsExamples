"""
Script for WallGeometryInteractor
"""

import math

import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_Input as AllplanIFW

from TraceService import TraceService

print('Load WallGeometryInteractor.py')


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
    Creation of element (only necessary for the library preview)

    Args:
        build_ele: the building element.
        doc:       input document
    """

    del build_ele
    del doc

    return (None, None, None)


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return WallGeometryInteractor(coord_input, pyp_path, str_table_service)


class WallGeometryInteractor():
    """
    Definition of class WallGeometryInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class WallGeometryInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service
        self.first_point_input = True
        self.first_point       = AllplanGeo.Point3D()

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Select the wall"))

        type_query = AllplanIFW.QueryTypeID(AllplanElementAdapter.WallTier_TypeUUID)

        sel_query = AllplanIFW.SelectionQuery(type_query)

        self.element_filter = AllplanIFW.ElementSelectFilterSetting(sel_query, True)


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        return True


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

        self.coord_input.SelectElement(mouse_msg, pnt, msg_info, False, True, True, self.element_filter)

        wall_tier = self.coord_input.GetSelectedElement()

        if wall_tier.IsNull():
            return True

        error, polygon, normal_vec = self.coord_input.SelectWallFace(wall_tier, pnt, True)


        if self.coord_input.IsMouseMove(mouse_msg):
            return True

        print("##############################################################################################################")
        print()
        print("Normal vector:", normal_vec)
        print()
        print("Face polygon:\n\n", polygon)
        print()

        wall = AllplanElementAdapter.BaseElementAdapterParentElementService.GetParentElement(wall_tier)


        #----------------- wall tiers

        wall_tiers = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetTierElements(wall)

        for wall_tier in wall_tiers:
            print()
            TraceService.trace_1(str(wall_tier) + ":")
            print()
            print("Ground view geometry:\n\n", wall_tier.GetGeometry())
            print()
            print("Model geometry:\n\n", wall_tier.GetModelGeometry())
            print()


        #----------------- wall axis

        for wall_child in AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(wall_tiers[0]):
            if wall_child == AllplanElementAdapter. WallAxis_TypeUUID:
                axis_childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(wall_child)

                for axis_child in axis_childs:
                    if axis_child == AllplanElementAdapter.WallAxisLine_TypeUUID:
                        print()
                        TraceService.trace_1(str(axis_child) + ":")
                        print()
                        print("Axis:", axis_child.GetGeometry())
                        print()
                        break


        #----------------- openings

        wall_tier_childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(wall_tier)

        opening_tiers = filter(lambda child: child == AllplanElementAdapter.WindowTier_TypeUUID  or  \
                                             child == AllplanElementAdapter.DoorTier_TypeUUID, wall_tier_childs)

        openings = map(lambda opening_tier: AllplanElementAdapter.BaseElementAdapterParentElementService.GetParentElement(opening_tier), opening_tiers)

        for opening in openings:
            TraceService.trace_1(str(opening) + ":")
            print()

            opening_childs = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(opening)

            for opening_child in opening_childs:
                if opening_child == AllplanElementAdapter.WindowTier_TypeUUID  or  opening_child == AllplanElementAdapter.DoorTier_TypeUUID:
                    TraceService.trace_1(str(opening_child) + ":")
                    print()
                    print("Ground view geometry:\n\n", opening_child.GetGeometry())
                    print()
                    print("Model geometry:\n\n", opening_child.GetModelGeometry())
                    print

        print()
        print()

        return True
