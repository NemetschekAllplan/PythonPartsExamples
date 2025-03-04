""" Example script for Spiral
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseEle

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil

from TypeCollections.ModelEleList import ModelEleList

from Utils.HandleCreator.HandleCreator import HandleCreator

if TYPE_CHECKING:
    from __BuildingElementStubFiles.SpiralBuildingElement import SpiralBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: Spiral.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return Spiral(build_ele, script_object_data)


class Spiral(BaseScriptObject):
    """ Definition of class Spiral
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


    def create_library_preview(self) -> CreateElementResult:
        """ create the library preview

        Returns:
            created elements for the preview
        """

        return self.execute()


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        build_ele = self.build_ele

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(self.create_geometry())


        #----------------- create the PythonPart

        if build_ele.IsPythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(model_ele_list)
            pyp_util.add_reinforcement_elements([self.create_reinforcement()])

            model_ele_list = pyp_util.create_pythonpart(build_ele)

        else:
            model_ele_list.append(self.create_reinforcement())

        return CreateElementResult(model_ele_list, self.create_handles(), multi_placement = True)


    def create_geometry(self) -> AllplanGeo.Cylinder3D:
        """ Create the geometry

        Returns:
            the created cylinder
        """

        build_ele = self.build_ele

        return AllplanGeo.Cylinder3D(build_ele.Radius.value, build_ele.Radius.value, AllplanGeo.Point3D(0, 0, build_ele.Height.value))


    def create_reinforcement(self) -> AllplanReinf.SpiralElement:
        """ Create the spiral placement

        Returns:
            the created spiral element
        """

        build_ele = self.build_ele

        place_per_linear_meter = build_ele.PlacePerLinearMeter.value

        start_hook_length = build_ele.StartHookLength.value if build_ele.StartHook.value and not place_per_linear_meter else 0
        end_hook_length   = build_ele.EndHookLength.value   if build_ele.EndHook.value   and not place_per_linear_meter else 0

        rotation_axis = AllplanGeo.Line3D(AllplanGeo.Point3D(0, 0, 0),
                                          AllplanGeo.Point3D(0, 0, build_ele.Height.value))

        contour = AllplanGeo.Polyline3D()
        contour += AllplanGeo.Point3D(build_ele.Radius.value, 0, 0)
        contour += AllplanGeo.Point3D(build_ele.Radius.value, 0, build_ele.Height.value)

        spiral = AllplanReinf.SpiralElement(1, build_ele.Diameter.value, build_ele.SteelGrade.value, build_ele.ConcreteGrade.value,
                                            rotation_axis, contour, build_ele.Pitch.value, start_hook_length,
                                            build_ele.StartHookAngle.value, end_hook_length, build_ele.EndHookAngle.value,
                                            build_ele.ConcreteCover.value, build_ele.ConcreteCover.value,  build_ele.ConcreteCover.value)

        spiral.SetPlacePerLinearMeter(place_per_linear_meter)
        spiral.SetLengthFactor(build_ele.LengthFactor.value)
        spiral.SetNumberLoopsStart(build_ele.LoopsStart.value)
        spiral.SetNumberLoopsEnd(build_ele.LoopsEnd.value)

        spiral.SetPitchSections(build_ele.Pitch1.value, build_ele.Length1.value,
                                build_ele.Pitch2.value, build_ele.Length2.value,
                                build_ele.Pitch3.value, build_ele.Length3.value,
                                build_ele.Pitch4.value, build_ele.Length4.value)

        spiral.SetCommonProperties(self.create_reinf_common_prop())

        return spiral


    def create_handles(self) -> list[HandleProperties]:
        """ Create handles

        Returns:
            list of handles
        """

        build_ele = self.build_ele

        handle_list = list[HandleProperties]()

        HandleCreator.z_distance(handle_list, "Height",  AllplanGeo.Point3D(0, 0, build_ele.Height.value), AllplanGeo.Point3D())
        HandleCreator.x_distance(handle_list, "Radius",  AllplanGeo.Point3D(build_ele.Radius.value, 0, 0), AllplanGeo.Point3D())

        return handle_list


    def create_reinf_common_prop(self) -> AllplanBaseEle.CommonProperties:
        """ Create the reinforcement common properties

        Returns:
            reinforcement common properties
        """

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        build_ele = self.build_ele

        match build_ele.Layer.value:
            case "Standard":
                com_prop.Layer = 3700

            case "RU_ALL":
                com_prop.Layer = 3864

            case "RU_R":
                com_prop.Layer = 3829

        com_prop.PenByLayer    = build_ele.PenByLayer.value
        com_prop.StrokeByLayer = build_ele.StrokeByLayer.value
        com_prop.ColorByLayer  = build_ele.ColorByLayer.value

        return com_prop
