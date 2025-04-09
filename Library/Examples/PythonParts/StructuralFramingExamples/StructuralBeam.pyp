<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <LanguageFile>etc\Examples\PythonParts\StructuralFramingExamples\StructuralFraming</LanguageFile>
  <Script>
    <Name>StructuralFramingExamples\StructuralBeam.py</Name>
    <Title>Beam</Title>
    <Version>1.0</Version>
    <ReadLastInput>False</ReadLastInput>
  </Script>
  <Page>
    <Name>PageGeometrie</Name>
    <Text>Geometry</Text>
    <TextId>1000</TextId>
    <Parameters>
      <Parameter>
        <Name>BeamType</Name>
        <TextId>9902</TextId>
        <Value>0</Value>
        <ValueList>0|1</ValueList>
        <ValueList2>15581|14601</ValueList2>
        <ValueType>PictureResourceButtonList</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <TextId>1002</TextId>
        <Value>100</Value>
        <MinValue>1</MinValue>
        <Visible>BeamType == 0</Visible>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness</Name>
        <TextId>1003</TextId>
        <Value>80</Value>
        <MinValue>1</MinValue>
        <Visible>BeamType == 0</Visible>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>ProfilePath</Name>
        <TextId>1005</TextId>
        <ValueType>Row</ValueType>
        <Visible>BeamType == 1</Visible>
        <Parameters>
          <Parameter>
            <Name>SymbolDialog</Name>
            <Value>Auswahl</Value>
            <ValueType>String</ValueType>
            <ValueDialog>SymbolDialog</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Angle</Name>
        <TextId>1006</TextId>
        <Value>0</Value>
        <ValueType>Angle</ValueType>
      </Parameter>
      <Parameter>
        <Name>SkeletonPlaneReferences</Name>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>BeamPlaneReferences</Name>
            <TextId>1007</TextId>
            <Value>None</Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
            <Visible>|BeamPlaneReferences.Height:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AnchorPointsExpander</Name>
        <TextId>1100</TextId>
        <ValueType>Expander</ValueType>
        <Visible>True</Visible>
        <Parameters>
          <Parameter>
            <Name>TwoAnchorPoints</Name>
            <TextId>1114</TextId>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>AnchorPoint</Name>
            <TextId>1101</TextId>
            <Value>top left</Value>
            <ValueTextId>1106</ValueTextId>
            <ValueList>top left|left in middle|left down|top in middle|in middle|in middle down|top right|right in middle|right down|in center of gravity</ValueList>
            <ValueList_TextIds>1102|1103|1104|1105|1106|1107|1108|1109|1110|1111</ValueList_TextIds>
            <Visible>TwoAnchorPoints == False</Visible>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>OffsetFromAnchorPoint</Name>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Offset</Name>
                <TextId>1112</TextId>
                <Value>(0,0)</Value>
                <Visible>TwoAnchorPoints == False</Visible>
                <ValueType>Point2D</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>AnchorPointStart</Name>
            <TextId>1116</TextId>
            <Value>top left</Value>
            <ValueTextId>1106</ValueTextId>
            <ValueList>top left|left in middle|left down|top in middle|in middle|in middle down|top right|right in middle|right down|in center of gravity</ValueList>
            <ValueList_TextIds>1102|1103|1104|1105|1106|1107|1108|1109|1110|1111</ValueList_TextIds>
            <Visible>TwoAnchorPoints == True</Visible>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>OffsetFromAnchorPoint</Name>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>OffsetStart</Name>
                <TextId>1112</TextId>
                <Value>(0,0)</Value>
                <Visible>TwoAnchorPoints == True</Visible>
                <ValueType>Point2D</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>AnchorPointEnd</Name>
            <TextId>1117</TextId>
            <Value>top left</Value>
            <ValueTextId>1106</ValueTextId>
            <ValueList>top left|left in middle|left down|top in middle|in middle|in middle down|top right|right in middle|right down|in center of gravity</ValueList>
            <ValueList_TextIds>1102|1103|1104|1105|1106|1107|1108|1109|1110|1111</ValueList_TextIds>
            <Visible>TwoAnchorPoints == True</Visible>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>OffsetFromAnchorPoint</Name>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>OffsetEnd</Name>
                <TextId>1112</TextId>
                <Value>(0,0)</Value>
                <Visible>TwoAnchorPoints == True</Visible>
                <ValueType>Point2D</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>StartAngle</Name>
            <TextId>1118</TextId>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>StartAngleX</Name>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
              <Parameter>
                <Name>StartAngleY</Name>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>EndAngle</Name>
            <TextId>1119</TextId>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>EndAngleX</Name>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
              <Parameter>
                <Name>EndAngleY</Name>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ShowAxis</Name>
            <TextId>1113</TextId>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>PageAttribute</Name>
    <Text>Attribute</Text>
    <TextId>3000</TextId>
    <Parameters>
      <Parameter>
        <Name>Material</Name>
        <TextId>3001</TextId>
        <Value>Steel_S355</Value>
        <ValueType>String</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
