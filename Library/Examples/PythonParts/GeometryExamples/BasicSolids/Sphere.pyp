<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\BasicSolids\Sphere.py</Name>
        <Title>Sphere</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Sphere</Text>

        <Parameter>
            <Name>PlacementParameterExpander</Name>
            <Text>Placement</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LocalXVector</Name>
                <Text>Local X axis</Text>
                <Value>Vector3D(1000,0,0)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>LocalZVector</Name>
                <Text>Local Z axis</Text>
                <Value>Vector3D(0,0,1000)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>DimensionsParameterExpander</Name>
            <Text>Dimensions</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Radius</Name>
                <Text>Radius</Text>
                <Value>500</Value>
                <MinValue>1</MinValue>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateAs</Name>
                <Text>Create as</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>CreateAsBRep</Name>
                    <Text>BRep</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>

                <Parameter>
                    <Name>CreateAsPolyhedron</Name>
                    <Text>Polyhedron</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>TesselationParameterExpander</Name>
            <Text>Tesselation parameters</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateAs == 1</Visible>

            <Parameter>
                <Name>TessellationDensity</Name>
                <Text>Density</Text>
                <Value>0.2</Value>
                <ValueType>Double</ValueType>
                <MinValue>0.0</MinValue>
                <MaxValue>1.0</MaxValue>
            </Parameter>

            <Parameter>
                <Name>TessellationMaxAngle</Name>
                <Text>Maximum angle</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
                <MinValue>0</MinValue>
                <MaxValue>180</MaxValue>
            </Parameter>

            <Parameter>
                <Name>TessellationMinLength</Name>
                <Text>Minimum length</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

            <Parameter>
                <Name>TessellationMaxLength</Name>
                <Text>Maximum length</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
            </Parameter>
        </Parameter>
    </Page>
</Element>
