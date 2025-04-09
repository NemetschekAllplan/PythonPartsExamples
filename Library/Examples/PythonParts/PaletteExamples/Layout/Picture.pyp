<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\Layout\Picture.py</Name>
    <Title>Picture</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>Picture1Exp</Name>
        <Text>PNG picture with left orientation</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Picture1</Name>
            <Value>PictureForPalette.png</Value>
            <!-- referencing local image -->
            <Orientation>Left</Orientation>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Picture2Exp</Name>
        <Text>SVG picture with middle orientation</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Picture2</Name>
            <Value>PictureForPalette.svg</Value>
            <!-- referencing local image -->
            <Orientation>Middle</Orientation>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Picture3Exp</Name>
        <Text>Resource picture with right orientation</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Picture3</Name>
            <Value>11851</Value>
            <!-- referencing Allplan resource image -->
            <Orientation>Right</Orientation>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PictureRowsExp</Name>
        <Text>Pictures in the row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RowWidth</Name>
            <Text>Width</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>InfoPicture1</Name>
                <Text>Enter the width</Text>
                <Value>info.svg</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>Width</Name>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>WidthParamPicture</Name>
                <Value>AllplanSettings.PictResParam.eParam01</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>RowThickness</Name>
            <Text>Thickness</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>InfoPicture2</Name>
                <Text>Enter the thickness</Text>
                <Value>info.svg</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>Thickness</Name>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>ThicknessParamPicture</Name>
                <Value>AllplanSettings.PictResParam.eParam02</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>RowDiameter</Name>
            <Text>Diameter</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>InfoPicture3</Name>
                <Text>Enter the diameter</Text>
                <Value>info.svg</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>Diameter</Name>
                <Value>500.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>DiameterParamPicture</Name>
                <Value>AllplanSettings.PictResParam.eParam03</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DynamicPictureExpander</Name>
        <Text>Dynamic picture form script</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DynamicPictureCombo</Name>
            <Text>Select the picture</Text>
            <Value>Representation 1</Value>
            <ValueList>Representation 1|Representation 2|Representation 3</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>DynamicPicture</Name>
            <Text/>
            <Value>etc\Library\Finish\Bitmaps\rs_rep3.png</Value>
            <ValueType>Picture</ValueType>
            <Orientation>Right</Orientation>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ListGroupExpander</Name>
        <Text>Dynamic picture in list group</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ListGroup</Name>
            <ValueType>ListGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>ListGroupRow</Name>
                <Text/>
                <TextDyn>
match $list_row:
    case 0:
        return "Row 1"

    case 1:
        return "Row 2"

    case 2:
        return "Row 3"
</TextDyn>
                <ValueType>Row</ValueType>
                <Value>OVERALL:2</Value>
                <Visible>$list_row &lt; 3</Visible>
                <Parameters>
                  <Parameter>
                    <Name>TextDummy</Name>
                    <Text/>
                    <Value/>
                    <ValueType>Text</ValueType>
                    <Visible>$list_row &lt; 3</Visible>
                    <WidthInRow>16</WidthInRow>
                  </Parameter>
                  <Parameter>
                    <Name>ListGroupPicture</Name>
                    <Value/>
                    <ValueType>Picture</ValueType>
                    <Orientation>LEFT</Orientation>
                    <ValueTextDyn>
match $list_row:
    case 0:
        return "etc\\Library\\Finish\\Bitmaps\\rs_rep3.png"

    case 1:
        return "etc\\Library\\Finish\\Bitmaps\\rs_rep2.png"

    case 2:
        return "etc\\Library\\Finish\\Bitmaps\\rs_rep1.png"
</ValueTextDyn>
                    <Visible>$list_row &lt; 3</Visible>
                  </Parameter>
                  <Parameter>
                    <Name>UseScale</Name>
                    <Text>Show</Text>
                    <Dimensions>3</Dimensions>
                    <Value>[1,1,1]</Value>
                    <ValueType>CheckBox</ValueType>
                    <Visible>$list_row &lt; 3</Visible>
                    <WidthInRow>25</WidthInRow>
                  </Parameter>
                  <Parameter>
                    <Name>Scale</Name>
                    <Text>RSC</Text>
                    <ValueList>0|1|5|10|20|25|50|100|200|250|500|1000|2000|5000|10000</ValueList>
                    <Dimensions>4</Dimensions>
                    <Value>[0,50,100,200]</Value>
                    <ValueType>IntegerComboBox</ValueType>
                    <Visible>$list_row &lt; 3</Visible>
                  </Parameter>
                  <Parameter>
                    <Name>Scale</Name>
                    <Text>RSC</Text>
                    <Dimensions>4</Dimensions>
                    <ValueType>IntegerComboBox</ValueType>
                    <Visible>$list_row &lt; 3</Visible>
                    <ListIndexOffset>1</ListIndexOffset>
                  </Parameter>
                </Parameters>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
