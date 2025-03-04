<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\AttributeControls\AttributeIdValue.py</Name>
        <Title>AttributeIdValue</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

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
            <Name>GeometryExp</Name>
            <Text>PythonPart with attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Sizes</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(5000,500,1000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SingleIdValueExp</Name>
            <Text>Attribute</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Attribute</Name>
                <Text>Attribute</Text>
                <Value>0</Value>
                <ValueType>AttributeIdValue</ValueType>
                <ValueDialog>AttributeSelectionInsert</ValueDialog>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ListIdValueExp</Name>
            <Text>Attribute list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AttributeList</Name>
                <Text>Attributes</Text>
                <Value>[(0,)]</Value>
                <ValueType>AttributeIdValue</ValueType>
                <ValueDialog>AttributeSelectionInsert</ValueDialog>
            </Parameter>
        </Parameter>
        
    </Page>
</Element>
