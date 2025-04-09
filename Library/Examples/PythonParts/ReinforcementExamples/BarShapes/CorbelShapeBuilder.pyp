<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\BarShapes\CorbelShapeBuilder.py</Name>
    <Title>Corbel shape</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>CorbelShape</Name>
    <Text>Corbel shape</Text>
    <Parameters>
      <Parameter>
        <Name>GeometryParametersExpander</Name>
        <Text>Rebar geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ColumnWidth</Name>
            <Text>Column width</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>ColumnThickness</Name>
            <Text>Column thickness</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>CorbelWidth</Name>
            <Text>Corbel width</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>CorbelTop</Name>
            <Text>Corbel top</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ShapePropertiesExpander</Name>
        <Text>ReinforcementShapeProperties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Diameter</Name>
            <Text>Bar diameter</Text>
            <Value>10.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>BendingRoller</Name>
            <Text>Bending roller</Text>
            <Value>4.0</Value>
            <ValueType>ReinfBendingRoller</ValueType>
          </Parameter>
          <Parameter>
            <Name>SteelGrade</Name>
            <Text>Steel grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfSteelGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteGrade</Name>
            <Text>Concrete grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfConcreteGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>BendingShapeType</Name>
            <Text>Bending shape type</Text>
            <Value>LongitudinalBar</Value>
            <ValueList>"|".join(str(key) for key in AllplanReinf.BendingShapeType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ConcreteCoverPropertiesExpander</Name>
        <Text>ConcreteCoverProperties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ConcreteCover</Name>
            <Text>Concrete cover</Text>
            <Value>20.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
