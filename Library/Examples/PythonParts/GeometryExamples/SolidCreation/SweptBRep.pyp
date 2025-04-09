<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\SolidCreation\SweptBRep.py</Name>
    <Title>Swept BRep</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Swept BRep</Text>
    <Parameters>
      <Parameter>
        <Name>ProfileExpander</Name>
        <Text>Profile</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MinorRadius</Name>
            <Text>Minor radius</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MajorRadius</Name>
            <Text>Major radius</Text>
            <Value>150</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PointsExpander</Name>
        <Text>Path points</Text>
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
            <Name>PathPoints</Name>
            <Text>Path points</Text>
            <Value>[Point3D(   0.0,   0.0,   0.0);
                        Point3D(-100.0,   0.0, 500.0);
                        Point3D(   0.0,   0.0, 900.0);
                        Point3D(1000.0,   0.0,1300.0);
                        Point3D(1000.0,1000.0,1700.0)]</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>False</XYZinRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SweepingParametersExpander</Name>
        <Text>Sweeping parameters</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CloseCaps</Name>
            <Text>Close caps</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>RailRotationType</Name>
            <Text>Rail rotation</Text>
            <Value>Unlocked</Value>
            <ValueList>"|".join(str(key) for key in AllplanGeo.SweepRotationType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OtherParameterExpander</Name>
        <Text>Other options</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CreatePathCurve</Name>
            <Text>Create path curve</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateProfileCurve</Name>
            <Text>Create profile curve</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
