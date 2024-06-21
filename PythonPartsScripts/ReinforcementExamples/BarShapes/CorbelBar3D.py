""" Example Script for 3D corbel bar
"""

# pylint: disable=no-self-use

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Reinforcement as AllplanReinf

from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.BarShapeSideDataList import BarShapeSideDataList
from StdReinfShapeBuilder.BarShapePointDataList import BarShapePointDataList

from CreateElementResult import CreateElementResult
from PythonPartUtil import PythonPartUtil

from Utils import LibraryBitmapPreview
from Utils.RotationUtil import RotationUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CorbelBar3DBuildingElement import CorbelBar3DBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Loading script: CorbelBar3D.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
            version is supported state
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the library preview

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        created element result
    """

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview( \
                               AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() +
                               r"Examples\PythonParts\ReinforcementExamples\BarShapes\CorbelBar3D.png"))


def create_element(build_ele: BuildingElement,
                   doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        created element result
    """

    element = CorbelBar3D(doc)

    return element.create(build_ele)


class CorbelBar3D():
    """ Definition of class CorbelBar3D
    """

    def __init__(self,
                 doc: AllplanEleAdapter.DocumentAdapter):
        """ Initialization of class CorbelBar3D

        Args:
            doc: input document
        """

        self.doc = doc

        self.com_prop        = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()
        self.com_prop_inside = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


    def create(self,
               build_ele: BuildingElement) -> CreateElementResult:
        """ Create the elements

        Args:
            build_ele: the building element.

        Returns:
            created element result
        """


        self.com_prop.Color        = build_ele.PreviewColor.value
        self.com_prop_inside.Color = build_ele.PreviewColorInside.value

        column_poly, column = self.create_geometry(build_ele)

        corbel_bar_local1 = self.create_corbel_bar_3d_local_by_sides(build_ele, column_poly)

        corbel_bar_local2 = self.create_corbel_bar_3d_local_by_points(build_ele, column_poly)

        corbel_bar_global = self.create_corbel_bar_3d_global(build_ele)

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(column)
        pyp_util.add_reinforcement_elements(corbel_bar_local1 + corbel_bar_local2 + corbel_bar_global)

        return CreateElementResult(pyp_util.create_pythonpart(build_ele))


    def create_geometry(self,
                        build_ele: BuildingElement) -> Tuple[AllplanGeo.Polyline3D, AllplanBasisEle.ModelElement3D]:
        """ Create the corbel geometry

        Args:
            build_ele: building element

        Returns:
            created corbel geometry
        """

        width             = build_ele.Width.value
        height            = build_ele.Height.value
        thickness         = build_ele.Thickness.value
        corbel_width      = build_ele.CorbelWidth.value
        corbel_height     = build_ele.CorbelHeight.value
        elevation_corbel1 = build_ele.ElevationCorbel1.value
        elevation_corbel2 = build_ele.ElevationCorbel2.value

        column_poly = AllplanGeo.Polyline3D([AllplanGeo.Point3D(),
                                             AllplanGeo.Point3D(width, 0, 0),
                                             AllplanGeo.Point3D(width, 0, elevation_corbel1 - corbel_height),
                                             AllplanGeo.Point3D(width + corbel_width, 0, elevation_corbel1 - corbel_height),
                                             AllplanGeo.Point3D(width + corbel_width, 0, elevation_corbel1),
                                             AllplanGeo.Point3D(width, 0, elevation_corbel1),
                                             AllplanGeo.Point3D(width, 0, height - corbel_height),
                                             AllplanGeo.Point3D(width + corbel_width, 0, height - corbel_height),
                                             AllplanGeo.Point3D(width + corbel_width, 0, height),
                                             AllplanGeo.Point3D(0, 0, height),
                                             AllplanGeo.Point3D()
                                             ])

        poly_list = AllplanGeo.Polyline3DList()

        poly_list.append(column_poly)

        path = AllplanGeo.Polyline3D([AllplanGeo.Point3D(), AllplanGeo.Point3D(0, thickness, 0)])

        _, column = AllplanGeo.CreateSweptPolyhedron3D(poly_list, path, True, True, AllplanGeo.Vector3D())

        corbel2 = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(0, thickness, elevation_corbel2 - corbel_height),
                                                       AllplanGeo.Point3D(width, thickness + corbel_width, elevation_corbel2))

        _, column = AllplanGeo.MakeUnion(column, corbel2)

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        model_ele = AllplanBasisEle.ModelElement3D(com_prop, column)

        return column_poly, model_ele


    def create_corbel_bar_3d_local_by_sides(self,
                                            build_ele  : BuildingElement,
                                            column_poly: AllplanGeo.Polyline3D) -> List[AllplanReinf.BarPlacement]:
        """ Create the corbel shape in the local coordinate system by sides and transform it to the global

        Args:
            build_ele:   building element
            column_poly: column shape polyline

        Returns:
            created corbel shape
        """

        cover          = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        side_length    = build_ele.BarStartEndLength.value
        bending_roller = build_ele.BendingRoller.value
        steel_grade    = build_ele.SteelGrade.value
        concrete_grade = build_ele.ConcreteGrade.value
        thickness      = build_ele.Thickness.value

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, concrete_grade,
                                                         AllplanReinf.BendingShapeType.Freeform)


        #----------------- create the shape geometry points

        pnt1 = AllplanGeo.Point2D()
        pnt2 = AllplanGeo.Point2D(0, column_poly[column_poly.Count() - 2].Z)
        pnt3 = AllplanGeo.Point2D(column_poly[5].X, column_poly[5].Z)
        pnt4 = AllplanGeo.Point2D(column_poly[4].X, column_poly[4].Z)


        #----------------- create the outer 3d shape by sides

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        z_coord = -thickness + 2 * cover

        shape_builder.AddSide(pnt1, pnt2, -cover, bending_roller)
        shape_builder.AddSide(pnt3, pnt4, -cover, bending_roller)
        shape_builder.AddSide(pnt4, pnt4,  cover, bending_roller, z_coord)
        shape_builder.AddSide(pnt4, pnt3,  cover, bending_roller, z_coord)
        shape_builder.AddSide(pnt2, pnt1,  cover, bending_roller, z_coord)

        shape_builder.SetSideLengthStart(side_length)
        shape_builder.SetSideLengthEnd(side_length)

        shape = shape_builder.CreateShape(shape_props)

        shape.Rotate(RotationUtil(90, 0, 0), AllplanGeo.Point3D())

        shape.Move(AllplanGeo.Vector3D(0, cover + diameter / 2, 0))

        placement = [AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(),
                                               AllplanGeo.Point3D(), AllplanGeo.Point3D(), shape)]

        placement[-1].CommonProperties = self.com_prop


        #----------------- create the first inner 3d shape by a BarShapeSideDataList

        diameter_inside = build_ele.DiameterInside.value
        cover_inside    = build_ele.ConcreteCoverInside.value

        shape_props = ReinforcementShapeProperties.rebar(diameter_inside, bending_roller, steel_grade, concrete_grade,
                                                         AllplanReinf.BendingShapeType.Freeform)

        z_coord = -thickness + 2 * cover_inside

        shape_data = BarShapeSideDataList([cover,
                                           (pnt1, pnt2, -cover, bending_roller),
                                           (pnt3, pnt4, -cover, bending_roller),
                                           (pnt4, pnt4,  cover + diameter, bending_roller, z_coord),
                                           (pnt4, pnt3,  cover, bending_roller, z_coord),
                                           (pnt2, pnt1,  cover, bending_roller, z_coord),
                                           cover])

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        shape_builder.AddSides(shape_data)
        shape_builder.SetSideLengthStart(side_length)
        shape_builder.SetSideLengthEnd(side_length)

        shape = shape_builder.CreateShape(shape_props)

        shape.Rotate(RotationUtil(90, 0, 0), AllplanGeo.Point3D())

        shape.Move(AllplanGeo.Vector3D(0,  cover_inside + diameter_inside / 2, 0))

        placement.append(AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(),
                                                   AllplanGeo.Point3D(), AllplanGeo.Point3D(), shape))

        placement[-1].CommonProperties = self.com_prop_inside

        return placement


    def create_corbel_bar_3d_local_by_points(self,
                                             build_ele  : BuildingElement,
                                             column_poly: AllplanGeo.Polyline3D) -> List[AllplanReinf.BarPlacement]:
        """ Create the corbel shape in the local coordinate system by points and transform it to the global

        Args:
            build_ele:   building element
            column_poly: columns shape polyline

        Returns:
            created corbel shape
        """

        cover          = build_ele.ConcreteCover.value
        diameter       = build_ele.Diameter.value
        side_length    = build_ele.BarStartEndLength.value
        bending_roller = build_ele.BendingRoller.value
        steel_grade    = build_ele.SteelGrade.value
        concrete_grade = build_ele.ConcreteGrade.value
        thickness      = build_ele.Thickness.value

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, concrete_grade,
                                                         AllplanReinf.BendingShapeType.Freeform)


        #----------------- create the shape geometry points

        pnt1 = AllplanGeo.Point2D(0, 0)
        pnt2 = AllplanGeo.Point2D(0, column_poly[column_poly.Count() - 2].Z)
        pnt3 = AllplanGeo.Point2D(column_poly[column_poly.Count() - 3].X, column_poly[column_poly.Count() - 3].Z)


        #----------------- create the outer 3d shape by sides

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        z_coord = -thickness + 2 * cover

        shape_builder.AddPoint(pnt1,  cover, bending_roller)
        shape_builder.AddPoint(pnt2, -cover, bending_roller)
        shape_builder.AddPoint(pnt3, -cover, bending_roller)
        shape_builder.AddPoint(pnt3,  cover, bending_roller, z_coord)
        shape_builder.AddPoint(pnt2,  cover, bending_roller, z_coord)
        shape_builder.AddPoint(pnt1,  cover, bending_roller, z_coord)

        shape_builder.SetSideLengthStart(side_length)
        shape_builder.SetSideLengthEnd(side_length)

        shape = shape_builder.CreateShape(shape_props)

        shape.Rotate(RotationUtil(90, 0, 0), AllplanGeo.Point3D())

        shape.Move(AllplanGeo.Vector3D(0, cover + diameter / 2, 0))

        placement = [AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(),
                                               AllplanGeo.Point3D(), AllplanGeo.Point3D(), shape)]

        placement[-1].CommonProperties = self.com_prop


        #----------------- create the first inner 3d shape by a BarShapePointDataList

        diameter_inside = build_ele.DiameterInside.value
        cover_inside    = build_ele.ConcreteCoverInside.value

        shape_props = ReinforcementShapeProperties.rebar(diameter_inside, bending_roller, steel_grade, concrete_grade,
                                                         AllplanReinf.BendingShapeType.Freeform)

        z_coord = -thickness + 2 * cover_inside

        point_data = BarShapePointDataList([(pnt1,  cover, bending_roller),
                                            (pnt2, -cover, bending_roller),
                                            (pnt3, -cover, bending_roller),
                                            (pnt3,  cover + diameter, bending_roller, z_coord),
                                            (pnt2,  cover, bending_roller, z_coord),
                                            (pnt1,  cover, bending_roller, z_coord),
                                            cover])

        shape_builder = AllplanReinf.ReinforcementShapeBuilder()

        shape_builder.AddPoints(point_data)
        shape_builder.SetSideLengthStart(side_length)
        shape_builder.SetSideLengthEnd(side_length)

        shape = shape_builder.CreateShape(shape_props)

        shape.Rotate(RotationUtil(90, 0, 0), AllplanGeo.Point3D())

        shape.Move(AllplanGeo.Vector3D(0, cover_inside + diameter_inside / 2, 0))

        placement.append(AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(),
                                                   AllplanGeo.Point3D(), AllplanGeo.Point3D(), shape))

        placement[-1].CommonProperties = self.com_prop_inside

        return placement


    def create_corbel_bar_3d_global(self,
                                    build_ele: BuildingElement) -> List[AllplanReinf.BarPlacement]:
        """ Create the corbel shape in the global coordinate system

        Args:
            build_ele: building element

        Returns:
            created corbel shape
        """

        cover            = build_ele.ConcreteCover.value
        diameter         = build_ele.Diameter.value
        side_length      = build_ele.BarStartEndLength.value
        bending_roller   = build_ele.BendingRoller.value
        steel_grade      = build_ele.SteelGrade.value
        concrete_grade   = build_ele.ConcreteGrade.value
        width            = build_ele.Width.value
        thickness        = build_ele.Thickness.value + build_ele.CorbelWidth.value
        elevation_corbel = build_ele.ElevationCorbel2.value

        shape_props = ReinforcementShapeProperties.rebar(diameter, bending_roller, steel_grade, concrete_grade,
                                                         AllplanReinf.BendingShapeType.Freeform)


        #----------------- create the shape geometry points

        pnt1 = AllplanGeo.Point3D(0, 0, 0)
        pnt2 = AllplanGeo.Point3D(0, 0, elevation_corbel)
        pnt3 = AllplanGeo.Point3D(0, thickness, elevation_corbel)
        pnt4 = AllplanGeo.Point3D(width, thickness, elevation_corbel)
        pnt5 = AllplanGeo.Point3D(width, 0, elevation_corbel)
        pnt6 = AllplanGeo.Point3D(width, 0, 0)


        #----------------- create the 3d shape

        shape_builder = AllplanReinf.ReinforcementShapeBuilder(RotationUtil(90, 0, 0).get_rotation_matrix(),
                                                               True, cover, cover)

        shape_builder.SetConcreteCoverStart(cover)

        shape_builder.AddSide(pnt1, pnt2, cover, bending_roller)
        shape_builder.AddSide(pnt2, pnt3, cover, bending_roller)
        shape_builder.AddSide(pnt3, pnt4, cover, bending_roller)
        shape_builder.AddSide(pnt4, pnt5, cover, bending_roller)
        shape_builder.AddSide(pnt5, pnt6, cover, bending_roller)

        shape_builder.SetConcreteCoverEnd(cover)
        shape_builder.SetSideLengthStart(side_length)
        shape_builder.SetSideLengthEnd(side_length)

        shape = shape_builder.CreateShape(shape_props)

        placement = [AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(),
                                               AllplanGeo.Point3D(), AllplanGeo.Point3D(), shape)]

        placement[-1].CommonProperties = self.com_prop


        #----------------- create the inner 3d shape

        diameter_inside = build_ele.DiameterInside.value
        cover_inside    = build_ele.ConcreteCoverInside.value

        shape_props = ReinforcementShapeProperties.rebar(diameter_inside, bending_roller, steel_grade, concrete_grade,
                                                         AllplanReinf.BendingShapeType.Freeform)

        shape_data = BarShapeSideDataList([cover,
                                           (pnt1, pnt2, cover_inside, bending_roller),
                                           (pnt2, pnt3, cover, bending_roller),
                                           (pnt3, pnt4, cover, bending_roller),
                                           (pnt4, pnt5, cover_inside, bending_roller),
                                           (pnt5, pnt6, cover_inside, bending_roller),
                                           cover])

        shape_builder = AllplanReinf.ReinforcementShapeBuilder(RotationUtil(90, 0, 0).get_rotation_matrix(),
                                                               True, cover, cover + diameter)

        shape_builder.AddSides(shape_data)
        shape_builder.SetSideLengthStart(side_length)
        shape_builder.SetSideLengthEnd(side_length)

        shape = shape_builder.CreateShape(shape_props)

        placement.append(AllplanReinf.BarPlacement(1, 1, AllplanGeo.Vector3D(),
                                                   AllplanGeo.Point3D(), AllplanGeo.Point3D(), shape))

        placement[-1].CommonProperties = self.com_prop_inside

        return placement
