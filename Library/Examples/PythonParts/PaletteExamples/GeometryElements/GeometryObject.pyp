<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\GeometryObject.py</Name>
    <Title>GeometryObject</Title>
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
        <Name>GeometryObjectExp</Name>
        <Text>Geometry object</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>GeometryObject</Name>
            <Text>Geometry object</Text>
            <Value>Arc3D(CenterPoint(0,0,0)MinorRadius(1000)MajorRadius(1000)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1))</Value>
            <ValueType>GeometryObject</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeometryObjectListExp</Name>
        <Text>Geometry objects</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>GeometryObjectList</Name>
            <Text/>
            <Value>[Arc3D(CenterPoint(0,5000,0)MinorRadius(1000)MajorRadius(1500)StartAngle(pi / 4 )EndAngle(pi * 3 / 2)XDirection(1,0,0)ZAxis(0,0,1)IsCounterClockwise(1));Line2D(5000,0,7000,-2000);Polygon3D(Points((5000,7000,0)(8000,8000,0)(8000,5000,0)(5000,5000,0)(5000,7000,0)))]</Value>
            <ValueType>GeometryObject</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
