"""
Script for the associative views example
"""

import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtility

import StdReinfShapeBuilder.GeneralReinfShapeBuilder as GeneralShapeBuilder
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder
import StdReinfShapeBuilder.BarPlacementUtil as BarUtil

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
from PythonPartUtil import PythonPartUtil


print('Load SectionsAndViews.py')


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = SectionsAndViews(doc)

    return element.create(build_ele)


class SectionsAndViews():
    """
    Definition of class SectionsAndViews
    """

    def __init__(self, doc):
        """
        Initialization of class SectionsAndViews

        Args:
            doc: input document
        """

        self.model_ele_list        = []
        self.handle_list           = []
        self.document              = doc
        self.reinf_ele_list        = []
        self.concrete_cover        = None
        self.diameter              = None
        self.diameter_longitudinal = None
        self.bending_roller        = None
        self.steel_grade           = None
        self.distance              = None
        self.mesh_type             = None
        self.length                = 0
        self.width                 = 0
        self.height                = 0
        self.common_prop           = None
        self.dim_prop              = None
        self.dim_line_x            = 0
        self.dim_line_y            = 0


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        self.length                = build_ele.Length.value
        self.width                 = build_ele.Width.value
        self.height                = build_ele.Height.value
        self.concrete_cover        = build_ele.ConcreteCover.value
        self.diameter              = build_ele.Diameter.value
        self.diameter_longitudinal = build_ele.DiameterLongitudinal.value
        self.bending_roller        = build_ele.BendingRoller.value
        self.steel_grade           = build_ele.SteelGrade.value
        self.distance              = build_ele.Distance.value

        self.common_prop = AllplanBaseElements.CommonProperties()
        self.common_prop.GetGlobalProperties()

        self.dim_prop = AllplanBasisElements.DimensionProperties(self.document, AllplanBasisElements.Dimensioning.eDimensionLine)

        self.create_model()

        self.create_sections_and_views(build_ele)

        return (self.model_ele_list, self.handle_list)


    def create_model(self):
        """
        Create the model
        """

        ref_pnt = AllplanGeo.Point3D(0, 0, 0)

        size = AllplanGeo.Vector3D(self.length, self.width, self.height)

        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(ref_pnt, ref_pnt + size)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.common_prop, polyhed))


        #----------------- create the stirrups

        concrete_cover_props = ConcreteCoverProperties.all(self.concrete_cover)

        model_angles = RotationAngles(90, 0 , 0)

        shape_props = ReinforcementShapeProperties.rebar(self.diameter, self.bending_roller, self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.Stirrup)

        stirrup_shapes = []

        stirrup_shapes.append(GeneralShapeBuilder.create_stirrup(self.length, self.height,
                                                         model_angles,
                                                         shape_props,
                                                         concrete_cover_props))

        self.reinf_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(1, stirrup_shapes[0],
                                                                         ref_pnt,
                                                                         ref_pnt + AllplanGeo.Point3D(0, self.width, 0),
                                                                         self.concrete_cover,
                                                                         self.concrete_cover - self.diameter,
                                                                         self.distance))


        #----------------- place the longitudinal shapes

        shape_props = ReinforcementShapeProperties.rebar(self.diameter_longitudinal, self.bending_roller,
                                                         self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        cover_props = ConcreteCoverProperties.left_right_bottom(self.concrete_cover,
                                                                self.concrete_cover,
                                                                self.concrete_cover + self.diameter)

        shape = GeneralShapeBuilder.create_longitudinal_shape_with_hooks(self.width, RotationAngles(90, 0 , 90),
                                                                         shape_props, cover_props)

        cover_left = BarUtil.get_placement_start_from_bending_roller( \
                                 stirrup_shapes[0], 4,
                                 self.bending_roller,
                                 AllplanGeo.Line2D(AllplanGeo.Point2D(), AllplanGeo.Point2D(self.length, 0)),
                                 self.diameter_longitudinal,
                                 RotationAngles(-90, 0, 0))

        cover_right = BarUtil.get_placement_end_from_bending_roller( \
                                 stirrup_shapes[0], 4,
                                 self.bending_roller,
                                 AllplanGeo.Line2D(AllplanGeo.Point2D(), AllplanGeo.Point2D(self.length, 0)),
                                 self.diameter_longitudinal,
                                 RotationAngles(-90, 0, 0))

        self.reinf_ele_list.append(
            LinearBarBuilder.create_linear_bar_placement_from_to_by_count( \
                    2, shape,
                    ref_pnt, ref_pnt + AllplanGeo.Point3D(self.length, 0, 0),
                    cover_left, cover_right,
                    6))


        #----------------- create the dimension points and lines

        dim_points_x = AllplanGeo.Point3DList()
        dim_points_y = AllplanGeo.Point3DList()

        dim_points_x.append(AllplanGeo.Point3D())
        dim_points_x.append(AllplanGeo.Point3D(self.length, 0, 0))

        dim_points_y.append(AllplanGeo.Point3D())
        dim_points_y.append(AllplanGeo.Point3D(0, self.width, 0))

        self.dim_line_x = AllplanBasisElements.DimensionLineElement(dim_points_x, AllplanGeo.Vector2D(0, -500),
                                                                    AllplanGeo.Vector2D(1000, 0),
                                                                    self.dim_prop)
        self.dim_line_y = AllplanBasisElements.DimensionLineElement(dim_points_y, AllplanGeo.Vector2D(-1000, 0),
                                                                    AllplanGeo.Vector2D(0, 1000),
                                                                    self.dim_prop)

        self.model_ele_list.append(self.dim_line_x)
        self.model_ele_list.append(self.dim_line_y)


    def create_sections_and_views(self, build_ele):
        """
        Create the views
        """

        dim_points_x = AllplanGeo.Point3DList()
        dim_points_y = AllplanGeo.Point3DList()
        dim_points_z = AllplanGeo.Point3DList()

        dim_points_x.append(AllplanGeo.Point3D())
        dim_points_x.append(AllplanGeo.Point3D(self.length, 0, 0))

        dim_points_y.append(AllplanGeo.Point3D())
        dim_points_y.append(AllplanGeo.Point3D(0, self.width, 0))

        dim_points_z.append(AllplanGeo.Point3D())
        dim_points_z.append(AllplanGeo.Point3D(0, 0, self.height))

        elevation_points_z = AllplanGeo.Point3DList()

        elevation_points_z.append(AllplanGeo.Point3D())
        elevation_points_z.append(AllplanGeo.Point3D())
        elevation_points_z.append(AllplanGeo.Point3D(0, 0, self.height))

        text_prop = AllplanBasisElements.TextProperties()

        elevation_prop = AllplanBasisElements.DimensionProperties(self.document, AllplanBasisElements.Dimensioning.eElevation)

        elevation_prop.ElevationBaseOffset = 5000


        #----------------- label properties

        label_prop = AllplanReinf.ReinforcementLabelProperties()

        label_prop.ShowBarDiameter = True
        label_prop.ShowBarCount    = True
        label_prop.ShowBarDistance = True


        #----------------- initialize the section and view properties

        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_format_props = view_props.FormatProperties
        view_filter_props = view_props.FilterProperties
        view_label_props  = view_props.LabelingProperties
        view_light_props  = view_props.LightProperties
        view_scale_props  = view_props.ScaleProperties


        #----------------- section format properties

        view_format_props.IsEliminationOn     = True
        view_format_props.EliminationAngle    = 22
        view_format_props.IsEliminationOn     = True
        view_format_props.FixtureAsWireframe  = True
        view_format_props.CosiderTransparancy = True
        view_format_props.SurfaceElements     = view_format_props.SurfaceElements_Enum.eNoElements


        #----------------- labeling properties

        view_label_props.HeadingOn = False


        #----------------- section drawing files properties

        view_draw_files_props = AllplanBasisElements.SectionDrawingFilesProperties()

        drawing_file_number = AllplanUtility.VecIntList()
        drawing_file_number.append(AllplanBaseElements.DrawingFileService.GetActiveFileNumber())

        view_draw_files_props.DrawingNumbers = drawing_file_number


        #----------------- section filter properties

        view_filter_props.DrawingFilesProperties = view_draw_files_props
        view_filter_props.IsAssociativityOn      = build_ele.AutoUpdate.value


        #----------------- section light properties

        view_light_props.ConsiderLight = False


        #----------------- section filter properties

        view_scale_props.Factor_X_direction = 1.0
        view_scale_props.Factor_Y_direction = 1.0


        #----------------- general section properties

        view_props = AllplanBasisElements.SectionGeneralProperties(True)

        view_props.Status             = AllplanBasisElements.SectionGeneralProperties.State.Hidden
        view_props.ShowSectionBody    = build_ele.ShowSectionBody.value
        view_props.FormatProperties   = view_format_props
        view_props.FilterProperties   = view_filter_props
        view_props.LabelingProperties = view_label_props
        view_props.LightProperties    = view_light_props
        view_props.ScaleProperties    = view_scale_props
        view_props.ReferenceScale     = 1.0


        #----------------- front view

        view_label = AllplanBasisElements.TextElement(self.common_prop, text_prop, "Front view",
                                                      AllplanGeo.Point2D(0, -1700))

        dim_line_z = AllplanBasisElements.DimensionLineElement(dim_points_z, AllplanGeo.Vector2D(-500, 0), AllplanGeo.Vector2D(0, 1000),
                                                               self.dim_prop)

        elevation_z = AllplanBasisElements.ElevationElement(elevation_points_z, AllplanGeo.Vector2D(self.length + 500, 0),
                                                            AllplanGeo.Vector2D(0, 1000), elevation_prop)

        label1 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithPointer, 1, label_prop,
                                                 5, 0.4, AllplanGeo.Vector2D(300, 0), AllplanGeo.Angle())
        label2 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithDimensionLine,
                                                 2, label_prop, False, -600)

        labels = AllplanReinf.ReinforcementLabelList()

        labels.append(label1)
        labels.append(label2)

        view_ele = AllplanBasisElements.ViewSectionElement()

        front_view_place_pnt = AllplanGeo.Point2D(0, - self.height - 2000)

        view_props.PlacementPoint     = front_view_place_pnt
        view_props.PlacementPointType = AllplanBasisElements.SectionGeneralProperties.PlacementPointPosition.TopLeft

        view_ele.GeneralSectionProperties = view_props
        view_ele.ViewMatrix               = RotationAngles(-90, 0, 0).get_rotation_matrix()
        view_ele.TextElements             = [view_label]
        view_ele.DimensionElements        = [dim_line_z, elevation_z]
        view_ele.ReinforcementLabels      = labels

        view_ele_list = [view_ele]


        #----------------- right view

        view_label = AllplanBasisElements.TextElement(self.common_prop, text_prop, "Right view",
                                                      AllplanGeo.Point2D(self.length + 3000, self.width + 300))

        dim_line_z = AllplanBasisElements.DimensionLineElement(dim_points_z, AllplanGeo.Vector2D(0, -500), AllplanGeo.Vector2D(-1000, 0),
                                                               self.dim_prop)

        label1 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithDimensionLine,
                                                 1, label_prop, False, 600)
        label2 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithPointer, 2, label_prop,
                                                 2, 0.4, AllplanGeo.Vector2D(300, 0), AllplanGeo.Angle())

        labels = AllplanReinf.ReinforcementLabelList()

        labels.append(label1)
        labels.append(label2)

        view_ele = AllplanBasisElements.ViewSectionElement()

        right_view_place_pnt = AllplanGeo.Point2D(self.length + 3000, 0)

        view_props.PlacementPoint = right_view_place_pnt
        view_props.PlacementAngle = math.radians(90)

        view_ele.GeneralSectionProperties = view_props
        view_ele.ViewMatrix               = RotationAngles(0, -90, 0).get_rotation_matrix()
        view_ele.TextElements             = [view_label]
        view_ele.DimensionElements        = [dim_line_z]
        view_ele.ReinforcementLabels      = labels

        view_ele_list.append(view_ele)


        #----------------- isometric view

        view_label = AllplanBasisElements.TextElement(self.common_prop, text_prop, "Isometric view",
                                                      AllplanGeo.Point2D(self.length + 3000, -1700))


        view_ele = AllplanBasisElements.ViewSectionElement()

        dist_fac = math.sin(30. / 180. * math.pi) * 0.77

        view_props.PlacementPoint = AllplanGeo.Point2D(self.length + 3000,
                                                       -self.height * 0.77 - self.width * dist_fac - self.length * dist_fac - 2000)
        view_props.PlacementAngle = 0

        view_ele.GeneralSectionProperties = view_props

        view_ele.ViewMatrix = AllplanGeo.Matrix3D(0.70710678118654757, 0.40824829046386302, -0.57735026918962573, 0.00000000000000000,
                                                  -0.70710678118654757, 0.40824829046386302, -0.57735026918962573,  0.00000000000000000,
                                                  0.00000000000000000, 0.81649658092772615, 0.57735026918962573, 0.00000000000000000,
                                                  0.00000000000000000, 0.00000000000000000, 0.00000000000000000, 0.00000000000000000)
        view_ele.TextElements = [view_label]

        view_ele_list.append(view_ele)


        #----------------- front view with section body

        view_label = AllplanBasisElements.TextElement(self.common_prop, text_prop, "Section 1-1",
                                                      front_view_place_pnt + AllplanGeo.Point2D(0, -1500))

        dim_line_z = AllplanBasisElements.DimensionLineElement(dim_points_z, AllplanGeo.Vector2D(-500, 0), AllplanGeo.Vector2D(0, 1000),
                                                               self.dim_prop)

        dim_line_x = AllplanBasisElements.DimensionLineElement(dim_points_x, AllplanGeo.Vector2D(0, -1000), AllplanGeo.Vector2D(1000, 0),
                                                               self.dim_prop)

        label1 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithPointer, 1, label_prop,
                                                 5, 0.4, AllplanGeo.Vector2D(300, 0), AllplanGeo.Angle())
        label2 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithDimensionLine,
                                                 2, label_prop, False, -600)

        labels = AllplanReinf.ReinforcementLabelList()

        labels.append(label1)
        labels.append(label2)

        sect_ele = AllplanBasisElements.ViewSectionElement()

        # placement point is bottom left point of the from the section path body in the view

        view_props.PlacementPoint  = front_view_place_pnt + AllplanGeo.Point2D(-100, -self.height - 2000)
        view_props.PlacementAngle  = 0
        view_props.ShowSectionBody = build_ele.ShowSectionBody.value

        sect_ele.GeneralSectionProperties = view_props
        sect_ele.ViewMatrix               = RotationAngles(-90, 0, 0).get_rotation_matrix()
        sect_ele.TextElements             = [view_label]
        sect_ele.DimensionElements        = [dim_line_z, dim_line_x]
        sect_ele.ReinforcementLabels      = labels

        section_def_data = AllplanBasisElements.SectionDefinitionData()

        section_path = AllplanGeo.Polyline2D()
        section_path += AllplanGeo.Point2D(-100, 1000)
        section_path += AllplanGeo.Point2D(self.length + 100, 1000)
        section_path += AllplanGeo.Point2D(self.length + 100, 1500)
        section_path += AllplanGeo.Point2D(-100, 1500)
        section_path += AllplanGeo.Point2D(-100, 1000)

        section_def_data.ClippingPath    = section_path
        section_def_data.DirectionVector = AllplanGeo.Vector3D(0, 1, 0)

        sec_def_prop = section_def_data.DefinitionProperties

        sec_def_prop.IsSectionBodyOn = build_ele.ShowSectionBodyInModel.value

        clip_path_prop = sec_def_prop.ClippingPathProperties

        clip_path_prop.TopLevel              = build_ele.SectionBottomLevel.value
        clip_path_prop.BottomLevel           = build_ele.SectionTopLevel.value
        clip_path_prop.IsHeightFromElementOn = build_ele.SectionHeightFromElement.value
        clip_path_prop.SectionIdentifier     = "1"

        sec_def_prop.ClippingPathProperties = clip_path_prop

        section_def_data.DefinitionProperties = sec_def_prop

        sect_ele.SectionDefinitionData = section_def_data

        view_ele_list.append(sect_ele)


        #----------------- right view with section body

        view_label = AllplanBasisElements.TextElement(self.common_prop, text_prop, "Section 2-2",
                                                      right_view_place_pnt + AllplanGeo.Point2D(4000, self.width + 300))

        dim_line_y = AllplanBasisElements.DimensionLineElement(dim_points_y, AllplanGeo.Vector2D(-self.height - 1000, 0),
                                                               AllplanGeo.Vector2D(0, 1000),
                                                               self.dim_prop)

        dim_line_z = AllplanBasisElements.DimensionLineElement(dim_points_z, AllplanGeo.Vector2D(0, -500), AllplanGeo.Vector2D(-1000, 0),
                                                               self.dim_prop)

        label1 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithDimensionLine,
                                                 1, label_prop, False, 600)
        label2 = AllplanReinf.ReinforcementLabel(AllplanReinf.Bar, AllplanReinf.LabelWithPointer, 2, label_prop,
                                                 2, 0.4, AllplanGeo.Vector2D(300, 0), AllplanGeo.Angle())

        labels = AllplanReinf.ReinforcementLabelList()

        labels.append(label1)
        labels.append(label2)

        sect_ele = AllplanBasisElements.ViewSectionElement()

        # placement point is bottom left point of the from the section path body in the view

        view_props.PlacementPoint  = right_view_place_pnt + AllplanGeo.Point2D(4000, -200)
        view_props.PlacementAngle  = math.radians(90)
        view_props.ShowSectionBody = build_ele.ShowSectionBody.value

        sect_ele.GeneralSectionProperties = view_props
        sect_ele.ViewMatrix               = RotationAngles(0, -90, 0).get_rotation_matrix()
        sect_ele.TextElements             = [view_label]
        sect_ele.DimensionElements        = [dim_line_z, dim_line_y]
        sect_ele.ReinforcementLabels      = labels

        section_def_data = AllplanBasisElements.SectionDefinitionData()

        length_3 = self.length / 3

        section_path = AllplanGeo.Polyline2D()
        section_path += AllplanGeo.Point2D(length_3, -200)
        section_path += AllplanGeo.Point2D(length_3 * 2, -200)
        section_path += AllplanGeo.Point2D(length_3 * 2, self.width + 200)
        section_path += AllplanGeo.Point2D(length_3, self.width + 200)
        section_path += AllplanGeo.Point2D(length_3, -200)

        section_def_data.ClippingPath    = section_path
        section_def_data.DirectionVector = AllplanGeo.Vector3D(-1, 0, 0)

        sec_def_prop = section_def_data.DefinitionProperties

        sec_def_prop.IsSectionBodyOn = build_ele.ShowSectionBodyInModel.value

        clip_path_prop = sec_def_prop.ClippingPathProperties

        clip_path_prop.TopLevel              = build_ele.SectionBottomLevel.value
        clip_path_prop.BottomLevel           = build_ele.SectionTopLevel.value
        clip_path_prop.IsHeightFromElementOn = build_ele.SectionHeightFromElement.value
        clip_path_prop.SectionIdentifier     = "2"

        sec_def_prop.ClippingPathProperties = clip_path_prop

        section_def_data.DefinitionProperties = sec_def_prop

        sect_ele.SectionDefinitionData = section_def_data

        view_ele_list.append(sect_ele)


        #----------------- use model elements

        if not build_ele.IsPythonPart.value:
            self.model_ele_list.extend(self.reinf_ele_list)
            self.model_ele_list.extend(view_ele_list)

            return


        #----------------- create the PythonPart

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)
        pyp_util.add_reinforcement_elements(self.reinf_ele_list)

        self.model_ele_list = pyp_util.create_pythonpart(build_ele)

        self.model_ele_list.extend(view_ele_list)
