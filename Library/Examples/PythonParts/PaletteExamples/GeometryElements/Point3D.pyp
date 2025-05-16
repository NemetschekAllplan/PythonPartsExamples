<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Point3D.py</Name>
    <Title>Point3D</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
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
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PointExp1</Name>
        <Text>Point controls expanded</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Point1</Name>
            <Text>Point 1</Text>
            <Value>Point3D(0,0,0)</Value>
            <ValueType>Point3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PointExp2</Name>
        <Text>Point controls in row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Point2</Name>
            <Text>Point 2</Text>
            <Value>Point3D(1000,1000,0)</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PointListExp</Name>
        <Text>Point list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PointCount</Name>
            <Text>Point count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>PointList</Name>
            <Text>Points</Text>
            <Value>[Point3D(0,-1000,0);Point3D(2000,1000,0);Point3D(3000,-2000,0)]</Value>
            <ValueType>Point3D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>PointCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CoordinateTextExp</Name>
        <Text>Coordinates with special text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RefPoint</Name>
            <Text>From left,From front,From bottom</Text>
            <Value>Point3D(1000,2000,3000)</Value>
            <ValueType>Point3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CoordConditionExp</Name>
        <Text>Coordinates with visible condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>StartPoint</Name>
            <Text>Start point</Text>
            <Value>Point3D(5000,1000,0)</Value>
            <ValueType>Point3D</ValueType>
            <Visible>|Y:False</Visible>
          </Parameter>
          <Parameter>
            <Name>EndPoint</Name>
            <Text>End point</Text>
            <Value>Point3D(10000,3000,0)</Value>
            <ValueType>Point3D</ValueType>
            <Visible>|X:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
