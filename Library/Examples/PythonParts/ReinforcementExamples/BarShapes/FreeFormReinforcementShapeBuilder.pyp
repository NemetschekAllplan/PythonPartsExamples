<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\BarShapes\FreeFormReinforcementShapeBuilder.py</Name>
        <Title>Reinforcement shape builder</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Stirrup2D</Name>
        <Text>Reinforcement shape builder</Text>

        <Parameter>
            <Name>BarShapeSideDataListExpander</Name>
            <Text>BarShapeSideDataList</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>NumberOfShapeSides</Name>
                <Text>Number of sides</Text>
                <Value>4</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>BarShapeSideSeparator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>BarShapeSideDataTexts</Name>
                <Text>Shape sides and covers</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>BarShapeSideStartXCoordText</Name>
                    <Text></Text>
                    <Value>start X</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapeSideStartYCoordText</Name>
                    <Text></Text>
                    <Value>start Y</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapeSideEndXCoordText</Name>
                    <Text></Text>
                    <Value>end X</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapeSideEndYCoordText</Name>
                    <Text></Text>
                    <Value>end Y</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BarShapeSideCoverText</Name>
                    <Text></Text>
                    <Value>cover</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>CoverAtStart</Name>
                <Text>Cover at start</Text>
                <Value>25</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>BarShapeSideData</Name>
                <Text></Text>
                <Value>[(Point2D(0,500)|Point2D(0,0)|25);(Point2D(0,0)|Point2D(300,0)|25);(Point2D(400,20)|Point2D(600,80)|25);(Point2D(700,100)|Point2D(1000,100)|25)]</Value>
                <ValueType>Tuple(Point2D,Point2D,ReinfConcreteCover)</ValueType>
                <Dimensions>NumberOfShapeSides</Dimensions>
            </Parameter>
            <Parameter>
                <Name>CoverAtEnd</Name>
                <Text>Cover at end</Text>
                <Value>25</Value>
                <ValueType>ReinfConcreteCover</ValueType>
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
                <Name>SetAtStart</Name>
                <Text>Set at start:</Text>
                <Value>Nothing</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>SetNothingAtStart</Name>
                    <Text>nothing</Text>
                    <Value>Nothing</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SetAnchorageAtStart</Name>
                    <Text>anchorage</Text>
                    <Value>Anchorage</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SetSideLengthAtStart</Name>
                    <Text>side length</Text>
                    <Value>SideLength</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>StartSideOrAnchorageLength</Name>
                <Text>Length</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>SetAtStart != "Nothing"</Visible>
            </Parameter>
            <Parameter>
                <Name>SideLengthStartSeparator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>SetAtEnd</Name>
                <Text>Set at end:</Text>
                <Value>Nothing</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>SetNothingAtEnd</Name>
                    <Text>nothing</Text>
                    <Value>Nothing</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SetAnchorageAtEnd</Name>
                    <Text>anchorage</Text>
                    <Value>Anchorage</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SetSideLengthAtEnd</Name>
                    <Text>side length</Text>
                    <Value>SideLength</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>EndSideOrAnchorageLength</Name>
                <Text>Length</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>SetAtEnd != "Nothing"</Visible>
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
                <Value>Freeform</Value>
                <ValueList>"|".join(str(key) for key in AllplanReinf.BendingShapeType.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>