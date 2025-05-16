<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\AxisPlacement3D.py</Name>
    <Title>AxisPlacement3D</Title>
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
        <Name>CircleRadius</Name>
        <Text>Circle radius</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>AxisPlacementExp1</Name>
        <Text>Axis placement controls expanded</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AxisPlacement1</Name>
            <Text>AxisPlacement 1</Text>
            <Value>AxisPlacement3D(Origin(0,0,0)XDirection(1,0,0)ZDirection(0,1,1))</Value>
            <ValueType>AxisPlacement3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AxisPlacementExp2</Name>
        <Text>AxisPlacement controls in row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AxisPlacement2</Name>
            <Text>AxisPlacement 2</Text>
            <Value>AxisPlacement3D(Origin(5000,0,0)XDirection(0,1,0)ZDirection(1,0,1))</Value>
            <ValueType>AxisPlacement3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AxisPlacementListExp</Name>
        <Text>AxisPlacement list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AxisPlacementCount</Name>
            <Text>AxisPlacement count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>AxisPlacementList</Name>
            <Text>AxisPlacement</Text>
            <Value>[AxisPlacement3D(Origin(0,5000,0)XDirection(1,0,0)ZDirection(0,0,1));AxisPlacement3D(Origin(5000,5000,0)XDirection(1,0,0)ZDirection(0,0,1));AxisPlacement3D(Origin(10000,5000,0)XDirection(1,0,0)ZDirection(0,0,1))]</Value>
            <ValueType>AxisPlacement3D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>AxisPlacementCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AxisPlacementTextExp</Name>
        <Text>Controls with special text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AxisPlacement3</Name>
            <Text>Origin,X direction,Z direction</Text>
            <Value>AxisPlacement3D(Origin(10000,0,0)XDirection(0,1,0)ZDirection(0,0,1))</Value>
            <ValueType>AxisPlacement3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AxisPlacementConditionExp</Name>
        <Text>AxisPlacement controls with condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AxisPlacement4</Name>
            <Text>AxisPlacement 4</Text>
            <Value>AxisPlacement3D(Origin(15000,0,0)XDirection(0,1,0)ZDirection(0,0,1))</Value>
            <ValueType>AxisPlacement3D</ValueType>
            <Visible>|XDirection:False</Visible>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
