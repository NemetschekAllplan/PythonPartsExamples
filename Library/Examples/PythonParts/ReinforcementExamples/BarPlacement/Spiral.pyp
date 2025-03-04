<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\BarPlacement\Spiral.py</Name>
        <Title>Spiral</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>IsPythonPart</Name>
            <Text>Create PythonPart</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>5000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
            <Parameter>
                <Name>Radius</Name>
                <Text>Radius</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander2</Name>
            <Text>Reinforcement</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Layer</Name>
                <Text>Layer</Text>
                <Value>RU_ALL</Value>
                <ValueList>Standard|RU_ALL|RU_R</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>PenByLayer</Name>
                <Text>Pen by layer</Text>
                <TextId>e_PEN_BY_LAYER</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>StrokeByLayer</Name>
                <Text>Linetype by layer</Text>
                <TextId>e_LINETYPE_BY_LAYER</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ColorByLayer</Name>
                <Text>Color by layer</Text>
                <TextId>e_COLOR_BY_LAYER</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ConcreteGrade</Name>
                <Text>Concrete grade</Text>
                <Value>4</Value>
                <ValueType>ReinfConcreteGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>4</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>PlacePerLinearMeter</Name>
                <Text>Place per linear meter</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>LengthFactor</Name>
                <Text>Length factor</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>Diameter</Name>
                <Text>Bar diameter</Text>
                <Value>10.0</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>Pitch</Name>
                <Text>Pitch</Text>
                <Value>200.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>50</MinValue>
            </Parameter>
            <Parameter>
                <Name>Pitch1</Name>
                <Text>Pitch section 1</Text>
                <Value>100.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>50</MinValue>
            </Parameter>
            <Parameter>
                <Name>LoopsStart</Name>
                <Text>Loops start</Text>
                <Value>0</Value>
                <ValueType>integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>Length1</Name>
                <Text>Length section 1</Text>
                <Value>0.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Pitch2</Name>
                <Text>Pitch section 2</Text>
                <Value>100.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>50</MinValue>
            </Parameter>
            <Parameter>
                <Name>Length2</Name>
                <Text>Length section 2</Text>
                <Value>0.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Pitch3</Name>
                <Text>Pitch section 3</Text>
                <Value>100.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>50</MinValue>
            </Parameter>
            <Parameter>
                <Name>Length3</Name>
                <Text>Length section 3</Text>
                <Value>0.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Pitch4</Name>
                <Text>Pitch section 4</Text>
                <Value>100.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>50</MinValue>
            </Parameter>
            <Parameter>
                <Name>Length4</Name>
                <Text>Length section 4</Text>
                <Value>0.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>LoopsEnd</Name>
                <Text>Loops end</Text>
                <Value>0</Value>
                <ValueType>integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>StartHook</Name>
                <Text>Use start hook</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
                <Enable>PlacePerLinearMeter == False</Enable>
            </Parameter>
            <Parameter>
                <Name>StartHookLength</Name>
                <Text>Start hook length</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
                <Enable>StartHook == True and PlacePerLinearMeter == False</Enable>
            </Parameter>
            <Parameter>
                <Name>StartHookAngle</Name>
                <Text>Start hook angle</Text>
                <Value>90.0</Value>
                <ValueType>Angle</ValueType>
                <Enable>StartHook == True and PlacePerLinearMeter == False</Enable>
                <MinValue>-180.0</MinValue>
                <MaxValue>180.0</MaxValue>
            </Parameter>
            <Parameter>
                <Name>EndHook</Name>
                <Text>Use end hook</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
                <Enable>PlacePerLinearMeter == False</Enable>
            </Parameter>
            <Parameter>
                <Name>EndHookLength</Name>
                <Text>End hook length</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
                <Enable>EndHook == True and PlacePerLinearMeter == False</Enable>
            </Parameter>
            <Parameter>
                <Name>EndHookAngle</Name>
                <Text>End hook angle</Text>
                <Value>90.0</Value>
                <ValueType>Angle</ValueType>
                <Enable>EndHook == True and PlacePerLinearMeter == False</Enable>
                <MinValue>-180.0</MinValue>
                <MaxValue>180.0</MaxValue>
            </Parameter>
        </Parameter>
    </Page>
</Element>