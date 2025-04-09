<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\AttributeValueControlByRuntime.py</Name>
    <Title>Change and modify controls during the runtime</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>AttributeInput</Name>
    <Text>Attribute input</Text>
    <Parameters>
      <Parameter>
        <Name>AttributeExpander</Name>
        <Text>Attribute value</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row</Name>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>AttributeID</Name>
                <Text>Attribute ID</Text>
                <Value>508</Value>
                <ValueDialog>AttributeSelection</ValueDialog>
                <ValueType>Integer</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>AttributeValue</Name>
            <Text>Attribute value</Text>
            <Value/>
            <ValueType>Attribute</ValueType>
            <AttributeId>508</AttributeId>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
