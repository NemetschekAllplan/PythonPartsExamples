<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\OptionalTags\TextDyn.py</Name>
        <Title>TextDyn</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>General</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>DynamicTextExpander</Name>
            <Text>Dynamic text selection</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>DimensionSel</Name>
                <Text>Select dimension text</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>Length</Name>
                    <Text>Length</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Width</Name>
                    <Text>Width</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Height</Name>
                    <Text>Height</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>DistanceHeader</Name>
                <Text>Select distance text</Text>
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>Top</Name>
                    <Text>Top</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Bottom</Name>
                    <Text>Bottom</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>DynamicControlTextExp</Name>
            <Text></Text>
            <TextDyn>
if not DimensionSel:
    return "Length expander"
if DimensionSel == 1:
    return "Width expander"
return "Height"
            </TextDyn>
            <Value>True</Value>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Dimension</Name>
                <Text>dynamic</Text>
                <TextDyn>
return "Length" if not DimensionSel else "Width" if DimensionSel == 1 else "Height"
                </TextDyn>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>DynamicHeaderText</Name>
            <Text>Distance expander</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Header</Name>
                <Text> </Text>
                <Value>dynamic</Value>
                <ValueTextDyn>__StringTable.get_string(1003, "Placement") + (" Bottom" if DistanceHeader else " Top")</ValueTextDyn>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>DistanceList</Name>
                <Text></Text>
                <TextDyn>
pre_text = "Bottom: " if DistanceHeader else "Top: "

if $list_row == 0:
    return pre_text + "Start"

if $list_row == len(DistanceList) - 1:
    return pre_text + "End"

return pre_text + str($list_row)
                </TextDyn>
                <Value>[1000,1500,1500,1200]</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>RadioButtonExp</Name>
            <Text>Radio button</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Angle</Name>
                <Text></Text>
                <TextDyn>
"Angle from bottom: " if DistanceHeader else "Angle from top"
                </TextDyn>
                <Value>45</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButton1</Name>
                    <Text>30°</Text>
                    <Value>30</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton2</Name>
                    <Text>45°</Text>
                    <Value>45</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton3</Name>
                    <Text>60°</Text>
                    <Value>60</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>ListGroupPage</Name>
        <Text>ListGroup</Text>

        <Parameter>
            <Name>SectionCount</Name>
            <Text>Section count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Parameter>

        <Parameter>
            <Name>SectionListGroup</Name>
            <ValueType>ListGroup</ValueType>
            <Parameter>
                <Name>SectionExpander</Name>
                <Text></Text>
                <TextDyn>str(SectionLength[$list_row])</TextDyn>
                <ValueType>Expander</ValueType>

                <Parameter>
                    <Name>SectionLength</Name>
                    <Text>Length</Text>
                    <Value>[1000,2000,3000]</Value>
                    <ValueType>Length</ValueType>
                    <Dimensions>SectionCount</Dimensions>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
