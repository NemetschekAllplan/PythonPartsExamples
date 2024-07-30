<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\BooleanOperations\IntersectBRepPolyhedron.py</Name>
        <Title>IntersectBRepPolyhedron</Title>
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
            <Name>BRepExp</Name>
            <Text>BRep-Cylinder</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CylinderSizes</Name>
                <Text>Radius,Height</Text>
                <Value>Vector2D(1000,5000)</Value>
                <ValueType>Vector2D</ValueType>
            </Parameter>

            <Parameter>
                <Name>PlacementPoint</Name>
                <Text>Placement point</Text>
                <Value>Point3D(-1000, 2000, 2000)</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>AxisVector</Name>
                <Text>Axis vector</Text>
                <Value>Vector3D(1000, 0, 0)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>BRepColor</Name>
                <Text>Color</Text>
                <Value>3</Value>
                <ValueType>Color</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PolyhedExp</Name>
            <Text>Polyhedron</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolyhedSizes</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(3000,4000,5000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>

            <Parameter>
                <Name>PolyhedColor</Name>
                <Text>Color</Text>
                <Value>4</Value>
                <ValueType>Color</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
