"""
Example Script for Combobox with localized string values
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElementStringTable import BuildingElementStringTable
from BuildingElement import BuildingElement
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil
from TraceService import TraceService

TraceService.trace_1('Load ComboboxLocalisedStringValues.py')


def check_allplan_version(build_ele: BuildingElement,
                          version:   float):
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


def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = ComboBoxExample(doc)

    return element.create(build_ele)


def move_handle(build_ele: BuildingElement,
                handle_prop: HandleProperties,
                input_pnt: AllplanGeo.Point3D,
                doc: AllplanElementAdapter.DocumentAdapter):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    element = ComboBoxExample(doc)

    return element.create(build_ele)


class ComboBoxExample():
    """
    Definition of class ComboBoxExample
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class ComboBoxExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = None
        self.document       = doc


    @staticmethod
    def __get_color_by_string__(color_for_quader: int,
                                local_str_table: BuildingElementStringTable,
                                global_str_table: BuildingElementStringTable):
        """
        Calculates the depending on inputvalue and the content of string tables

        Args:
             color_for_quader       : localized string value
             local_str_table        : local string table
             global_str_table       : global string table

        Returns:
            int value for color
        """

        #<ValueList>red|green|blue</ValueList>
        #<ValueList_TextIds>1001|1002|1003</ValueList_TextIds>

        text_id_possible = [1001,1002,1003]

        text_id_used = 0
        ret_col      = 0

        for elem in text_id_possible:
            res_str, res  = local_str_table.get_entry(str(elem))

            if res is True:
                if res_str == color_for_quader:
                    text_id_used = elem
                    break

            res_str, res  = global_str_table.get_entry(str(elem))

            if res is True:
                if res_str == color_for_quader:
                    text_id_used = elem
                    break

        if text_id_used == 1001:
            ret_col = 6 # 1001 stands for red
        elif text_id_used == 1002:
            ret_col = 4 # 1002 stands for green
        elif text_id_used == 1003:
            ret_col = 7 # 1002 stands for blue
        else:
            text_id_used = 0

        return ret_col


    def create(self,
               build_ele: BuildingElement):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        self.create_geometry(build_ele)

        return (self.model_ele_list, self.handle_list)


    def create_geometry(self,
                        build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette parameter values

        length = 1000

        color_for_quader = build_ele.Color_for_quader.value

        TraceService.trace_1(color_for_quader)


        #------------------ Define the cube polyhedron

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        local_str_table, global_str_table = build_ele.get_string_tables()

        com_prop.Color = self.__get_color_by_string__(color_for_quader, local_str_table, global_str_table)

        if com_prop.Color == 0:
            str_msg = 'No localisation available.\n'
            str_msg += 'This PythonPart can only run correct with a valid localisation file.\n'
            str_msg += 'No geometry will be created.'
            AllplanUtil.ShowMessageBox(str_msg, AllplanUtil.MB_OK)
            TraceService.trace_1('Could not evaluate comprop.color. No localisation available?')


        #------------------ Append cubes as new Allplan elements

        if com_prop.Color == 0:
            self.model_ele_list = []
        else:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, polyhed))

            self.model_ele_list = pyp_util.create_pythonpart(build_ele)


        #------------------ No handles

        self.handle_list = []
