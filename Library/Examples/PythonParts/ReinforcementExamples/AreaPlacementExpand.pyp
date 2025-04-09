<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\AreaPlacementExpand.py</Name>
    <Title>AreaPlacement</Title>
    <GeometryExpand>True</GeometryExpand>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Reinforcement</Text>
    <Parameters>
      <Parameter>
        <Name>SteelGrade</Name>
        <Text>Steel grade</Text>
        <Value>4</Value>
        <ValueType>ReinfSteelGrade</ValueType>
      </Parameter>
      <Parameter>
        <Name>Diameter</Name>
        <Text>Bar diameter</Text>
        <Value>10</Value>
        <ValueType>ReinfBarDiameter</ValueType>
      </Parameter>
      <Parameter>
        <Name>ConcreteCover</Name>
        <Text>Concrete cover</Text>
        <Value>25</Value>
        <ValueType>ReinfConcreteCover</ValueType>
      </Parameter>
      <Parameter>
        <Name>Distance</Name>
        <Text>Bar spacing</Text>
        <Value>200</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BarMaxLength</Name>
        <Text>Maximal bar length</Text>
        <Value>12000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BarOverlap</Name>
        <Text>Bar overlap</Text>
        <Value>0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
