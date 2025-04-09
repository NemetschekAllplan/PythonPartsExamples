<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\BooleanOperations\IntersectRayPolyhedron.py</Name>
    <Title>IntersectRayPolyhedron</Title>
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
        <Name>PolyhedExp</Name>
        <Text>Polyhedron</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PolyhedSizes</Name>
            <Text>Length,Width,Height</Text>
            <Value>Vector3D(3000,4000,5000)</Value>
            <ValueType>Vector3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RayExp1</Name>
        <Text>Ray 1</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RayLine1</Name>
            <Text>Ray start point,Ray end point</Text>
            <Value>Line3D(1000, 1500, 3000, 5000, 1500, 1500)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>IntersectFlag1</Name>
            <Text>Intersection flag</Text>
            <Value>eNegativePreferred</Value>
            <ValueList>"|".join(str(key) for key in AllplanGeo.IntersectRayPolyhedronFlag.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>RayLine1Color</Name>
            <Text>Color</Text>
            <Value>4</Value>
            <ValueType>Color</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RayExp2</Name>
        <Text>Ray 2</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RayLine2</Name>
            <Text>Ray start point,Ray end point</Text>
            <Value>Line3D(1000, -1000, 500, 1000, 5000, 2000)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>RayLine2Color</Name>
            <Text>Color</Text>
            <Value>3</Value>
            <ValueType>Color</ValueType>
          </Parameter>
          <Parameter>
            <Name>FaceIndex</Name>
            <Text>Intersection face</Text>
            <Value>5</Value>
            <ValueList>0|1|2|3|4|5</ValueList>
            <ValueType>IntegerComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
