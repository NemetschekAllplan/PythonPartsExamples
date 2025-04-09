<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\SolidCreation\PolyhedronBuilder.py</Name>
    <Title>Polyhedron Builder</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Polyhedron Builder</Text>
    <Parameters>
      <Parameter>
        <Name>VerticesExpander</Name>
        <Text>Polyhedron vertices</Text>
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
            <Name>PolyhedronVertices</Name>
            <Text>Vertices</Text>
            <Value>[Point3D(-500.0,-500.0,   0.0);
                        Point3D( 500.0,-500.0,   0.0);
                        Point3D( 500.0, 500.0,   0.0);
                        Point3D(-500.0, 500.0,   0.0);
                        Point3D(   0.0,   0.0,1000.0)]</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>False</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PolyhedronParameterExpander</Name>
        <Text>Polyhedron parameter</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PolyhedronType</Name>
            <Text>Polyhedron type</Text>
            <Value>tVolume</Value>
            <ValueList>"|".join(str(key) for key in AllplanGeo.PolyhedronType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
