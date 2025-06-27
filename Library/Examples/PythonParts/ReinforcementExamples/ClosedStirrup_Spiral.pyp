<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\ClosedStirrupSpiral.py</Name>
    <Title>Closed Stirrup Spiral Freeform</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Reinforcement</Text>
    <Parameters>
      <Parameter>
        <Name>Expander1</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>500.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>500.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>PlacementLength</Name>
            <Text>Placement length</Text>
            <Value>2000.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>2 * ConcreteCover + 2 * Diameter + Distance</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander2</Name>
        <Text>Reinforcement</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>HorizontalPlacement</Name>
            <Text>Horizontal placement</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteGrade</Name>
            <Text>Concrete grade</Text>
            <Value>4</Value>
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
            <Value>10.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCover</Name>
            <Text>Concrete cover</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>Distance</Name>
            <Text>Bar spacing</Text>
            <Value>200.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>2 * Diameter</MinValue>
          </Parameter>
          <Parameter>
            <Name>BendingRoller</Name>
            <Text>Bending roller</Text>
            <Value>4.0</Value>
            <ValueType>ReinfBendingRoller</ValueType>
          </Parameter>
          <Parameter>
            <Name>StirrupType</Name>
            <Text>Type</Text>
            <Value>Torsion</Value>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander3</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Surface</Name>
            <Text>Surface</Text>
            <Value>SMT\\concrete_exposed_concrete_holes</Value>
            <DisableButtonIsShown>False</DisableButtonIsShown>
            <ValueType>MaterialButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>Layer</Name>
            <Text>Layer</Text>
            <Value>0</Value>
            <ValueType>Layer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Pen</Name>
            <Text>Line thickness</Text>
            <Value>1</Value>
            <ValueType>Pen</ValueType>
          </Parameter>
          <Parameter>
            <Name>Stroke</Name>
            <Text>Line type</Text>
            <Value>1</Value>
            <ValueType>Stroke</ValueType>
          </Parameter>
          <Parameter>
            <Name>Color</Name>
            <Text>Line color</Text>
            <Value>1</Value>
            <ValueType>Color</ValueType>
          </Parameter>
          <Parameter>
            <Name>UseConstructionLineMode</Name>
            <Text>Use construction line mode</Text>
            <Value>1</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
