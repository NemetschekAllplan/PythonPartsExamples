""" Script for MeshLabelWithPointer
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_Utility as AllplanUtility

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from CreateElementResult import CreateElementResult

from StdReinfShapeBuilder import GeneralReinfShapeBuilder

from StdReinfShapeBuilder.ConcreteCoverProperties import ConcreteCoverProperties
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties

from TypeCollections.ModelEleList import ModelEleList

from Utils.RotationUtil import RotationUtil
from Utils import LibraryBitmapPreview
from Utils.TextAlignmentUtil import TextAlignmentUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.MeshLabelWithPointerBuildingElement import \
         MeshLabelWithPointerBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load MeshLabelWithPointer.py')


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


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        created script object
    """

    return MeshLabelWithPointer(build_ele, script_object_data)


class MeshLabelWithPointer(BaseScriptObject):
    """ Definition of class MeshLabelWithPointer
    """

    def __init__(self,
                 build_ele         : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization

        Args:
            build_ele:   building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.build_ele = build_ele


    def create_library_preview(self) -> CreateElementResult:
        """ Creation of the element preview

        Returns:
            created elements for the preview
        """

        return CreateElementResult(
            LibraryBitmapPreview.create_library_bitmap_preview(fr"{self.build_ele.pyp_file_path}\{self.build_ele.pyp_name}.png"))


    def execute(self) -> CreateElementResult:
        """ execute the script

        Returns:
            created element result
        """

        model_ele_list = self.create_geometry()

        model_ele_list.append(self.create_stirrup_mesh_placement())
        model_ele_list.append(self.create_longitudinal_mesh_placement())
        model_ele_list.append(self.create_open_stirrup_mesh_placement())

        model_ele_list.append(self.create_view())

        return CreateElementResult(model_ele_list, multi_placement = True)


    @staticmethod
    def create_geometry() -> ModelEleList:
        """ create the geometry of the reinforcement

        Returns:
            model element list with the created geometry
        """

        model_ele_list = ModelEleList()

        model_ele_list.append_geometry_3d(AllplanGeo.Polyhedron3D.CreateCuboid(500, 1000, 2000))

        model_ele_list.append_geometry_3d(AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(3000, 0, 0),
                                                                               AllplanGeo.Point3D(6000, 2000, 500)))

        return model_ele_list


    def create_stirrup_mesh_placement(self) -> AllplanReinf.MeshPlacement:
        """ create the stirrup mesh placement

        Returns:
            mesh placement of the stirrup
        """

        build_ele = self.build_ele

        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        model_angles = RotationUtil(0, 0, 0)

        shape_props = ReinforcementShapeProperties.mesh(build_ele.MeshType.value, mesh_bending_dir,
                                                        build_ele.BendingRoller.value, build_ele.ConcreteGrade.value,
                                                        AllplanReinf.BendingShapeType.Stirrup)

        shape = GeneralReinfShapeBuilder.create_stirrup(500, 1000, model_angles, shape_props, ConcreteCoverProperties.all(25),
                                                        AllplanReinf.StirrupType.Normal)

        stirrup_mesh_placement = AllplanReinf.MeshPlacement(1, AllplanGeo.Vector3D(0, 0, 1950), shape)

        label = AllplanReinf.MeshLabel(1, self.create_label_properties(), build_ele.LabelPoint.value) \
                    if build_ele.LabelPositionDef.value == build_ele.LABEL_BY_POINT else \
                AllplanReinf.MeshLabel(1, self.create_label_properties(), build_ele.ShapeSide.value,
                                       build_ele.ShapeSideFactor.value, build_ele.LabelOffset.value)

        self.set_text_properties(label)

        stirrup_mesh_placement.SetLabel(label, AllplanEleAdapter.AssocViewElementAdapter())

        return stirrup_mesh_placement


    def create_longitudinal_mesh_placement(self) -> AllplanReinf.MeshPlacement:
        """ create the longitudinal mesh placement

        Returns:
            mesh placements of the longitudinal mesh
        """

        build_ele = self.build_ele

        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        model_angles = RotationUtil(0, 0, 0)

        shape_props = ReinforcementShapeProperties.mesh(build_ele.MeshType.value, mesh_bending_dir,
                                                        build_ele.BendingRoller.value, build_ele.ConcreteGrade.value,
                                                        AllplanReinf.BendingShapeType.LongitudinalBar)

        shape = GeneralReinfShapeBuilder.create_longitudinal_shape_with_hooks(3000, model_angles, shape_props,
                                                                              ConcreteCoverProperties.all(25), -1, -1)

        shape.Move(AllplanGeo.Vector3D(3000, 0, 475))

        return AllplanReinf.MeshPlacement(2, AllplanGeo.Vector3D(0, 1950, 0), shape)


    def create_open_stirrup_mesh_placement(self) -> AllplanReinf.MeshPlacement:
        """ create the u shape mesh placement

        Returns:
            mesh placements of the u shape mesh
        """

        build_ele = self.build_ele

        mesh_bending_dir = AllplanReinf.MeshBendingDirection.LongitudinalBars

        model_angles = RotationUtil(90, 0, 0)

        shape_props = ReinforcementShapeProperties.mesh(build_ele.MeshType.value, mesh_bending_dir,
                                                        build_ele.BendingRoller.value, build_ele.ConcreteGrade.value,
                                                        AllplanReinf.BendingShapeType.LongitudinalBar)

        shape = GeneralReinfShapeBuilder.create_open_stirrup(3000, 300, model_angles, shape_props,
                                                             ConcreteCoverProperties.all(25), -1, -1)

        shape.Move(AllplanGeo.Vector3D(3000, 25, 0))

        return AllplanReinf.MeshPlacement(3, AllplanGeo.Vector3D(0, 1950, 0), shape)


    def create_label_properties(self) -> AllplanReinf.MeshLabelProperties:
        """ Create label properties

        Returns:
            label properties for the reinforcement mesh
        """

        build_ele = self.build_ele


        #----------------- label properties

        label_props                    = AllplanReinf.MeshLabelProperties()
        label_props.ShowPositionNumber = build_ele.ShowPositionNumber.value
        label_props.ShowMeshType       = build_ele.ShowMeshType.value
        label_props.ShowMeshCount      = build_ele.ShowMeshCount.value
        label_props.ShowMeshDimensions = build_ele.ShowMeshDimensions.value
        label_props.ShowPositionAtEnd  = build_ele.ShowPositionAtEnd.value

        return label_props


    def set_text_properties(self,
                            label: AllplanReinf.MeshLabel) -> AllplanReinf.MeshLabel:
        """ set the

        Args:
            label: label for the reinforcement

        Returns:
            Reinforcement label
        """

        build_ele = self.build_ele


        #----------------- text properties

        text_props           = build_ele.LabelTextProp.value
        text_props.Alignment = TextAlignmentUtil.get_text_alignment_from_ref_point_button_index(build_ele.RefPointPosition.value)    # pylint: disable = line-too-long
        text_props.TextAngle = AllplanGeo.Angle.FromDeg(build_ele.Angle.value)


        #----------------- text properties

        label.PointerProperties = build_ele.PointerProperties.value
        label.TextProperties    = text_props
        label.ShowTextPointer   = build_ele.ShowTextPointer.value

        if build_ele.ShowTextPointer.value:
            label.AutomaticTextPointer = build_ele.AutomaticTextPointer.value

            if not build_ele.AutomaticTextPointer.value:
                label.PointerStartPoint = build_ele.PointerStartPoint.value

        return label


    def create_view(self) -> AllplanBasisEle.ViewSectionElement:
        """ create the view of the reinforcement

        Returns:
            front view of the reinforcement
        """

        #----------------- initialize the view properties

        view_props = AllplanBasisEle.SectionGeneralProperties(True)

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

        view_draw_files_props = AllplanBasisEle.SectionDrawingFilesProperties()

        drawing_file_number = AllplanUtility.VecIntList()
        drawing_file_number.append(AllplanBaseEle.DrawingFileService.GetActiveFileNumber())

        view_draw_files_props.DrawingNumbers = drawing_file_number


        #----------------- section filter properties

        view_filter_props.DrawingFilesProperties = view_draw_files_props
        view_filter_props.IsAssociativityOn      = True


        #----------------- section light properties

        view_light_props.ConsiderLight = False


        #----------------- section scale properties

        view_scale_props.Factor_X_direction = 1.0
        view_scale_props.Factor_Y_direction = 1.0


        #----------------- general section properties

        view_props = AllplanBasisEle.SectionGeneralProperties(True)

        view_props.Status             = AllplanBasisEle.SectionGeneralProperties.State.Hidden
        view_props.FormatProperties   = view_format_props
        view_props.FilterProperties   = view_filter_props
        view_props.LabelingProperties = view_label_props
        view_props.LightProperties    = view_light_props
        view_props.ScaleProperties    = view_scale_props
        view_props.ReferenceScale     = 1.0


        #----------------- front view

        view_ele = AllplanBasisEle.ViewSectionElement()

        front_view_place_pnt = AllplanGeo.Point2D(0, 3000)

        view_props.PlacementPoint     = front_view_place_pnt
        view_props.PlacementPointType = AllplanBasisEle.SectionGeneralProperties.PlacementPointPosition.TopLeft

        view_ele.GeneralSectionProperties = view_props
        view_ele.ViewMatrix               = RotationUtil(-90, 0, 0).get_rotation_matrix()

        label2 = AllplanReinf.MeshLabel(2, self.create_label_properties(), 1, 0.3, AllplanGeo.Vector2D(0, 500))
        label3 = AllplanReinf.MeshLabel(3, self.create_label_properties(), 2, 0.5, AllplanGeo.Vector2D(0, -500))

        self.set_text_properties(label2)
        self.set_text_properties(label3)

        view_ele.MeshLabels = AllplanReinf.MeshLabelList([label2, label3])

        return view_ele
