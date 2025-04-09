<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\BooleanOperations\IntersectRayBRep.py</Name>
    <Title>IntersectRayBRep</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters>
      <Parameter>
        <Name>FormatExp</Name>
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
        <Name>BRepExp</Name>
        <Text>BRep</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CylinderSizes</Name>
            <Text>Radius,Height</Text>
            <Value>Vector2D(1000,3000)</Value>
            <ValueType>Vector2D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RayExp1</Name>
        <Text>Ray</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RayLine1</Name>
            <Text>Ray start point,Ray end point</Text>
            <Value>Line3D(0, 0, 1000, 5000, 1500, 1500)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>NegativePreferred</Name>
            <Text>Negative preferred</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>RayLine1Color</Name>
            <Text>Color</Text>
            <Value>4</Value>
            <ValueType>Color</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
