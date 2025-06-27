<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>ReinforcementExamples\Labels\MeshLabelWithPointer.py</Name>
        <Title>MeshLabelWithPointer</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>LABEL_BY_POINT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>LABEL_BY_OFFSET</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Label</Text>
        <Parameters>
            <Parameter>
                <Name>Reinforcement</Name>
                <Text>Reinforcement</Text>
                <Value>False</Value>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>ConcreteGrade</Name>
                        <Text>Concrete grade</Text>
                        <Value>4</Value>
                        <ValueType>ReinfConcreteGrade</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>MeshGroup</Name>
                        <Text>Cross-section catalog</Text>
                        <Value>-1</Value>
                        <ValueType>ReinfMeshGroup</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>MeshType</Name>
                        <Text>Meshtype</Text>
                        <Value>Q257A</Value>
                        <ValueType>ReinfMeshType</ValueType>
                        <Constraint>MeshGroup</Constraint>
                    </Parameter>
                    <Parameter>
                        <Name>BendingRoller</Name>
                        <Text>Bending roller</Text>
                        <Value>4</Value>
                        <ValueType>ReinfBendingRoller</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>LabelExp</Name>
                <Text>Label position</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>RefPointPosition</Name>
                        <Text>Refrence point</Text>
                        <Value>AllplanPalette.RefPointPosition.eCenterLeft</Value>
                        <ValueType>RefPointButton</ValueType>
                        <EnumList2>AllplanPalette.RefPointButtonType.eAllNinePositions</EnumList2>
                    </Parameter>
                    <Parameter>
                        <Name>MeshPointerAutomatic</Name>
                        <Text>Mesh pointer automatic</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>LabelPositionDef</Name>
                        <Text>Define label position by</Text>
                        <Value>LABEL_BY_POINT</Value>
                        <ValueType>RadioButtonGroup</ValueType>
                        <Parameters>
                            <Parameter>
                                <Name>LabelPositionByPoint</Name>
                                <Text>point</Text>
                                <Value>LABEL_BY_POINT</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>LabelPositionByOffset</Name>
                                <Text>shape side and offset</Text>
                                <Value>LABEL_BY_OFFSET</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                    <Parameter>
                        <Name>Separator</Name>
                        <ValueType>Separator</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>LabelPoint</Name>
                        <Text>Label point</Text>
                        <Value>Point2D(1000, 500)</Value>
                        <XYZinRow>True</XYZinRow>
                        <ValueType>Point2D</ValueType>
                        <Visible>LabelPositionDef == LABEL_BY_POINT</Visible>
                    </Parameter>
                    <Parameter>
                        <Name>ShapeSide</Name>
                        <Text>Shape side</Text>
                        <Value>5</Value>
                        <MinValue>1</MinValue>
                        <MaxValue>6</MaxValue>
                        <ValueType>Integer</ValueType>
                        <Visible>LabelPositionDef == LABEL_BY_OFFSET</Visible>
                    </Parameter>
                    <Parameter>
                        <Name>ShapeSideFactor</Name>
                        <Text>Shape side factor</Text>
                        <Value>.5</Value>
                        <MinValue>0</MinValue>
                        <MaxValue>1</MaxValue>
                        <ValueType>Double</ValueType>
                        <Visible>LabelPositionDef == LABEL_BY_OFFSET</Visible>
                    </Parameter>
                    <Parameter>
                        <Name>LabelOffset</Name>
                        <Text>Label offset</Text>
                        <Value>Vector2D(500, 0)</Value>
                        <XYZinRow>True</XYZinRow>
                        <ValueType>Vector2D</ValueType>
                        <Visible>LabelPositionDef == LABEL_BY_OFFSET</Visible>
                    </Parameter>
                    <Parameter>
                        <Name>Angle</Name>
                        <Text>Angle</Text>
                        <Value>0</Value>
                        <ValueType>Angle</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>LabelPropertiesExpander</Name>
                <Text>Label properties</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>ShowPositionNumber</Name>
                        <Text>Show position number</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>ShowMeshType</Name>
                        <Text>Show mesh type</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>ShowMeshCount</Name>
                        <Text>Show bar count</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>ShowMeshDimensions</Name>
                        <Text>Show bar length</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>ShowPositionAtEnd</Name>
                        <Text>Show position at end</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>TextPointerExp</Name>
                <Text>Leader</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>ShowTextPointer</Name>
                        <Text>Text leader</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>AutomaticTextPointer</Name>
                        <Text>Automatic leader</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                        <Visible>ShowTextPointer</Visible>
                    </Parameter>
                    <Parameter>
                        <Name>PointerStartPoint</Name>
                        <Value>Point2D(0,300)</Value>
                        <ValueType>Point2D</ValueType>
                        <Visible>not AutomaticTextPointer</Visible>
                    </Parameter>
                    <Parameter>
                        <Name>PointerProperties</Name>
                        <Text></Text>
                        <Value></Value>
                        <ValueType>ReinfMeshLabelPointer</ValueType>
                        <Visible>ShowTextPointer</Visible>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
    <Page>
        <Name>TextPage</Name>
        <Text>Text properties</Text>
        <Parameters>
            <Parameter>
                <Name>MarkTextExp</Name>
                <Text>Label text</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>LabelTextProp</Name>
                        <Text></Text>
                        <Value></Value>
                        <ValueType>ReinfLabelText</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
</Element>