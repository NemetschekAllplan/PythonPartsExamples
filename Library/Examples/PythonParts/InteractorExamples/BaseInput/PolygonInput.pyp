<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>InteractorExamples\BaseInput\PolygonInput.py</Name>
        <Title>PolygonInput</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
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
            <Name>PolygonInputOptions</Name>
            <Text>Options of the polygon input</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>EnableZCoordinate</Name>
                <Text>Enable Z coordinates</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>AllowMultiPolygon</Name>
                <Text>Allow multiple polygons</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
