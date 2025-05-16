<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Point2D.py</Name>
    <Title>Point2D</Title>
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
            <Value>Point2D(0,0)</Value>
            <ValueType>Point2D</ValueType>
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
            <Value>Point2D(1000, 1000)</Value>
            <ValueType>Point2D</ValueType>
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
            <Value>[Point2D(0,-1000);Point2D(2000,1000);Point2D(3000,-2000)]</Value>
            <ValueType>Point2D</ValueType>
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
            <Text>From left,From front</Text>
            <Value>Point2D(1000,2000)</Value>
            <ValueType>Point2D</ValueType>
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
            <Text>X coordinate start</Text>
            <Value>Point2D(5000,1000)</Value>
            <ValueType>Point2D</ValueType>
            <Visible>|Y:False</Visible>
          </Parameter>
          <Parameter>
            <Name>EndPoint</Name>
            <Text>Y coordinate end</Text>
            <Value>Point2D(10000,3000)</Value>
            <ValueType>Point2D</ValueType>
            <Visible>|X:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
