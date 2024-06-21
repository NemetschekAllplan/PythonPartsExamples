﻿<?xml version="1.0" encoding="utf-8"?>
<Element>
    <LanguageFile>AllControls</LanguageFile>
    <Script>
        <Name>PaletteExamples\AllControls.py</Name>
        <Title>AllControls</Title>
        <Version>1.0</Version>
        <TextId>1001</TextId>
        <DataColumnWidth>150</DataColumnWidth>
        <ShowFavoriteButtons>True</ShowFavoriteButtons>
    </Script>
    <Constants>
        <Constant>
            <Name>CENTER_OF_GRAVITY</Name>
            <Value>1003</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>CENTER_OF_GRAVITY_SELECTED</Name>
            <Value>1004</Value>
            <ValueType>Integer</ValueType>
        </Constant>

    </Constants>
    <Page>
        <Name>GeneralControls</Name>
        <Text>Edit</Text>

        <Parameter>
            <Name>Integer</Name>
            <Text>Integer</Text>
            <Value>4711</Value>
            <ValueType>Integer</ValueType>
            <FontFaceCode>1</FontFaceCode>
            <BackgroundColor>(0, 255, 0)</BackgroundColor>
        </Parameter>
        <Parameter>
            <Name>IntegerSlider</Name>
            <Text>Integer slider</Text>
            <Value>5</Value>
            <MinValue>1</MinValue>
            <MaxValue>10</MaxValue>
            <ValueType>Integer</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>2</IntervalValue>
            <FontFaceCode>2</FontFaceCode>
        </Parameter>
        <Parameter>
            <Name>Double</Name>
            <Text>Double</Text>
            <Value>47.11</Value>
            <ValueType>Double</ValueType>
            <MinValue>-Integer</MinValue>
            <MaxValue>2 * Integer</MaxValue>
            <FontFaceCode>4</FontFaceCode>
            <BackgroundColor>(0, 0, 255) if Double &lt; 50 else (-1, -1, -1)</BackgroundColor>
        </Parameter>
        <Parameter>
            <Name>DoubleSlider</Name>
            <Text>Double slider</Text>
            <Value>5</Value>
            <MinValue>1</MinValue>
            <MaxValue>10</MaxValue>
            <ValueType>Double</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>IntegerSlider</IntervalValue>
        </Parameter>
        <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>4711</Value>
            <ValueType>Length</ValueType>
            <MinValue>-Double * 1000 if Double &lt; 1000 else -Double</MinValue>
            <MaxValue>
if Double &lt; 1000:
    return 2 * Double * 1000
else:
    return 2 * Double
            </MaxValue>
            <BackgroundColor>
if Double &lt; 1000:
    return (0, 255, 0)

