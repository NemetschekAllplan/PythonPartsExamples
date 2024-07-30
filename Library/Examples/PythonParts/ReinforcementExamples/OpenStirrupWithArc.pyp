<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\OpenStirrupWithArc.py</Name>
        <Title>Open Stirrup with arc</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
            
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
            <Parameter>
                <Name>PlacementLength</Name>
                <Text>Placement length</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * ConcreteCover + 2 * Diameter</MinValue>
            </Parameter>
        </Parameter>
        
        <Parameter>
            <Name>Expander2</Name>
            <Text>Reinforcement</Text>
            <ValueType>Expander</ValueType>
            
            <Parameter>
                <Name>HorizontalPlacement</Name>
                <Text>Horizontal placement</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
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
                <Name>Distance</Name>
                <Text>Bar spacing</Text>
                <Value>200.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * Diameter</MinValue>
            </Parameter>
            <Parameter>
                <Name>BendingRoller</Name>
                <Text>Bending roller</Text>
                <Value>4.0</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>
            <Parameter>
                <Name>StartHook</Name>
                <Text>Use start hook</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>EndHook</Name>
                <Text>Use end hook</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>StartHookAngle</Name>
                <Text>Start hook angle</Text>
                <Value>90.0</Value>
                <ValueType>Angle</ValueType>
                <Enable>StartHook == True</Enable>
                <Visible>StartHook == True</Visible>
                <MinValue>-180.0</MinValue>
                <MaxValue>180.0</MaxValue>
            </Parameter>
            <Parameter>
                <Name>EndHookAngle</Name>
                <Text>End hook angle</Text>
                <Value>90.0</Value>
                <ValueType>Angle</ValueType>
                <Enable>EndHook == True</Enable>
                <Visible>EndHook == True</Visible>
                <MinValue>-180.0</MinValue>
                <MaxValue>180.0</MaxValue>
            </Parameter>
        </Parameter>
        
        
        <Parameter>
            <Name>Expander3</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Surface</Name>
                <Text>Surface</Text>
                <Value>SMT\\concrete_exposed_concrete_holes</Value>
                <DisableButtonIsShown>False</DisableButtonIsShown>
                <ValueType>MaterialButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>Layer</Name>
                <Text>Layer</Text>
                <Value>0</Value>
                <ValueType>Layer</ValueType>
            </Parameter>
            <Parameter>
                <Name>Pen</Name>
                <Text>Pen</Text>
                <Value>1</Value>
                <ValueType>Pen</ValueType>
            </Parameter>
            <Parameter>
                <Name>Stroke</Name>
                <Text>Stroke</Text>
                <Value>1</Value>
                <ValueType>Stroke</ValueType>
            </Parameter>
            <Parameter>
                <Name>Color</Name>
                <Text>Color</Text>
                <Value>1</Value>
                <ValueType>Color</ValueType>
            </Parameter>
            <Parameter>
                <Name>UseConstructionLineMode</Name>
                <Text>Use construction line mode</Text>
                <Value>1</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>            
    </Page>
</Element>