<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\Circle3D.py</Name>
        <Title>Circle3D</Title>
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
            <Name>CircleExp1</Name>
            <Text>Circle controls expanded</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Circle1</Name>
                <Text>Circle 1</Text>
                <Value>Circle3D(CenterPoint(0,0,0)ZAxis(0,0,1)MajorRadius(500))</Value>
                <ValueType>Circle3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CircleExp2</Name>
            <Text>Circle controls in row</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Circle2</Name>
                <Text>Circle 2</Text>
                <Value>Circle3D(CenterPoint(2000, 1000,0)ZAxis(0,0,1)MajorRadius(250))</Value>
                <ValueType>Circle3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CircleListExp</Name>
            <Text>Circle list</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CircleCount</Name>
                <Text>Circle count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>CircleList</Name>
                <Text>Circle</Text>
                <Value>[Circle3D(CenterPoint(0,2000,0)ZAxis(0,0,1)MajorRadius(100));Circle3D(CenterPoint(1000,2000,0)ZAxis(0,0,1)MajorRadius(200));Circle3D(CenterPoint(2000,2000,0)ZAxis(0,0,1)MajorRadius(300))]</Value>
                <ValueType>Circle3D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>CircleCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CircleTextExp</Name>
            <Text>Controls with special text</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Circle3</Name>
                <Text>Center,Radius,Z-Axis</Text>
                <Value>Circle3D(CenterPoint(1000,0,0)MajorRadius(200)ZAxis(0,0,1))</Value>
                <ValueType>Circle3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CircleConditionExp</Name>
            <Text>Circle controls with condition</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Circle4</Name>
                <Text>Circle 4</Text>
                <Value>Circle3D(CenterPoint(2000,0,0)MajorRadius(300)ZAxis(0,0,1))</Value>
                <ValueType>Circle3D</ValueType>
                <Visible>|Circle4.MajorRadius:False</Visible>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>
</Element>
