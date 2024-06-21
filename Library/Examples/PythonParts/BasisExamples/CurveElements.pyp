<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\CurveElements.py</Name>
        <Title>CurveElements</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>CurveElements</Text>

        <Parameter>
            <Name>CreatePythonPart</Name>
            <Text>Create PythonPart</Text>
            <Value>True</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>EndSymbolSettings</Name>
            <Text>End symbol settings</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>HasStartSymbol</Name>
                <Text>Start symbol</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>StartSymbolID</Name>
                <Text>Start symbol ID</Text>
                <Value>1</Value>
                <Visible>HasStartSymbol == 1</Visible>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>StartSymbolSize</Name>
                <Text>Start symbol size</Text>
                <Value>3.0</Value>
                <Visible>HasStartSymbol == 1</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>HasEndSymbol</Name>
                <Text>End symbol</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>EndSymbolID</Name>
                <Text>End symbol ID</Text>
                <Value>1</Value>
                <Visible>HasEndSymbol == 1</Visible>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>EndSymbolSize</Name>
                <Text>End symbol size</Text>
                <Value>3.0</Value>
                <Visible>HasEndSymbol == 1</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PatternCurveSettings</Name>
            <Text>Pattern curve settings</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>HasPatternCurve</Name>
                <Text>Pattern curve</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>PatternID</Name>
                <Text>Pattern ID</Text>
                <Value>-1</Value>
                <Visible>HasPatternCurve == 1</Visible>
                <ValueType>Pattern</ValueType>
            </Parameter>
            <Parameter>
                <Name>PatternHeight</Name>
                <Text>Pattern height</Text>
                <Value>100.0</Value>
                <Visible>HasPatternCurve == 1</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>PatternWidth</Name>
                <Text>Pattern width</Text>
                <Value>50.0</Value>
                <Visible>HasPatternCurve == 1</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Alignment</Name>
                <Text>Alignment</Text>
                <Value>Center</Value>
                <ValueList>Left|Center|Right</ValueList>
                <Visible>HasPatternCurve == 1</Visible>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Intersection</Name>
                <Text>Intersection</Text>
                <Value>Disabled</Value>
                <ValueList>Disabled|Miter|Joint|Seamless</ValueList>
                <Visible>HasPatternCurve == 1</Visible>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PlacementSettings</Name>
            <Text>Placement</Text>
            <ValueType>Expander</ValueType>
            <Visible>__is_input_mode()</Visible>

            <Parameter>
                <Name>GlobalPlacementPoint</Name>
                <Text>Global placement point</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
                <Persistent>Favorite</Persistent>
            </Parameter>

            <Parameter>
                <Name>PlacementPointRow</Name>
                <Text>_</Text>
                <ValueType>Row</ValueType>
                <Visible>GlobalPlacementPoint</Visible>

                <Parameter>
                    <Name>PlacementPoint</Name>
                    <Text>Placement point</Text>
                    <Value>Point2D(1000,2000)</Value>
                    <ValueType>Point2D</ValueType>
                    <Persistent>Favorite</Persistent>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>MultiPlacement</Name>
                <Text>Multi placement</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
                <Persistent>Favorite</Persistent>
            </Parameter>
        </Parameter>
    </Page>
</Element>
