"""Example Script showing how to create a polygonal placement
using BarPlacement class
"""

#pylint: enable=W1401
# Only disabled for comment part

from __future__ import annotations

from typing import TYPE_CHECKING

import GeometryValidate
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from TypeCollections import ModelEleList
from TypeCollections import Curve3DList

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PolygonalPlacementBuildingElement import \
        PolygonalPlacementBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: PolygonalPlacement.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   _doc:      AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of element

    Args:
        build_ele:  the building element.
        _doc:       input document

    Returns:
        result of the element creation
    """
    element = PolygonalPlacement(build_ele)

    return element.create()


class PolygonalPlacement():
    """Definition of class PolygonalPlacement

    Attributes:
        build_ele:      building element with the parameter properties from the property palette
        model_ele_list: model element list containing the trapezoidal prism bounding the reinforcement
        reinf_ele_list: model element list containing the polygonal bar placement
    """

    def __init__(self, build_ele: BuildingElement):
        """Initialization of class PolygonalPlacement

        Args:
            build_ele: building element with the parameter properties from the property palette
        """
        self.build_ele      = build_ele
        self.model_ele_list = ModelEleList(self.build_ele.CommonProp.value)
        self.reinf_ele_list = ModelEleList(self.build_ele.CommonProp.value)


    def create(self) -> CreateElementResult:
        """Creation of the model elements: prism and polygonal bar placement

        Returns:
            created element result
        """

        if (prism := self.create_bounding_geometry()) is not None:
            self.model_ele_list.append_geometry_3d(prism)

        self.reinf_ele_list.append(self.create_reinforcement())

        # create the PythonPart, if the option was selected in the palette
        if self.build_ele.IsPythonPart.value:
            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)
            pyp_util.add_reinforcement_elements(self.reinf_ele_list)

            return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))

        # otherwise just return the bounding geometry and the reinforcement
        return CreateElementResult(self.model_ele_list + self.reinf_ele_list)

    def create_bounding_geometry(self) -> AllplanGeo.BRep3D|None:
        """Creates a trapezoidal prism with a rectangular base that tapers to a smaller
        rectangular top. This prism is a bounding box for the reinforcement shapes.

        Returns:
            Created prism. If geometrical error occurred, None is returned
        """

        bottom_rectangle  = AllplanGeo.Polyline3D()
        bottom_rectangle += AllplanGeo.Point3D(x= -self.build_ele.BottomDimensions.value.X/2,
                                               y= -self.build_ele.BottomDimensions.value.Y/2,
                                               z=  0)

        bottom_rectangle += AllplanGeo.Point3D(x=  self.build_ele.BottomDimensions.value.X/2,
                                               y= -self.build_ele.BottomDimensions.value.Y/2,
                                               z=  0)

        bottom_rectangle += AllplanGeo.Point3D(x= self.build_ele.BottomDimensions.value.X/2,
                                               y= self.build_ele.BottomDimensions.value.Y/2,
                                               z= 0)

        bottom_rectangle += AllplanGeo.Point3D(x= -self.build_ele.BottomDimensions.value.X/2,
                                               y=  self.build_ele.BottomDimensions.value.Y/2,
                                               z=  0)
        bottom_rectangle += bottom_rectangle.Points[0]

        top_rectangle  = AllplanGeo.Polyline3D()
        top_rectangle += AllplanGeo.Point3D(x= -self.build_ele.TopDimensions.value.X/2,
                                            y= -self.build_ele.TopDimensions.value.Y/2,
                                            z=  self.build_ele.Height.value)

        top_rectangle += AllplanGeo.Point3D(x=  self.build_ele.TopDimensions.value.X/2,
                                            y= -self.build_ele.TopDimensions.value.Y/2,
                                            z=  self.build_ele.Height.value)

        top_rectangle += AllplanGeo.Point3D(x= self.build_ele.TopDimensions.value.X/2,
                                            y= self.build_ele.TopDimensions.value.Y/2,
                                            z= self.build_ele.Height.value)

        top_rectangle += AllplanGeo.Point3D(x= -self.build_ele.TopDimensions.value.X/2,
                                            y=  self.build_ele.TopDimensions.value.Y/2,
                                            z=  self.build_ele.Height.value)
        top_rectangle += top_rectangle.Points[0]

        error, prism = AllplanGeo.CreateLoftedBRep3D(
            outerProfiles        = Curve3DList([bottom_rectangle, top_rectangle]),
            innerProfiles        = Curve3DList(),
            closecaps            = True,
            createprofileedges   = False,
            linear               = True,
            periodic             = False)

        if GeometryValidate.polyhedron(error):
            return prism
        return None

    def create_reinforcement(self) -> AllplanReinf.BarPlacement:
        """ Create the polygonal stirrup placement using BarPlacement by:

        -   start shape
        -   end shape
        -   bar count

        Both shapes are rectangular, closed stirrups, defined in global coordinate system

        Returns:
            polygonal placement of the stirrups
        """

        #--------- define bar shape properties common for both bottom and top shape

        bending_roller = AllplanReinf.BendingRollerService.GetBendingRollerFactor(self.build_ele.DiameterStirrup.value,
                                                                                  self.build_ele.SteelGrade.value,
                                                                                  -1,
                                                                                  True)

        concrete_cover_props = ConcreteCoverProperties.all(self.build_ele.ConcreteCover.value)

        shape_props = ReinforcementShapeProperties.rebar(self.build_ele.DiameterStirrup.value,
                                                         bending_roller,
                                                         self.build_ele.SteelGrade.value,
                                                         -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        local_to_global = AllplanGeo.Matrix3D()


        #--------- define bottom bar shape

        shape_bottom = GeneralShapeBuilder.create_stirrup(self.build_ele.BottomDimensions.value.X,
                                                          self.build_ele.BottomDimensions.value.Y,
                                                          RotationAngles(0,0,0),
                                                          shape_props,
                                                          concrete_cover_props)

        # transformation from local system of the stirrup to the global coordinate system
        local_to_global.SetTranslation(AllplanGeo.Vector3D(-self.build_ele.BottomDimensions.value.X/2,
                                                           -self.build_ele.BottomDimensions.value.Y/2,
                                                           0))
        shape_bottom.Transform(local_to_global)


        #--------- define top bar shape

        shape_top = GeneralShapeBuilder.create_stirrup(self.build_ele.TopDimensions.value.X,
                                                       self.build_ele.TopDimensions.value.Y,
                                                       RotationAngles(0,0,0),
                                                       shape_props,
                                                       concrete_cover_props)

        # transformation from local system of the stirrup to the global coordinate system
        local_to_global.SetTranslation(AllplanGeo.Vector3D(-self.build_ele.TopDimensions.value.X/2,
                                                           -self.build_ele.TopDimensions.value.Y/2,
                                                           self.build_ele.Height.value))
        shape_top.Transform(local_to_global)


        #--------- create the placement

        return AllplanReinf.BarPlacement(positionNumber    = 1,
                                         barCount          = self.build_ele.Count.value,
                                         startBendingShape = shape_bottom,
                                         endBendingShape   = shape_top)
