<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\SolidCreation\RevolvedBRep.py</Name>
    <Title>Revolved BRep</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Revolved BRep</Text>
    <Parameters>
      <Parameter>
        <Name>PointsExpander</Name>
        <Text>Profile points</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CoordinatesTextRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>CoordinateXText</Name>
                <Text/>
                <Value>X</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>CoordinateYText</Name>
                <Text/>
                <Value>Y</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>CoordinateZText</Name>
                <Text/>
                <Value>Z</Value>
                <ValueType>Text</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ProfilePoints</Name>
            <Text>Profile points</Text>
            <Value>[Point3D(  0.0,   0.0,   0.0);
                        Point3D(400.0, 200.0,   0.0);
                        Point3D(100.0, 500.0,   0.0);
                        Point3D(500.0, 700.0,   0.0);
                        Point3D(  0.0, 900.0,   0.0)]</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>False</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RevolvingParametersExpander</Name>
        <Text>Revolving parameters</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RevolveAngle</Name>
            <Text>Revolve angle</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>359</MaxValue>
          </Parameter>
          <Parameter>
            <Name>CloseCaps</Name>
            <Text>Close caps</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>NumProfiles</Name>
            <Text>Number of control profiles</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
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
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
