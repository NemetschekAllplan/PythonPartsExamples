<?xml version="1.0" encoding="utf-8"?>
<Element>
    <LanguageFile>AllControls</LanguageFile>
    <Script>
        <Name>ObjectAccessExamples\GetObjectByAttributeValue.py</Name>
        <Title>GetObjectByAttributeValue</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Input</Name>
        <Text>Input</Text>

        <Parameter>
            <Name>AttributeID</Name>
            <Text>Attribute</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
        </Parameter>

        <Parameter>
            <Name>AttributeValue</Name>
            <Text>Attribute value</Text>
            <Value></Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>508</AttributeId>
            <Visible>AttributeID</Visible>
        </Parameter>
    </Page>
</Element>
