<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\SolidCreation\ExtrudedPolyhedron.py</Name>
    <Title>Extruded Polyhedron</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Extruded polyhedron</Text>
    <Parameters>
      <Parameter>
        <Name>VectorsExpander</Name>
        <Text>Vectors</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CoordinatesTextRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>CoordinateXText</Name>
                <Text/>
                <Value>X</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>CoordinateYText</Name>
                <Text/>
                <Value>Y</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>CoordinateZText</Name>
                <Text/>
                <Value>Z</Value>
                <ValueType>Text</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ProfileNormalVector</Name>
            <Text>Profile's normal vector</Text>
            <Value>Vector3D(0,0,1000)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>ExtrusionDirection</Name>
            <Text>Extrusion vector</Text>
            <Value>Vector3D(0,0,1000)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PointsExpander</Name>
        <Text>Profile points</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CoordinatesTextRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>CoordinateXText</Name>
                <Text/>
                <Value>X</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>CoordinateYText</Name>
                <Text/>
                <Value>Y</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>CoordinateZText</Name>
                <Text/>
                <Value>Z</Value>
                <ValueType>Text</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ProfilePoints</Name>
            <Text>Profile points</Text>
            <Value>[Point3D(  0.0,   0.0,   0.0);
                        Point3D(500.0, 100.0,   0.0);
                        Point3D(800.0, 800.0,   0.0);
                        Point3D(500.0, 700.0,   0.0);
                        Point3D(100.0, 400.0,   0.0);
                        Point3D(  0.0, 900.0,   0.0)]</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>False</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
