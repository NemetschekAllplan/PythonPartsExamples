<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\Arc2D.py</Name>
        <Title>Arc2D</Title>
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
            <Name>ArcExp1</Name>
            <Text>Arc controls expanded</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Arc1</Name>
                <Text>Arc 1</Text>
                <Value>Arc2D(CenterPoint(0,0)MinorRadius(1000)MajorRadius(2000)AxisAngle(pi / 4)StartAngle(pi / 4)EndAngle(pi * 3 / 2)IsCounterClockwise(1))</Value>
                <ValueType>Arc2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ArcExp2</Name>
            <Text>Arc controls in row</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Arc2</Name>
                <Text>Arc 2</Text>
                <Value>Arc2D(CenterPoint(3000,0)MinorRadius(1000)MajorRadius(1000)AxisAngle(pi / 4)StartAngle(pi / 4)EndAngle(pi * 3 / 2)IsCounterClockwise(1))</Value>
                <ValueType>Arc2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ArcListExp</Name>
            <Text>Arc list</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>ArcCount</Name>
                <Text>Arc count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>ArcList</Name>
                <Text>Arc</Text>
                <Value>[Arc2D(CenterPoint(6000,0)MinorRadius(1000)MajorRadius(1000)AxisAngle(0.0)StartAngle(0.0)EndAngle(pi * 2)IsCounterClockwise(1));
                        Arc2D(CenterPoint(9000,0)MinorRadius(1000)MajorRadius(1500)AxisAngle(0.0)StartAngle(pi / 4)EndAngle(pi * 3 / 2)IsCounterClockwise(1));
                        Arc2D(CenterPoint(13000,0)MinorRadius(1000)MajorRadius(2000)AxisAngle(pi / 4)StartAngle(0.0)EndAngle(pi * 3 / 2)IsCounterClockwise(1))]</Value>
                <ValueType>Arc2D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>ArcCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ArcTextExp</Name>
            <Text>Controls with special text</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Arc3</Name>
                <Text>Center,Minor,Major,Axis angle,Start angle,End angle</Text>
                <Value>Arc2D(CenterPoint(0,5000)MinorRadius(1000)MajorRadius(1000)AxisAngle(0)StartAngle(pi / 4)EndAngle(pi * 3 / 2)IsCounterClockwise(1))</Value>
                <ValueType>Arc2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ArcConditionExp</Name>
            <Text>Arc controls with condition</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Arc4</Name>
                <Text>Arc 4</Text>
                <Value>Arc2D(CenterPoint(5000,5000)MinorRadius(1000)MajorRadius(1000)AxisAngle(0)StartAngle(pi / 4)EndAngle(pi * 3 / 2)IsCounterClockwise(1))</Value>
                <ValueType>Arc2D</ValueType>
                <Visible>|Arc4.MinorRadius:False|Arc4.MajorRadius:False</Visible>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>
</Element>
