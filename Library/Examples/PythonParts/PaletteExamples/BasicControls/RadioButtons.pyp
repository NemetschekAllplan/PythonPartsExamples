<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\RadioButtons.py</Name>
        <Title>RadioButtons</Title>
        <Version>1.0</Version>
    </Script>
    <Constants>
        <Constant>
            <Name>RED</Name>
            <Value>6</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>GREEN</Name>
            <Value>4</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>BLUE</Name>
            <Value>7</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>RadioButtonTest</Text>

        <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>RadioButtonExp</Name>
            <Text>Radio button</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RadioGroup</Name>
                <Text>Color of body</Text>
                <!-- selected value -->
                <Value>GREEN</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButton1</Name>
                    <Text>red</Text>
                    <Value>RED</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton2</Name>
                    <Text>green</Text>
                    <Value>GREEN</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton3</Name>
                    <Text>blue</Text>
                    <Value>BLUE</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RadioButtonRowExp</Name>
            <Text>Radio button in row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LengthRadioGroup</Name>
                <Text></Text>
                <!-- selected value -->
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>Row1</Name>
                    <Text>Distance from left</Text>
                    <ValueType>Row</ValueType>

                    <Parameter>
                        <Name>RadioButton4</Name>
                        <Text></Text>
                        <Value>0</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>DistanceLeft</Name>
                        <Text>Distance</Text>
                        <Value>1000.</Value>
                        <ValueType>Length</ValueType>
                        <Enable>LengthRadioGroup == 0</Enable>
                    </Parameter>
                </Parameter>

                <Parameter>
                    <Name>Row2</Name>
                    <Text>Distance from right</Text>
                    <ValueType>Row</ValueType>

                    <Parameter>
                        <Name>RadioButton5</Name>
                        <Text></Text>
                        <Value>1</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>DistanceRight</Name>
                        <Text>Distance</Text>
                        <Value>1000.</Value>
                        <ValueType>Length</ValueType>
                        <Enable>LengthRadioGroup == 1</Enable>
                    </Parameter>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>MultipleValueExp</Name>
            <Text>Multiple value types</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MultiRadioGroup</Name>
                <Text>Value types</Text>
                <Value>68.4</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButton11</Name>
                    <Text>5</Text>
                    <Value>5</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton12</Name>
                    <Text>68.4</Text>
                    <Value>68.4</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton13</Name>
                    <Text>blue</Text>
                    <Value>blue</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>MultipleValueRowExp</Name>
            <Text>Multiple value types in overall row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MultiRadioGroupRowRow</Name>
                <Text></Text>
                <Value>OVERALL</Value>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RowText</Name>
                    <Text></Text>
                    <Value>Value types</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>MultiRadioGroupRow</Name>
                    <Text></Text>
                    <Value>12.4</Value>
                    <ValueType>RadioButtonGroup</ValueType>

                    <Parameter>
                        <Name>RadioButtonRow11</Name>
                        <Text>7</Text>
                        <Value>7</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioButtonRow12</Name>
                        <Text>12.4</Text>
                        <Value>12.4</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioButtonRow13</Name>
                        <Text>green</Text>
                        <Value>green</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>NameTupleRadioButton</Name>
            <Text>From namedtuple list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ImportInto</Name>
                <Text> </Text>
                <Value>Import in drawing file</Value>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>ImportFileNumber</Name>
                <Text>Import file</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>ImportFileSelection</Name>
                    <Text>Import</Text>
                    <Value>[_]</Value>
                    <ValueType>namedtuple(DisplayText,RadioButton)</ValueType>
                    <NamedTuple>
                        <TypeName>ImportFileSelection</TypeName>
                        <FieldNames>RowText,FileSelection</FieldNames>
                    </NamedTuple>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Page2</Name>
        <Text>One dimensional list</Text>

        <Parameter>
            <Name>OneDimList</Name>
            <Text>One dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ColorCount</Name>
                <Text>Color count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>RadioGroupColorList</Name>
                <Text>Colors</Text>
                <TextDyn>"Color " + str($list_row + 1)</TextDyn>
                <Value>[RED,GREEN,BLUE]</Value>
                <Dimensions>ColorCount</Dimensions>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioGroupColorList1</Name>
                    <Text>red</Text>
                    <Value>RED</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioGroupColorList2</Name>
                    <Text>green</Text>
                    <Value>GREEN</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioGroupColorList3</Name>
                    <Text>blue</Text>
                    <Value>BLUE</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>OneDimRowList</Name>
            <Text>One dimensional list in rows</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>HeaderRow</Name>
                <Text>Colors</Text>
                <Value>OVERALL</Value>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>Colors</Name>
                    <Text></Text>
                    <Value>Colors</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Red</Name>
                    <Text></Text>
                    <Value>Red</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Green</Name>
                    <Text></Text>
                    <Value>Green</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Blue</Name>
                    <Text></Text>
                    <Value>Blue</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>RadioGroupRowColorList</Name>
                <Text></Text>
                <Value>[RED,GREEN,BLUE]</Value>
                <Dimensions>ColorCount</Dimensions>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>ColorRow</Name>
                    <TextDyn>"Color " + str($list_row + 1)</TextDyn>
                    <Text></Text>
                    <Value>OVERALL</Value>
                    <ValueType>Row</ValueType>

                    <Parameter>
                        <Name>RadioGroupRowColorList1</Name>
                        <Text></Text>
                        <Value>RED</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioGroupRowColorList2</Name>
                        <Text></Text>
                        <Value>GREEN</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioGroupRowColorList3</Name>
                        <Text></Text>
                        <Value>BLUE</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Page3</Name>
        <Text>Two dimensional list</Text>

        <Parameter>
            <Name>TwoDimList</Name>
            <Text>Two dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ColorCount2Dim</Name>
                <Text>Color count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>ColumnCount</Name>
                <Text>Column count</Text>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>RadioGroupColorList2Dim</Name>
                <Text>Colors</Text>
                <TextDyn>"Color " + str($list_row + 1) + "/" + str($list_col + 1)</TextDyn>
                <Value>[[RED,RED],[GREEN,GREEN],[BLUE,BLUE]]</Value>
                <Dimensions>ColorCount2Dim,ColumnCount</Dimensions>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioGroupColorList2Dim1</Name>
                    <Text>red</Text>
                    <Value>RED</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioGroupColorList2Dim2</Name>
                    <Text>green</Text>
                    <Value>GREEN</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioGroupColorList2Dim3</Name>
                    <Text>blue</Text>
                    <Value>BLUE</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TwoDimRowList</Name>
            <Text>Two dimensional list in rows</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RadioGroupRowColorList2Dim</Name>
                <Text>Colors</Text>
                <Value>[[RED,RED],[GREEN,GREEN],[BLUE,BLUE]]</Value>
                <Dimensions>ColorCount2Dim,ColumnCount</Dimensions>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>ColorRow2Dim</Name>
                    <Text></Text>
                    <TextDyn>"Color " + str($list_row + 1) + "/" + str($list_col + 1)</TextDyn>
                    <Value>OVERALL</Value>
                    <ValueType>Row</ValueType>

                    <Parameter>
                        <Name>RadioGroupRowColorList2Dim1</Name>
                        <Text>red</Text>
                        <Value>RED</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioGroupRowColorList2Dim2</Name>
                        <Text>green</Text>
                        <Value>GREEN</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioGroupRowColorList2Dim3</Name>
                        <Text>blue</Text>
                        <Value>BLUE</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
