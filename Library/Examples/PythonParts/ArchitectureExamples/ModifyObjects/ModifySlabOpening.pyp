<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ArchitectureExamples\ModifyObjects\ModifySlabOpening.py</Name>
    <Title>Slab opening</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>ELEMENT_SELECT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>OPENING_PLACEMENT</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>OPENING_INPUT</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Visible>InputMode == OPENING_INPUT</Visible>
    <Parameters>
      <Parameter>
        <Name/>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\ShapeGeometryProperties.incl</Value>
        <ValueType>Include</ValueType>
      </Parameter>
      <Parameter>
        <Name/>
        <ValueType>ConditionGroup</ValueType>
        <Enable>OpeningType != "Opening"</Enable>
        <Parameters>
          <Parameter>
            <Name>HeightSettings</Name>
            <Text>Opening height</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>UseTopLevelOfSlab</Name>
            <Text>Top level = TL slab</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>UseBottomLevelOfSlab</Name>
            <Text>Bottom level = BL slab</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name/>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSymbolsProperties.incl</Value>
        <Visible>OpeningSymbolTierIndex:False</Visible>
        <ValueType>Include</ValueType>
      </Parameter>
      <Parameter>
        <Name>AttributesExp</Name>
        <Text>Attributes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>OpeningType</Name>
            <Text>Type</Text>
            <Value>Opening</Value>
            <ValueList>Opening|Recess</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>HasIndependent2DInteraction</Name>
            <Text>Above/below section plane</Text>
            <Value/>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value/>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>ElementTierCount</Name>
        <Text>Element tier count</Text>
        <Value>1</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
