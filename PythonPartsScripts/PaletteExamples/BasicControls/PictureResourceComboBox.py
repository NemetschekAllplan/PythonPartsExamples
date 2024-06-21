""" Example script for PictureResourceComboBox
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PictureResourceComboBoxBuildingElement \
        import PictureResourceComboBoxBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PictureResourceComboBox.py')


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
ö
    Args:
        _build_ele: building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               f"{AllplanSettings.AllplanPaths.GetPythonPartsEtcPath()}"
                               r"Examples\PythonParts\PaletteExamples\BasicControls\PictureResourceComboBox.png"))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return PictureResourceComboBox(build_ele, coord_input)


class PictureResourceComboBox(BaseScriptObject):
    """ Definition of class PictureResourceComboBox
    """

    def __init__(self,
                 build_ele  : BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            coord_input: API object for the coordinate input, element selection, ... in the Allplan view
        """

        super().__init__(coord_input)

        self.build_ele = build_ele


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        com_prop = build_ele.CommonProp.value

        text_prop = AllplanBasisEle.TextProperties()

        y_dist = -(text_prop.Height * 2 * self.document.GetScalingFactor())

        texts = [AllplanBasisEle.TextElement(com_prop, text_prop,
                                             f"EdgeOffsetType: {build_ele.EdgeOffsetType.value}",  AllplanGeo.Point2D(0, 0)),
                 AllplanBasisEle.TextElement(com_prop, text_prop,
                                             f"TierCount: {build_ele.TierCount.value}",  AllplanGeo.Point2D(0, y_dist)),
                 AllplanBasisEle.TextElement(com_prop, text_prop,
                                             f"ShapeType: {build_ele.ShapeType.value}",  AllplanGeo.Point2D(0, y_dist * 2))]


        #----------------- add the types from the list

        y_text = y_dist * 4

        for index, shape_type in enumerate(build_ele.ShapeTypes.value):
            texts.append(AllplanBasisEle.TextElement(com_prop, text_prop,
                                                     f"ShapeType[{index}]: {shape_type}",
                                                     AllplanGeo.Point2D(0, y_text)))

            y_text += y_dist


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(texts)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
