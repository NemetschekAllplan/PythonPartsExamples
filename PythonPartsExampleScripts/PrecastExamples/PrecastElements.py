"""
Example Script for PrecastElements
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Precast as AllplanPrecast

from BuildingElement import BuildingElement
from HandleProperties import HandleProperties
from PythonPartUtil import PythonPartUtil
from DocumentManager import DocumentManager

# Print some information
print('Load PrecastElements.py')

# Method for checking the supported versions
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

def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = PrecastElementsExample(doc)
    if not DocumentManager.get_instance().pythonpart_element.IsNull():
        element.is_modification_mode = True

    model_ele_list, handle_list = element.create(build_ele)
    element.create_precast_element(build_ele)
    model_ele_list.append(element.PrecastElement)

    return (model_ele_list, handle_list)

def move_handle(build_ele: BuildingElement,
                handle_prop: HandleProperties,
                input_pnt: AllplanGeo.Point3D,
                doc: AllplanElementAdapter.DocumentAdapter):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    element = PrecastElementsExample(doc)

    model_ele_list, handle_list = element.create(build_ele)
    element.create_precast_element(build_ele)
    model_ele_list.append(element.PrecastElement)

    return (model_ele_list, handle_list)


def modify_element_properties(build_ele, con_props, name, value, doc):
    """
    Modify property of element

    Args:
        build_ele:  the building element.

    Returns:
        True/False if palette refresh is necessary
    """

    del con_props
    del value
    del doc

    return False

def modify_control_properties(build_ele, con_props, name, value, doc):
    """
    Modify property of element

    Args:
        build_ele:  the building element.
        name:       the name of the property.
        value:      new value for property.

    Returns:
        True/False if palette refresh is necessary
    """

    del con_props
    del value
    del doc

    return True

class PrecastElementsExample():
    """
    Definition of class PrecastElementsExample
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class PrecastElementsExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = None
        self.document       = doc
        self.is_modification_mode = False

        self.PrecastElementProperties = AllplanPrecast.PrecastElementProperties()
        self.PrecastElement = AllplanPrecast.PrecastElement(self.PrecastElementProperties)

    def create(self,
               build_ele: BuildingElement):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        self.create_geometry(build_ele)

        return (self.model_ele_list, self.handle_list)

    def create_geometry(self,
                        build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #------------------ Define the cube polyhedron

        polyhed1 = AllplanGeo.Polyhedron3D.CreateCuboid(1000, 1000, 1000)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        #------------------ Append cubes as new Allplan elements

        elements = []

        elements.append(AllplanBasisElements.ModelElement3D(com_prop, polyhed1))

        pyp_util = PythonPartUtil()

        pyp_util.add_pythonpart_view_2d3d(elements)

        if self.is_modification_mode or build_ele.CreatePEWithPythonPart.value == 1:
            self.model_ele_list = pyp_util.create_pythonpart(build_ele)
        else:
            self.model_ele_list = elements

        #------------------ No handles

        self.handle_list = []

        return (self.model_ele_list, self.handle_list)

    def create_precast_element(self,
                               build_ele : BuildingElement):
        """
        Create PrecastElement

        Args:
            build_ele:  the building element.

        Returns:
            True if creation was successfull
        """

        if build_ele.Element.selected_value == '' and build_ele.Element.value == "":
            return False

        self.insert_matrix = build_ele.get_insert_matrix()
        mat3D = AllplanGeo.Matrix3D(self.insert_matrix)
        mat3D.SetTranslation(AllplanGeo.Vector3D())
        # spannvektor:X,Y,Z
        self.SpanVector = AllplanGeo.Point3D(0, 0, 1)
        # viewvektor:X,Y,Z
        self.ViewVector = AllplanGeo.Point3D(1, 0, 0)

        vec = self.insert_matrix.GetTranslationVector()

        self.PrecastElementProperties.SpanDirection = AllplanGeo.Transform(self.SpanVector, mat3D)
        self.PrecastElementProperties.ViewDirection = AllplanGeo.Transform(self.ViewVector, mat3D)
        self.PrecastElementProperties.ReferencePoint = AllplanGeo.Point3D(0,0,0)
        self.PrecastElementProperties.Factory = build_ele.Factory.value
        self.PrecastElementProperties.FactoryCatAddressOffset = self.PrecastElementProperties.SetFactoryCatalogAddressOffset(self.PrecastElementProperties.Factory)
        self.PrecastElementProperties.Norm = build_ele.Norm.value
        self.PrecastElementProperties.NormCatAddressOffset = self.PrecastElementProperties.SetNormCatalogAddressOffset(self.PrecastElementProperties.Norm)
        self.PrecastElementProperties.Layers = self.create_precast_element_layer(build_ele)
        self.PrecastElementProperties.ElementTypeCatGUID = self.PrecastElementProperties.SetElementTypeCatalogGUID_from_Name(build_ele.Element.value)

        # fill with correct values
        self.PrecastElementProperties.ElementType = 3000    # preparation for upcoming element types
        self.PrecastElementProperties.PieceFactor = build_ele.Stueckzahl.value
        self.PrecastElementProperties.PosNr = build_ele.PosNr.value
        self.PrecastElementProperties.PosNrText = build_ele.ZusTextPosNr.value

        self.PrecastElementProperties.CreateLabeling = build_ele.CreateLabellingValue.value
        self.PrecastElementProperties.LabelingTextRefPoint = build_ele.LabelingTextRefPointValue.value
        self.PrecastElementProperties.ElemTypeAttribut = build_ele.TypenKennValue.value
        self.PrecastElementProperties.ManualDimensions = build_ele.ManualDimensionsValue.value
        self.PrecastElementProperties.DimensionViewing = build_ele.DimensionViewingValue.value
        self.PrecastElementProperties.DimensionSpan = build_ele.DimensionSpanValue.value
        self.PrecastElementProperties.DimensionCross = build_ele.DimensionCrossValue.value

        self.PrecastElement = AllplanPrecast.PrecastElement(self.PrecastElementProperties)
        self.PrecastElement.deletePython = build_ele.CreatePEWithPythonPart.value == False

        # Debug
        print(self.PrecastElement)

        return True

    def create_precast_element_layer(self,
                                     build_ele : BuildingElement):
        """
        Create PrecastElementLayer

        Args:
            build_ele:  the building element.

        Returns:
            Layer(s)
        """

        precast_layers = []
        layers = build_ele.Layer.value

        if isinstance(layers, list):
            for idx, layer in enumerate(layers):
                layer_prop = AllplanPrecast.PrecastLayerProperties()
                layer_prop.LayerName = layer.LayerName
                layer_prop.CalculateLayerThickness = layer.CalculateLayerThickness
                layer_prop.LayerThickness = layer.LayerThickness
                layer_prop.MaterialType = layer.MaterialType
                layer_prop.Material = layer.Material
                layer_prop.MaterialCatAddressOffset = layer_prop.SetMaterialCatalogAddressOffset(layer_prop.MaterialType, layer_prop.Material)
                layer_prop.LayerNumber = layer.LayerNumber
                precast_layer = AllplanPrecast.PrecastLayer(layer_prop)
                precast_layers.append(precast_layer)
        else:
            layer_prop = AllplanPrecast.PrecastLayerProperties()
            layer_prop.LayerName = layers.LayerName
            layer_prop.CalculateLayerThickness = layers.CalculateLayerThickness
            layer_prop.LayerThickness = layers.LayerThickness
            layer_prop.MaterialType = layers.MaterialType
            layer_prop.Material = layers.Material
            layer_prop.MaterialCatAddressOffset = layer_prop.SetMaterialCatalogAddressOffset(get_material_type_str(layers.MaterialType), layer_prop.Material)
            layer_prop.LayerNumber = layers.LayerNumber
            precast_layer = AllplanPrecast.PrecastLayer(layer_prop)
            precast_layers.append(precast_layer)

        return precast_layers

def get_material_type_str(materialtype : int):
    """
    Get materialTypeEnum
    Args:
        material:  materialType string
    Returns:
        MaterialTypeEnum
    """
    if materialtype == 0:
        return "Concrete"
    if materialtype == 1:
        return "Insulation"
    if materialtype == 2:
        return "In-situ Concrete"
    if materialtype == 3:
        return "Brick/Tile"
    return ""

