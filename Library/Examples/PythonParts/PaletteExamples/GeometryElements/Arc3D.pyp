<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Arc3D.py</Name>
    <Title>Arc3D</Title>
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
        <Name>ArcExp1</Name>
        <Text>Arc controls expanded</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Arc1</Name>
            <Text>Arc 1</Text>
            <Value>Arc3D(CenterPoint(0,0,0)MinorRadius(1000)MajorRadius(2000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1))</Value>
            <ValueType>Arc3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ArcExp2</Name>
        <Text>Arc controls in row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Arc2</Name>
            <Text>Arc 2</Text>
            <Value>Arc3D(CenterPoint(5000,0,0)MinorRadius(1000)MajorRadius(1000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1))</Value>
            <ValueType>Arc3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ArcListExp</Name>
        <Text>Arc list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ArcCount</Name>
            <Text>Arc count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>ArcList</Name>
            <Text>Arc</Text>
            <Value>[Arc3D(CenterPoint(0,5000,0)MinorRadius(1000)MajorRadius(1000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1));Arc3D(CenterPoint(5000,5000,0)MinorRadius(1000)MajorRadius(1000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1));Arc3D(CenterPoint(10000,5000,0)MinorRadius(1000)MajorRadius(1000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1))]</Value>
            <ValueType>Arc3D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>ArcCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ArcTextExp</Name>
        <Text>Controls with special text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Arc3</Name>
            <Text>Center,Minor,Major,Start angle,End angle,X axis,Y axis</Text>
            <Value>Arc3D(CenterPoint(10000,0,0)MinorRadius(1000)MajorRadius(2000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(0,1,0)ZAxis(0,0,1)IsCounterClockwise(1))</Value>
            <ValueType>Arc3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ArcConditionExp</Name>
        <Text>Arc controls with condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Arc4</Name>
            <Text>Arc 4</Text>
            <Value>Arc3D(CenterPoint(15000,0,0)MinorRadius(1000)MajorRadius(2000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(0,1,0)ZAxis(0,0,1)IsCounterClockwise(1))</Value>
            <ValueType>Arc3D</ValueType>
            <Visible>|MajorRadius:False</Visible>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
