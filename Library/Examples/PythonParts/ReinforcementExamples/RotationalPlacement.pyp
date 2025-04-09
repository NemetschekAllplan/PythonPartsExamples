<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\RotationalPlacement.py</Name>
    <Title>RotationalPlacement</Title>
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
        <Value>10.0</Value>
        <ValueType>ReinfBarDiameter</ValueType>
      </Parameter>
      <Parameter>
        <Name>ConcreteCover</Name>
        <Text>Concrete cover</Text>
        <Value>30.0</Value>
        <ValueType>ReinfConcreteCover</ValueType>
      </Parameter>
      <Parameter>
        <Name>Count</Name>
        <Text>Bar count</Text>
        <Value>20</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>BendingRoller</Name>
        <Text>Bending roller</Text>
        <Value>4.0</Value>
        <ValueType>ReinfBendingRoller</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
