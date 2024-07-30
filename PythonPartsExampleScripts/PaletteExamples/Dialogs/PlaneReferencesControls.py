""" Example script for PlaneReferencesControls
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PlaneReferencesControlsBuildingElement \
        import PlaneReferencesControlsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load PlaneReferencesControls.py')


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
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\PaletteExamples\Dialogs\PlaneReferencesControls.png"))


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return PlaneReferencesControls(build_ele, script_object_data)


class PlaneReferencesControls(BaseScriptObject):
    """ Definition of class PlaneReferencesControls
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


        #----------------- create the geometry

        model_ele_list = ModelEleList(build_ele.CommonProp.value)

        x_pos = 0

        model_ele_list.append_geometry_3d(self.create_polyhedron(build_ele.PlanRefPolyhed1.value, x_pos, 0))
        model_ele_list.append_geometry_3d(self.create_polyhedron(build_ele.PlanRefPolyhed2.value, x_pos + 2000, 0))
        model_ele_list.append_geometry_3d(self.create_polyhedron(build_ele.PlanRefPolyhed3.value, x_pos + 4000, 0))

        model_ele_list.append_geometry_3d(self.create_cylinder(build_ele.PlanRefCylinder1.value, x_pos + 6000, 0))
        model_ele_list.append_geometry_3d(self.create_cylinder(build_ele.PlanRefCylinder2.value, x_pos + 8000, 0))
        model_ele_list.append_geometry_3d(self.create_cylinder(build_ele.PlanRefCylinder3.value, x_pos + 10000, 0))

        model_ele_list.set_common_properties(build_ele.ConstraintCommonProp.value)

        model_ele_list.append_geometry_3d(self.create_polyhedron(build_ele.PlaneRefBoxCylinder.value, x_pos + 13000,
                                                                 -build_ele.CylinderHeight.value))

        model_ele_list.append_geometry_3d(self.create_cylinder(build_ele.PlaneRefBoxCylinder.value, x_pos + 13500,
                                                               build_ele.BoxHeight.value))

        model_ele_list.set_common_properties(build_ele.CommonProp.value)

        for index, plane_ref in enumerate(build_ele.PlaneReferencesCone.value):
            model_ele_list.append_geometry_3d(self.create_cone(plane_ref, x_pos + 16000 + 2000 * index))


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(model_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    @staticmethod
    def create_polyhedron(plane_ref : AllplanArchEle.PlaneReferences,
                          x_pos     : float,
                          top_offset: float) -> AllplanGeo.Polyhedron3D:
        """ create a polyhedron

        Args:
            plane_ref:  plane references
            x_pos:      x position
            top_offset: top offset value

        Returns:
            created polyhedron
        """

        abs_bottom_elevation = plane_ref.AbsBottomElevation
        abs_top_elevation    = plane_ref.AbsTopElevation + top_offset

        if (height := abs_top_elevation - abs_bottom_elevation) < 1:
            height = 100

        size = 1000

        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(size, size, height)
        cuboid_geo = AllplanGeo.Move(cuboid_geo, AllplanGeo.Vector3D(x_pos, 0, abs_bottom_elevation))

        return cuboid_geo


    @staticmethod
    def create_cylinder(plane_ref    : AllplanArchEle.PlaneReferences,
                        x_pos        : float,
                        bottom_offset: float) -> AllplanGeo.BRep3D:
        """ create a cylinder

        Args:
            plane_ref:     plane references
            x_pos:         x position
            bottom_offset: bottom offset

        Returns:
            created cylinder
        """

        abs_bottom_elevation = plane_ref.AbsBottomElevation + bottom_offset
        abs_top_elevation    = plane_ref.AbsTopElevation

        if (height := abs_top_elevation - abs_bottom_elevation) < 1:
            height = 100

        return AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(x_pos, 500, abs_bottom_elevation)),
                                                500, height)


    @staticmethod
    def create_cone(plane_ref: AllplanArchEle.PlaneReferences,
                    x_pos    : float) -> AllplanGeo.BRep3D:
        """ create a cone

        Args:
            plane_ref: plane references
            x_pos:     x position

        Returns:
            created cylinder
        """

        abs_bottom_elevation = plane_ref.AbsBottomElevation
        abs_top_elevation    = plane_ref.AbsTopElevation

        if (height := abs_top_elevation - abs_bottom_elevation) < 1:
            height = 100

        ref_pnt = AllplanGeo.Point3D(x_pos, 500, abs_bottom_elevation)

        return AllplanGeo.BRep3D.CreateCone(AllplanGeo.Cone3D(AllplanGeo.AxisPlacement3D(ref_pnt), 500, 200,
                                                              ref_pnt + AllplanGeo.Point3D(0, 0, height)))
