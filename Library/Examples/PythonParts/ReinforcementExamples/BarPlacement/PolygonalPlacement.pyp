<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\BarPlacement\PolygonalPlacement.py</Name>
        <Title>Polygonal placement</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>GeneralPage</Name>
        <Text></Text>
        <Parameter>
            <Name>Geometry</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BottomDimensions</Name>
                <Text>Bottom dimensions</Text>
                <Value>Vector2D(800,500)</Value>
                <ValueType>Vector2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
            <Parameter>
                <Name>TopDimensions</Name>
                <Text>Top dimensions</Text>
                <Value>Vector2D(600,300)</Value>
                <ValueType>Vector2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>5000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BarShapeExpander</Name>
            <Text>BarShapeProperties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>-1</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>DiameterStirrup</Name>
                <Text>Stirrup diameter</Text>
                <Value>10</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BarPlacementExpander</Name>
            <Text>BarPlacementProperties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Count</Name>
                <Text>Bar count</Text>
                <Value>20</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>OthersExpander</Name>
            <Text>Others</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>IsPythonPart</Name>
                <Text>Create as PythonPart</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
