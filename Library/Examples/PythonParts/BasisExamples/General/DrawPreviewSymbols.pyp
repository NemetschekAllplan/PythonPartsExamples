<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\General\DrawPreviewSymbols.py</Name>
    <Title>ComboBox</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>PreviewSymbol</Name>
        <Text>Preview symbol</Text>
        <Value>Circle</Value>
        <ValueList>Circle|Polyline|Cross|Mark|Coordinate cross|Arrow|Filled rectangle|Text</ValueList>
        <ValueType>StringComboBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>Radius</Name>
        <Text>Radius in pixel</Text>
        <Value>10</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Circle"</Visible>
      </Parameter>
      <Parameter>
        <Name>ArrowSize</Name>
        <Text>Size in pixel</Text>
        <Value>20</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Arrow"</Visible>
      </Parameter>
      <Parameter>
        <Name>CrossSize</Name>
        <Text>Cross size in pixel</Text>
        <Value>20</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Cross"</Visible>
      </Parameter>
      <Parameter>
        <Name>MarkSize</Name>
        <Text>Mark size in pixel</Text>
        <Value>20</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Mark"</Visible>
      </Parameter>
      <Parameter>
        <Name>ArmSize</Name>
        <Text>Arm size in pixel</Text>
        <Value>50</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Coordinate cross"</Visible>
      </Parameter>
      <Parameter>
        <Name>TextHeight</Name>
        <Text>Text height in pixel</Text>
        <Value>40</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Text"</Visible>
      </Parameter>
      <Parameter>
        <Name>RectSize</Name>
        <Text>Rectangle size in pixel</Text>
        <Value>20</Value>
        <ValueType>Integer</ValueType>
        <Visible>PreviewSymbol == "Filled rectangle"</Visible>
      </Parameter>
      <Parameter>
        <Name>RotationAngle</Name>
        <Text>Rotation angle</Text>
        <Value>0</Value>
        <ValueType>Angle</ValueType>
        <Visible>PreviewSymbol in ["Text", "Arrow", "Filled rectangle"]</Visible>
      </Parameter>
      <Parameter>
        <Name>ColorID</Name>
        <Text>Line color</Text>
        <Value>16711680</Value>
        <ValueType>Integer</ValueType>
        <ValueDialog>RGBColorDialog</ValueDialog>
      </Parameter>
    </Parameters>
  </Page>
</Element>
