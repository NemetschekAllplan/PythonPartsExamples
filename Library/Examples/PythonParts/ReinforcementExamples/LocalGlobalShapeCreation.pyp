<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\LocalGlobalShapeCreation.py</Name>
    <Title>LocalGlobalShapeCreation</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <Text>Length</Text>
        <Value>4000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <Text>Width</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <Text>Height</Text>
        <Value>500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>AngleZ</Name>
        <Text>Rotation angle</Text>
        <Value>33</Value>
        <ValueType>Double</ValueType>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Page2</Name>
    <Text>Reinforcement</Text>
    <Parameters>
      <Parameter>
        <Name>ConcreteGrade</Name>
        <Text>Concrete grade</Text>
        <Value>-1</Value>
        <ValueType>ReinfConcreteGrade</ValueType>
      </Parameter>
      <Parameter>
        <Name>SteelGrade</Name>
        <Text>Steel grade</Text>
        <Value>4</Value>
        <ValueType>ReinfSteelGrade</ValueType>
      </Parameter>
      <Parameter>
        <Name>Diameter</Name>
        <Text>Bar diameter</Text>
        <Value>20</Value>
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
        <Name>BendingRoller</Name>
        <Text>Bending roller</Text>
        <Value>4</Value>
        <ValueType>ReinfBendingRoller</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
