"""
Script for GetObjectAttributesInteractor
"""

# pylint: disable=too-many-nested-blocks

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BuildingElementService import BuildingElementService
from BuildingElementPaletteService import BuildingElementPaletteService
from TraceService import TraceService

print('Load GetObjectAttributesInteractor.py')


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


def get_listed_elements(coord_input, id_list):
    """ read the model to get all bar data """

    print("#######################")
    print("GETTING LISTED ELEMENTS")
    print("#######################")

    validElement = [AllplanElementAdapter.BarsLinearPlacement_TypeUUID,
                      AllplanElementAdapter.BarsCircularPlacement_TypeUUID,
                      AllplanElementAdapter.BarsLinearMultiPlacement_TypeUUID,
                      AllplanElementAdapter.BarsLinearPlacement_TypeUUID,
                      AllplanElementAdapter.BarsLinearPlacement_TypeUUID,
                      AllplanElementAdapter.BarsRotationalPlacement_TypeUUID,
                      AllplanElementAdapter.BarsRotationalSolidPlacement_TypeUUID,
                      AllplanElementAdapter.BarsSpiralPlacement_TypeUUID,
                      AllplanElementAdapter.BarsTangentionalPlacement_TypeUUID,
                      AllplanElementAdapter.BarsAreaRepresentation_TypeUUID,
                      AllplanElementAdapter.BarsRepresentation_TypeUUID,
                      AllplanElementAdapter.BarsRepresentationLine_TypeUUID,
                      AllplanElementAdapter.MeshRepresentation_TypeUUID,
                      AllplanElementAdapter.BarsAreaRepresentationLine_TypeUUID,
                      AllplanElementAdapter.MeshAreaRepresentation_TypeUUID]

    ele_list = AllplanElementAdapter.BaseElementAdapterList()
    print("Searching for elements")

    for id in id_list:
        print(id)

    for element in AllplanBaseElements.ElementsSelectService.SelectAllElements(
            coord_input.GetInputViewDocument()):
        # find bar definition

        if element == AllplanElementAdapter.BarsDefinition_TypeUUID:
            children = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(
                element)

            for child in children:
                if child in validElement:
                    atts = dict(AllplanBaseElements.ElementsAttributeService.GetAttributes(child))

                    if 683 in atts:
                        bar_id = str(atts[683])
                        print(bar_id)

                        if str(id_list) == "":
                            ele_list.append(child)
                            grandChildren = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(child)
                            for grandChild in grandChildren:
                                if grandChild in validElement:
                                    ele_list.append(grandChild)
                            print("Element found " + bar_id)
                        else:
                            for id in id_list:
                                if str(bar_id) in str(id):
                                    ele_list.append(child)
                                    grandChildren = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(child)
                                    for grandChild in grandChildren:
                                        if grandChild in validElement:
                                            ele_list.append(grandChild)
                                    print("Element found " + bar_id)

    return ele_list

def create_interactor(coord_input, pyp_path, show_pal_close_btn, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return GetObjectAttributesInteractor(coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list)


class GetObjectAttributesInteractor():
    """
    Definition of class GetObjectAttributesInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
        """
        Initialization of class GetObjectAttributesInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        ele_list = get_listed_elements(coord_input, "")

        AllplanIFW.HighlightService.HighlightElements(ele_list)
        AllplanBaseElements.DrawingService.RedrawAll(coord_input.GetInputViewDocument())


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

        #self.palette_service.close_palette()

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

        return True
