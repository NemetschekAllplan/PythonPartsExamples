<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Others\Tessellation.py</Name>
    <Title>Quantity take-off</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>SelectGeometry</Name>
    <Text>Tessellation</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>General 3D objects</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>TessellationOptionsExapander</Name>
        <Text>Tessellation options</Text>
        <ValueType>Expander</ValueType>
        <Visible>True</Visible>
        <Parameters>
          <Parameter>
            <Name>Density</Name>
            <Text>Density</Text>
            <Value>0.2</Value>
            <ValueType>Double</ValueType>
            <MinValue>0.0</MinValue>
            <MaxValue>1.0</MaxValue>
          </Parameter>
          <Parameter>
            <Name>MinLength</Name>
            <Text>Minimum edge length</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0.0</MinValue>
          </Parameter>
          <Parameter>
            <Name>MaxLength</Name>
            <Text>Maximum edge length</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0.0</MinValue>
          </Parameter>
          <Parameter>
            <Name>MaxAngle</Name>
            <Text>Maximum angle</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>90</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
