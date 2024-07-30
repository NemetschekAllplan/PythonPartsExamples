""" Script for Attribute control example
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from TypeCollections import ModelEleList
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from AttributesBuildingElement import AttributesBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Attribute.py')


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


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\BasisExamples\General\Attributes.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Attributes(build_ele, script_object_data)


class Attributes(BaseScriptObject):
    """ Definition of class LabelElement
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:          building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        model_ele_list.append_geometry_3d(AllplanGeo.Polyhedron3D.CreateCuboid(*build_ele.Sizes.value.Values()))


        #----------------- add the attributes to the model object

        attributes_list = BuildingElementAttributeList()

        attributes_list.add_attributes_from_parameters(build_ele)

        model_ele_list.set_element_attributes(-1, attributes_list.get_attribute_list())

        return CreateElementResult(model_ele_list)
