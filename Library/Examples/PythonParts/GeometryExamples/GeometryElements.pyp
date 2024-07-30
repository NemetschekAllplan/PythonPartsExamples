<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\GeometryElements.py</Name>
        <Title>GeometryElements</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>General</Text>

        <Parameter>
            <Name>CreatePythonPart</Name>
            <Text>Create PythonPart</Text>
            <Value>True</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>

        <Parameter>
            <Name>Expander</Name>
            <Text>Rotation</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RotationAngleX</Name>
                <Text>Rotation x-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>RotationAngleY</Name>
                <Text>Rotation y-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>RotationAngleZ</Name>
                <Text>Rotation z-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Page1</Name>
        <Text>2D Geometry elements</Text>

        <Parameter>
            <Name>Line2D</Name>
            <Text>Line2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Polyline2D</Name>
            <Text>Polyline2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Polygon2D</Name>
            <Text>Polygon2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Arc2D</Name>
            <Text>Arc2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Spline2D</Name>
            <Text>Spline2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Path2D</Name>
            <Text>Path2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>

    <Page>
        <Name>Page2</Name>
        <Text>3D Geometry elements</Text>

        <Parameter>
            <Name>Line3D</Name>
            <Text>Line3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Polyline3D</Name>
            <Text>Polyline3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Polygon3D</Name>
            <Text>Polygon3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Arc3D</Name>
            <Text>Arc3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Spline3D</Name>
            <Text>Spline3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Polyhedron3D</Name>
            <Text>Polyhedron3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>BRep3D</Name>
            <Text>BRep3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Ellipsoid3D</Name>
            <Text>Ellipsoid3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Cuboid3D</Name>
            <Text>Cuboid3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Cone3D</Name>
            <Text>Cone3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Cylinder3D</Name>
            <Text>Cylinder3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
</Element>
