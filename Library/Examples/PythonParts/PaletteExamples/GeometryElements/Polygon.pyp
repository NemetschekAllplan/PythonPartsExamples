<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Polygon.py</Name>
    <Title>Polygon</Title>
    <Version>1.0</Version>
    <ReadLastInput>False</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>2D polygon</Text>
    <Parameters>
      <Parameter>
        <Name>Format2D</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp2D</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Polygon2DSingleRowExp</Name>
        <Text>Polygon - Single row for x/y</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Polygon1</Name>
            <Text>Point</Text>
            <Value>Polygon2D(Points((0,2000)(1000,3100)(0,3500)))</Value>
            <ValueType>Polygon2D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Polygon2DOneRowExp</Name>
        <Text>Polygon - One row for x/y</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Polygon2</Name>
            <Text>Point</Text>
            <Value>Polygon2D(Points((5000,2000)(8000,2000)(8000,0)(5000,0)))</Value>
            <ValueType>Polygon2D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Polygon2DOneRowExp</Name>
        <Text>List of Polygon2D</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PolygonCount</Name>
            <Text>Polygon count</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>PolygonList</Name>
            <Text>Point</Text>
            <Value>[Polygon2D(Points((12000,2000)(14000,3100)(12000,3500)));Polygon2D(Points((15000,2000)(18000,3000)(18000,0)(15000,0)))]</Value>
            <ValueType>Polygon2D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>PolygonCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Page2</Name>
    <Text>3D polygon</Text>
    <Parameters>
      <Parameter>
        <Name>Format3D</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp3D</Name>
            <Text/>
            <Value>CommonProperties(Color(5))</Value>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Polygon3DSingleRowExp</Name>
        <Text>Polygon - Single row for x/y/z</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Polygon6</Name>
            <Text>Point</Text>
            <Value>Polygon3D(Points((0,7000,0)(1000,8100,1000)(0,8500,3000)))</Value>
            <ValueType>Polygon3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Polygon3DOneRowExp</Name>
        <Text>Polygon - One row for x/y/z</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Polygon7</Name>
            <Text>Point</Text>
            <Value>Polygon3D(Points((5000,7000,0)(8000,8000,0)(8000,5000,0)(5000,5000,0)))</Value>
            <ValueType>Polygon3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Polygon3DOneRowExp</Name>
        <Text>Hidden y</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Polygon8</Name>
            <Text>Point</Text>
            <Value>Polygon3D(Points((10000,7000,0)(14000,8000,0)(18000,5000,0)(10000,5000,0)))</Value>
            <ValueType>Polygon3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <Visible>|Y:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
