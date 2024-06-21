<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\BooleanOperations\UnitePolyhedrons.py</Name>
        <Title>UnitePolyhedrons</Title>
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
            <Name>Polyhedron</Name>
            <Text>Polyhedron</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyhedron</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(3000, 4000, 5000)</Value>
                <ValueType>Vector3D</ValueType>

            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Copy</Name>
            <Text>Copies</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Distance</Name>
                <Text>Distance</Text>
                <Value>Vector3D(2000, 2000, 0)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
            <Parameter>
                <Name>Count</Name>
                <Text>Count</Text>
                <Value>5</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>