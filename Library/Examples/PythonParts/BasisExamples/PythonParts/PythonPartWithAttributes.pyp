<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
<Script>
    <Name>BasisExamples\PythonParts\PythonPartWithAttributes.py</Name>
    <Title>PythonPart with attributes</Title>
    <Version>1.0</Version>
    <AttributeEvent>True</AttributeEvent>
    <ReadLastInput>True</ReadLastInput>
    <ModifyBySingleClick>False</ModifyBySingleClick>
</Script>
<Page>
    <Name>PythonPart</Name>
    <Text>PythonPart</Text>
    <Parameters>
        <Parameter>
            <Name>GeometryExpander</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>Dimensions</Name>
                    <Text>Length,Width,Height</Text>
                    <Value>Vector3D(1000,1000,1000)</Value>
                    <ValueType>Vector3D</ValueType>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>CommonPropsExpander</Name>
            <Text>Common properties</Text>
            <Value>True</Value>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>CommonProp</Name>
                    <Text/>
                    <Value/>
                    <ValueType>CommonProperties</ValueType>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>DrawingTypeExp</Name>
            <Text>Drawing type</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>AllDrawingTypesRow</Name>
                    <Text>All drawing types</Text>
                    <ValueType>Row</ValueType>
                    <Parameters>
                        <Parameter>
                            <Name>AllDrawingTypes</Name>
                            <Text></Text>
                            <Value>True</Value>
                            <ValueType>CheckBox</ValueType>
                        </Parameter>
                        <Parameter>
                            <Name>ScaleDependent</Name>
                            <Text></Text>
                            <Value>Scale dependent</Value>
                            <ValueType>Text</ValueType>
                        </Parameter>
                    </Parameters>
                </Parameter>
                <Parameter>
                    <Name>DrawingTypesListGroup</Name>
                    <ValueType>ListGroup</ValueType>
                    <Parameters>
                        <Parameter>
                            <Name>DrawingTypesRow</Name>
                            <TextDyn>" " * ($list_row + 1)</TextDyn>
                            <ValueType>Row</ValueType>
                            <Visible>not AllDrawingTypes</Visible>
                            <Parameters>
                                <Parameter>
                                    <Name>DrawingTypes</Name>
                                    <Text></Text>
                                    <Value>[False] * 10</Value>
                                    <ValueType>CheckBox</ValueType>
                                </Parameter>
                                <Parameter>
                                    <Name>DrawingTypesText</Name>
                                    <Text></Text>
                                    <Value>["Schematic design drawing", "Design drawing", "Building drawing", "Working drawing", "Presentation drawing", "KeyPlan", "GeneralArrangement drawing", "Reinforcement drawing", "Building alteration drawing", "Building alteration drawing colored"]</Value>
                                    <ValueType>Text</ValueType>
                                </Parameter>
                            </Parameters>
                        </Parameter>
                    </Parameters>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>AttributesExpander</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>AppendGeometryAttributes</Name>
                    <Text>Append geometry attributes</Text>
                    <Value>True</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>LayerThickness</Name>
                    <Text>Layer thickness</Text>
                    <Value>300</Value>
                    <MaxValue>Dimensions.Z</MaxValue>
                    <ValueType>Attribute</ValueType>
                    <AttributeId>AttributeIdEnums.LAYER_THICKNESS</AttributeId>
                </Parameter>
                <Parameter>
                    <Name>Separator</Name>
                    <ValueType>Separator</ValueType>
                </Parameter>
                <Parameter>
                    <Name>OtherAttributesText</Name>
                    <Text>Append other attributes:</Text>
                    <Value/>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>DynamicAttributeList</Name>
                    <Text>Attributes</Text>
                    <Value>[(AttributeIdEnums.FIRE_RISK_FACTOR,A1);(0,)]</Value>
                    <ValueType>AttributeIdValue</ValueType>
                    <ValueDialog>AttributeSelection</ValueDialog>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>CopyExpander</Name>
            <Text>Copies</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>NumberOfCopies</Name>
                    <Text>Number of copies</Text>
                    <Value>1</Value>
                    <ValueType>Integer</ValueType>
                    <Persistent>FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>Distance</Name>
                    <Text>Distance</Text>
                    <Value>Vector3D(0, 2000, 0)</Value>
                    <ValueType>Vector3D</ValueType>
                    <XYZinRow>True</XYZinRow>
                    <Visible>NumberOfCopies &gt; 1</Visible>
                    <Persistent>FAVORITE</Persistent>
                </Parameter>
            </Parameters>
        </Parameter>
    </Parameters>
</Page>
</Element>
