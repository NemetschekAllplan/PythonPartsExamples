<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Resources\Font.py</Name>
        <Title>Font</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Font</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>|CommonProp.Stroke:False|CommonProp.StrokeByLayer:False</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>FontExp</Name>
            <Text>Font</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>FontId</Name>
                <Text>Font ID</Text>
                <Value>21</Value>
                <ValueType>Font</ValueType>
            </Parameter>
            <Parameter>
                <Name>FontEmphasis</Name>
                <Text>Emphasis</Text>
                <Value>0</Value>
                <ValueType>FontEmphasis</ValueType>
                <Constraint>FontId</Constraint>
            </Parameter>
            <Parameter>
                <Name>FontAngle</Name>
                <Text>Angle for italic text</Text>
                <Value>90</Value>
                <ValueType>Angle</ValueType>
                <Constraint>FontId;FontEmphasis</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>FontConditionExp</Name>
            <Text>Font with visible condition</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>FontIdCond</Name>
                <Text>Font ID</Text>
                <Value>21</Value>
                <ValueType>Font</ValueType>
            </Parameter>
            <Parameter>
                <Name>FontEmphasisCond</Name>
                <Text>Emphasis</Text>
                <Value>0</Value>
                <ValueType>FontEmphasis</ValueType>
                <Visible>|FontEmphasisCond.CrossedOut:False</Visible>
                <Constraint>FontId</Constraint>
            </Parameter>
            <Parameter>
                <Name>FontAngleCond</Name>
                <Text>Angle for italic text</Text>
                <Value>90</Value>
                <ValueType>Angle</ValueType>
                <Constraint>FontIdCond;FontEmphasisCond</Constraint>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>List</Name>
        <Text>List</Text>

        <Parameter>
            <Name>FontListExp</Name>
            <Text>Font list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>FontCount</Name>
                <Text>Count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>FontSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>FontListGroup</Name>
                <ValueType>ListGroup</ValueType>

                <Parameter>
                    <Name>FontIdList</Name>
                    <Text></Text>
                    <TextDyn>"Font " + str($list_row + 1)</TextDyn>
                    <Value>[21,22,23]</Value>
                    <ValueType>Font</ValueType>
                    <Dimensions>FontCount</Dimensions>
                </Parameter>
                <Parameter>
                    <Name>FontEmphasisList</Name>
                    <Text></Text>
                    <TextDyn>"Emphasis " + str($list_row + 1)</TextDyn>
                    <Value>[1,2,4]</Value>
                    <ValueType>FontEmphasis</ValueType>
                    <Dimensions>FontCount</Dimensions>
                    <Constraint>FontIdList</Constraint>
                </Parameter>
                <Parameter>
                    <Name>FontAngleList</Name>
                    <Text>"Angle for italic text " + str($list_row + 1)</Text>
                    <Value>[90,90,90]</Value>
                    <ValueType>Angle</ValueType>
                    <Dimensions>FontCount</Dimensions>
                    <Constraint>FontIdList;FontEmphasisList</Constraint>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
