<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Vector2D.py</Name>
    <Title>Vector2D</Title>
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
        <Name>VectorExp1</Name>
        <Text>Vector controls expanded</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Vector1</Name>
            <Text>Vector 1</Text>
            <Value>Vector2D(0,0)</Value>
            <ValueType>Vector2D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>VectorExp2</Name>
        <Text>Vector controls in row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Vector2</Name>
            <Text>Vector 2</Text>
            <Value>Vector2D(1000, 1000)</Value>
            <ValueType>Vector2D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>VectorListExp</Name>
        <Text>Vector list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>VectorCount</Name>
            <Text>Vector count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>VectorList</Name>
            <Text>Vectors</Text>
            <Value>[Vector2D(0,-1000);Vector2D(2000,1000);Vector2D(3000,-2000)]</Value>
            <ValueType>Vector2D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>VectorCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CoordinateTextExp</Name>
        <Text>Vector values with special text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Sizes</Name>
            <Text>Length,Width</Text>
            <Value>Vector2D(1000,2000)</Value>
            <ValueType>Vector2D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CoordConditionExp</Name>
        <Text>Vector values with visible condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>StartVector</Name>
            <Text>X distance start</Text>
            <Value>Vector2D(5000,1000)</Value>
            <ValueType>Vector2D</ValueType>
            <Visible>|Y:False</Visible>
          </Parameter>
          <Parameter>
            <Name>EndVector</Name>
            <Text>Y distance end</Text>
            <Value>Vector2D(10000,3000)</Value>
            <ValueType>Vector2D</ValueType>
            <Visible>|X:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
