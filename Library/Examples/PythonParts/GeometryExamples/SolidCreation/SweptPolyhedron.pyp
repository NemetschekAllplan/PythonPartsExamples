<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\SolidCreation\SweptPolyhedron.py</Name>
        <Title>Swept polyhedron</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Swept polyhedron</Text>

        <Parameter>
            <Name>ProfilePointsExpander</Name>
            <Text>Profile points</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CoordinatesTextRow</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>CoordinateXText</Name>
                    <Text></Text>
                    <Value>X</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>CoordinateYText</Name>
                    <Text></Text>
                    <Value>Y</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>CoordinateZText</Name>
                    <Text></Text>
                    <Value>Z</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>ProfilePoints</Name>
                <Text>Profile points</Text>
                <Value>[Point3D(  0.0,   0.0,   0.0);
                        Point3D(100.0,  20.0,   0.0);
                        Point3D(160.0, 160.0,   0.0);
                        Point3D(  0.0, 180.0,   0.0)]</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>False</XYZinRow>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>PathPointsExpander</Name>
            <Text>Path points</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CoordinatesTextRow</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>CoordinateXText</Name>
                    <Text></Text>
                    <Value>X</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>CoordinateYText</Name>
                    <Text></Text>
                    <Value>Y</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>CoordinateZText</Name>
                    <Text></Text>
                    <Value>Z</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PathPoints</Name>
                <Text>Path points</Text>
                <Value>[Point3D(   0.0,   0.0,   0.0);
                        Point3D(-100.0,   0.0, 200.0);
                        Point3D(   0.0,   0.0, 600.0);
                        Point3D( 200.0,   0.0, 800.0);
                        Point3D( 300.0, 300.0,1000.0)]</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>False</XYZinRow>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>SweepingParameterExpander</Name>
            <Text>Sweeping options</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CloseCaps</Name>
                <Text>Close caps</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>RailRotation</Name>
                <Text>Standard rotation</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>RotationAxis</Name>
                <Text>Rotation axis</Text>
                <Value>Vector3D(1000,1000,0)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Enable>not RailRotation</Enable>
            </Parameter>
        </Parameter>
    </Page>
</Element>
