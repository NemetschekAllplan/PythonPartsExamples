<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\Labels\LabelWithFan.py</Name>
        <Title>Label with dimension line</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Label</Text>

        <Parameter>
            <Name>ReinforcementLabelExpander</Name>
            <Text>Reinforcement label</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LabelPoint</Name>
                <Text>Label point</Text>
                <Value>Point2D(400, 250)</Value>
                <XYZinRow>True</XYZinRow>
                <ValueType>Point2D</ValueType>
            </Parameter>

            <Parameter>
                <Name>Angle</Name>
                <Text>Angle</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowTextPointer</Name>
                <Text>Show text pointer</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowTextPointerEndSymbol</Name>
                <Text>Show text pointer end symbol</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
                <Visible>ShowTextPointer</Visible>
            </Parameter>

            <Parameter>
                <Name>AdditionalTextRow</Name>
                <Text>Set additional text</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>SetAdditionalText</Name>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>AdditionalText</Name>
                    <Value></Value>
                    <ValueType>String</ValueType>
                    <Visible>SetAdditionalText</Visible>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ReinforcementLabelPropertiesExpander</Name>
            <Text>Reinforcement label properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ShowPositionNumber</Name>
                <Text>Show position number</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowBarDiameter</Name>
                <Text>Show bar diameter</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowBarCount</Name>
                <Text>Show bar count</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowBendingShape</Name>
                <Text>Show bending shape</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowBarPlace</Name>
                <Text>Show bar place</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowBarLength</Name>
                <Text>Show bar length</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowSteelGrade</Name>
                <Text>Show steel grade</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowPositionAtEnd</Name>
                <Text>Show position at end</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShowTwoLineText</Name>
                <Text>Show two line text</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
                <Enable>False</Enable>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>TextPropertiesExpander</Name>
            <Text>Text properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>TextAlignment</Name>
                <Text>Text alignment</Text>
                <Value>eLeftMiddle</Value>
                <ValueList>"|".join(str(key) for key in AllplanBasisEle.TextAlignment.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
