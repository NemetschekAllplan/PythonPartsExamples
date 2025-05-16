<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\GeometryElements\Line3D.py</Name>
    <Title>Line3D</Title>
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
        <Name>LineControlExp</Name>
        <Text>Line controls expanded</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Line1</Name>
            <Text>Line 1</Text>
            <Value>Line3D(0,0,0,2000,1000,1000)</Value>
            <ValueType>Line3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>LineRowExp</Name>
        <Text>Line controls in row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Line2</Name>
            <Text>Line 2</Text>
            <Value>Line3D(2000,0,0,4000,-2000,1000)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>LineListExp</Name>
        <Text>Line list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>LineCount</Name>
            <Text>Line count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>LineList</Name>
            <Text>Lines</Text>
            <Value>[Line3D(5000,0,0,7000,-2000,-2000);Line3D(5000,0,0,7000,0,0);Line3D(5000,0,0,7000,2000,2000)]</Value>
            <ValueType>Line3D</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>LineCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>LineTextExp</Name>
        <Text>Points with special text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Line3</Name>
            <Text>From point,To point</Text>
            <Value>Line3D(0,5000,0,3000,7000,0)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>LineConditionExp</Name>
        <Text>Line points with condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Line4</Name>
            <Text>Line 4</Text>
            <Value>Line3D(5000,5000,5000,7000,7000,7000)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <Visible>|EndPoint:False</Visible>
          </Parameter>
          <Parameter>
            <Name>Line5</Name>
            <Text>Line 5</Text>
            <Value>Line3D(7000,7000,7000,7000,9000,7000)</Value>
            <ValueType>Line3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <Visible>|StartPoint:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
