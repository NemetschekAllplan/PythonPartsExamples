<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\BarShapes\StirrupReinforcementShapeBuilder.py</Name>
        <Title>Reinforcement shape builder</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Stirrup2D</Name>
        <Text>Reinforcement shape builder</Text>

        <Parameter>
            <Name>BarShapePointDataListExpander</Name>
            <Text>BarShapePointDataList</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>NumberOfShapePoints</Name>
                <Text>Number of points</Text>
                <Value>5</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>BarShapePointSeparator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>BarShapePointDataTexts</Name>
                <Text>Shape points and covers</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>BarShapePointXCoordText</Name>
                    <Text></Text>
                    <Value>X</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapePointYCoordText</Name>
                    <Text></Text>
                    <Value>Y</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapePointCoverText</Name>
                    <Text></Text>
                    <Value>cover</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>BarShapePointData</Name>
                <Text></Text>
                <Value>[(Point2D(330,500)|25);(Point2D(-30,500)|25);(Point2D(0,0)|25);(Point2D(300,0)|25);(Point2D(330,500)|25)]</Value>
                <ValueType>Tuple(Point2D,ReinfConcreteCover)</ValueType>
                <Dimensions>NumberOfShapePoints</Dimensions>
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
                <Value>Stirrup</Value>
                <ValueList>"|".join(str(key) for key in AllplanReinf.BendingShapeType.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ReinfShapeBuilderParametersExpander</Name>
            <Text>ReinforcementShapeBuilder</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>SetStartHook</Name>
                <Text>Set start hook</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>StartHookLength</Name>
                <Text>Start hook (0=calculate)</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>SetStartHook</Visible>
            </Parameter>
            <Parameter>
                <Name>StartHookAngle</Name>
                <Text>Start hook angle</Text>
                <Value>135</Value>
                <MinValue>-180</MinValue>
                <MaxValue>180</MaxValue>
                <ValueType>Angle</ValueType>
                <Visible>SetStartHook</Visible>
            </Parameter>
            <Parameter>
                <Name>StartHookType</Name>
                <Text>Start hook type</Text>
                <Value>eStirrup</Value>
                <ValueType>StringComboBox</ValueType>
                <ValueList>"|".join(str(key) for key in AllplanReinf.HookType.names.keys())</ValueList>
                <Visible>SetStartHook</Visible>
            </Parameter>
            <Parameter>
                <Name>StartHookSeparator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>SetEndHook</Name>
                <Text>Set end hook</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>EndHookLength</Name>
                <Text>End hook (0=calculate)</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>SetEndHook</Visible>
            </Parameter>
            <Parameter>
                <Name>EndHookAngle</Name>
                <Text>End hook angle</Text>
                <Value>135</Value>
                <MinValue>-180</MinValue>
                <MaxValue>180</MaxValue>
                <ValueType>Angle</ValueType>
                <Visible>SetEndHook</Visible>
            </Parameter>
            <Parameter>
                <Name>EndHookType</Name>
                <Text>End hook type</Text>
                <Value>eStirrup</Value>
                <ValueType>StringComboBox</ValueType>
                <ValueList>"|".join(str(key) for key in AllplanReinf.HookType.names.keys())</ValueList>
                <Visible>SetEndHook</Visible>
            </Parameter>
            <Parameter>
                <Name>EndHookSeparator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>StirrupType</Name>
                <Text>Stirrup type</Text>
                <Value>Normal</Value>
                <ValueType>StringComboBox</ValueType>
                <ValueList>"|".join(str(key) for key in AllplanReinf.StirrupType.names.keys())</ValueList>
            </Parameter>
        </Parameter>
    </Page>
</Element>