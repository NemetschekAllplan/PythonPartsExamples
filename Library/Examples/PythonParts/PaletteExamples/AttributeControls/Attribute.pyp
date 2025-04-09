<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\AttributeControls\Attribute.py</Name>
    <Title>Attribute example</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Attributes</Text>
    <Parameters>
      <Parameter>
        <Name>Format</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeometryExp</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Sizes</Name>
            <Text>Length,Width,Height</Text>
            <Value>Vector3D(5000,500,1000)</Value>
            <ValueType>Vector3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AttributeExp</Name>
        <Text>Attributes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SequenceNumber</Name>
            <Text>Sequence number</Text>
            <Value>1111</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.SEQUENCE_NUMBER</AttributeId>
          </Parameter>
          <Parameter>
            <Name>LayerThickness</Name>
            <Text>Layer thickness</Text>
            <Value>30</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.LAYER_THICKNESS</AttributeId>
          </Parameter>
          <Parameter>
            <Name>Material</Name>
            <Text>Material</Text>
            <Value>Concrete</Value>
            <ValueList>Concrete|Steel|Wooden</ValueList>
            <ValueType>StringComboBox</ValueType>
            <ValueListFile>usr\tmp\PypComboSettings\Material.val</ValueListFile>
            <AttributeId>AttributeIdEnums.MATERIAL</AttributeId>
          </Parameter>
          <Parameter>
            <Name>ApprovalDate</Name>
            <Text>Approval date</Text>
            <Value>date(2022,4,27)</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.APPROVAL_DATE</AttributeId>
          </Parameter>
          <Parameter>
            <Name>LoadBearing</Name>
            <Text>Load bearing</Text>
            <Value>1</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.LOAD_BEARING</AttributeId>
          </Parameter>
          <Parameter>
            <Name>CalculationMode</Name>
            <Text>Calculation mode</Text>
            <Value>2</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.CALCULATION_MODE</AttributeId>
          </Parameter>
          <Parameter>
            <Name>Unit</Name>
            <Text>Unit</Text>
            <Value>m</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.UNIT</AttributeId>
          </Parameter>
          <Parameter>
            <Name>LayoutFormat</Name>
            <Text>Layout format</Text>
            <Value>DIN A0</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.LAYOUT_FORMAT</AttributeId>
          </Parameter>
          <Parameter>
            <Name>IfCObjectType</Name>
            <Text>IFC object type</Text>
            <Value>IfcBeam</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.IFC_ENTITY</AttributeId>
          </Parameter>
          <Parameter>
            <Name>AreaTypeFloorSpace</Name>
            <Text>Area type floor space</Text>
            <Value>WO</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>AttributeIdEnums.AREA_TYPE_FLOOR_SPACE</AttributeId>
          </Parameter>
          <Parameter>
            <Name>Hatching</Name>
            <Text>Hatching</Text>
            <Value>301</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>5001</AttributeId>
          </Parameter>
          <Parameter>
            <Name>Filling</Name>
            <Text>Filling</Text>
            <Value>4</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>5002</AttributeId>
          </Parameter>
          <Parameter>
            <Name>Pattern</Name>
            <Text>Pattern</Text>
            <Value>301</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>5003</AttributeId>
          </Parameter>
          <Parameter>
            <Name>IntegerCombo</Name>
            <Text>Integer value</Text>
            <Value>22</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>5004</AttributeId>
          </Parameter>
          <Parameter>
            <Name>DoubleCombo</Name>
            <Text>Double values</Text>
            <Value>33.3</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>5005</AttributeId>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>List</Name>
    <Text>Attribute list</Text>
    <Parameters>
      <Parameter>
        <Name>AttributeList</Name>
        <Text/>
        <TextDyn>"$Attribute_Name"</TextDyn>
        <Value>["A1","F30",2]</Value>
        <ValueType>Attribute</ValueType>
        <AttributeId>[AttributeIdEnums.FIRE_RISK_FACTOR, AttributeIdEnums.FIRE_RATING, AttributeIdEnums.TRADE]</AttributeId>
      </Parameter>
    </Parameters>
  </Page>
</Element>
