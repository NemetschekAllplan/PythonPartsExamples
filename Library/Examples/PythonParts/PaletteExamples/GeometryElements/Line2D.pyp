<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\Line2D.py</Name>
        <Title>Line2D</Title>
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
            <Name>LineControlExp</Name>
            <Text>Line controls expanded</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Line1</Name>
                <Text>Line 1</Text>
                <Value>Line2D(0,0,2000,1000)</Value>
                <ValueType>Line2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>LineRowExp</Name>
            <Text>Line controls in row</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Line2</Name>
                <Text>Line 2</Text>
                <Value>Line2D(2000,0,4000,-2000)</Value>
                <ValueType>Line2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>LineListExp</Name>
            <Text>Line list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LineCount</Name>
                <Text>Line count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>LineList</Name>
                <Text>Lines</Text>
                <Value>[Line2D(5000,0,7000,-2000);Line2D(5000,0,7000,-0);Line2D(5000,0,7000,2000)]</Value>
                <ValueType>Line2D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>LineCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>LineTextExp</Name>
            <Text>Points with special text</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Line3</Name>
                <Text>From point,To point</Text>
                <Value>Line2D(0,5000,3000,7000)</Value>
                <ValueType>Line2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>LineConditionExp</Name>
            <Text>Line points with condition</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Line4</Name>
                <Text>Line 4</Text>
                <Value>Line2D(5000,5000,7000,7000)</Value>
                <ValueType>Line2D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Visible>|Line4.EndPoint:False</Visible>
            </Parameter>
            <Parameter>
                <Name>Line5</Name>
                <Text>Line 5</Text>
                <Value>Line2D(7000,7000,7000,9000)</Value>
                <ValueType>Line2D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Visible>|Line5.StartPoint:False</Visible>
            </Parameter>
        </Parameter>
    </Page>
</Element>
