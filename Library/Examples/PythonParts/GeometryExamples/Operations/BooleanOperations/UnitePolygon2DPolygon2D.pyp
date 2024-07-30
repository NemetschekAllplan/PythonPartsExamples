<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\BooleanOperations\UnitePolygon2DPolygon2D.py</Name>
        <Title>UnitePolygon2DPolygon2D</Title>
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
            <Name>Polygon1Exp</Name>
            <Text>Polygon 1</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Polygon1</Name>
                <Text>Length,Width</Text>
                <Value>Vector2D(5000,3000)</Value>
                <ValueType>Vector2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polygon2Exp</Name>
            <Text>Polygon 2</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Polygon2</Name>
                <Text>Length,Width</Text>
                <Value>Vector2D(4000,3000)</Value>
                <ValueType>Vector2D</ValueType>
            </Parameter>

            <Parameter>
                <Name>PlacementPoint</Name>
                <Text>Placement</Text>
                <Value>Point2D(3000,2000)</Value>
                <ValueType>Point2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>
</Element>
