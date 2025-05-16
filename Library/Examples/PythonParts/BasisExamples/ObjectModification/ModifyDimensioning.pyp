<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\ObjectModification\ModifyDimensioning.py</Name>
        <Title>Dimensioning</Title>
        <Version>1.0</Version>
    </Script>
    <Constants>
        <Constant>
            <Name>DIMENSIONING_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>DIMENSIONING_MODIFY</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Dimensioning</Text>
        <Visible>InputMode == DIMENSIONING_MODIFY</Visible>
        <Parameter>
            <Name>ColorDimLine</Name>
            <Text>Color dimension line</Text>
            <Value>1</Value>
            <ValueType>Color</ValueType>
        </Parameter>
        <Parameter>
            <Name>ShowDimLine</Name>
            <Text>Show Dimension Line</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>SizeDimText</Name>
            <Text>Size dimension number</Text>
            <Value>1</Value>
            <ValueType>Double</ValueType>
        </Parameter>
        <Parameter>
            <Name>SizeArrowHead</Name>
            <Text>Size arrow head</Text>
            <Value>1</Value>
            <ValueType>Double</ValueType>
        </Parameter>
        <Parameter>
            <Name>TextOffset</Name>
            <Text>Text Offset</Text>
            <Value>1</Value>
            <ValueType>Double</ValueType>
        </Parameter>
        <Parameter>
            <Name>FirstElementIsUnderlined</Name>
            <Text>First element is underlined</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
