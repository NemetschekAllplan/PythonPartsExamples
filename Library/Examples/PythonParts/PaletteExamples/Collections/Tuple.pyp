<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Collections\Tuple.py</Name>
        <Title>ValueList</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Text>Single tuple</Text>

        <Parameter>
            <Name>MultiRowTupleExp</Name>
            <Text>Tuple in multiple rows</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MultiRowTuple</Name>
                <Text>Length|Width|Height</Text>
                <Value>(1000,2000,3000)</Value>
                <ValueType>Tuple(Length,LengthComboBox,Length)</ValueType>
                <ValueList>,1000|2000|3000|4000|5000,</ValueList>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>OneRowTupleExp</Name>
            <Text>Tuple in one row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>OneRowTuplerRow</Name>
                <Text>Sizes</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>OneRowTuple</Name>
                    <Text></Text>
                    <Value>(1500,2000,3000)</Value>
                    <ValueType>Tuple(Length,LengthComboBox,Length)</ValueType>
                    <ValueList>,1000|2000|3000|4000|5000,</ValueList>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>FullRowTupleExp</Name>
            <Text>Tuple in one full row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>FullOneRowTuplerRow</Name>
                <Text>Sizes</Text>
                <ValueType>Row</ValueType>
                <Value>1</Value>

                <Parameter>
                    <Name>FullOneRowTuple</Name>
                    <Text></Text>
                    <Value>(2000,2000,3000)</Value>
                    <ValueType>Tuple(Length,LengthComboBox,Length)</ValueType>
                    <ValueList>,1000|2000|3000|4000|5000,</ValueList>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Text>Tuple list</Text>

        <Parameter>
            <Name>ListMultiRowTupleExp</Name>
            <Text>Tuple list in multiple rows</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ListMultiRowTuple</Name>
                <Text>Length|Width|Height</Text>
                <Value>[(1000,2000,3000),(1200,2000,3200),(1400,2000,3400)]</Value>
                <ValueType>Tuple(Length,LengthComboBox,Length,Separator)</ValueType>
                <ValueList>,1000|2000|3000|4000|5000,</ValueList>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ListOneRowTupleExp</Name>
            <Text>Tuple list in one row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ListOneRowTuple</Name>
                <Text></Text>
                <TextDyn>f"Sizes {$list_row + 1}"</TextDyn>
                <Value>[(1500,2000,3000),(1700,2000,3200),(1900,2000,3400)]</Value>
                <ValueType>Tuple(Length,LengthComboBox,Length)</ValueType>
                <ValueList>,1000|2000|3000|4000|5000,</ValueList>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ListFullRowTupleExp</Name>
            <Text>Tuple list in one full row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>TupleCount</Name>
                <Text>Tuple count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>LineSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>FullOneRowTuplerRow</Name>
                <Text></Text>
                <ValueType>Row</ValueType>
                <Value>1</Value>

                <Parameter>
                    <Name>ListFullOneRowTuple</Name>
                    <Text></Text>
                    <Value>[(Vector3D(1500,3000,3000),True),(Vector3D(1700,3000,3200),True),(Vector3D(1900,3000,3400),True)]</Value>
                    <ValueType>Tuple(Vector3D,CheckBox)</ValueType>
                    <Dimensions>TupleCount</Dimensions>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
