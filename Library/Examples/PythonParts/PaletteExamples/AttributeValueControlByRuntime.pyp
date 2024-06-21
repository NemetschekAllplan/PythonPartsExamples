<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\AttributeValueControlByRuntime.py</Name>
        <Title>Change and modify controls during the runtime</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Attribute input</Name>
        <Parameter>
            <Name>AttributeExpander</Name>
            <Text>Attribute value</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Row</Name>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>AttributeID</Name>
                    <Text>Attribute ID</Text>
                    <Value>508</Value>
                    <ValueDialog>AttributeSelection</ValueDialog>
                    <ValueType>Integer</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>AttributeValue</Name>
                <Text>Attribute value</Text>
                <Value></Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>508</AttributeId>
            </Parameter>
        </Parameter>
    </Page>
</Element>