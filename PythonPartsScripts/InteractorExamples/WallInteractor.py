""" Script for WallInteractor
"""

from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_ArchElements as AllplanArchElements
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_IFW_Input as AllplanIFW

from BuildingElement import BuildingElement
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from CreateElementResult import CreateElementResult
from PythonPartPreview import PythonPartPreview
from PythonPartTransaction import PythonPartTransaction
from PythonPartUtil import PythonPartUtil
from StringTableService import StringTableService

from TypeCollections.ModificationElementList import ModificationElementList

from Utils.FormatUtil import FormatUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.WallInteractorBuildingElement import WallInteractorBuildingElement
else:
    WallInteractorBuildingElement = BuildingElement

print('Load WallInteractor.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of library preview

    Args:
        _build_ele: the building element.
        _doc:       input document

    Returns:
        created element result
    """

    com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    return CreateElementResult([AllplanBasisElements.ModelElement3D(com_prop, AllplanGeo.Polyhedron3D.CreateCuboid(5000, 300, 2500))])




def create_interactor(coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties],
                      _modification_ele_list  : ModificationElementList) -> Any:
    """ Create the interactor

    Args:
        coord_input:              API object for the coordinate input, element selection, ... in the Allplan view
        pyp_path:                 path of the pyp file
        global_str_table_service: global string table service
        build_ele_list:           list with the building elements
        build_ele_composite:      building element composite with the building element constraints
        control_props_list:       control properties list
        _modification_ele_list:   UUIDs of the existing elements in the modification mode

    Returns:
          Created interactor object
    """

    return WallInteractor(coord_input, pyp_path, global_str_table_service, build_ele_list, build_ele_composite, control_props_list)


class WallInteractor():
    """ Definition of class WallInteractor
    """

    def __init__(self,coord_input             : AllplanIFW.CoordinateInput,
                      pyp_path                : str,
                      global_str_table_service: StringTableService,
                      build_ele_list          : list[BuildingElement],
                      build_ele_composite     : BuildingElementComposite,
                      control_props_list      : list[BuildingElementControlProperties]):
        """ Create the interactor

        Args:
            coord_input:               coordinate input
            pyp_path:                  path of the pyp file
            global_str_table_service:  global string table service
            build_ele_list:            building element list
            build_ele_composite:       building element composite
            control_props_list:        control properties list
        """

        self.coord_input                    = coord_input
        self.pyp_path                       = pyp_path
        self.str_table_service              = global_str_table_service
        self.first_point_input              = True
        self.first_point                    = AllplanGeo.Point3D()
        self.wall_ele_list                  = []
        self.build_ele_list                 = build_ele_list
        self.control_props_list             = control_props_list
        self.build_ele                      = cast(WallInteractorBuildingElement, build_ele_list[0])
        self.is_start_new_joined_wall_group = True


        #----------------- show the palette

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, build_ele_composite,
                                                             None,
                                                             self.control_props_list,
                                                             AllplanSettings.AllplanPaths.GetPythonPartsEtcPath() + \
                                                             "PythonPartsFramework\\GeneralScripts\\Bitmaps\\")

        FormatUtil.update_build_ele_list_values(self.build_ele)

        self.palette_service.show_palette(self.build_ele.script_name)



        #----------------- get the properties and start the input

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

        self.set_wall_properties()


    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """ Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        update_palette = self.palette_service.modify_element_property(page, name, value)

        build_ele = self.build_ele

        if name == "AxisFromTop":
            build_ele.AxisFromBottom.value = build_ele.OverallThickness.value - value

            update_palette = True

        elif name == "AxisFromBottom":
            build_ele.AxisFromTop.value = build_ele.OverallThickness.value - value

            update_palette = True

        elif name.find("Thickness[") != -1 or name == "TierCount":
            build_ele.OverallThickness.value = sum(build_ele.Thickness.value)

            update_palette = True

        elif name.find("Is") == 0 and value is True:
            index = build_ele.TierIndex.value - 1

            update_palette = True

            if name.find("IsHatch") != -1:
                build_ele.IsPattern.value[index]   = False
                build_ele.IsFaceStyle.value[index] = False

            elif name.find("IsPattern") != -1:
                build_ele.IsHatch.value[index]     = False
                build_ele.IsFaceStyle.value[index] = False

            elif name.find("IsFaceStyle") != -1:
                build_ele.IsHatch.value[index]   = False
                build_ele.IsPattern.value[index] = False

        if FormatUtil.update_build_ele_list_values(self.build_ele) or update_palette:
            self.palette_service.update_palette(-1, False)

        self.set_wall_properties()

        self.on_preview_draw()


    def on_control_event(self, event_id: int):
        """ On control event

        Args:
            event_id: event id of control.
        """

        if event_id in {1001, 1002}:
            tier_count = self.build_ele.TierCount.value

            if event_id == 1001:
                if self.build_ele.TierIndex.value == tier_count:
                    return

                self.build_ele.TierIndex.value += 1
            else:
                if self.build_ele.TierIndex.value == 1:
                    return

                self.build_ele.TierIndex.value -= 1

            self.palette_service.update_palette(-1, False)


    def on_cancel_by_menu_function(self):
        """ Check for input function cancel in case of a started menu function
        """

        self.palette_service.close_palette()


    def on_cancel_function(self) -> bool:
        """ Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        if self.first_point_input:
            self.palette_service.close_palette()

            return True

        self.first_point_input = True

        self.coord_input.InitFirstPointInput(AllplanIFW.InputStringConvert("From point"))

        self.is_start_new_joined_wall_group = True

        return False


    def on_preview_draw(self):
        """ Handles the preview draw event
        """

        if self.first_point_input:
            return

        input_pnt = self.coord_input.GetCurrentPoint(self.first_point).GetPoint()

        self.draw_preview(input_pnt)


    def on_mouse_leave(self):
        """ Handles the mouse leave event
        """

        self.on_preview_draw()


    def process_mouse_msg(self,
                          mouse_msg: int,
                          pnt      : AllplanGeo.Point2D,
                          msg_info : Any) -> bool:
        """ Handles the process mouse message event

        Args:
            mouse_msg: the mouse message.
            pnt      : the input point.
            msg_info : additional message info.

        Returns:
            True/False for success.
        """

        input_pnt = self.coord_input.GetInputPoint(mouse_msg, pnt, msg_info,
                                                   self.first_point, not self.first_point_input).GetPoint()


        #----------------- Set the input point

        if self.first_point_input:
            self.first_point = input_pnt

        else:
            self.draw_preview(input_pnt)

        if self.coord_input.IsMouseMove(mouse_msg):
            return True


        #----------------- Change to "To point" input

        if self.first_point_input:
            self.first_point_input = False

            self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("To point"))

            return True


        #----------------- stand-alone elements

        if not self.build_ele.IsPythonPart.value:
            AllplanBaseElements.CreateElements(self.coord_input.GetInputViewDocument(),
                                               AllplanGeo.Matrix3D(),
                                               self.wall_ele_list, [], None)


        #----------------- create the PythonPart (create a box for selection)

        else:
            sphere = AllplanGeo.BRep3D.CreateSphere(AllplanGeo.AxisPlacement3D((self.first_point + input_pnt) / 2), 500)

            com_prop = AllplanBaseElements.CommonProperties()
            com_prop.GetGlobalProperties()
            com_prop.HelpConstruction = True

            pyp_util = PythonPartUtil()

            pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, sphere))
            pyp_util.add_architecture_elements(self.wall_ele_list)

            pyp_transaction = PythonPartTransaction(self.coord_input.GetInputViewDocument())

            pyp_transaction.execute(AllplanGeo.Matrix3D(),
                                    self.coord_input.GetViewWorldProjection(),
                                    pyp_util.create_pythonpart(self.build_ele),
                                    ModificationElementList())

            self.build_ele.StartPoint.value = self.first_point
            self.build_ele.EndPoint.value   = input_pnt


        #----------------- next input point

        self.is_start_new_joined_wall_group = False

        self.first_point = input_pnt

        self.coord_input.InitNextPointInput(AllplanIFW.InputStringConvert("From point"))

        return True


    def draw_preview(self, input_pnt: AllplanGeo.Point3D):
        """ Draw the preview

        Args:
            input_pnt:  Input point
        """

        axis = AllplanGeo.Line2D(AllplanGeo.Point2D(self.first_point),AllplanGeo.Point2D(input_pnt))

        self.wall_prop.IsStartNewJoinedWallGroup = self.is_start_new_joined_wall_group

        wall_ele = AllplanArchElements.WallElement(self.wall_prop, axis)

        self.wall_ele_list = [wall_ele]

        PythonPartPreview.execute(self.coord_input.GetInputViewDocument(), AllplanGeo.Matrix3D(),
                                  self.wall_ele_list, True)


    def set_wall_properties(self):
        """ set the wall properties """

        build_ele = self.build_ele

        wall_prop      = AllplanArchElements.WallProperties()
        wall_axis_prop = AllplanArchElements.AxisProperties()

        wall_axis_prop.Distance  = build_ele.AxisFromTop.value
        wall_axis_prop.Extension = 1 if build_ele.MirroTiers.value else -1
        wall_axis_prop.Position  = AllplanArchElements.WallAxisPosition.eFree

        tier_count = build_ele.TierCount.value

        wall_prop.SetTierCount(tier_count)
        wall_prop.SetAxis(wall_axis_prop)


        #----------------- set the tier properties

        for tier_index in range(tier_count):
            wall_tier_prop = wall_prop.GetWallTierProperties(tier_index + 1)

            com_prop = AllplanBaseElements.CommonProperties()

            com_prop.Color         = build_ele.Color.value[tier_index]
            com_prop.Pen           = build_ele.Pen.value[tier_index]
            com_prop.Stroke        = build_ele.Stroke.value[tier_index]
            com_prop.ColorByLayer  = build_ele.ColorByLayer.value[tier_index]
            com_prop.PenByLayer    = build_ele.PenByLayer.value[tier_index]
            com_prop.StrokeByLayer = build_ele.StrokeByLayer.value[tier_index]
            com_prop.Layer         = build_ele.Layer.value[tier_index]

            wall_tier_prop.SetThickness(build_ele.Thickness.value[tier_index])
            wall_tier_prop.SetCommonProperties(com_prop)

            if build_ele.IsFilling.value[tier_index]:
                wall_tier_prop.SetBackgroundColor(build_ele.FillingId.value[tier_index])
            else:
                wall_tier_prop.ResetBackgroundColor()

            wall_tier_prop.SetHatch(0)
            wall_tier_prop.SetPattern(0)
            wall_tier_prop.SetFaceStyle(0)

            if build_ele.IsHatch.value[tier_index]:
                wall_tier_prop.SetHatch(build_ele.HatchId.value[tier_index])

            elif build_ele.IsPattern.value[tier_index]:
                wall_tier_prop.SetPattern(build_ele.PatternId.value[tier_index])

            elif build_ele.IsFaceStyle.value[tier_index]:
                wall_tier_prop.SetFaceStyle(build_ele.FaceStyleId.value[tier_index])

            elif build_ele.IsFilling.value[tier_index]:
                wall_tier_prop.SetFilling(build_ele.FillingId.value[tier_index])
                wall_tier_prop.ResetBackgroundColor()

            wall_tier_prop.SetPlaneReferences(build_ele.PlaneReferences.value[tier_index])

            wall_tier_prop.SetMaterial(build_ele.Material.value[tier_index])
            wall_tier_prop.SetTrade(build_ele.Trade.value[tier_index])

        self.wall_prop = wall_prop
