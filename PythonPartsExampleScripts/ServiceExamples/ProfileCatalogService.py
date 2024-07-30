""" Script for ProfileCatalogService
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BuildingElementAttributeList import BuildingElementAttributeList
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from TypeCollections import ModelEleList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ProfileCatalogServiceBuildingElement import ProfileCatalogServiceBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ProfileCatalogService.py')


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
                               r"Examples\PythonParts\ServiceExamples\ProfileCatalogService.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: building element with the parameter properties
        doc:       document of the Allplan drawing files

    Returns:
        created element result
    """

    element = ProfileCatalogService(doc)

    return element.create(build_ele)


class ProfileCatalogService():
    """ Definition of class ProfileCatalogService
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class ProfileCatalogService

        Args:
            doc: document of the Allplan drawing files
        """

        self.document = doc


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: building element with the parameter properties

        Returns:
            created element result
        """

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        if not build_ele.Profile.value:
            return CreateElementResult([])


        #----------------- get the profile

        if build_ele.ProfileAccess.value == build_ele.GET_PROFILE:
            shape_geo = AllplanArchEle.ProfileCatalogService.GetProfileGeometry(build_ele.Profile.value,
                                                                                build_ele.OverrideDefaultGap.value,
                                                                                build_ele.OverrideGap.value)

            model_ele_list.append_geometry_3d(shape_geo, build_ele.CommonProp.value)

        elif build_ele.ProfileAccess.value == build_ele.GET_BOUNDARY_POLYLINE:
            shape_polylines = AllplanArchEle.ProfileCatalogService.GetFullProfileBoundaryPolylines(build_ele.Profile.value,
                                                                                                   build_ele.OverrideDefaultGap.value,
                                                                                                   build_ele.OverrideGap.value)

            model_ele_list.append_geometry_2d(shape_polylines, build_ele.CommonProp.value)

        elif build_ele.ProfileAccess.value == build_ele.GET_BOUNDARY_PATH:
            shape_paths = AllplanArchEle.ProfileCatalogService.GetFullProfileBoundaryPaths(build_ele.Profile.value,
                                                                                           build_ele.OverrideDefaultGap.value,
                                                                                           build_ele.OverrideGap.value)

            model_ele_list.append_geometry_2d(shape_paths, build_ele.CommonProp.value)


        #----------------- get the attributes

        attribute_list = BuildingElementAttributeList()

        attribute_list.add_attributes(AllplanArchEle.ProfileCatalogService.GetProfileAttributes(build_ele.Profile.value, self.document))


        #----------------- return the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)
        pyp_util.add_attribute_list(attribute_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))
