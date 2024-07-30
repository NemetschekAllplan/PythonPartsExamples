<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\SolidCreation\PolyhedronBuilder.py</Name>
        <Title>Polyhedron Builder</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Polyhedron Builder</Text>

        <Parameter>
            <Name>VerticesExpander</Name>
            <Text>Polyhedron vertices</Text>
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
                <Name>PolyhedronVertices</Name>
                <Text>Vertices</Text>
                <Value>[Point3D(-500.0,-500.0,   0.0);
                        Point3D( 500.0,-500.0,   0.0);
                        Point3D( 500.0, 500.0,   0.0);
                        Point3D(-500.0, 500.0,   0.0);
                        Point3D(   0.0,   0.0,1000.0)]</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>False</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PolyhedronParameterExpander</Name>
            <Text>Polyhedron parameter</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolyhedronType</Name>
                <Text>Polyhedron type</Text>
                <Value>tVolume</Value>
                <ValueList>"|".join(str(key) for key in AllplanGeo.PolyhedronType.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
