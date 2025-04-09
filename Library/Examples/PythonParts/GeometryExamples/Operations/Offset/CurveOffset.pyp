<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Offset\CurveOffset.py</Name>
    <Title>Curve offset</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>CurveOffset</Name>
    <Text>Curve offset</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>2D and 3D curves</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>OffsetDistanceExpander</Name>
        <Text>Input method</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>InputType</Name>
            <Text>Input type</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>InputByPoint</Name>
                <Text>by point</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>InputByDistance</Name>
                <Text>by distance</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>OffsetDistance</Name>
            <Text>Offset distance</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
            <Visible>InputType == 1</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OffsetPlaneExpander</Name>
        <Text>Offset plane</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Text1</Name>
            <Text>For 3D polylines and 3D splines:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlaneRefPoint</Name>
            <Text>Reference point</Text>
            <Value>Point3D(0,0,0)</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>PlaneNormalVector</Name>
            <Text>Normal vector</Text>
            <Value>Vector3D(0,0,1000)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>Offset3DPlane</Name>
            <Text>For 3D lines</Text>
            <Value>eXY</Value>
            <ValueList>"|".join(str(key) for key in AllplanGeo.Offset3DPlane.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OffsetPropertiesExpander</Name>
        <Text>Options of Offset function</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Text2</Name>
            <Text>For 3D polylines:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>ParallelsCount</Name>
            <Text>Number of parallels</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
            <Visible>InputType == 1</Visible>
          </Parameter>
          <Parameter>
            <Name>Text3</Name>
            <Text>For polylines (2D) or splines (2D and 3D):</Text>
            <Value/>
            <ValueType>Text</ValueType>
            <Visible>InputType == 1</Visible>
          </Parameter>
          <Parameter>
            <Name>CheckSegmentsOrientation</Name>
            <Text>Check segments orientation</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>InputType == 1</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
