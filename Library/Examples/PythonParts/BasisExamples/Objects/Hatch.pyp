<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\Objects\Hatch.py</Name>
    <Title>Hatch</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>GeometryExp</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
          <Parameter>
            <Name>Size</Name>
            <Text>Length,Width</Text>
            <Value>Vector2D(1000,2000)</Value>
            <ValueType>Vector2D</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowPolygon</Name>
            <Text>Show polygon</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>HatchExp</Name>
        <Text>Hatch</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonPropHatch</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
            <Visible>|CommonPropHatch.Stroke:False|CommonPropHatch.StrokeByLayer:False</Visible>
          </Parameter>
          <Parameter>
            <Name>HatchId</Name>
            <Text>Hatch ID</Text>
            <Value>1</Value>
            <ValueType>Hatch</ValueType>
          </Parameter>
          <Parameter>
            <Name>RotationAngle</Name>
            <Text>Rotation angle</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>IsScaleDependent</Name>
            <Text>Scale dependent</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>DirectionToReferenceLine</Name>
            <Text>Direction to ref line</Text>
            <Value>0</Value>
            <ValueList>0|1|2|3|4</ValueList>
            <ValueType>IntegerComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>DefineBackgroundColor</Name>
            <Text>Define background color</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>BackgroundColor</Name>
            <Text>Background color</Text>
            <Value/>
            <ValueType>Integer</ValueType>
            <ValueDialog>RGBColorDialog</ValueDialog>
            <Visible>DefineBackgroundColor == 1</Visible>
          </Parameter>
          <Parameter>
            <Name>DefineReferencePoint</Name>
            <Text>Define reference point</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ReferencePoint</Name>
            <Text>Reference point</Text>
            <Value>Point2D()</Value>
            <ValueType>Point2D</ValueType>
            <Visible>DefineReferencePoint == 1</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
