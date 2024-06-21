""" Script for Font
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.FontBuildingElement \
        import FontBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load Font.py')


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
                               r"Examples\PythonParts\PaletteExamples\Resources\Font.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = Font(doc)

    return element.create(build_ele)


class Font():
    """ Definition of class Font
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class Font

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    @staticmethod
    def create(build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        #----------------- single font input

        text_prop = AllplanBasisEle.TextProperties()

        text_prop.Font       = build_ele.FontId.value
        text_prop.FontStyles = build_ele.FontEmphasis.value
        text_prop.FontAngle  = AllplanGeo.Angle.FromDeg(build_ele.FontAngle.value)

        model_ele_list = ModelEleList()

        model_ele_list.append(AllplanBasisEle.TextElement(build_ele.CommonProp.value, text_prop, "Font", AllplanGeo.Point2D()))


        #----------------- single font input without crossed out

        text_prop.Font       = build_ele.FontIdCond.value
        text_prop.FontStyles = build_ele.FontEmphasisCond.value
        text_prop.FontAngle  = AllplanGeo.Angle.FromDeg(build_ele.FontAngleCond.value)

        model_ele_list.append(AllplanBasisEle.TextElement(build_ele.CommonProp.value, text_prop, "Font without crossed out",
                                                          AllplanGeo.Point2D(0, 200)))


        #----------------- font for the list

        y_text = 400

        for index, (font_id, font_emphasis, font_angle) in enumerate(zip(build_ele.FontIdList.value,
                                                                         build_ele.FontEmphasisList.value,
                                                                         build_ele.FontAngleList.value)):
            text_prop.Font       = font_id
            text_prop.FontStyles = font_emphasis
            text_prop.FontAngle  =  AllplanGeo.Angle.FromDeg(font_angle)

            model_ele_list.append(AllplanBasisEle.TextElement(build_ele.CommonProp.value, text_prop,
                                                              "Font from list item " + str(index + 1),
                                                              AllplanGeo.Point2D(0, y_text)))

            y_text += 200


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
