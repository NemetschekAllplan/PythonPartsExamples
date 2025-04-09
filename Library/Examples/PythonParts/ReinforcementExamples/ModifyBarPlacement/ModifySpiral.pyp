<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\ModifyBarPlacement\ModifySpiral.py</Name>
    <Title>Spiral</Title>
    <Version>1.0</Version>
  </Script>
  <Constants>
    <Constant>
      <Name>ELEMENT_SELECT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>SPIRAL_INPUT</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Spiral</Text>
    <Visible>InputMode == SPIRAL_INPUT</Visible>
    <Parameters>
      <Parameter>
        <Name>Expander2</Name>
        <Text>Reinforcement</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SteelGrade</Name>
            <Text>Steel grade</Text>
            <Value>4</Value>
            <ValueType>ReinfSteelGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacePerLinearMeter</Name>
            <Text>Place per linear meter</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>LengthFactor</Name>
            <Text>Length factor</Text>
            <Value>1.0</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>Diameter</Name>
            <Text>Bar diameter</Text>
            <Value>10.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverStart</Name>
            <Text>Concrete cover start</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverContour</Name>
            <Text>Concrete cover contour</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverEnd</Name>
            <Text>Concrete cover end</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>Pitch</Name>
            <Text>Pitch</Text>
            <Value>200.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>50</MinValue>
          </Parameter>
          <Parameter>
            <Name>LoopsStart</Name>
            <Text>Loops start</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Pitch1</Name>
            <Text>Pitch section 1</Text>
            <Value>100.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>50</MinValue>
            <Visible>Length1 &gt; 0</Visible>
          </Parameter>
          <Parameter>
            <Name>Length1</Name>
            <Text>Length section 1</Text>
            <Value>0.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Pitch2</Name>
            <Text>Pitch section 2</Text>
            <Value>100.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>50</MinValue>
            <Visible>Length2 &gt; 0</Visible>
          </Parameter>
          <Parameter>
            <Name>Length2</Name>
            <Text>Length section 2</Text>
            <Value>0.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Pitch3</Name>
            <Text>Pitch section 3</Text>
            <Value>100.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>50</MinValue>
            <Visible>Length3 &gt; 0</Visible>
          </Parameter>
          <Parameter>
            <Name>Length3</Name>
            <Text>Length section 3</Text>
            <Value>0.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Pitch4</Name>
            <Text>Pitch section 4</Text>
            <Value>100.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>50</MinValue>
            <Visible>Length4 &gt; 0</Visible>
          </Parameter>
          <Parameter>
            <Name>Length4</Name>
            <Text>Length section 4</Text>
            <Value>0.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>LoopsEnd</Name>
            <Text>Loops end</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>StartHook</Name>
            <Text>Use start hook</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Enable>PlacePerLinearMeter == False</Enable>
          </Parameter>
          <Parameter>
            <Name>StartHookLength</Name>
            <Text>Start hook length</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
            <Enable>StartHook == True and PlacePerLinearMeter == False</Enable>
          </Parameter>
          <Parameter>
            <Name>StartHookAngle</Name>
            <Text>Start hook angle</Text>
            <Value>90.0</Value>
            <ValueType>Angle</ValueType>
            <Enable>StartHook == True and PlacePerLinearMeter == False</Enable>
            <MinValue>-180.0</MinValue>
            <MaxValue>180.0</MaxValue>
          </Parameter>
          <Parameter>
            <Name>EndHook</Name>
            <Text>Use end hook</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Enable>PlacePerLinearMeter == False</Enable>
          </Parameter>
          <Parameter>
            <Name>EndHookLength</Name>
            <Text>End hook length</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
            <Enable>EndHook == True and PlacePerLinearMeter == False</Enable>
          </Parameter>
          <Parameter>
            <Name>EndHookAngle</Name>
            <Text>End hook angle</Text>
            <Value>90.0</Value>
            <ValueType>Angle</ValueType>
            <Enable>EndHook == True and PlacePerLinearMeter == False</Enable>
            <MinValue>-180.0</MinValue>
            <MaxValue>180.0</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value/>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
