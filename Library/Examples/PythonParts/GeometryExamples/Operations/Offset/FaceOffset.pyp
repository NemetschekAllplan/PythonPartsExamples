<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\Offset\FaceOffset.py</Name>
        <Title>Face offset</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>FaceOffset</Name>
        <Text>Face offset</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>solids and surfaces</Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>FilletPropertiesExpander</Name>
            <Text>Options of FaceOffset</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>OffsetSelectedFaces</Name>
                <Text>Faces to consider</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>OptionOffsetAll</Name>
                    <Text>all</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>OptionOffsetSelected</Name>
                    <Text>selected</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>FacesToOffset</Name>
                <Text>Faces indices</Text>
                <Value>1,2</Value>
                <ValueType>String</ValueType>
                <Visible>OffsetSelectedFaces == 1</Visible>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>CalculationType</Name>
                <Text>Calculate</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>OptionCalculateOffset</Name>
                    <Text>offset</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>OptionCalculateShell</Name>
                    <Text>shell</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>OffsetDistance</Name>
                <Text>Distance</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>OffsetDirection</Name>
                <Text>Direction</Text>
                <Value>eNormalDirection</Value>
                <ValueList>"|".join(str(key) for key in AllplanGeo.FaceOffset.eFaceOffsetDirection.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>PunchDirection</Name>
                <Text>Punch direction (optional)</Text>
                <Value>Vector3D()</Value>
                <ValueType>Vector3D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Enable>OffsetSelectedFaces</Enable>
            </Parameter>
            <Parameter>
                <Name>UseOffsetStepPierce</Name>
                <Text>Use offset step pierce</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
                <Enable>PunchDirection.X + PunchDirection.Y + PunchDirection.Z == 0.0 and OffsetSelectedFaces</Enable>
            </Parameter>
            <Parameter>
                <Name>UseOrthoVXSplit</Name>
                <Text>Use ortho VX split</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>CommonPropertiesExpander</Name>
            <Text>Common porperties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonPropertiesFromSourceObject</Name>
                <Text>From source object</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
                <Visible>not CommonPropertiesFromSourceObject</Visible>
            </Parameter>
            <Parameter>
                <Name>CommonProperties</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>not CommonPropertiesFromSourceObject</Visible>
            </Parameter>

        </Parameter>
    </Page>
</Element>