return (0, 0, 255)
            </BackgroundColor>
        </Parameter>
        <Parameter>
            <Name>LengthSlider</Name>
            <Text>Length slider</Text>
            <Value>5000</Value>
            <MinValue>1000</MinValue>
            <MaxValue>10000</MaxValue>
            <ValueType>Length</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>250</IntervalValue>
        </Parameter>
        <Parameter>
            <Name>Area</Name>
            <Text>Area</Text>
            <Value>133161126</Value>
            <ValueType>Area</ValueType>
            <Enable>False</Enable>
        </Parameter>
        <Parameter>
            <Name>AreaSlider</Name>
            <Text>Area slider</Text>
            <Value>50000000</Value>
            <MinValue>1000000</MinValue>
            <MaxValue>100000000</MaxValue>
            <ValueType>Area</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>1000000</IntervalValue>
        </Parameter>
        <Parameter>
            <Name>Volume</Name>
            <Text>Volume</Text>
            <Value>104553677431</Value>
            <ValueType>Volume</ValueType>
            <Enable>False</Enable>
        </Parameter>
        <Parameter>
            <Name>VolumeSlider</Name>
            <Text>Volume slider</Text>
            <Value>5000000000</Value>
            <MinValue>1000000000</MinValue>
            <MaxValue>10000000000</MaxValue>
            <ValueType>Volume</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>1000000000</IntervalValue>
        </Parameter>
        <Parameter>
            <Name>Angle</Name>
            <Text>Angle</Text>
            <Value>45</Value>
            <ValueType>Angle</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>180</MaxValue>
        </Parameter>
        <Parameter>
            <Name>AngleSlider</Name>
            <Text>Angle slider</Text>
            <Value>45</Value>
            <MinValue>0</MinValue>
            <MaxValue>90</MaxValue>
            <ValueType>Angle</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>5</IntervalValue>
        </Parameter>
        <Parameter>
            <Name>Weight</Name>
            <Text>Weight</Text>
            <Value>100</Value>
            <ValueType>Weight</ValueType>
        </Parameter>
        <Parameter>
            <Name>WeightSlider</Name>
            <Text>Weight slider</Text>
            <Value>75</Value>
            <MinValue>0</MinValue>
            <MaxValue>100</MaxValue>
            <ValueType>Weight</ValueType>
            <ValueSlider>True</ValueSlider>
            <IntervalValue>1</IntervalValue>
        </Parameter>
        <Parameter>
            <Name>String</Name>
            <Text>String</Text>
            <Value>4, 7, 1, 1</Value>
            <ValueType>String</ValueType>
            <BackgroundColor>(0, 128, 128)</BackgroundColor>
        </Parameter>
        <Parameter>
            <Name>Date</Name>
            <Text>Date</Text>
            <Value>date(2023,10,16)</Value>
            <ValueType>Date</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>IntegerWithValueList</Name>
            <Text>Integer (1, 4, 8, 9)</Text>
            <Value>4</Value>
            <ValueList>1|4|8|9</ValueList>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>RangeEnd</Name>
            <Text>Integer range end</Text>
            <Value>100</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>IntegerWithValueRange</Name>
            <Text>Integer (0, 5, 10, ... RangeEnd)</Text>
            <Value>60</Value>
            <ValueList>[value for value in range(0, RangeEnd + 1 , 5)]</ValueList>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>DoubleWithValueList</Name>
            <Text>Double (1, 1.4, 1.8, 2)</Text>
            <Value>1.4</Value>
            <ValueList>1|1.4|1.8|2</ValueList>
            <ValueType>Double</ValueType>
        </Parameter>
        <Parameter>
            <Name>LengthWithValueRange</Name>
            <Text>Length (0, 1, ... 10)</Text>
            <Value>1000</Value>
            <ValueList>[value for value in range(0, 10001)]</ValueList>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>StringWithValueList</Name>
            <Text>String (a, d, x, z)</Text>
            <Value>d</Value>
            <ValueList>a|d|x|z</ValueList>
            <ValueType>String</ValueType>
        </Parameter>
    </Page>

    <Page>
        <Name>ComboBoxControls</Name>
        <Text>ComboBox</Text>
        <Parameter>
            <Name>IntegerComboBox</Name>
            <Text>IntegerComboBox</Text>
            <Value>1</Value>
            <ValueList>1|2|3|4|</ValueList>
            <ValueType>IntegerComboBox</ValueType>
            <BackgroundColor>(128, 0, 0)</BackgroundColor>
        </Parameter>
        <Parameter>
            <Name>AreaComboBox</Name>
            <Text>DoubleComboBox</Text>
            <Value>1.0</Value>
            <ValueList>1.0|2.0|3.0|4.0</ValueList>
            <ValueType>DoubleComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>StringComboBox</Name>
            <Text>StringComboBox</Text>
            <Value>Text1</Value>
            <ValueList>Text1|Text2|Text3</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>LengthCombobox</Name>
            <Text>LengthCombobox</Text>
            <Value>1000</Value>
            <ValueList>1000|2000|3000|4000</ValueList>
            <ValueType>LengthComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>AngleCombobox</Name>
            <Text>AngleCombobox</Text>
            <Value>45</Value>
            <ValueList>0|45|90|180</ValueList>
            <ValueType>AngleComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>PictureComboBox</Name>
            <Text>PictureComboBox</Text>
            <Value>0</Value>
            <ValueList>0|1|2</ValueList>
            <ValueTextList>Value=0|Value=1|Value=2</ValueTextList>
            <ValueList2>param01.png|param02.png|param03.png</ValueList2>
            <ValueType>PictureComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>PictureResourceComboBox</Name>
            <Text>PictureResourceComboBox</Text>
            <Value>0</Value>
            <ValueList>0|1|2|3</ValueList>
            <ValueTextList>Value=0|Value=1|Value=2|Value=3</ValueTextList>
            <ValueList2>16433|16441|16449|14563</ValueList2>
            <ValueType>PictureResourceComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>SeparatorComboBox</Name>
            <ValueType>Separator</ValueType>
        </Parameter>
        <Parameter>
            <Name>IntegerComboBoxRange</Name>
            <Text>IntegerComboBox (1, 3, ... 21)</Text>
            <Value>11</Value>
            <ValueList>[value for value in range(1, 22, 2)]</ValueList>
            <ValueType>IntegerComboBox</ValueType>
        </Parameter>
    </Page>


    <Page>
        <Name>SelectionControls</Name>
        <Text>Selection</Text>

        <Parameter>
            <Name>CheckBox</Name>
            <Text>CheckBox</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>RadioGroup</Name>
            <Text>RadioGroup</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>RadioButton1</Name>
                <Text>RadioButton1</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>RadioButton2</Name>
                <Text>RadioButton2</Text>
                <Value>2</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>RadioButton3</Name>
                <Text>RadioButton3</Text>
                <Value>3</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>ButtonControls</Name>
        <Text>Button</Text>

        <Parameter>
            <Name>ButtonRow</Name>
            <Text>Button</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Button</Name>
                <Text>Button text</Text>
                <EventId>1000</EventId>
                <ValueType>Button</ValueType>
                <FontStyle>1</FontStyle>
                <FontFaceCode>1</FontFaceCode>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>WebLinkButtonRow</Name>
            <Text>Web link</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>WebLinkButton</Name>
                <Text>Allplan</Text>
                <EventId>2000</EventId>
                <Value>https://www.allplan.com</Value>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PictureButtonRow</Name>
            <Text>PictureButton</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>PictureButton</Name>
                <Text>PictureButton tooltip</Text>
                <Value>ButtonImageReset16.png</Value>
                <EventId>1001</EventId>
                <ValueType>PictureButton</ValueType>
                <HeightInRow>40</HeightInRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PictureResourceButtonRow</Name>
            <Text>PictureResourceButton</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>PictureResourceButton</Name>
                <Text>PictureResourceButton tooltip</Text>
                <Value>17027</Value>
                <EventId>1002</EventId>
                <ValueType>PictureResourceButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PictureButtonList</Name>
            <Text>PictureButtonList</Text>
            <Value>0</Value>
            <ValueList>0|1|2</ValueList>
            <ValueTextList>Length=1|Length=2|Length=3</ValueTextList>
            <ValueList2>param01.png|param02.png|param03.png</ValueList2>
            <ValueType>PictureButtonList</ValueType>
        </Parameter>

        <Parameter>
            <Name>PictureResourceButtonList</Name>
            <Text>PictureResourceButtonList</Text>
            <Value>0</Value>
            <ValueList>0|1|2|3</ValueList>
            <ValueTextList>Width=1|Width=2|Width=3|Width=4</ValueTextList>
            <ValueList2>16433|16441|16449|14563</ValueList2>
            <ValueType>PictureResourceButtonList</ValueType>
            <HeightInRow>50</HeightInRow>
        </Parameter>

        <Parameter>
            <Name>MaterialButton</Name>
            <Text>MaterialButton</Text>
            <Value>Glas</Value>
            <DisableButtonIsShown>True</DisableButtonIsShown>
            <ValueType>MaterialButton</ValueType>
        </Parameter>

        <Parameter>
            <Name>RefPointButtonRow</Name>
            <Text>RefPointButton</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>RefPointId</Name>
                <Text>Reference point index</Text>
                <Value>AllplanPalette.RefPointPosition.eCenterCenter</Value>
                <ValueType>RefPointButton</ValueType>
                <EnumList2>AllplanPalette.RefPointButtonType.eAllNinePositions</EnumList2>
            </Parameter>
            <Parameter>
                <Name>CenterOfGravity</Name>
                <Text>Center of gravity</Text>
                <Value>19407</Value>
                <EventId>1003</EventId>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>RefPointId != 0</Visible>
            </Parameter>
            <Parameter>
                <Name>CenterOfGravitySelected</Name>
                <Text>Center of gravity selected</Text>
                <Value>19405</Value>
                <EventId>1004</EventId>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>RefPointId == 0</Visible>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>ButtonDialogs</Name>
        <Text>Dialogs</Text>

        <Parameter>
            <Name>SymbolName</Name>
            <Text>Symbol</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>SymbolDialog</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>TradeID</Name>
            <Text>Trade</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>Trade</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>AttributeID</Name>
            <Text>All attributes ID</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>InsertAttributeID</Name>
            <Text>Insert attribute ID</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>ProjectAttributeID</Name>
            <Text>Project attribute ID</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>AttributeSelectionProject</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>AttributeIdValue</Name>
            <Text>All attribute</Text>
            <Value></Value>
            <ValueType>AttributeIdValue</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>InsertAttributeIdValue</Name>
            <Text>Insert attribute</Text>
            <Value></Value>
            <ValueType>AttributeIdValue</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>ProjectAttributeIdValue</Name>
            <Text>Project attribute</Text>
            <Value></Value>
            <ValueType>AttributeIdValue</ValueType>
            <ValueDialog>AttributeSelectionProject</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>AttributeName</Name>
            <Text>All attribute name</Text>
            <Value></Value>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>InsertAttributeName</Name>
            <Text>Insert attribute name</Text>
            <Value></Value>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>ProjectAttributeIdName</Name>
            <Text>Project attribute name</Text>
            <Value></Value>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelectionProject</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>ColorID</Name>
            <Text>RGB-Color</Text>
            <Value>255</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>RGBColorDialog</ValueDialog>
         </Parameter>

        <Parameter>
            <Name>BitmapName</Name>
            <Text>Bitmap</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>BitmapResourceDialog</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>BottomPlane</Name>
            <Text>Bottom plane</Text>
            <Value></Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>BottomPlaneReferences</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>TopPlane</Name>
            <Text>Top plane</Text>
            <Value></Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>TopPlaneReferences</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>PlaneReferences</Name>
            <Text>Planes</Text>
            <Value></Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>OpenFile</Name>
            <Text>Open file</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
            <FileFilter>pypsub-files(*.pypsub)|*.pypsub|py-files(*.py)|*.py|</FileFilter>
            <FileExtension>pypsub</FileExtension>
            <DefaultDirectories>etc|STD</DefaultDirectories>
        </Parameter>

        <Parameter>
            <Name>SaveFile</Name>
            <Text>Save file</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>SaveFileDialog</ValueDialog>
            <FileFilter>pypsub-files(*.pypsub)|*.pypsub|py-files(*.py)|*.py|</FileFilter>
            <FileExtension>pypsub</FileExtension>
            <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
        </Parameter>

        <Parameter>
            <Name>OpenFavoriteFile</Name>
            <Text>Open favorite file</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFavoriteFileDialog</ValueDialog>
            <FileFilter>pyv-files(pyv-files(*.pyv)|*.pyv|</FileFilter>
            <FileExtension>pyv</FileExtension>
        </Parameter>

        <Parameter>
            <Name>SaveFavoriteFile</Name>
            <Text>Save favorite file</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>SaveFavoriteFileDialog</ValueDialog>
            <FileFilter>pyv-files(pyv-files(*.pyv)|*.pyv|</FileFilter>
            <FileExtension>pyv</FileExtension>
        </Parameter>

        <Parameter>
            <Name>DateWithDialog</Name>
            <Text>Date</Text>
            <Value>date(2023,10,16)</Value>
            <ValueType>Date</ValueType>
            <ValueDialog>DateDialog</ValueDialog>
        </Parameter>
    </Page>

    <Page>
        <Name>ResourceComboBoxControls</Name>
        <Text>Resoure ComboBox</Text>
        <Parameter>
            <Name>Pen</Name>
            <Text>Pen</Text>
            <Value>-1</Value>
            <ValueType>Pen</ValueType>
        </Parameter>
        <Parameter>
            <Name>Stroke</Name>
            <Text>Stroke</Text>
            <Value>-1</Value>
            <ValueType>Stroke</ValueType>
        </Parameter>
        <Parameter>
            <Name>Color</Name>
            <Text>Color</Text>
            <Value>-1</Value>
            <ValueType>Color</ValueType>
        </Parameter>
        <Parameter>
            <Name>Layer</Name>
            <Text>Layer</Text>
            <Value>-1</Value>
            <ValueType>Layer</ValueType>
        </Parameter>
        <Parameter>
            <Name>Hatching</Name>
            <Text>Hatching</Text>
            <Value>-1</Value>
            <ValueType>Hatch</ValueType>
        </Parameter>
        <Parameter>
            <Name>Pattern</Name>
            <Text>Pattern</Text>
            <Value>-1</Value>
            <ValueType>Pattern</ValueType>
        </Parameter>
        <Parameter>
            <Name>FaceStyle</Name>
            <Text>FaceStyle</Text>
            <Value>-1</Value>
            <ValueType>FaceStyle</ValueType>
        </Parameter>
        <Parameter>
            <Name>CommonPropertiesSeparator</Name>
            <ValueType>Separator</ValueType>
        </Parameter>
        <Parameter>
            <Name>CommonProp</Name>
            <Text>Cube</Text>
            <Value></Value>
            <ValueType>CommonProperties</ValueType>
        </Parameter>

        <Parameter>
            <Name>FontSep</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>FontId</Name>
            <Text>Font ID</Text>
            <Value>21</Value>
            <ValueType>Font</ValueType>
        </Parameter>
        <Parameter>
            <Name>FontEmphasis</Name>
            <Text>Emphasis</Text>
            <Value>0</Value>
            <ValueType>FontEmphasis</ValueType>
            <Constraint>FontId</Constraint>
        </Parameter>
        <Parameter>
            <Name>FontAngle</Name>
            <Text>Angle for italic text</Text>
            <Value>90</Value>
            <ValueType>Angle</ValueType>
            <Constraint>FontId;FontEmphasis</Constraint>
        </Parameter>
    </Page>

    <Page>
        <Name>LayoutControls</Name>
        <Text>Layout controls</Text>

        <Parameter>
            <Name>Expander</Name>
            <Text>Expander</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Picture</Name>
                <Value>Layout\PictureForPalette.png</Value>
                <Orientation>Right</Orientation>
                <ValueType>Picture</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>Row1</Name>
                <Text>Text labels</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>FirstText</Name>
                    <Text></Text>
                    <Value></Value>
                    <ValueTextId>1002</ValueTextId>
                    <ValueType>Text</ValueType>
                    <FontStyle>1</FontStyle>
                    <FontFaceCode>1</FontFaceCode>
                </Parameter>

                <Parameter>
                    <Name>SecondText</Name>
                    <Text></Text>
                    <Value>Y</Value>
                    <ValueType>Text</ValueType>
                    <FontStyle>2</FontStyle>
                    <FontFaceCode>2</FontFaceCode>
                </Parameter>

                <Parameter>
                    <Name>ThirdText</Name>
                    <Text></Text>
                    <Value>Z</Value>
                    <ValueType>Text</ValueType>
                    <FontStyle>2</FontStyle>
                    <FontFaceCode>4</FontFaceCode>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row</Name>
                <Text>Coordinates</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>XCoord</Name>
                    <Text> </Text>
                    <Value>1000</Value>
                    <ValueType>Double</ValueType>
                    <WidthInRow>40</WidthInRow>
                </Parameter>
                <Parameter>
                    <Name>YCoord</Name>
                    <Text> </Text>
                    <Value>2000</Value>
                    <ValueType>Double</ValueType>
                    <WidthInRow>80</WidthInRow>
                </Parameter>
                <Parameter>
                    <Name>ZCoord</Name>
                    <Text> </Text>
                    <Value>3000</Value>
                    <ValueType>Double</ValueType>
                    <WidthInRow>120</WidthInRow>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>ReinforcementControls</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>ReinfSteelGrade</Name>
            <Text>ReinfSteelGrade</Text>
            <Value>-1</Value>
            <ValueType>ReinfSteelGrade</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReinfConcreteGrade</Name>
            <Text>ReinfConcreteGrade</Text>
            <Value>-1</Value>
            <ValueType>ReinfConcreteGrade</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReinfBarDiameter</Name>
            <Text>ReinfBarDiameter</Text>
            <Value>-1</Value>
            <ValueType>ReinfBarDiameter</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReinfConcreteCover</Name>
            <Text>ReinfConcreteCover</Text>
            <Value>25</Value>
            <ValueType>ReinfConcreteCover</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReinfBendingRoller</Name>
            <Text>ReinfBendingRoller</Text>
            <Value>-1</Value>
            <ValueType>ReinfBendingRoller</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReinfMeshGroup</Name>
            <Text>ReinfMeshGroup</Text>
            <Value>-1</Value>
            <ValueType>ReinfMeshGroup</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReinfMeshType</Name>
            <Text>ReinfMeshType</Text>
            <Value>-1</Value>
            <ValueType>ReinfMeshType</ValueType>
        </Parameter>

        <Parameter>
            <Name>ReinfPosition</Name>
            <Text>ReinfPosition</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <ReinfID>1</ReinfID>
                <Picture>OpenStirrup_NoHooks.png</Picture>
                <Diameter>10</Diameter>
                <MeshType>-1</MeshType>
                <SideLengthStart>1000</SideLengthStart>
                <SideLengthEnd>500</SideLengthEnd>
                <Distance>150.</Distance>
                <ValueType>ReinfPosition</ValueType>
                <Select>1</Select>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ReinforcementShapeBarProperties</Name>
            <Text>ReinforcementShapeBarProperties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BarProperties</Name>
                <Text>Bar shape properties</Text>
                <Value>ReinforcementShapeProperties(ConcreteGrade(-1),SteelGrade(-1),Diameter(25.0),BendingRoller(4.0))</Value>
                <ValueType>ReinforcementShapeBarProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ReinforcementShapeMeshProperties</Name>
            <Text>ReinforcementShapeMeshProperties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MeshProperties</Name>
                <Text>Mesh shape properties</Text>
                <Value>ReinforcementShapeProperties(ConcreteGrade(-1),MeshType(-1),MeshBendingDirection(LongitudinalBars),BendingRoller(4.0))</Value>
                <ValueType>ReinforcementShapeMeshProperties</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>FromOtherPages</Name>
        <Text>Multiple appearence</Text>

        <Parameter>
            <Name>Integer</Name>
            <Text>Integer from "Edit"</Text>
            <Value>4711</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>LengthCombobox</Name>
            <Text>LengthCombobox from "ComboBox"</Text>
            <Value>1000</Value>
            <ValueList>1000|2000|3000|4000</ValueList>
            <ValueType>LengthComboBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>CheckBox</Name>
            <Text>CheckBox from "Selection"</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>ButtonRowMulti</Name>
            <Text>Button from "Button"</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Button</Name>
                <Text>Button text from "Button"</Text>
                <EventId>1000</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Pen</Name>
            <Text>Pen from "Resoure ComboBox"</Text>
            <Value>-1</Value>
            <ValueType>Pen</ValueType>
        </Parameter>
    </Page>
</Element>
