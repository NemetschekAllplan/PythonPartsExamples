<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\Labels\LabelWithDimensionLine.py</Name>
        <Title>Label with dimension line</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Label</Text>

        <Parameter>
            <Name>ReinforcementLabelExpander</Name>
            <Text>Reinforcement label</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DimLineOffset</Name>
                <Text>Dimension line offset</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>DimLineAtShapeStart</Name>
                <Text>Dimension line at shape start</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>SetLabelOffsetRow</Name>
                <Text>Set label offset</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>SetLabelOffset</Name>
                    <Value>True</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>LabelOffset</Name>
                    <Text>Label offset</Text>
                    <Value>Vector2D(0, 200)</Value>
                    <ValueType>Vector2D</ValueType>
                    <Visible>SetLabelOffset</Visible>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>SetVisibleBarsRow</Name>
                <Text>Set visible bars</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>SetVisibleBars</Name>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>VisibleBars</Name>
                    <Text>Label offset</Text>
                    <Value>1,2,0,-2,-1</Value>
                    <ValueType>String</ValueType>
                    <Visible>SetVisibleBars</Visible>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>ShowAllBars</Name>
                <Text>Show all bars</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
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
                <Name>ShowBarDistance</Name>
                <Text>Show bar distance</Text>
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
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>TextPropertiesExpander</Name>
            <Text>Text properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>TextAlignment</Name>
                <Text>Text alignment</Text>
                <Value>eLeftBottom</Value>
                <ValueList>"|".join(str(key) for key in AllplanBasisEle.TextAlignment.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
