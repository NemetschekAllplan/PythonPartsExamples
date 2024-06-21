""" Example Script for PrecastElements
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElementControlProperties import BuildingElementControlProperties
from PythonPartUtil import PythonPartUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PrecastElementsBuildingElement import PrecastElementsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

# Print some information
print('Load PrecastElements.py')


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
                   doc      : AllplanEleAdapter.DocumentAdapter):
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files
    """
    element = PrecastElementsExample(doc)

    return element.create(build_ele)


def modify_control_properties(build_ele : BuildingElement,
                              _con_props: BuildingElementControlProperties,
                              name      : str,
                              _value    : Any,
                              _doc      : AllplanEleAdapter.DocumentAdapter):
    """ Modify property of element

    Args:
        build_ele:  building element with the parameter properties
        _con_props: control properties
        name:       the name of the property.
        _value:     new value for property.
        _doc:       document of the Allplan drawing files
    """

    return fill_layers(build_ele, name)


def fill_layers(build_ele: BuildingElement,
                name     : str):
    """ Fill layers of precastElementType

    Args:
        build_ele: building element with the parameter properties
        name:      the name of the property.
    """

    if build_ele.Element.value == 1:
        build_ele.Layer.value = []
        return True

    if name[0:name.find("[")] != "Layer" and name != "Element":
        return False

    start_values = name.find("[")
    end_values   = name.find("]")

    if start_values > 0:
        prop_name = name[0 : start_values]
        val_idx   = int(name[start_values + 1 : end_values])

        tmp = build_ele.get_existing_property(prop_name)

        if name.find("(1)") < 0:
            tmp.value[val_idx] = tuple([tmp.value[val_idx][0],
                                        tmp.value[val_idx][1],
                                        tmp.value[val_idx][2],
                                        tmp.value[val_idx][2] + "Cat(" + tmp.value[val_idx][3] + ")"])
        return True

    if build_ele.Element.selected_value != "":
        layers = build_ele.Element.selected_value.split(";")

        values = []

        for layer in layers:
            parameters = layer[1:len(layer) - 1].split("|")
            values.append(tuple([parameters[0], parameters[1], parameters[2], parameters[3]]))

        build_ele.Layer.value = values

        return True

    return False


class PrecastElementsExample():
    """
    Definition of class PrecastElementsExample
    """

    def __init__(self,
                 doc : AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class PrecastElementsExample

        Args:
            doc:  document of the Allplan drawing files
        """

        self.model_ele_list = []
        self.handle_list    = None
        self.document       = doc

    def create(self,
               build_ele: BuildingElement):
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties
        """

        self.create_geometry(build_ele)

        return (self.model_ele_list, self.handle_list)


    def create_geometry(self,
                        build_ele: BuildingElement):
        """ Create the element geometries

        Args:
            build_ele: building element with the parameter properties
        """

        #------------------ Define the cube polyhedron

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(1000, 1000, 1000)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        #------------------ Append cubes as new Allplan elements

        elements = []

        elements.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed1))

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(elements)

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        #------------------ No handles

        self.handle_list = []

        return (self.model_ele_list, self.handle_list)
