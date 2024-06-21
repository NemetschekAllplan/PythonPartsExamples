""" Elementplan example """

import NemAll_Python_AllplanSettings as AllplanSettings             # pylint: disable=import-error
import NemAll_Python_IFW_Input as AllplanIFW                        # pylint: disable=import-error
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter    # pylint: disable=import-error
import NemAll_Python_Precast as MultiMaterialPlan                   # pylint: disable=import-error
import NemAll_Python_Geometry as AllplanGeo                         # pylint: disable=import-error
import NemAll_Python_BaseElements as AllplanBaseElements            # pylint: disable=import-error
import NemAll_Python_BasisElements as AllplanBasisElements          # pylint: disable=import-error

from PythonPartTransaction import PythonPartTransaction
from BuildingElement import BuildingElement
from .MWSPlacement import RebarPlacement

# Print some information
print('Load Elementplan.py')

def check_allplan_version(__build_ele: BuildingElement,
                          _version   : str) -> bool:
    """ Check the current Allplan version

    Args:
        :param __build_ele: the building element.
        :param _version:    the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    del __build_ele
    del _version

    # Support all versions
    return True

def create_preview(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> tuple:
    """ Creation of the preview

    Args:
        :param _build_ele:  the building element.
        :param _doc:        document

    Returns:
            created preview tuple with elements and handles.
    """
    del _build_ele
    del _doc

    com_prop = AllplanBaseElements.CommonProperties()
    com_prop.GetGlobalProperties()

    text_prop = AllplanBasisElements.TextProperties()
    model_ele_list = [AllplanBasisElements.TextElement(com_prop, text_prop, "Elementplan", AllplanGeo.Point2D(0, 100))]

    return (model_ele_list, [])

def create_element(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> tuple:
    """ Creation of element

    Args:
        :param _build_ele:  the building element.
        :param _doc:        input _doc

    Returns:
            created Elementplan tuple with elements and handles.
    """

    python_elementplan = PythonElementplan(_build_ele, _doc)

    return python_elementplan.create_element()

def on_control_event(build_ele: BuildingElement,
                     event_id : int,
                     doc      : AllplanElementAdapter.DocumentAdapter) -> None:
    """ handle the button click

    Args:
        :param build_ele:   build_ele
        :param event_id:    eventID
        :param doc:         doc
    """
    if event_id == 1001:
        python_elementplan = PythonElementplan(build_ele, doc)
        python_elementplan.create_plan()

class PythonElementplan:
    """ class for pyhon elementplan
    """
    def __init__(self,
                 _build_ele: BuildingElement,
                 _doc      : AllplanElementAdapter.DocumentAdapter) -> None:
        """ Initialization
        Args:
            :param _build_ele:  the building element.
            :param _doc:        input _doc
        """

        self.build_ele = _build_ele
        self.doc = _doc

        self.model_elem_list = []
        self.handle_list = []
        self.common_props = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()
        self.name = "Elementplan"
        self.pyp_transaction = PythonPartTransaction(self.doc)

    def create_element(self) -> tuple:
        """ Creation of element

        Returns:
            :return tuple:  created elements and handles.
        """
        return (self.model_elem_list, self.handle_list)

    def create_mws_group(self) -> AllplanElementAdapter.BaseElementAdapter:
        """Creates a MWS group for debug elementplan

        Returns:
            AllplanElementAdapter.BaseElementAdapter: MWSGroup
        """

        mws = RebarPlacement(self.doc)
        mws_ele_list = mws.create(self.build_ele)[0]

        base_ele_adapter = self.pyp_transaction.execute(AllplanGeo.Matrix3D(),
                                AllplanIFW.ViewWorldProjection(),
                                mws_ele_list,
                                [])

        for tmp in base_ele_adapter:
            child_eles = AllplanElementAdapter.BaseElementAdapterChildElementsService.GetChildModelElements(tmp, True)
            for ele in child_eles:
                if ele.GetElementAdapterType().GetGuid() == AllplanElementAdapter.PrecastReinforcementGroup_TypeUUID:
                    return ele

        return AllplanElementAdapter.BaseElementAdapter()

    def create_plan(self) -> None:
        """ Creates the elementplan
        """
        # Plan
        plan = MultiMaterialPlan.Plan(self.doc)#, AllplanElementAdapter.BaseElementAdapterList([self.create_mws_group()]))
        plan.Offset = AllplanGeo.Point2D(8000.0, 0.0)
        # plan.DrawingFile = 27

        # Page
        page = MultiMaterialPlan.Page(doc=self.doc,
                                      pageNr=1,
                                      scale=25.0,
                                      anchors=[],
                                      centeringCells=True,
                                      size=AllplanGeo.MinMax2D(AllplanGeo.Point2D(0.0, -210.0), AllplanGeo.Point2D(297.0, 0.0)))#,
                                    #   conditionTemplate="@507@ = \"MWS_1\"")
        # page.DrawingFile = 28

        # Views
        view1 = MultiMaterialPlan.View(doc=self.doc,
                                      cellId=1,
                                      direction=MultiMaterialPlan.Direction.eDirectionI,
                                      rotation=MultiMaterialPlan.Rotation.eRotation270,
                                      viewProps=MultiMaterialPlan.ViewProperties())
        page.add_cell(view1)
        view2 = MultiMaterialPlan.View(doc=self.doc,
                                       cellId=2,
                                       direction=MultiMaterialPlan.Direction.eDirectionIV,
                                       rotation=MultiMaterialPlan.Rotation.eRotation270)
        page.add_cell(view2)
        view3 = MultiMaterialPlan.View(doc=self.doc,
                                       cellId=3,
                                       direction=MultiMaterialPlan.Direction.eDirectionV,
                                       rotation=MultiMaterialPlan.Rotation.eRotation90)
        page.add_cell(view3)

        # Legend
        legend_props = MultiMaterialPlan.LegendProperties()
        legend_props.FileEntryPath = MultiMaterialPlan.FileEntryPath.eFileEntryPathStandard
        legend_props.FileNr = 19
        legend_props.EntryNr = 42
        legend_props.MaxHeight = 150.0
        legend_props.MaxWidth = 100.0
        legend = MultiMaterialPlan.Legend(doc=self.doc,
                                          cellId=4,
                                          legendProps=legend_props)#,
                                        #   conditionTemplate="@507@ = \"Legend\"")
        page.add_cell(legend)


        # LabelStyle
        label_style_props = MultiMaterialPlan.LabelStyleProperties()
        label_style_props.FileEntryPath = MultiMaterialPlan.FileEntryPath.eFileEntryPathStandard
        label_style_props.FileNr = 8
        label_style_props.EntryNr = 18
        label_style = MultiMaterialPlan.LabelStyle(self.doc,
                                                   cellId=5,
                                                   labelStyleProps=label_style_props,
                                                   allowOverlapping=False)#,
                                                #    conditionTemplate="@507@ = \"LabelStyle\"")
        page.add_cell(label_style)

        # Anchors
        anchors = []

        # Anchor View1 -> View2
        anchors.append(MultiMaterialPlan.Anchor(id=1,
                                                fromCell=view1,
                                                fromPos=MultiMaterialPlan.AnchorBorderPosition.eBorderRight,
                                                toCell=view2,
                                                toPos=MultiMaterialPlan.AnchorBorderPosition.eBorderLeft,
                                                align=False,
                                                offsetX=25.0,
                                                offsetY=0.0))
        # Anchor View1 -> View3
        anchors.append(MultiMaterialPlan.Anchor(id=2,
                                                fromCell=view1,
                                                fromPos=MultiMaterialPlan.AnchorBorderPosition.eBorderBottom,
                                                toCell=view3,
                                                toPos=MultiMaterialPlan.AnchorBorderPosition.eBorderTop,
                                                align=False,
                                                offsetX=0.0,
                                                offsetY=25.0))
        # Anchor Page -> Legend
        anchors.append(MultiMaterialPlan.Anchor(id=3,
                                                fromPos=MultiMaterialPlan.AnchorBorderPosition.eCornerRightTop,
                                                toId=4,
                                                toPos=MultiMaterialPlan.AnchorBorderPosition.eCornerRightTop,
                                                offsetX=-10.0,
                                                offsetY=10.0))

        # Anchor Page -> LabelStyle
        anchors.append(MultiMaterialPlan.Anchor(id=4,
                                                fromPos=MultiMaterialPlan.AnchorBorderPosition.eCornerRightBottom,
                                                toId=5,
                                                toPos=MultiMaterialPlan.AnchorBorderPosition.eCornerRightBottom))

        page.add_anchors(anchors)

        plan.add_page(page)

        # Page 2
        # page2 = MultiMaterialPlan.Page(doc=self.doc,
        #                               pageNr=2,
        #                               anchors=[],
        #                               scale=25.0,
        #                               centeringCells=True,
        #                               size=AllplanGeo.MinMax2D(AllplanGeo.Point2D(0.0, -297.0), AllplanGeo.Point2D(210.0, 0.0)))#,
        #                             #   conditionTemplate="@507@ = \"MWS_1\"")
        # # page2.DrawingFile = 28
        # view2 = MultiMaterialPlan.View(doc=self.doc,
        #                               cellId=2,
        #                               direction=MultiMaterialPlan.Direction.eDirectionI,
        #                               rotation=MultiMaterialPlan.Rotation.eRotation270)
        # page2.add_cell(view2)
        # plan.add_page(page2)

        # Create elementplan
        ele_plan = AllplanElementAdapter.BaseElementAdapter()

        if plan.create(ele_plan, AllplanElementAdapter.BaseElementAdapterList([self.create_mws_group()])):
            self.model_elem_list = [ele_plan]
            _ = self.pyp_transaction.execute(AllplanGeo.Matrix3D(),
                                        AllplanIFW.ViewWorldProjection(),
                                        self.model_elem_list,
                                        [])
