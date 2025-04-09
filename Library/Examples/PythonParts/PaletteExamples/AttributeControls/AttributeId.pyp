<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\AttributeControls\AttributeId.py</Name>
    <Title>AttributeId</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters>
      <Parameter>
        <Name>SingleIdExp</Name>
        <Text>Attribute ID</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AttributeID</Name>
            <Text/>
            <Value/>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>AttributeInfo</Name>
            <Text>Attribute ID</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ListIdExp</Name>
        <Text>Attribute ID list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AttributeIDList</Name>
            <Text/>
            <Value>[0]</Value>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
            <ValueListStartRow>1</ValueListStartRow>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>AttributeInfoList</Name>
            <Text>Attribute IDs</Text>
            <Value>[]</Value>
            <ValueType>Integer</ValueType>
            <Enable>False</Enable>
            <ValueListStartRow>1</ValueListStartRow>
            <Visible>len(AttributeIDList) &gt; 1</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
