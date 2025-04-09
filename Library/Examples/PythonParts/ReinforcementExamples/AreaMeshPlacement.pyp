<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\AreaMeshPlacement.py</Name>
    <Title>AreaMeshPlacement</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Reinforcement</Text>
    <Parameters>
      <Parameter>
        <Name>Geometry</Name>
        <Text>Geometry</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>20000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>10000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverBorder</Name>
            <Text>Concrete cover</Text>
            <Value>50</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverZDir</Name>
            <Text>Concrete cover z direction</Text>
            <Value>50</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>CornerRecessLength</Name>
            <Text>Corner recess length</Text>
            <Value>5000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>CornerRecessWidth</Name>
            <Text>Corner recess width</Text>
            <Value>3000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OpeningPosition</Name>
            <Text>Opening position</Text>
            <Value>Point3D(12000,4000,0)</Value>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>OpeningLength</Name>
            <Text>Opening length</Text>
            <Value>2500</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OpeningWidth</Name>
            <Text>Opening width</Text>
            <Value>2000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OpeningConcreteCover</Name>
            <Text>Concrete cover opening</Text>
            <Value>50</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Placement</Name>
        <Text>Placement</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlacementAngle</Name>
            <Text>Placement angle</Text>
            <Value>90</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>StartLength</Name>
            <Text>Start length</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>StartWidth</Name>
            <Text>Start width</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OverlapLongitudinal</Name>
            <Text>Overlap longitudinal</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OverlapCross</Name>
            <Text>Overlap cross</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MeshSizeRound</Name>
            <Text>Round the mesh size</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacementEndJustified</Name>
            <Text>End justified placement</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacementStartChange</Name>
            <Text>Change placement start</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>LapJointOffset</Name>
            <Text>Lap joint offset</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacementDirection</Name>
            <Text>Placement direction</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>Longitudinal</Name>
                <Text>Longitudinal</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>Cross</Name>
                <Text>Cross</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Reinforcement</Name>
        <Text>Reinforcement</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
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
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
