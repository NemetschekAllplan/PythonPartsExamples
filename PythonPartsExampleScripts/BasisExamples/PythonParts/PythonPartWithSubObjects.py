""" An example script showing creation of a single PythonPart with other objects
linked to it with a Parent-Child relationship (PythonPart being the Parent)
"""
from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Precast as AllplanPrecast
import NemAll_Python_Reinforcement as AllplanReinf

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearPlacementBuilder

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil
from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from TypeCollections.ModelEleList import ModelEleList
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.PythonPartWithSubObjectsBuildingElement import \
        PythonPartWithSubObjectsBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version: float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element containing parameter values from the property palette
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_element(build_ele: BuildingElement,
                   _doc: AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Function for the element creation

    Args:
        build_ele: building element containing parameter values from the property palette
        _doc:      input document

    Returns:
        created element result
    """

    python_part_util = PythonPartUtil(build_ele.CommonProp.value)

    cube = create_cuboid(build_ele)
    python_part_util.add_pythonpart_view_2d3d(cube)

    if build_ele.CreateReinforcement.value:
        stirrups = create_reinforcement(build_ele)
        python_part_util.add_reinforcement_elements(stirrups)

    if build_ele.CreateArchitectureElement.value:
        wall_element = create_walls(build_ele)
        python_part_util.add_architecture_elements(wall_element)

    if build_ele.CreateLibrarySymbol.value:
        library_element = create_library_element(build_ele)
        python_part_util.add_library_elements(library_element)

    if build_ele.CreateFixture.value:
        fixture_placement = create_fixture(build_ele)
        python_part_util.add_fixture_elements(fixture_placement)

    return CreateElementResult(python_part_util.create_pythonpart(build_ele,
                                                                  type_uuid = "b09d5feb-949f-44d8-99ca-08516a66ea1c",
                                                                  type_display_name = "PythonPart with sub objects"))


def create_cuboid(build_ele: BuildingElement) -> ModelEleList:
    """Create a list of model elements containing one cuboid with
    dimensions specified in the property palette

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        model element list with one element, the cuboid
    """
    cuboid_geo     = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(),
                                                          AllplanGeo.Point3D() + build_ele.Dimensions.value)
    common_props   = AllplanBaseElements.CommonProperties()
    model_ele_list = ModelEleList(common_props)
    model_ele_list.append_geometry_3d(cuboid_geo)

    return model_ele_list

def create_walls(build_ele: BuildingElement) -> list[AllplanArchElements.WallElement]:
    """Creates four walls enclosing a rectangle. The dimensions of the rectangle
    are specified by the user in the property palette.

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        model element list with four lines representing a rectangle
    """
    rectangle = AllplanGeo.Polygon2D.CreateRectangle(AllplanGeo.Point2D(),
                                                     AllplanGeo.Point2D() + AllplanGeo.Vector2D(build_ele.Dimensions.value))
    _, wall_axes         = rectangle.GetSegments()

    axis_props           = AllplanArchElements.AxisProperties()
    axis_props.OnTier    = 0
    axis_props.Extension = -1
    axis_props.Position  = AllplanArchElements.WallAxisPosition.eLeft

    wall_props = AllplanArchElements.WallProperties()
    wall_props.SetTierCount(1)
    wall_props.SetAxis(axis_props)

    return [AllplanArchElements.WallElement(wall_props, axis) for axis in wall_axes]


def create_reinforcement(build_ele: BuildingElement) -> AllplanReinf.BarPlacement:
    """ Create rectangular closed stirrups in XY plane, with 30 mm cover in each side. The stirrups are
    placed along the Z+ axis with a spacing of 150 mm

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        stirrup placement
    """
    # define the bending shape and its properties
    shape_props     = ReinforcementShapeProperties.rebar(10, 4.0, -1, -1, AllplanReinf.BendingShapeType.Stirrup)
    concrete_covers = ConcreteCoverProperties.all(30)
    shape           = GeneralShapeBuilder.create_stirrup(build_ele.Dimensions.value.X,
                                                         build_ele.Dimensions.value.Y,
                                                         RotationUtil(0,0,0),
                                                         shape_props,
                                                         concrete_covers)

    # define the stirrup placement
    from_pnt = AllplanGeo.Point3D()
    to_point = from_pnt + AllplanGeo.Point3D(0, 0, build_ele.Dimensions.value.Z)

    return LinearPlacementBuilder.create_linear_bar_placement_from_to_by_dist(1, shape, from_pnt, to_point, 30, 30, 150)

def create_library_element(build_ele: BuildingElement) -> AllplanBasisElements.LibraryElement:
    """Creates a library element based on the path provided by the user in the property palette

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        library element
    """

    library_element_properties = AllplanBasisElements.LibraryElementProperties(build_ele.SymbolPath.value,
                                                                               elementType     = AllplanBasisElements.LibraryElementType.eSymbol,
                                                                               placementMatrix = AllplanGeo.Matrix3D())

    return AllplanBasisElements.LibraryElement(library_element_properties)

def create_fixture(build_ele: BuildingElement) -> AllplanPrecast.FixturePlacementElement:
    """Creates a point fixture represented by a 100x100x100 cube places on
    the top face of the PythonPart

    Args:
        build_ele:  building element containing parameter values from the property palette

    Returns:
        point fixture placement
    """

    # define common properties of the fixture
    common_props       = AllplanBaseElements.CommonProperties()
    common_props.Color = 6

    # define the geometry of the fixture
    fixture_geometry   = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(-50,-50,-100),
                                                              AllplanGeo.Point3D( 50, 50,   0))

    # create the fixture slide
    slide_prop                 = AllplanPrecast.FixtureSlideProperties()
    slide_prop.ViewType        = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
    slide_prop.VisibilityGeo3D = True
    slide_prop.VisibilityGeo2D = True

    slide_element = AllplanBasisElements.ModelElement3D(common_props,fixture_geometry)
    slides        = [AllplanPrecast.FixtureSlideElement(slide_prop, [slide_element])]

    # define the properties of the fixture element
    fixture_prop         = AllplanPrecast.FixtureProperties()
    fixture_prop.Type    = AllplanPrecast.MacroType.ePoint_Fixture
    fixture_prop.SubType = AllplanPrecast.MacroSubType.eConnectorEBT
    fixture_prop.Name    = "AnchoragePlate"

    # create the fixture element
    fixture_element = AllplanPrecast.FixtureElement(fixture_prop, slides)
    fixture_element.SetHash(hashlib.sha224(str(fixture_element).encode('utf-8')).hexdigest())

    # define the placement matrix
    placement_matrix = AllplanGeo.Matrix3D()
    placement_matrix.SetTranslation(AllplanGeo.Vector3D(build_ele.Dimensions.value.X / 2,
                                                        build_ele.Dimensions.value.Y / 2,
                                                        build_ele.Dimensions.value.Z))

    # define the properties of the fixture placement
    fixture_placement_prop             = AllplanPrecast.FixturePlacementProperties()
    fixture_placement_prop.Name        = "Connector"
    fixture_placement_prop.OutlineType = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_NO_AFFECT
    fixture_placement_prop.Matrix      = placement_matrix

    # create the
    return AllplanPrecast.FixturePlacementElement(common_props,
                                                  fixture_placement_prop,
                                                  fixture_element)
