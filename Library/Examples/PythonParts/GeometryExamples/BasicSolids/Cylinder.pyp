<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\BasicSolids\Cylinder.py</Name>
    <Title>Cylinder</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Cylinder</Text>
    <Parameters>
      <Parameter>
        <Name>PlacementParameterExpander</Name>
        <Text>Placement</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>LocalXVector</Name>
            <Text>Local X axis</Text>
            <Value>Vector3D(1000,0,0)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>LocalZVector</Name>
            <Text>Local Z axis</Text>
            <Value>Vector3D(0,0,1000)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DimensionsParameterExpander</Name>
        <Text>Dimensions</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MajorRadius</Name>
            <Text>Major radius</Text>
            <Value>500</Value>
            <MinValue>1</MinValue>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MinorRadius</Name>
            <Text>Minor radius</Text>
            <Value>500</Value>
            <MinValue>1</MinValue>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Apex</Name>
            <Text>Apex</Text>
            <Value>Point3D(0,0,1000)</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <Text/>
            <Value/>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateAs</Name>
            <Text>Create as</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>CreateAsBRep</Name>
                <Text>BRep</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
                <Enable>MinorRadius == MajorRadius and Apex.X == 0 and Apex.Y == 0</Enable>
              </Parameter>
              <Parameter>
                <Name>CreateAsPolyhedron</Name>
                <Text>Polyhedron</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TesselationParameterExpander</Name>
        <Text>Tesselation</Text>
        <ValueType>Expander</ValueType>
        <Visible>CreateAs == 1</Visible>
        <Parameters>
          <Parameter>
            <Name>CountOfSegments</Name>
            <Text>Number of segments</Text>
            <Value>36</Value>
            <ValueType>Integer</ValueType>
            <MinValue>3</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
