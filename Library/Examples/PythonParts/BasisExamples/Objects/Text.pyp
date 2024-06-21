<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\Objects\Text.py</Name>
        <Title>Text</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

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
                <Name>Text</Name>
                <Text>Text</Text>
                <Value>This is the first text line
and this is the second one</Value>
                <ValueType>String</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\TextProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>
    </Page>
</Element>
