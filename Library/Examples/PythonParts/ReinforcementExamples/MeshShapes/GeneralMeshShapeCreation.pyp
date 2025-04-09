<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\MeshShapes\GeneralMeshShapeCreation.py</Name>
    <Title>GeneralShapeCreation</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Reinforcement</Text>
    <Parameters>
      <Parameter>
        <Name>Reinforcement</Name>
        <Text>Reinforcement</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
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
            <Name>ConcreteCover</Name>
            <Text>Concrete cover</Text>
            <Value>25</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>MeshGroup</Name>
            <Text>Cross-section catalog</Text>
            <Value>-1</Value>
            <ValueType>ReinfMeshGroup</ValueType>
          </Parameter>
          <Parameter>
            <Name>MeshType</Name>
            <Text>Meshtype</Text>
            <Value>-1</Value>
            <ValueType>ReinfMeshType</ValueType>
            <Constraint>MeshGroup</Constraint>
          </Parameter>
          <Parameter>
            <Name>MeshGroupDiamond</Name>
            <Text>Cross-section catalog diamond</Text>
            <Value>-1</Value>
            <ValueType>ReinfMeshGroup</ValueType>
          </Parameter>
          <Parameter>
            <Name>MeshTypeDiamond</Name>
            <Text>Meshtype diamond</Text>
            <Value>-1</Value>
            <ValueType>ReinfMeshType</ValueType>
            <Constraint>MeshGroupDiamond</Constraint>
          </Parameter>
          <Parameter>
            <Name>BendingRoller</Name>
            <Text>Bending roller</Text>
            <Value>4</Value>
            <ValueType>ReinfBendingRoller</ValueType>
          </Parameter>
          <Parameter>
            <Name>Rearrange</Name>
            <Text>Rearrange</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
