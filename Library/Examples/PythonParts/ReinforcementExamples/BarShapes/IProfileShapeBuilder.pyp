<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\BarShapes\IProfileShapeBuilder.py</Name>
        <Title>I profile shapes</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>IProfileShape</Name>
        <Text>I profile shapes</Text>

        <Parameter>
            <Name>ShapeTypeExpander</Name>
            <Text>Shape type</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>ShapeType</Name>
                <Text>Function of IProfileReinfShapeBuilder</Text>
                <Value>Bottom flange</Value>
                <ValueList>Bottom flange|Bottom flange 2|Top flange|Top flange 2|Web shape|Web stirrup</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>GeometryParametersExpander</Name>
            <Text>I-profile geometry</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>IProfileTexts</Name>
                <Text>Profile points</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>YCoordText</Name>
                    <Text></Text>
                    <Value>Y</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>ZCoordText</Name>
                    <Text></Text>
                    <Value>Z</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>ProfilePoints</Name>
                <Text>Profile points</Text>
                <Value>[Point2D(0,0);Point2D(0,100);Point2D(200,200);Point2D(200,800);Point2D(0,900);Point2D(0,1000);Point2D(500,1000);Point2D(500,900);Point2D(300,800);Point2D(300,200);Point2D(500,100);Point2D(500,0)]</Value>
                <ValueType>Point2D</ValueType>
            </Parameter>
            <Parameter>
                <Name>SideLength</Name>
                <Text>Side length</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
                <Visible>ShapeType in ["Bottom flange 2","Top flange 2","Web shape"]</Visible>
            </Parameter>
            <Parameter>
                <Name>Distance</Name>
                <Text>Distance</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
                <Visible>ShapeType == "Web shape"</Visible>
            </Parameter>

        </Parameter>


        <Parameter>
            <Name>ShapePropertiesExpander</Name>
            <Text>ReinforcementShapeProperties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Diameter</Name>
                <Text>Bar diameter</Text>
                <Value>10.0</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>BendingRoller</Name>
                <Text>Bending roller</Text>
                <Value>4.0</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>
            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>-1</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteGrade</Name>
                <Text>Concrete grade</Text>
                <Value>-1</Value>
                <ValueType>ReinfConcreteGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>BendingShapeType</Name>
                <Text>Bending shape type</Text>
                <Value>LongitudinalBar</Value>
                <ValueList>"|".join(str(key) for key in AllplanReinf.BendingShapeType.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>ConcreteCoverPropertiesExpander</Name>
            <Text>ConcreteCoverProperties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>ConcreteCoverLeft</Name>
                <Text>Left</Text>
                <Value>20.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCoverBottom</Name>
                <Text>Bottom</Text>
                <Value>20.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCoverRight</Name>
                <Text>Right</Text>
                <Value>20.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCoverTop</Name>
                <Text>Top</Text>
                <Value>20.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>