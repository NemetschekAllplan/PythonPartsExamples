<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ModelObjectExamples\SelectionExamples\WallGeometrySelection.py</Name>
        <Title>WallFaceSelection</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>

    <Constants>
        <Constant>
            <Name>PURE_WALL_GEOMETRY</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>MODEL_GEOMETRY</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>GROUND_VIEW_GEOMETRY</Name>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Constant>
   </Constants>

    <Page>
        <Parameter>
            <Name>SelectedExp</Name>
            <Text>Select geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>GeometryType</Name>
                <Text>Geometry type</Text>
                <Value>PURE_WALL_GEOMETRY</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>PureWallGeometry</Name>
                    <Text>Pure wall geometry</Text>
                    <Value>PURE_WALL_GEOMETRY</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>ModelGeometry</Name>
                    <Text>Model geometry</Text>
                    <Value>MODEL_GEOMETRY</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>GroundViewGeometry</Name>
                    <Text>Ground view geometry</Text>
                    <Value>GROUND_VIEW_GEOMETRY</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>

            </Parameter>
        </Parameter>

        <Parameter>
            <Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CoordinateRow</Name>
                <Text></Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>WallGeometry</Name>
                    <Text>Polyhedron point </Text>
                    <Value>[_]</Value>
                    <ValueType>Polyhedron3D</ValueType>
                    <Enable>False</Enable>
                    <Persistent>False</Persistent>
                </Parameter>

                <Parameter>
                    <Name>WallGroundViewGeometry</Name>
                    <Text></Text>
                    <Value>[_]</Value>
                    <ValueType>Polygon2D</ValueType>
                    <XYZinRow>True</XYZinRow>
                    <Enable>False</Enable>
                    <Persistent>False</Persistent>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
