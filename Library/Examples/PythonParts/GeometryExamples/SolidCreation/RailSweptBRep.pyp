<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\SolidCreation\RailSweptBRep.py</Name>
    <Title>Rail swept brep</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Rail swept brep</Text>
    <Parameters>
      <Parameter>
        <Name>GeometryParameterExpander</Name>
        <Text>Geometry parameters</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>BottomSquareSide</Name>
            <Text>Side of the bottom square </Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MiddleSquareSide</Name>
            <Text>Side of the middle square </Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>TopCircleRadius</Name>
            <Text>Radius of the top circular profile</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Distance</Name>
            <Text>Distance between profiles</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MiddleSquareRotation</Name>
            <Text>Rotation of the middle profile</Text>
            <Value>45</Value>
            <ValueSlider>True</ValueSlider>
            <MinValue>0</MinValue>
            <MaxValue>90</MaxValue>
            <IntervalValue>5</IntervalValue>
            <ValueType>Angle</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RailSweptBRepParameterExpander</Name>
        <Text>Parameters of RailSweptBRep3D</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CloseCaps</Name>
            <Text>Close caps</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>UniformScaling</Name>
            <Text>Uniform scaling</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>RailRotation</Name>
            <Text>Standard rotation</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OtherParameterExpander</Name>
        <Text>Other options</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CreateProfileCurves</Name>
            <Text>Create profile curves</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateRailCurves</Name>
            <Text>Create rail curves</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
