<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>Grasshopper\GrasshopperConnection.py</Name>
        <Title>GrasshopperConnection</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text></Text>
        <Parameter>
            <Name>Text1</Name>
            <Text>Python Host is started</Text>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>Text2</Name>
            <Text>Press ESC to stop</Text>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>HidePlaneReference</Name>
            <Text>Hide Plane Reference</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Visible>False</Visible>
        </Parameter>
        <Parameter>
            <Name>PlaneReferences</Name>
            <Text>Height connection</Text>
            <TextId>1063</TextId>
            <Value>None</Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
        </Parameter>
        <Parameter>
            <Name>Bake All Row</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>bake_all</Name>
                <Text>Bake all</Text>
                <EventId>1003</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
