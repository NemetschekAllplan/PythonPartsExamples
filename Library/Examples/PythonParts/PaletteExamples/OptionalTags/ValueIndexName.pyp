<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\OptionalTags\ValueIndexName.py</Name>
        <Title>ValueIndexName</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
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
        <Text>General</Text>

        <Parameter>
            <Name>OneDimListExp</Name>
            <Text>One dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LengthRowCount</Name>
                <Text>Row count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>LengthList</Name>
                <Text>Length</Text>
                <Value>[1000,2000,3000]</Value>
                <ValueType>Length</ValueType>
                <Dimensions>LengthRowCount</Dimensions>
                <ValueIndexName>VisibleLengthRow</ValueIndexName>
                <ValueListStartRow>1</ValueListStartRow>
            </Parameter>

            <Parameter>
                <Name>OneDimSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>VisibleLengthRow</Name>
                <Text>Visible row (0=all)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <MinValue>-1</MinValue>
                <MaxValue>LengthRowCount</MaxValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TwoDimListExp</Name>
            <Text>Tow dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>IntRowCount</Name>
                <Text>Row count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>IntColumnCount</Name>
                <Text>Column count</Text>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>IntegerList</Name>
                <Text>Integer</Text>
                <Value>[[1,2],[11,12],[21,22]]</Value>
                <ValueType>Integer</ValueType>
                <ValueIndexName>VisibleIntRow,VisibleIntColumn</ValueIndexName>
                <ValueListStartRow>1</ValueListStartRow>
            </Parameter>

            <Parameter>
                <Name>TwoDimSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>VisibleIntRow</Name>
                <Text>Visible row (0=all)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <MinValue>-1</MinValue>
                <MaxValue>IntRowCount</MaxValue>
            </Parameter>

            <Parameter>
                <Name>VisibleIntColumn</Name>
                <Text>Visible column (0=all)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <MinValue>-1</MinValue>
                <MaxValue>IntColumnCount</MaxValue>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>RadioButton</Name>
        <Text>Radio button</Text>

        <Parameter>
            <Name>OneDimRowList</Name>
            <Text>One dimensional list in rows</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ColorCount</Name>
                <Text>Color count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

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
                <ValueIndexName>VisibleRadioRow</ValueIndexName>

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

            <Parameter>
                <Name>OneDimRadioSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>VisibleRadioRow</Name>
                <Text>Visible row (0=all)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <MinValue>-1</MinValue>
                <MaxValue>LengthRowCount</MaxValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TwoDimRowList</Name>
            <Text>Two dimensional list in rows</Text>
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
                <Name>RadioGroupRowColorList2Dim</Name>
                <Text>Colors</Text>
                <Value>[[RED,RED],[GREEN,GREEN],[BLUE,BLUE]]</Value>
                <Dimensions>ColorCount2Dim,ColumnCount</Dimensions>
                <ValueType>RadioButtonGroup</ValueType>
                <ValueIndexName>VisibleRadioRow2Dim,VisibleRadioColumn</ValueIndexName>

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

            <Parameter>
                <Name>TwoDimRadioSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>VisibleRadioRow2Dim</Name>
                <Text>Visible row (0=all)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <MinValue>-1</MinValue>
                <MaxValue>ColorCount2Dim</MaxValue>
            </Parameter>

            <Parameter>
                <Name>VisibleRadioColumn</Name>
                <Text>Visible column (0=all)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <MinValue>-1</MinValue>
                <MaxValue>ColumnCount</MaxValue>
            </Parameter>
        </Parameter>
    </Page>
</Element>
