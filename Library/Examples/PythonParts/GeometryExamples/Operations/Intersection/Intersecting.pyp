<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\Intersection\Intersecting.py</Name>
        <Title>Check intersection</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>SelectGeometry</Name>
        <Text>Calculate intersection</Text>
        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>3D object
Arc (3D)
Line (2D)
Hatching, Filling, etc.
Splines (3D)
            </Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>IntersectingOptions</Name>
            <Text>Options of the Intersecting function</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolygonOptionsText</Name>
                <Text>For 2D lines and polygons only:</Text>
                <Value></Value>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>Tolerance</Name>
                <Text>Tolerance</Text>
                <Value>0.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
