<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\Labels\LabelBarPlacement.py</Name>
        <Title>LabelBarPlacement</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>ELEMENT_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>LABEL_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>LABEL_POSITION_BY_POINT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>LABEL_POSITION_BY_OFFSET</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>

    <Page>
        <Name>DimensionLine</Name>
        <Text>Dimension line</Text>
        <Visible>InputMode == LABEL_INPUT</Visible>

        <Parameter>
            <Name>ReinforcementLabelExpander</Name>
            <Text>Dimension line placement</Text>
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
       </Parameter>

        <Parameter>
            <Name>DimLine</Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\Reinforcement\DimensionLineProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>DimLine</Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\Reinforcement\LabelProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>TextPropertiesExpander</Name>
            <Text>Text properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>TextAlignmentDimLine</Name>
                <Text>Text alignment</Text>
                <Value>eLeftBottom</Value>
                <ValueList>"|".join(str(key) for key in AllplanBasisEle.TextAlignment.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Pointer</Name>
        <Text>Pointer</Text>
        <Visible>InputMode == LABEL_INPUT</Visible>

        <Parameter>
            <Name>ReinforcementLabelExpander2</Name>
            <Text>Pointer placement</Text>
            <ValueType>Expander</ValueType>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\Reinforcement\TextPointerProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>Pointer</Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\Reinforcement\LabelProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>TextPropertiesExpander2</Name>
            <Text>Text properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>PointerTextAlignment</Name>
                <Text>Text alignment</Text>
                <Value>eLeftBottom</Value>
                <ValueList>"|".join(str(key) for key in AllplanBasisEle.TextAlignment.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>ElementTierCount</Name>
            <Text>Element tier count</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
