<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\BarPlacement\BarPlacement.py</Name>
    <Title>RebarPlacement</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>ReinforcementPage</Name>
    <Text>Reinforcement</Text>
    <Parameters>
      <Parameter>
        <Name>BarShapeExpander</Name>
        <Text>BarShapeProperties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
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
            <Name>DiameterStirrup</Name>
            <Text>Stirrup diameter</Text>
            <Value>10</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>DiameterLongitudinal</Name>
            <Text>Longitudinal bar diameter</Text>
            <Value>20</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>StirrupPlacementExpander</Name>
        <Text>BarPlacement properties for stirrup</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DistanceStirrup</Name>
            <Text>Distance</Text>
            <Value>150</Value>
            <MinValue>20</MinValue>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacementRuleStirrup</Name>
            <Text>Placement rule</Text>
            <Value>AdditionalCover</Value>
            <ValueList>AdaptDistance|AdditionalCover|AdditionalCoverLeft|AdditionalCoverRight</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacePerLinearMeter</Name>
            <Text>Place per linear meter</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>LengthFactor</Name>
            <Text>Length factor</Text>
            <Value>1.1</Value>
            <ValueType>Double</ValueType>
            <Visible>PlacePerLinearMeter</Visible>
            <MinValue>1</MinValue>
            <MaxValue>2</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>LongitudinalExp</Name>
        <Text>BarPlacement properties for longitudinal bars</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>BarCountLongitudinal</Name>
            <Text>Bar count</Text>
            <Value>4</Value>
            <MinValue>0</MinValue>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacePerLinearMeterLongitudinal</Name>
            <Text>Place per linear meter</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>LengthFactorLongitudinal</Name>
            <Text>Length factor</Text>
            <Value>1.1</Value>
            <ValueType>Double</ValueType>
            <Visible>PlacePerLinearMeterLongitudinal</Visible>
            <MinValue>1</MinValue>
            <MaxValue>2</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>OthersPage</Name>
    <Text>Others</Text>
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
        <Name>Geometry</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Sizes</Name>
            <Text>Length,Width,Height</Text>
            <Value>Vector3D(300,1500,600)</Value>
            <ValueType>Vector3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ElementCreation</Name>
        <Text>Element creation</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>IsPythonPart</Name>
            <Text>Create as PythonPart</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
