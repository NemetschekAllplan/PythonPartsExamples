<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\BooleanOperations\ImprintProfileOnFaces.py</Name>
        <Title>ImprintProfileOnFaces</Title>
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

        ><Parameter>
            <Name>CuboidExp</Name>
            <Text>BRep-Cuboid</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Cuboid</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(5000,4000,2000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RectangleExp</Name>
            <Text>Bottom rectangle imprint</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Rectangle</Name>
                <Text>Length,Width</Text>
                <Value>Vector2D(3000,3000)</Value>
                <ValueType>Vector2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CircleExp</Name>
            <Text>Top circle imprint</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Circle</Name>
                <Text>Circle</Text>
                <Value>Circle2D(CenterPoint(2500, 2000)MajorRadius(1000))</Value>
                <ValueType>Circle2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PolylineExp</Name>
            <Text>Left polyline imprint</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyline</Name>
                <Text>Polyline</Text>
                <Value>Polyline3D(Points((0,0,-500)(0,2000,2500)(0,4000,-500)))</Value>
                <ValueType>Polyline3D</ValueType>
                 <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>
</Element>
