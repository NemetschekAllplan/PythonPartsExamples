<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\ComboBoxControls.py</Name>
        <Title>ComboBoxControls</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>VALUE_0</Name>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>VALUE_1</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>VALUE_2</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Single controls</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ComboBoxControlsExp</Name>
            <Text>Combo box controls</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Angle</Name>
                <Text>Angle</Text>
                <Value>45</Value>
                <ValueList>15|30|45|60|75|90</ValueList>
                <ValueType>AngleComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Double</Name>
                <Text>Double</Text>
                <Value>700</Value>
                <ValueList>500|600|700|800|900</ValueList>
                <ValueType>DoubleComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Integer</Name>
                <Text>Integer</Text>
                <Value>3</Value>
                <ValueList>1|2|3|4|5</ValueList>
                <ValueType>IntegerComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>1200</Value>
                <ValueList>1000|1100|1200|1500</ValueList>
                <ValueType>LengthComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>String</Name>
                <Text>String</Text>
                <Value>Munich</Value>
                <ValueList>London|Munich|Paris</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>LocalizedString</Name>
                <Text>Localized string</Text>
                <Value>Munich {1002}</Value>
                <ValueList>London|Munich|Paris</ValueList>
                <ValueList_TextIds>1001|1002|1003</ValueList_TextIds>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>EditComboBoxControlsExp</Name>
            <Text>Editable combo box controls</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>EditAngle</Name>
                <Text>Angle</Text>
                <Value>45</Value>
                <ValueList>15|30|45|60|75|90</ValueList>
                <ValueType>AngleComboBox</ValueType>
                <ValueListFile>usr\tmp\PypComboSettings\Angle.val</ValueListFile>
            </Parameter>
            <Parameter>
                <Name>EditDouble</Name>
                <Text>Double</Text>
                <Value>700</Value>
                <ValueList>500|600|700|800|900</ValueList>
                <ValueType>DoubleComboBox</ValueType>
                <ValueListFile>usr\tmp\PypComboSettings\Double.val</ValueListFile>
            </Parameter>
            <Parameter>
                <Name>EditInteger</Name>
                <Text>Integer</Text>
                <Value>3</Value>
                <ValueList>1|2|3|4|5</ValueList>
                <ValueType>IntegerComboBox</ValueType>
                <ValueListFile>usr\tmp\PypComboSettings\Integer.val</ValueListFile>
            </Parameter>
            <Parameter>
                <Name>EditLength</Name>
                <Text>Length</Text>
                <Value>1200</Value>
                <ValueList>1000|1100|1200|1500</ValueList>
                <ValueType>LengthComboBox</ValueType>
                <ValueListFile>usr\tmp\PypComboSettings\Length.val</ValueListFile>
            </Parameter>
            <Parameter>
                <Name>EditString</Name>
                <Text>String</Text>
                <Value>Munich</Value>
                <ValueList>London|Munich|Paris</ValueList>
                <ValueType>StringComboBox</ValueType>
                <ValueListFile>usr\tmp\PypComboSettings\String.val</ValueListFile>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Page2</Name>
        <Text>List controls</Text>

        <Parameter>
            <Name>OneDimList</Name>
            <Text>One dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LineCount</Name>
                <Text>Line count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>LineSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>LineLength</Name>
                <Text></Text>
                <TextDyn>"Line length " + str($list_row + 1)</TextDyn>
                <Value>[1100,2200,3300]</Value>
                <ValueType>LengthComboBox</ValueType>
                <ValueList>1100|2200|3300|4400|5500</ValueList>
                <Dimensions>LineCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TwoDimList</Name>
            <Text>Two dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LineCoords</Name>
                <Text></Text>
                <TextDyn>"X/Y " + str($list_row + 1)</TextDyn>
                <Value>[[1000,0],[3000,0],[5000,0]]</Value>
                <ValueType>LengthComboBox</ValueType>
                <ValueList>0|1000|2000|3000|4000|5000</ValueList>
                <Dimensions>LineCount,2</Dimensions>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Page3</Name>
        <Text>Dynamic</Text>
        <Parameter>
            <Name>DynamicValueList</Name>
            <Text>Dynamic value list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>WidthDimension</Name>
                <Text>Width dimensions</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>WidthSmall</Name>
                    <Text>Small</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>WidthMedium</Name>
                    <Text>Medium</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>WidthLarge</Name>
                    <Text>Large</Text>
                    <Value>3</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>700.</Value>
                <ValueList>"500.|600|700" if WidthDimension == 1 else "1000|1200|1400" if WidthDimension == 2 else "1500|1800|2100"</ValueList>
                <ValueType>LengthComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>HeightDimension</Name>
                <Text>Height dimensions</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>HeightSmall</Name>
                    <Text>Small</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>HeightMedium</Name>
                    <Text>Medium</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>HeightLarge</Name>
                    <Text>Large</Text>
                    <Value>3</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>500.</Value>
                <ValueList>
if HeightDimension == 1:
    return "700.|725|750|775"
elif HeightDimension == 2:
    return "800|825|850|875"
else:
    return "900|925|950|975"
                </ValueList>
                <ValueType>LengthComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ValueListFromEnum</Name>
            <Text>Value list from enumeration</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>IfcVersion</Name>
                <Text>IFC version</Text>
                <Value>Ifc_4</Value>
                <ValueList>"|".join(str(key) for key in AllplanBaseEle.IFC_Version.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>DrawingType</Name>
                <Text>Drawing type</Text>
                <Value></Value>
                <ValueList>"|".join(str(item) for item in AllplanBaseEle.DrawingTypeService.GetDrawingTypeDescriptions(__document))</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

        </Parameter>
    </Page>
</Element>
