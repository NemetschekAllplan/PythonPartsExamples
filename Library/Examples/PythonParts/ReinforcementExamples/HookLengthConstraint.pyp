<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\HookLengthConstraint.py</Name>
        <Title>HookLengthConstraint</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>HookLengthConstraint</Name>
        <Text>HookLengthConstraint</Text>

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
            <Name>Expander1</Name>
            <Text>Bar</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BarDiameter</Name>
                <Text>Bar diameter</Text>
                <Value>-1</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>BarHookAngle</Name>
                <Text>Hook angle</Text>
                <Value>90</Value>
                <ValueList>90|-90|135|-135|150|-150|180|-180</ValueList>
                <ValueType>AngleComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>BarHookType</Name>
                <Text>Hook type</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButtonStirrup</Name>
                    <Text>Stirrup</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButtonAngle</Name>
                    <Text>Angle</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButtonAnchorage</Name>
                    <Text>Anchorage</Text>
                    <Value>3</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>BarHookLength</Name>
                <Text>Hook length</Text>
                <Value>-1</Value>
                <ValueType>ReinfHookLength</ValueType>
                <Constraint>BarDiameter;SteelGrade;ConcreteGrade;BarHookAngle;__ReinfHookType__ = BarHookType</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander2</Name>
            <Text>Mesh</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MeshGroup</Name>
                <Text>Mesh group</Text>
                <Value>-1</Value>
                <ValueType>ReinfMeshGroup</ValueType>
            </Parameter>
            <Parameter>
                <Name>MeshType</Name>
                <Text>Mesh type</Text>
                <Value>-1</Value>
                <ValueType>ReinfMeshType</ValueType>
            </Parameter>

            <Parameter>
                <Name>MeshBendingDirection</Name>
                <Text>Bending direction</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButtonLongitudinal</Name>
                    <Text>longitudinal</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>

                <Parameter>
                    <Name>RadioButtonCross</Name>
                    <Text>cross</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>MeshHookAngle</Name>
                <Text>Hook angle</Text>
                <Value>90</Value>
                <ValueType>Angle</ValueType>
            </Parameter>

            <Parameter>
                <Name>MeshHookType</Name>
                <Text>Hook type</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>MeshRadioButtonStirrup</Name>
                    <Text>Stirrup</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>MeshRadioButtonAngle</Name>
                    <Text>Angle</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>MeshRadioButtonAnchorage</Name>
                    <Text>Anchorage</Text>
                    <Value>3</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>MeshHookLength</Name>
                <Text>HookLength mesh</Text>
                <Value>-1</Value>
                <ValueType>ReinfHookLength</ValueType>
                <Constraint>MeshType;SteelGrade;ConcreteGrade;__ReinfHookType__ = MeshHookType;__ReinfMeshBendingDirection__ = MeshBendingDirection</Constraint>
            </Parameter>
        </Parameter>
    </Page>
</Element>
