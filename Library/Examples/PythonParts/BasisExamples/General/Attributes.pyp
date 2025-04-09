<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\General\Attributes.py</Name>
    <Title>Attributes example</Title>
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
            <AttributeId>206</AttributeId>
          </Parameter>
          <Parameter>
            <Name>LayerThickness</Name>
            <Text>Layer thickness</Text>
            <Value>30</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>211</AttributeId>
          </Parameter>
          <Parameter>
            <Name>Material</Name>
            <Text>Material</Text>
            <Value>Concrete</Value>
            <ValueList>Concrete|Steel|Wooden</ValueList>
            <ValueType>Attribute</ValueType>
            <AttributeId>508</AttributeId>
          </Parameter>
          <Parameter>
            <Name>FactorHeatRequirement</Name>
            <Text>Factor heat requirement</Text>
            <Value>1.5</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>987</AttributeId>
          </Parameter>
          <Parameter>
            <Name>FireRiskFactor</Name>
            <Text>Fire risk factor</Text>
            <Value>A1</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>1398</AttributeId>
          </Parameter>
          <Parameter>
            <Name>CalculationMode</Name>
            <Text>Calculation mode</Text>
            <Value>2</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>120</AttributeId>
          </Parameter>
          <Parameter>
            <Name>ApprovalDate</Name>
            <Text>Approval date</Text>
            <Value>date(2022,4,27)</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>386</AttributeId>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
