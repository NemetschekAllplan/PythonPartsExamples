<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Spline.py</Name>
    <Title>Spline</Title>
    <Version>1.0</Version>
    <ReadLastInput>False</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>2D spline</Text>
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
        <Name>Spline2DSingleRowExp</Name>
        <Text>Spline - Single row for x/y</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Spline1</Name>
            <Text>Point</Text>
            <Value>Spline2D(StartVector(1, 1)EndVector(1, 1)Points((0,2000)(1000,3100)(2000,3500)(4000,0)))</Value>
            <ValueType>Spline2D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Spline2DOneRowExp</Name>
        <Text>Spline - One row for x/y</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Spline2</Name>
            <Text>Point</Text>
            <Value>Spline2D(StartVector(1, 1)EndVector(1, 1)Points((5000,2000)(6000,3100)(7000,3500)(10000,0)))</Value>
            <ValueType>Spline2D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Spline2DOneRowExp</Name>
        <Text>List of Spline2D</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SplineCount</Name>
            <Text>Spline count</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>SplineList</Name>
            <Text>Point</Text>
            <Value>[Spline2D(StartVector(1, 1)EndVector(1, 1)Points((11000,2000)(13000,3100)(14000,3500)(15000,0)));Spline2D(StartVector(1, 1)EndVector(1, 1)Points((15000,2000)(16000,3100)(17000,3500)(20000,0)))]</Value>
            <ValueType>Spline2D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>SplineCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Page2</Name>
    <Text>3D spline</Text>
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
        <Name>Spline3DSingleRowExp</Name>
        <Text>Spline - Single row for x/y/z</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Spline6</Name>
            <Text>Point</Text>
            <Value>Spline3D(StartVector(1, 1, 1)EndVector(1, 1, 1)Points((0,7000,0)(2000,8100,1000)(4000,8500,3000)))</Value>
            <ValueType>Spline3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Spline3DOneRowExp</Name>
        <Text>Spline - One row for x/y/z</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Spline7</Name>
            <Text>Point</Text>
            <Value>Spline3D(StartVector(1, 1, 1)EndVector(1, 1, 1)Points((5000,7000,0)(7000,9100,1000)(10000,8500,3000)))</Value>
            <ValueType>Spline3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Spline3DOneRowExp</Name>
        <Text>Hidden y</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Spline8</Name>
            <Text>Point</Text>
            <Value>Spline3D(StartVector(1, 1, 1)EndVector(1, 1, 1)Points((11000,7000,0)(13000,8100,1000)(16000,6500,3000)))</Value>
            <ValueType>Spline3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <Visible>|Y:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
