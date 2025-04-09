<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\Objects\Text.py</Name>
    <Title>Text</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
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
            <Visible>|CommonProp.Stroke:False|CommonProp.StrokeByLayer:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TextExp</Name>
        <Text>Text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Text</Name>
            <Text>Text</Text>
            <Value>This is the first text line
and this is the second one</Value>
            <ValueType>String</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name/>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\TextProperties.incl</Value>
        <ValueType>Include</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
