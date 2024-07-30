<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\SolidCreation\ClippedSweptSolid.py</Name>
        <Title>Clipped swept solid</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Clipped swept solid</Text>

        <Parameter>
            <Name>TopPlaneParametersExpander</Name>
            <Text>Top plane</Text>
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
                <Name>TopPlaneReferencePoint</Name>
                <Text>Reference point</Text>
                <Value>Point3D(0, 0, 1000)</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>TopPlaneDirectionVector</Name>
                <Text>Direction vector</Text>
                <Value>Vector3D(-500, 0, 1000)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>BottomPlaneParametersExpander</Name>
            <Text>Bottom plane</Text>
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
                <Name>BottomPlaneReferencePoint</Name>
                <Text>Reference point</Text>
                <Value>Point3D(0, 0, -1000)</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>BottomPlaneDirectionVector</Name>
                <Text>Direction vector</Text>
                <Value>Vector3D(500, 0, 1000)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PointsExpander</Name>
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
            </Parameter>

            <Parameter>
                <Name>ProfilePoints</Name>
                <Text>Profile points</Text>
                <Value>[Point2D(  0.0,   0.0);
                        Point2D(500.0, 100.0);
                        Point2D(800.0, 800.0);
                        Point2D(500.0, 700.0);
                        Point2D(100.0, 400.0);
                        Point2D(  0.0, 900.0)]</Value>
                <ValueType>Point2D</ValueType>
                <XYZinRow>False</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>
</Element>
