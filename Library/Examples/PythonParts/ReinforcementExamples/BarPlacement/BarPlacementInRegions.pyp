<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\BarPlacement\BarPlacementInRegions.py</Name>
        <Title>Rebar placement in regions</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>ReinforcementPage</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>BarShapeExpander</Name>
            <Text>Shape properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>4</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>StirrupPlacementExpander</Name>
            <Text>Placement properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>NumberOfRegions</Name>
                <Text>Number of regions</Text>
                <Value>5</Value>
                <ValueType>Integer</ValueType>
                <MinValue>1</MinValue>
            </Parameter>
            <Parameter>
                <Name>BarShapeSideSeparator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>BarShapeSideDataTexts</Name>
                <Text>Placement regions</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>BarShapeSideStartXCoordText</Name>
                    <Text></Text>
                    <Value>length</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapeSideStartYCoordText</Name>
                    <Text></Text>
                    <Value>spacing</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapeSideEndXCoordText</Name>
                    <Text></Text>
                    <Value>diameter</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PlacementRegions</Name>
                <Text>Placement regions</Text>
                <Value>[(300.|50.|10.);(700.|100.|10.);(0.|200.|8.);(700.|100.|10.);(300.|50.|10.)]</Value>
                <ValueType>tuple(Length,Length,ReinfBarDiameter)</ValueType>
                <MinValue>0,10,0</MinValue>
                <Dimensions>NumberOfRegions</Dimensions>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>OthersPage</Name>
        <Text>Others</Text>

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
            <Name>Geometry</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Sizes</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(4000,300,600)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ElementCreation</Name>
            <Text>Element creation</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>IsPythonPart</Name>
                <Text>Create as PythonPart</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
