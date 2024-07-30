<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\BasicSolids\Cuboid.py</Name>
        <Title>Cuboid</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Cuboid</Text>
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
                <Name>CuboidLength</Name>
                <Text>Length</Text>
                <Value>3000</Value>
                <MinValue>1</MinValue>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>CuboidWidth</Name>
                <Text>Width</Text>
                <Value>2000</Value>
                <MinValue>1</MinValue>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>CuboidHeight</Name>
                <Text>Height</Text>
                <Value>1000</Value>
                <MinValue>1</MinValue>
                <ValueType>Length</ValueType>
            </Parameter>
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

    </Page>
</Element>
