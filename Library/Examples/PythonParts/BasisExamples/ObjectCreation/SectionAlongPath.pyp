<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\ObjectCreation\SectionAlongPath.py</Name>
    <Title>SectionAlongPath</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters>
      <Parameter>
        <Name>SectionPathInput</Name>
        <Text>Section path</Text>
        <Value>1</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>SectionPartByPolyline</Name>
            <Text>Polyline input</Text>
            <Value>1</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>SectionPathSelect</Name>
            <Text>Select</Text>
            <Value>2</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
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
            <Visible>SectionPathInput == 1</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Labeling</Name>
        <Text>Labeling</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Header</Name>
            <Text>Header</Text>
            <Value>Section</Value>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>SectionIdentifier</Name>
            <Text>Section identifier</Text>
            <Value>A</Value>
            <ValueType>String</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
