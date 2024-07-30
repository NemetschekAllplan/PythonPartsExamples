"""Example script showing the implementation of Offset function,
to calculate parallel curves
"""
from typing import TYPE_CHECKING, Any, List, Tuple, Union, cast

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFWInput
from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from ControlProperties import ControlProperties
from StringTableService import StringTableService
from TypeCollections.ModelEleList import ModelEleList

from GeometryExamples.Operations import OperationExampleBaseInteractor

if TYPE_CHECKING:
    from __BuildingElementStubFiles.CurveOffsetBuildingElement import (
        CurveOffsetBuildingElement,
    )
else:
    CurveOffsetBuildingElement = BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """Called when the PythonPart is started to check, if the current
    Allplan version is supported.

    Args:
        _build_ele: building element with the parameter properties
        _version:   current Allplan version

    Returns:
        True if current Allplan version is supported and PythonPart script can be run, False otherwise
    """

    return True


def create_interactor(coord_input              : AllplanIFWInput.CoordinateInput,
                      _pyp_path                : str,
                      _global_str_table_service: StringTableService,
                      build_ele_list           : List[BuildingElement],
                      build_ele_composite      : BuildingElementComposite,
                      control_props_list       : List[ControlProperties],
                      _modify_uuid_list        : List[str]) -> Any       :
    """Function for the interactor creation, called when PythonPart is initialized.

    Args:
        coord_input:               coordinate input
        _pyp_path:                 path of the pyp file
        _global_str_table_service: global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:         UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return CurveOffsetInteractor(coord_input,
                                 build_ele_list,
                                 build_ele_composite,
                                 control_props_list)


class CurveOffsetInteractor(OperationExampleBaseInteractor):
    """ Curve offset interactor showing the example implementation of the Offset function
    from the NemAll_Python_Geometry module. the calculation is performed on one of the
    two ways: using the offset distance or a helping point. In the first case the user
    only selects the curve to offset. In second case, an additional workflow step is introduced,
    where the user is prompt to input a point.

    Attributes:
        build_ele:              contains, among others, parameter properties from the palette
        selected_curve:         curve selected by the user to perform offset operation on
        offset_plane:           reference plane for the offset calculation of 3D curves
        input_mode:             indicates, whether a curve selection or point input is active
        post_element_selection: object containing selected elements after successful selection
    """

    def __init__(self,
                 coord_input        : AllplanIFWInput.CoordinateInput,
                 build_ele_list     : List[BuildingElement],
                 build_ele_composite: BuildingElementComposite,
                 control_props_list : List[ControlProperties])       :
        """ Constructor

        Args:
            coord_input:               coordinate input
            build_ele_list:            list with the building elements containing parameter properties
            build_ele_composite:       building element composite
            control_props_list:        control properties list
        """

        # set initial values
        self.build_ele      = cast(CurveOffsetBuildingElement, build_ele_list[0])
        self.selected_curve = AllplanElementAdapter.BaseElementAdapter()
        self.offset_plane   = AllplanGeometry.Plane3D(self.build_ele.PlaneRefPoint.value,
                                                      self.build_ele.PlaneNormalVector.value)

        self.post_element_selection: Union[AllplanIFWInput.PostElementSelection, None] = None

        super().__init__(coord_input,
                         build_ele_list,
                         build_ele_composite,
                         control_props_list)

        # start element selection
        self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
        self.whitelist = [AllplanGeometry.Arc2D,
                          AllplanGeometry.Arc3D,
                          AllplanGeometry.Line2D,
                          AllplanGeometry.Line3D,
                          AllplanGeometry.Path2D,
                          AllplanGeometry.Path3D,
                          AllplanGeometry.Polyline2D,
                          AllplanGeometry.Polyline3D,
                          AllplanGeometry.Spline2D,
                          AllplanGeometry.Spline3D,
                          ]
        self.start_geometry_selection("Select a curve", self.whitelist)

    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any) -> None:
        """ Called after each property modification in the property palette.

        Args:
            page:   index of the page, beginning with 0
            name:   name of the modified property
            value:  new property value
        """

        super().modify_element_property(page, name, value)

        # When reference point or normal vector of the offset plane is modified
        # the plane is recalculated
        if name.startswith(("PlaneRefPoint", "PlaneNormalVector")):
            self.offset_plane = AllplanGeometry.Plane3D(self.build_ele.PlaneRefPoint.value,
                                                        self.build_ele.PlaneNormalVector.value)
            print("\n\nNew offset plane:")
            print(self.offset_plane)

    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeometry.Point2D,
                          msg_info : AllplanIFWInput.AddMsgInfo) -> bool:
        """ Called on each mouse message. A mouse message can be mouse movement,
        pressing a mouse button or releasing it.

        Args:
            mouse_msg: the mouse message (e.g. 512 - mouse movement)
            pnt:       the input point in view coordinates
            msg_info:  additional message info.

        Returns:
            True/False for success.
        """

        # selection mode for selecting curve to offset
        if self.input_mode == self.InteractorInputMode.ELEMENT_SELECTION and self.post_element_selection:
            selected_elements           = self.post_element_selection.GetSelectedElements(self.coord_input.GetInputViewDocument())
            self.post_element_selection = None

            # if nothing selected, restart selection
            if len(selected_elements) == 0:
                self.start_geometry_selection("Select a curve")
                return True

            self.selected_curve = selected_elements[0]

            # if the input type "by distance" was selected, perform offset calculation
            if self.build_ele.InputType.value == 1:
                curve             = self.selected_curve.GetGeometry()
                err, offset_curve = self.calculate_offset_by_distance(curve)

                if err == AllplanGeometry.eOK:
                    self.create_offset_curve(offset_curve)

            # otherwise, prompt for a reference point
            else:
                self.start_point_input("Reference point")
                self.input_mode = self.InteractorInputMode.COORDINATE_INPUT
                return True

        # coordinate input mode for the offset reference point
        elif self.input_mode == self.InteractorInputMode.COORDINATE_INPUT:
            reference_point = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info).GetPoint()
            curve           = self.selected_curve.GetGeometry()

            # perform offset calculation by a reference point
            err, offset_curve = self.calculate_offset_by_point(
                curve, reference_point)

            # if mouse is moved and offset calculation was successful, draw a preview
            if self.coord_input.IsMouseMove(mouse_msg):
                if err == AllplanGeometry.eOK:
                    self.draw_offset_curve_preview(offset_curve)
                return True

            # in case of click and successful calculation, create the curve
            if err == AllplanGeometry.eOK:
                self.create_offset_curve(offset_curve)

        else:
            return True

        print("\n\n-------- Curve offset result ------",
              f"Offset operation on {self.selected_curve.GetDisplayName()} (geometry type: {type(self.selected_curve.GetGeometry()).__name__})",
              f"resulted in: {err}",
              "-----------------------------------",
              sep="\n")

        # clear the memory
        self.selected_curve = AllplanElementAdapter.BaseElementAdapter()

        # restart selection
        self.input_mode = self.InteractorInputMode.ELEMENT_SELECTION
        self.start_geometry_selection("Additional info in trace; select next curve",
                                      self.whitelist)
        return True

    def calculate_offset_by_point(self,
                                  curve: Any,
                                  point: AllplanGeometry.Point3D) -> Tuple[AllplanGeometry.eGeometryErrorCode, Any]:
        """Calculates a parallel to a given curve by a helping point and (if needed)
        other parameters specified in the property palette (e.g., the number of parallel
        curves) using the Offset function of the NemAll_Python_Geometry module

        Args:
            curve:  geometry of the curve to calculate offset curve for
            point:  reference point

        Returns:
            geometry error code (eOK if operation was successful)
            offset curve
        """
        # implementation for all 2D curves
        if isinstance(curve, (AllplanGeometry.Arc2D,
                              AllplanGeometry.Line2D,
                              AllplanGeometry.Path2D,
                              AllplanGeometry.Polyline2D,
                              AllplanGeometry.Spline2D)):
            point_2d = AllplanGeometry.Point2D(point)  # convert 3D point to 2D
            return AllplanGeometry.Offset(point_2d, curve)

        # implementation for 3D arcs
        if isinstance(curve, AllplanGeometry.Arc3D):
            return AllplanGeometry.Offset(point, curve)

        # implementation for 3D lines
        if isinstance(curve, AllplanGeometry.Line3D):
            return AllplanGeometry.Offset(point,
                                          0,
                                          curve,
                                          AllplanGeometry.Offset3DPlane.names[self.build_ele.Offset3DPlane.value])

        # implementation for 3D splines
        if isinstance(curve, AllplanGeometry.Spline3D):
            return AllplanGeometry.Offset(point,
                                          curve,
                                          self.offset_plane)

        # implementation for 3D splines
        if isinstance(curve, AllplanGeometry.Polyline3D):
            return AllplanGeometry.Offset(point,
                                          self.offset_plane,
                                          self.build_ele.ParallelsCount.value,
                                          curve)

        return AllplanGeometry.eError, None

    def calculate_offset_by_distance(self, curve: Any) -> Tuple[AllplanGeometry.eGeometryErrorCode, Any]:
        """Calculates a parallel to a given curve by offset distance and (if needed)
        other parameters specified in the property palette (e.g. the number of parallel
        curves) using the Offset function of the NemAll_Python_Geometry module

        Args:
            curve:  geometry of the curve to calculate offset curve for

        Returns:
            geometry error code (eOK if operation was successful)
            offset curve
        """
        # implementation for two dimensional lines and arcs
        if isinstance(curve, (AllplanGeometry.Arc2D,
                              AllplanGeometry.Line2D)):
            return AllplanGeometry.Offset(self.build_ele.OffsetDistance.value,
                                          curve)

        # implementation for two dimensional polylines and splines
        if isinstance(curve, (AllplanGeometry.Path2D,
                              AllplanGeometry.Polyline2D,
                              AllplanGeometry.Spline2D)):
            return AllplanGeometry.Offset(self.build_ele.OffsetDistance.value,
                                          curve,
                                          self.build_ele.CheckSegmentsOrientation.value)

        # implementation for three dimensional arc
        if isinstance(curve, AllplanGeometry.Arc3D):
            return AllplanGeometry.Offset(self.build_ele.OffsetDistance.value,
                                          curve)

        # implementation for three dimensional line
        if isinstance(curve, AllplanGeometry.Line3D):
            return AllplanGeometry.Offset(AllplanGeometry.Point3D(),
                                          self.build_ele.OffsetDistance.value,
                                          curve,
                                          AllplanGeometry.Offset3DPlane.names[self.build_ele.Offset3DPlane.value])

        # implementation for three dimensional polyline
        if isinstance(curve, AllplanGeometry.Polyline3D):
            return AllplanGeometry.Offset(self.build_ele.OffsetDistance.value,
                                          self.offset_plane,
                                          self.build_ele.ParallelsCount.value,
                                          curve)

        # implementation for three dimensional spline
        if isinstance(curve, AllplanGeometry.Spline3D):
            return AllplanGeometry.Offset(self.build_ele.OffsetDistance.value,
                                          curve,
                                          self.offset_plane,
                                          self.build_ele.CheckSegmentsOrientation.value)

        # implementation for three dimensional path
        if isinstance(curve, AllplanGeometry.Path3D):
            return AllplanGeometry.Offset(curve,
                                          self.build_ele.PlaneNormalVector.value,
                                          self.build_ele.OffsetDistance.value)

        return AllplanGeometry.eError, None

    def create_offset_curve(self, curve_geometry: Any):
        """Creates a model element in the current drawing file representing the given
        curve (2D or 3D). The common properties used fro creation come from the curve
        selected by the user for the offset calculation.

        Args:
            curve_geometry: geometry of the curve, that is to be created

        """
        common_props = self.selected_curve.GetCommonProperties()

        offset_curve = ModelEleList(common_props)

        if self.selected_curve.Is3DElement():
            offset_curve.append_geometry_3d(curve_geometry)
        else:
            offset_curve.append_geometry_2d(curve_geometry)

        AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                           AllplanGeometry.Matrix3D(),
                                           offset_curve,
                                           modelUuidList = [],
                                           assoRefObj    = None)

    def draw_offset_curve_preview(self, curve_geometry: Any):
        """Draws a preview of the given curve (2D or 3D) as a red line.

        Args:
            curve_geometry: geometry of the curve, that is to be previewed

        """
        common_props = AllplanBaseElements.CommonProperties()
        common_props.Color = 6

        offset_curve = ModelEleList(common_props)
        if self.selected_curve.Is3DElement():
            offset_curve.append_geometry_3d(curve_geometry)
        else:
            offset_curve.append_geometry_2d(curve_geometry)

        AllplanBaseElements.DrawElementPreview(doc          = self.coord_input.GetInputViewDocument(),
                                               insertionMat = AllplanGeometry.Matrix3D(),
                                               modelEleList = offset_curve,
                                               bDirectDraw  = False,
                                               assoRefObj   = None)
