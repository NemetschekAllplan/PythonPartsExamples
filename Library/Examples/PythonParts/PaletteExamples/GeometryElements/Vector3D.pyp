<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\Vector3D.py</Name>
        <Title>Vector3D</Title>
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
            <Name>VectorExp1</Name>
            <Text>Vector controls expanded</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Vector1</Name>
                <Text>Vector 1</Text>
                <Value>Vector3D(0,0,0)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>VectorExp2</Name>
            <Text>Vector controls in row</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Vector2</Name>
                <Text>Vector 2</Text>
                <Value>Vector3D(1000, 1000, 1000)</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>VectorListExp</Name>
            <Text>Vector list</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>VectorCount</Name>
                <Text>Vector count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>VectorList</Name>
                <Text>Vectors</Text>
                <Value>[Vector3D(0,-1000,0);Vector3D(2000,1000,1000);Vector3D(3000,-2000,2000)]</Value>
                <ValueType>Vector3D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>VectorCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CoordinateTextExp</Name>
            <Text>Vector values with special text</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Sizes</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(1000,2000,3000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CoordConditionExp</Name>
            <Text>Vector values with visible condition</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>StartVector</Name>
                <Text>X distance start</Text>
                <Value>Vector3D(5000,1000,2000)</Value>
                <ValueType>Vector3D</ValueType>
                <Visible>|StartVector.Y:False</Visible>
            </Parameter>
            <Parameter>
                <Name>EndVector</Name>
                <Text>Y distance end</Text>
                <Value>Vector3D(10000,3000,2000)</Value>
                <ValueType>Vector3D</ValueType>
                <Visible>|EndVector.X:False</Visible>
            </Parameter>
        </Parameter>
    </Page>
</Element>
