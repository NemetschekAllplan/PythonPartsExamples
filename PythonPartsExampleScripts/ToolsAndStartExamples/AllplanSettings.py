"""
Example Script for AllplanSettings
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_AllplanSettings as AllplanSettings

from Utilities.AllplanEnvironment import AllplanEnvironment

print('Load AllplanSettings.py')


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
    element = AllplanSettingsExample(doc)

    return element.create(build_ele)


def move_handle(build_ele, handle, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    del handle

    build_ele.change_property(handle_prop, input_pnt)

    element = AllplanSettingsExample(doc)

    return element.create(build_ele)


class AllplanSettingsExample():
    """
    Definition of class AllplanSettingsExample
    """

    def __init__(self, doc):
        """
        Initialisation of class AllplanSettingsExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = None
        self.document = doc
        self.init_string_values = False


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        if not hasattr(build_ele, 'init_string_values'):
            # do evaluation of strings only once
            build_ele.init_string_values = True
            self.evaluate_string_values(build_ele)

        self.create_geometry(build_ele)

        return (self.model_ele_list, self.handle_list)


    def evaluate_string_values(self, build_ele):
        """
        fills the defined string with the values from the AllplanSettings interfaces

        Args:
            build_ele:  the building element.

        Returns:

        """
        build_ele.Path_ETC.value = AllplanSettings.AllplanPaths.GetEtcPath()
        build_ele.Path_STD.value = AllplanSettings.AllplanPaths.GetStdPath()
        build_ele.Curr_Path_PRJ.value = AllplanSettings.AllplanPaths.GetCurPrjPath()
        build_ele.Path_Usr.value = AllplanSettings.AllplanPaths.GetUsrPath()
        build_ele.Path_Tmp.value = AllplanSettings.AllplanPaths.GetTmpPath()
        build_ele.Path_Prg.value = AllplanSettings.AllplanPaths.GetPrgPath()
        build_ele.Language_Allplan.value = AllplanSettings.AllplanLocalisationService.AllplanLanguage()
        build_ele.Language.value = AllplanSettings.AllplanLocalisationService.Language()
        build_ele.Version.value = AllplanSettings.AllplanVersion.Version()

        offset_pnt = AllplanSettings.AllplanGlobalSettings.GetOffsetPoint()

        build_ele.XOffset.value = offset_pnt.X
        build_ele.YOffset.value = offset_pnt.Y
        build_ele.ZOffset.value = offset_pnt.Z

        build_ele.IsDarkTheme.value = AllplanEnvironment.is_dark_mode()

        return


    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        # Delete unused arguments
        del build_ele


        #----------------- Extract palette parameter values

        length = 1000 #fixed value
        #------------------ Define the cube polyhedron

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(length, length, length)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Append for creation as new Allplan elements

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed1))

        polyhed1 = AllplanGeo.Move(polyhed1, AllplanGeo.Vector3D(length * 1.5, 0, 0))


        #------------------ No handles

        self.handle_list = []
