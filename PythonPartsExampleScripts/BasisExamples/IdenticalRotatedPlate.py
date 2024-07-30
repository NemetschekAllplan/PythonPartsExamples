"""
The example script shows:

- how to exclude transformation parameter from the "Identical PythonPart check"
- how to create an additional placement matrix from these transformation parameter
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from Utils import RotationUtil

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   _doc     : AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        _doc:      input document
    """

    com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    plate = AllplanGeo.Polyhedron3D.CreateCuboid(build_ele.Length.value,
                                                 build_ele.Width.value,
                                                 build_ele.Thickness.value)


    #--------------------- the rotation is included in a local placement matrix

    local_placement_mat = RotationUtil(build_ele.RotationAngleX.value,
                                       build_ele.RotationAngleY.value,
                                       build_ele.RotationAngleZ.value).get_rotation_matrix()


    #--------------------- create the PythonPart

    pyp_util = PythonPartUtil()

    pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, plate))

    return CreateElementResult(pyp_util.create_pythonpart(build_ele, local_placement_mat),
                               multi_placement = True)
