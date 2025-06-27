<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\Layout\Row.py</Name>
    <Title>Row</Title>
    <Version>1.0</Version>
  </Script>
  <PaletteLayoutScript>
button_width          = 22
default_control_width = 30
min_color_width       = 55

#----------------- calculate a minimal useful width for the color combo box

control_width_general = AllplanPalette.GetPaletteDataColumnWidth() / 4
color_width_general = max(min_color_width, control_width_general)
edit_width_general  = max(10, (AllplanPalette.GetPaletteDataColumnWidth() - color_width_general) / 3)

#----------------- set the with for controls in the full row

color_width_overall = default_control_width + 20
edit_width_overall  = color_width_general / 2
    </PaletteLayoutScript>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>GeneralRowExp</Name>
        <Text>General row, same control width</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row1</Name>
            <Text>First Cube</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Length1</Name>
                <Text>Length</Text>
                <TextId>1001</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Width1</Name>
                <Text>Width</Text>
                <TextId>1002</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Height1</Name>
                <Text>Height</Text>
                <TextId>1003</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Color1</Name>
                <Text>Line color</Text>
                <TextId>e_COLOR</TextId>
                <Value>1</Value>
                <ValueType>Color</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeneralRowExp1</Name>
        <Text>General row, different control width</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row1a</Name>
            <Text>First Cube</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Length1</Name>
                <Text>Length</Text>
                <TextId>1001</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
                <WidthInRow>edit_width_general</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>Width1</Name>
                <Text>Width</Text>
                <TextId>1002</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
                <WidthInRow>edit_width_general</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>Height1</Name>
                <Text>Height</Text>
                <TextId>1003</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
                <WidthInRow>edit_width_general</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>Color1</Name>
                <Text>Line color</Text>
                <TextId>e_COLOR</TextId>
                <Value>1</Value>
                <ValueType>Color</ValueType>
                <WidthInRow>color_width_general</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OverallRow</Name>
        <Text>Overall row, same control width</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row2</Name>
            <Text>Second cube</Text>
            <Value>OVERALL</Value>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Length2</Name>
                <Text>Length</Text>
                <TextId>1004</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Width2</Name>
                <Text>Width</Text>
                <TextId>1005</TextId>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Height2</Name>
                <Text>Height</Text>
                <TextId>1006</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Color2</Name>
                <Text>Line color</Text>
                <TextId>e_COLOR</TextId>
                <Value>2</Value>
                <ValueType>Color</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OverallRow1</Name>
        <Text>Overall row, different control width</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row2</Name>
            <Text>Second cube</Text>
            <Value>OVERALL</Value>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Length2</Name>
                <Text>Length</Text>
                <TextId>1004</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
                <WidthInRow>edit_width_overall</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>Width2</Name>
                <Text>Width</Text>
                <TextId>1005</TextId>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
                <WidthInRow>edit_width_overall</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>Height2</Name>
                <Text>Height</Text>
                <TextId>1006</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
                <WidthInRow>edit_width_overall</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>Color2</Name>
                <Text>Line color</Text>
                <TextId>e_COLOR</TextId>
                <Value>2</Value>
                <ValueType>Color</ValueType>
                <WidthInRow>color_width_overall</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SplittedRow</Name>
        <Text>Splitted row, one control left</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row3</Name>
            <Text>Third cube</Text>
            <Value>OVERALL:1</Value>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Length3</Name>
                <Text>Length</Text>
                <TextId>1004</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Width3</Name>
                <Text>Width</Text>
                <TextId>1005</TextId>
                <Value>3000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Height3</Name>
                <Text>Height</Text>
                <TextId>1006</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Color3</Name>
                <Text>Line color</Text>
                <TextId>e_COLOR</TextId>
                <Value>3</Value>
                <ValueType>Color</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>MultiLineButtonExp</Name>
        <Text>General row, multi line button list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MultiLineShapeType</Name>
            <Text>Shape</Text>
            <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
            <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eDiamond|
                          AllplanArchEle.VerticalOpeningShapeType.eCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eSemiCircle</EnumList>
            <ValueTextList>Rectangle|Diamond|Round/oval|Circle at top</ValueTextList>
            <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eDiamond|
                           AllplanSettings.PictResShapeType.eCircle|
                           AllplanSettings.PictResShapeType.eSemiCircle</EnumList2>
            <ValueType>PictureResourceButtonList</ValueType>
            <WidthInRow>button_width * 4</WidthInRow>
          </Parameter>
          <Parameter>
            <Name>MultiLineShapeRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>EmptyText</Name>
                <Text/>
                <Value/>
                <ValueType>Text</ValueType>
                <WidthInRow>button_width</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>MultiLineShapeType1</Name>
                <Text/>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eSemiDiamond|
                              AllplanArchEle.VerticalOpeningShapeType.eRiseBottomTop|
                              AllplanArchEle.VerticalOpeningShapeType.eArbitrary</EnumList>
                <ValueTextList>Semi diamong|Rise bottom and top|Profile from library</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eSemiDiamond|
                               AllplanSettings.PictResShapeType.eRiseBottomTop|
                               AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <WidthInRow>button_width * 3</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>MultiLineOverallRowButtonExp</Name>
        <Text>Overall row, multi line button list with text</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MultiLineOverallTextRowShapeTypeRow</Name>
            <Text>Shape</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>MultiLineOverallTextRowShapeType</Name>
                <Text/>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                              AllplanArchEle.VerticalOpeningShapeType.eDiamond|
                              AllplanArchEle.VerticalOpeningShapeType.eCircle|
                              AllplanArchEle.VerticalOpeningShapeType.eSemiCircle</EnumList>
                <ValueTextList>Rectangle|Diamond|Round/oval|Circle at top</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                               AllplanSettings.PictResShapeType.eDiamond|
                               AllplanSettings.PictResShapeType.eCircle|
                               AllplanSettings.PictResShapeType.eSemiCircle</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <WidthInRow>default_control_width * 4</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>MultiLineOverallTextRowShapeTypeRow1</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>EmptyText2</Name>
                <Text/>
                <Value/>
                <ValueType>Text</ValueType>
                <WidthInRow>default_control_width * 2</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>MultiLineOverallTextRowShapeType1</Name>
                <Text/>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eSemiDiamond|
                              AllplanArchEle.VerticalOpeningShapeType.eRiseBottomTop|
                              AllplanArchEle.VerticalOpeningShapeType.eArbitrary</EnumList>
                <ValueTextList>Semi diamong|Rise bottom and top|Profile from library</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eSemiDiamond|
                               AllplanSettings.PictResShapeType.eRiseBottomTop|
                               AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <WidthInRow>default_control_width * 3</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>MultiLineOverallRowButtonExp</Name>
        <Text>Overall row, multi line button list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MultiLineOverallRowShapeTypeRow</Name>
            <Text/>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>MultiLineOverallRowShapeType</Name>
                <Text/>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                                AllplanArchEle.VerticalOpeningShapeType.eDiamond|
                                AllplanArchEle.VerticalOpeningShapeType.eCircle|
                                AllplanArchEle.VerticalOpeningShapeType.eSemiCircle</EnumList>
                <ValueTextList>Rectangle|Diamond|Round/oval|Circle at top</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                                AllplanSettings.PictResShapeType.eDiamond|
                                AllplanSettings.PictResShapeType.eCircle|
                                AllplanSettings.PictResShapeType.eSemiCircle</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <WidthInRow>button_width * 4</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>MultiLineOverallRowShapeTypeRow1</Name>
            <Text>Text</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>EmptyText3</Name>
                <Text/>
                <Value/>
                <ValueType>Text</ValueType>
                <WidthInRow>button_width</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>MultiLineOverallRowShapeType1</Name>
                <Text/>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eSemiDiamond|
                              AllplanArchEle.VerticalOpeningShapeType.eRiseBottomTop|
                              AllplanArchEle.VerticalOpeningShapeType.eArbitrary</EnumList>
                <ValueTextList>Semi diamong|Rise bottom and top|Profile from library</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eSemiDiamond|
                               AllplanSettings.PictResShapeType.eRiseBottomTop|
                               AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <WidthInRow>button_width *  3</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
