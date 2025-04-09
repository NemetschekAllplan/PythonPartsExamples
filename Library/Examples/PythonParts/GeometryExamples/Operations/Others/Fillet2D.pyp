<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Others\Fillet2D.py</Name>
    <Title>Fillet 2D</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>Fillet2d</Name>
    <Text>Fillet of 2D lines and arcs</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>2D lines and arcs</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>FilletPropertiesExpander</Name>
        <Text>Options of FilletCalculus2D</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>FilletRadius</Name>
            <Text>Radius</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
