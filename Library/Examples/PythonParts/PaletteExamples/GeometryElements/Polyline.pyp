<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\Polyline.py</Name>
        <Title>Polyline</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>2D polyline</Text>

        <Parameter>
            <Name>Format2D</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp2D</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polyline2DSingleRowExp</Name>
            <Text>Polyline - Single row for x/y</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyline1</Name>
                <Text>Point</Text>
                <Value>Polyline2D(Points((0,2000)(1000,3100)(2000,3500)(4000,0)))</Value>
                <ValueType>Polyline2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polyline2DOneRowExp</Name>
            <Text>Polyline - One row for x/y</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyline2</Name>
                <Text>Point</Text>
                <Value>Polyline2D(Points((5000,2000)(6000,3100)(7000,3500)(10000,0)))</Value>
                <ValueType>Polyline2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polyline2DOneRowExp</Name>
            <Text>List of Polyline2D</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolylineCount</Name>
                <Text>Polyline count</Text>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>PolylineList</Name>
                <Text>Point</Text>
                <Value>[Polyline2D(Points((11000,2000)(13000,3100)(14000,3500)(15000,0)));Polyline2D(Points((15000,2000)(16000,3100)(17000,3500)(20000,0)))]</Value>
                <ValueType>Polyline2D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>PolylineCount</Dimensions>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Page2</Name>
        <Text>3D polyline</Text>

        <Parameter>
            <Name>Format3D</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp3D</Name>
                <Text></Text>
                <Value>CommonProperties(Color(5))</Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polyline3DSingleRowExp</Name>
            <Text>Polyline - Single row for x/y/z</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyline6</Name>
                <Text>Point</Text>
                <Value>Polyline3D(Points((0,7000,0)(2000,8100,1000)(4000,8500,3000)))</Value>
                <ValueType>Polyline3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polyline3DOneRowExp</Name>
            <Text>Polyline - One row for x/y/z</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyline7</Name>
                <Text>Point</Text>
                <Value>Polyline3D(Points((5000,7000,0)(7000,9100,1000)(10000,8500,3000)))</Value>
                <ValueType>Polyline3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Polyline3DOneRowExp</Name>
            <Text>Hidden y</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Polyline8</Name>
                <Text>Point</Text>
                <Value>Polyline3D(Points((11000,7000,0)(13000,8100,1000)(16000,6500,3000)))</Value>
                <ValueType>Polyline3D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Visible>|Polyline8.Y:False</Visible>
            </Parameter>
        </Parameter>
    </Page>
</Element>