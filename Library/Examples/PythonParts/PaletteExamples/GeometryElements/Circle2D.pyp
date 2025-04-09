<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Circle2D.py</Name>
    <Title>Circle2D</Title>
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
        <Name>CircleExp1</Name>
        <Text>Circle controls expanded</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Circle1</Name>
            <Text>Circle 1</Text>
            <Value>Circle2D(CenterPoint(0,0)MajorRadius(500))</Value>
            <ValueType>Circle2D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CircleExp2</Name>
        <Text>Circle controls in row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Circle2</Name>
            <Text>Circle 2</Text>
            <Value>Circle2D(CenterPoint(1000, 1000)MajorRadius(250))</Value>
            <ValueType>Circle2D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CircleListExp</Name>
        <Text>Circle list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CircleCount</Name>
            <Text>Circle count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>CircleList</Name>
            <Text>Circle</Text>
            <Value>[Circle2D(CenterPoint(0,2000)MajorRadius(100));Circle2D(CenterPoint(1000,2000)MajorRadius(200));Circle2D(CenterPoint(2000,2000)MajorRadius(300))]</Value>
            <ValueType>Circle2D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>CircleCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CircleTextExp</Name>
        <Text>Controls with special text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Circle3</Name>
            <Text>Center,Radius</Text>
            <Value>Circle2D(CenterPoint(1000,0)MajorRadius(200))</Value>
            <ValueType>Circle2D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CircleConditionExp</Name>
        <Text>Circle controls with condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Circle4</Name>
            <Text>Circle 4</Text>
            <Value>Circle2D(CenterPoint(2000,0)MajorRadius(300))</Value>
            <ValueType>Circle2D</ValueType>
            <Visible>|Circle4.MajorRadius:False</Visible>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
