<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\BarPlacement\CircularArea.py</Name>
    <Title>CircularArea</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>GeometryPage</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Expander1</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>InnerRadius</Name>
            <Text>Inner radius</Text>
            <Value>2000.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>InnerArcAngles</Name>
            <Text>Inner arc start/end</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>InnerAngleStart</Name>
                <Text/>
                <Value>0.0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
              <Parameter>
                <Name>InnerAngleEnd</Name>
                <Text/>
                <Value>180.0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>OuterRadius</Name>
            <Text>Outer radius</Text>
            <Value>5000.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>InnerRadius + 100</MinValue>
          </Parameter>
          <Parameter>
            <Name>OuterArcAngles</Name>
            <Text>Outer arc start/end</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>OuterAngleStart</Name>
                <Text/>
                <Value>0.0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
              <Parameter>
                <Name>OuterAngleEnd</Name>
                <Text/>
                <Value>180.0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CreateReinforcementExpander</Name>
        <Text>Reinforcement to create</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CreateCircularReinf</Name>
            <Text>Circular</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateRadialReinf</Name>
            <Text>Radial</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OthersExpander</Name>
        <Text>Others</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>IsPythonPart</Name>
            <Text>Create as Pythonpart</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>CircularReinforcementPage</Name>
    <Text>Circular</Text>
    <Visible>CreateCircularReinf</Visible>
    <Parameters>
      <Parameter>
        <Name>CircularReinforcementPropertiesExpander</Name>
        <Text>Reinforcement properties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CircularBarDiameter</Name>
            <Text>Bar diameter</Text>
            <Value>10.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CircularConcterCoversExpander</Name>
        <Text>Concrete covers</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CircularConcreteCoverStart</Name>
            <Text>Concrete cover start</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>CircularConcreteCoverEnd</Name>
            <Text>Concrete cover end</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>CircularConcreteCoverContour</Name>
            <Text>Concrete cover contour</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>BarPropertiesExpander</Name>
        <Text>Bar properties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Distance</Name>
            <Text>Distance</Text>
            <Value>200.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>50</MinValue>
          </Parameter>
          <Parameter>
            <Name>MaxBarLength</Name>
            <Text>Maximal bar length</Text>
            <Value>14000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MinBarLength</Name>
            <Text>Minimal bar length</Text>
            <Value>500.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacementRule</Name>
            <Text>Placement rule</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>RadioButton1</Name>
                <Text>No</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>RadioButton2</Name>
                <Text>Swapped</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>RadioButton3</Name>
                <Text>Optimized</Text>
                <Value>2</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>OddFirstBarLength</Name>
            <Text>First bar length odd ring number</Text>
            <Value>7000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>EvenFirstBarLength</Name>
            <Text>First bar length even ring number</Text>
            <Value>4000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MinBarRadius</Name>
            <Text>Minimal radius</Text>
            <Value>100.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MaxBarRise</Name>
            <Text>Maximal rise</Text>
            <Value>2000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OverlapPropertiesExpander</Name>
        <Text>Overlap properties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>OverlapStartAsCircle</Name>
            <Text>Overlap start as circle</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>OddOverlapStart</Name>
            <Text>Overlap start odd ring</Text>
            <Value>1000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>EvenOverlapStart</Name>
            <Text>Overlap start even ring</Text>
            <Value>500.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OverlapEndAsCircle</Name>
            <Text>Overlap end as circle</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>OddOverlapEnd</Name>
            <Text>Overlap end odd ring number</Text>
            <Value>500.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>EvenOverlapEnd</Name>
            <Text>Overlap end even ring number</Text>
            <Value>1000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>OverlapLength</Name>
            <Text>Overlap Length</Text>
            <Value>1000.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CircularPerLinearMeterExpander</Name>
        <Text>Placement per linear meter</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlaceCircularPerLinearMeter</Name>
            <Text>Place per linear meter</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CircularLengthFactor</Name>
            <Text>Length factor</Text>
            <Value>1</Value>
            <ValueType>Double</ValueType>
            <Visible>PlaceCircularPerLinearMeter</Visible>
            <MinValue>1</MinValue>
            <MaxValue>2</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>RadialReinforcementPage</Name>
    <Text>Radial</Text>
    <Visible>CreateRadialReinf</Visible>
    <Parameters>
      <Parameter>
        <Name>RadialReinforcementPropertiesExpander</Name>
        <Text>Reinforcement properties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RadialBarDiameter</Name>
            <Text>Bar diameter</Text>
            <Value>10.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RadialPlacementPropertiesExpander</Name>
        <Text>PlacementPropeties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RadialBarCount</Name>
            <Text>Bar count</Text>
            <Value>10</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RadialConcterCoversExpander</Name>
        <Text>Concrete covers</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RadialConcreteCoverLeft</Name>
            <Text>Concrete cover left</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>RadialConcreteCoverRight</Name>
            <Text>Concrete cover right</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>RadialConcreteCoverBottom</Name>
            <Text>Concrete cover bottom</Text>
            <Value>50.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RadialPerLinearMeterExpander</Name>
        <Text>Placement per linear meter</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlaceRadialPerLinearMeter</Name>
            <Text>Place per linear meter</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>RadialLengthFactor</Name>
            <Text>Length factor</Text>
            <Value>1</Value>
            <ValueType>Double</ValueType>
            <Visible>PlaceRadialPerLinearMeter</Visible>
            <MinValue>1</MinValue>
            <MaxValue>2</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
