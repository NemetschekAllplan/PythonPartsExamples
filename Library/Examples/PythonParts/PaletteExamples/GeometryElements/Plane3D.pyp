<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\Plane3D.py</Name>
        <Title>Plane3D</Title>
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
            <Name>CircleRadius</Name>
            <Text>Circle radius</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>PlaneExp1</Name>
            <Text>Axis placement controls expanded</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Plane1</Name>
                <Text>Plane 1</Text>
                <Value>Plane3D(Point(0,0,0)Vector(0,1,1))</Value>
                <ValueType>Plane3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PlaneExp2</Name>
            <Text>Plane controls in row</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Plane2</Name>
                <Text>Plane 2</Text>
                <Value>Plane3D(Point(5000,0,0)Vector(1,0,1))</Value>
                <ValueType>Plane3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PlaneListExp</Name>
            <Text>Plane list</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>PlaneCount</Name>
                <Text>Plane count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>PlaneList</Name>
                <Text>Plane</Text>
                <Value>[Plane3D(Point(0,5000,0)Vector(0,0,1));Plane3D(Point(5000,5000,0)Vector(0,0,1));Plane3D(Point(10000,5000,0)Vector(0,0,1))]</Value>
                <ValueType>Plane3D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>PlaneCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PlaneTextExp</Name>
            <Text>Controls with special text</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Plane3</Name>
                <Text>Point,Vector</Text>
                <Value>Plane3D(Point(10000,0,0)Vector(0,0,1))</Value>
                <ValueType>Plane3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PlaneConditionExp</Name>
            <Text>Plane controls with condition</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Plane4</Name>
                <Text>Plane 4</Text>
                <Value>Plane3D(Point(15000,0,0)Vector(0,0,1))</Value>
                <ValueType>Plane3D</ValueType>
                <Visible>|Plane4.Vector:False</Visible>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>
</Element>
