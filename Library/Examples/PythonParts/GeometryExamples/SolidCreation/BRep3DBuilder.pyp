<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\SolidCreation\BRep3DBuilder.py</Name>
    <Title>BRep 3D Builder</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>BRep 3D Builder</Text>
    <Parameters>
      <Parameter>
        <Name>CylinderGeoemtryExpander</Name>
        <Text>Cylinder geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Radius</Name>
            <Text>Radius</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OverrideKnots</Name>
            <Text>Override knots vector</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>KnotsExpander</Name>
        <Text>Knots vector</Text>
        <ValueType>Expander</ValueType>
        <Visible>OverrideKnots</Visible>
        <Parameters>
          <Parameter>
            <Name>Knots</Name>
            <Text>Knots</Text>
            <Value>[0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1.0, 1.0, 1.0]</Value>
            <ValueType>Double</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
