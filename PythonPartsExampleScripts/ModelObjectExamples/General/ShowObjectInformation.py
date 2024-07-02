""" Show the object information accessed by the BaseElementAdapter
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import NemAll_Python_BaseElements as AllplanBaseEle
import NemAll_Python_BasisElements as AllplanBasisEle
import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil
from BaseScriptObject import BaseScriptObject
from CreateElementResult import CreateElementResult
from ScriptObjectInteractors.SingleElementSelectInteractor import SingleElementSelectInteractor, SingleElementSelectResult
from Utils import LibraryBitmapPreview

if TYPE_CHECKING:
    from __BuildingElementStubFiles.ShowObjectInformationBuildingElement import \
        ShowObjectInformationBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement

print('Load ShowObjectInformation.py')


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


def create_preview(build_ele : BuildingElement,
                   _doc      : AllplanEleAdapter.DocumentAdapter) -> CreateElementResult:
    """ Creation of the element preview

    Args:
        build_ele:  building element with the parameter properties
        _doc:       document of the Allplan drawing files

    Returns:
        created elements for the preview
    """
    script_path = Path(build_ele.pyp_file_path) / Path(build_ele.pyp_file_name).name
    thumbnail_path = script_path.with_suffix(".png")

    return CreateElementResult(LibraryBitmapPreview.create_library_bitmap_preview(str(thumbnail_path)))


def create_script_object(build_ele  : BuildingElement,
                         coord_input: AllplanIFW.CoordinateInput) -> BaseScriptObject:
    """ Creation of the script object

    Args:
        build_ele:   building element with the parameter properties
        coord_input: API object for the coordinate input, element selection, ... in the Allplan view

    Returns:
        created script object
    """

    return ObjectInformationExtractor(build_ele, coord_input)


class ObjectInformationExtractor(BaseScriptObject):
    """Implementation of an interactor, where the user has to select a single object
    and the properties of this object, such as display name, UUIDs, attributes, common
    properties, parent and child elements are printed in the console.

    Subsequently, the user can select another object to print information about.
    Terminating the interactor happens by pressing ESC.
    """

    def __init__(self,
                 build_ele: BuildingElement,
                 coord_input: AllplanIFW.CoordinateInput):
        """Default constructor

        Args:
            build_ele:      building element with parameter values from the property palette
            coord_input:    object representing the coordinate input inside the viewport
        """
        super().__init__(coord_input)
        self.build_ele = build_ele

        self.interaction_result = SingleElementSelectResult()
        self.text_ele = AllplanBasisEle.TextElement()

    def execute(self) -> CreateElementResult:
        """Execute the element creation

        Returns:
            created element
        """
        return CreateElementResult()   # this interactor class just prints info, nothing to create

    def start_input(self):
        """Start the element selection"""

        self.script_object_interactor = SingleElementSelectInteractor(self.interaction_result)


    def start_next_input(self):
        """Print the information about selected element and restarts the input"""

        self.print_element_info(self.interaction_result.sel_element)
        self.start_input()


    def print_element_info(self, element: AllplanEleAdapter.BaseElementAdapter):
        """Print the information about the element in the trace.

        What kind information is printed depends on the options set in the property palette

        Args:
            element:    element to print the information about
        """

        doc = element.GetDocument()

        model_elements = AllplanBaseEle.GetElements(AllplanEleAdapter.BaseElementAdapterList([element]))


        print(f"{'='*50} Object information {'='*50}")
        print()

        # print the descriptive data of the selected element
        if self.build_ele.DescriptiveData.value:
            print(f"{'-'*51} Descriptive data {'-'*51}\n",
                  f"Name:                        {element.GetDisplayName()}",
                  f"Drawing file number:         {element.GetDrawingfileNumber()}",
                  f"Element adapter type:        {element.GetElementAdapterType().GetTypeName()}",
                  f"Element UUID:                {element.GetElementUUID()}",
                  f"Model element UUID:          {element.GetModelElementUUID()}",
                  f"Is 3D element:               {element.Is3DElement()}",
                  f"Is general element:          {element.IsGeneralElement()}",
                  "",
                  sep="\n"
            )


        # print the descriptive data of the parent element
        if self.build_ele.ParentObject.value:
            parent_element = AllplanEleAdapter.BaseElementAdapterParentElementService.GetParentElement(element)
            print(f"{'-'*52} Parent object {'-'*53}\n",
                  f"Name:                        {parent_element.GetDisplayName()}",
                  f"Element adapter type:        {parent_element.GetElementAdapterType().GetTypeName()}",
                  f"Element UUID:                {parent_element.GetElementUUID()}",
                  f"Model element UUID:          {parent_element.GetModelElementUUID()}",
                  f"Is 3D element:               {parent_element.Is3DElement()}",
                  f"Is general element:          {parent_element.IsGeneralElement()}",
                  "",
                  sep="\n"
            )


        # print the list of child elements; childs, grandchild, great-grandchilds, etc. are printed in one list
        if self.build_ele.ChildObjects.value and \
            (child_elements := AllplanEleAdapter.BaseElementAdapterChildElementsService.GetChildModelElementsFromTree(element)):
            print(f"{'-'*52} Child objects {'-'*53}\n")

            for i, child in enumerate(child_elements):
                print(f"{i}. {child.GetDisplayName():<30} Type: {child.GetElementAdapterType().GetTypeName():<20} ")

            print()

        # print the common properties
        if self.build_ele.CommonProp.value:
            common_props = element.GetCommonProperties()
            print(f"{'-'*51} Common properties {'-'*51}\n",
                  f"Pen:                         {common_props.Pen}",
                  f"Pen by layer:                {common_props.PenByLayer}",
                  f"Stroke:                      {common_props.Stroke}",
                  f"Stroke by layer:             {common_props.StrokeByLayer}",
                  f"Color:                       {common_props.Color}",
                  f"Color by layer:              {common_props.ColorByLayer}",
                  f"Help construction:           {common_props.HelpConstruction}",
                  "",
                  sep="\n"
            )

            # in case of a 3D object print data about texture
            if model_elements and isinstance((model_ele := model_elements[0]), AllplanBasisEle.ModelElement3D):
                print(f"{'-'*50} Texture definition {'-'*50}",
                      f"Surface path: {model_ele.TextureDefinition.SurfacePath}",
                      "",
                      sep="\n")

                print(model_ele.TextureMapping)
                print()

        # print the attributes
        if self.build_ele.Attributes.value and (attributes := element.GetAttributes(AllplanBaseEle.eAttibuteReadState.ReadAll)) != []:
            print(f"{'-'*54} Attributes {'-'*54}\n")

            for attribute in attributes:
                print(f"{attribute[0]:<7}\t{AllplanBaseEle.AttributeService.GetAttributeName(doc, attribute[0]):<40} = {attribute[1]:<55}")

            print()

        # print the element geometry
        if self.build_ele.ElementGeometry.value:
            print(f"{'-'*51} Element geometry {'-'*51}\n")
            print(element.GetGeometry())
            print()

        # print the model element geometry
        if self.build_ele.ModelGeometry.value:
            print(f"{'-'*48} Model element geometry {'-'*48}\n")
            print(element.GetModelGeometry())
            print()

        # print the ground view geometry (only for architecture objects)
        if self.build_ele.GroundViewGeo.value and (ground_view_geo := element.GetGroundViewArchitectureElementGeometry()) is not None:
            print(f"{'-'*39} Ground view architecture object geometry {'-'*39} \n")

            print(ground_view_geo)
            print()

        # print the pure architecture geometry (geometry without cut-outs, only for architecture objects)
        if self.build_ele.PureArchEleGeometry.value and (pure_arch_geo := element.GetPureArchitectureElementGeometry()) is not None:
            print(f"{'-'*42} Pure architecture object geometry {'-'*42}\n")
            print(pure_arch_geo)
            print()

        # print the type of the Python API object
        if self.build_ele.APIObject.value:
            print(f"{'-'*54} API object {'-'*54}\n")
            if (api_object := AllplanBaseEle.GetElement(element)):
                object_type = type(api_object)
                print(f"Object of type {object_type.__name__} from the module {object_type.__module__} was got from the element adapter")

                print(api_object)
            else:
                print("Couldn't get any API objects from the element adapter: ", element)


        print("-"*120)

        AllplanUtil.ShowMessageBox("The output is displayed in the Trace window", AllplanUtil.MB_OK)
