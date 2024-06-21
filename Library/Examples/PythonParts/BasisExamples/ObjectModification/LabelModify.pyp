<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\ObjectModification\LabelModify.py</Name>
        <Title>Label</Title>
        <Version>1.0</Version>
    </Script>
    <Constants>
        <Constant>
            <Name>LABEL_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>LABEL_MODIFY</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>

    <Page>
        <Name>Label</Name>
        <Text>Label</Text>
        <Visible>InputMode == LABEL_MODIFY</Visible>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>|CommonProp.Stroke:False|CommonProp.StrokeByLayer:False</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TextExp</Name>
            <Text>Text</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Texts</Name>
                <Text></Text>
                <Value>[]</Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\TextProperties.incl</Value>
            <ValueType>Include</ValueType>
            <Visible>Alignment:False</Visible>
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
