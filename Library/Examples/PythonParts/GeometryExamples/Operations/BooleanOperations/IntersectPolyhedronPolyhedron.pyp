<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\BooleanOperations\IntersectPolyhedronPolyhedron.py</Name>
        <Title>IntersectPolyhedronPolyhedron</Title>
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
            <Name>PolyhedExp1</Name>
            <Text>Polyhedron1</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolyhedSizes1</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(3000,4000,5000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>

            <Parameter>
                <Name>PolyhedColor1</Name>
                <Text>Color</Text>
                <Value>4</Value>
                <ValueType>Color</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PolyhedExp2</Name>
            <Text>Polyhedron2</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolyhedSizes2</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(3000,4000,5000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>

            <Parameter>
                <Name>PlacementPoint</Name>
                <Text>Placement point</Text>
                <Value>Point3D(2000, 1000, 2000)</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>PolyhedColor2</Name>
                <Text>Color</Text>
                <Value>3</Value>
                <ValueType>Color</ValueType>
            </Parameter>

        </Parameter>
    </Page>
</Element>
