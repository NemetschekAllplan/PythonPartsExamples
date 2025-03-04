<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Layout\NestedExpanders.py</Name>
        <Title>Nested Expanders</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page1</Text>

        <Parameter>
            <Name>CommonPropertiesExp</Name>
            <Text>Common Properties</Text>
            <ValueType>Expander</ValueType>
            <Value>True</Value> <!-- Should this expander be collapsed-->

            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value>CommonProperties(Color(3))</Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ExpanderBottomColumns</Name>
            <Text>Bottom columns (Expander level 1)</Text>
            <Value>False</Value> <!-- Should this expander be collapsed-->
            <ValueType>Expander</ValueType>
            <Visible>HideBottomColumns == False</Visible>

            <Parameter>
                <Name>ExpanderBottomLeftColumn</Name>
                <Text>Left Column (Expander level 2)</Text>
                <Value>False</Value> <!-- Should this expander be collapsed-->
                <ValueType>Expander</ValueType>                
                
                <Parameter>
                    <Name>GeometryBottomLeftExp</Name>
                    <Text>Geometry (Expander level 3)</Text>
                    <ValueType>Expander</ValueType>
                    <Value>False</Value> <!-- Should this expander be collapsed-->
                    
                    <Parameter>
                        <Name>Width1_1</Name>
                        <Text>Width of left column</Text>                    
                        <Value>2000.</Value>
                        <ValueType>Length</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>Depth1_1</Name>
                        <Text>Depth of left column</Text>                    
                        <Value>1000.</Value>
                        <ValueType>Length</ValueType>
                    </Parameter>
                </Parameter>

                <Parameter>
                    <Name>SurfacePropBottomLeftExp</Name>
                    <Text>Surface Properties (Expander level 3)</Text>
                    <ValueType>Expander</ValueType>
                    <Value>True</Value> <!-- Should this expander be collapsed-->
                    <Visible>HideSurfaceProperties == False</Visible>

                    <Parameter>
                        <Name>SurfacePropBottomLeft</Name>
                        <Text></Text>
                        <Value></Value>
                        <ValueType>SurfaceElementProperties</ValueType>
                    </Parameter>
                </Parameter>                
            </Parameter>

            <Parameter>
                <Name>ExpanderBottomRightColumn</Name>
                <Text>Right Column (Expander level 2)</Text>
                <Value>False</Value> <!-- Should this expander be collapsed-->
                <ValueType>Expander</ValueType>                
                
                <Parameter>
                    <Name>Width1_2</Name>
                    <Text>Width of right column</Text>                    
                    <Value>1000.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Depth1_2</Name>
                    <Text>Depth of right column</Text>                    
                    <Value>2000.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>

                <Parameter>
                    <Name>SurfacePropBottomRightExp</Name>
                    <Text>Surface Properties (Expander level 3)</Text>
                    <ValueType>Expander</ValueType>
                    <Value>True</Value> <!-- Should this expander be collapsed-->
                    <Visible>HideSurfaceProperties == False</Visible>

                    <Parameter>
                        <Name>SurfacePropBottomRight</Name>
                        <Text></Text>
                        <Value></Value>
                        <ValueType>SurfaceElementProperties</ValueType>
                    </Parameter>
                </Parameter>                
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ExpanderTopColumns</Name>
            <Text>Top columns (Expander level 1)</Text>
            <Value>True</Value> <!-- Should this expander be collapsed-->
            <ValueType>Expander</ValueType>
            <Visible>HideTopColumns == False</Visible>

            <Parameter>
                <Name>Width2</Name>
                <Text>Width of top columns</Text>                    
                <Value>1500.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Depth2</Name>
                <Text>Depth of top columns</Text>                    
                <Value>1500.</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>SurfacePropTopExp</Name>
                <Text>Surface Properties (Expander level 2)</Text>
                <ValueType>Expander</ValueType>
                <Value>False</Value> <!-- Should this expander be collapsed-->
                <Visible>HideSurfaceProperties == False</Visible>

                <Parameter>
                    <Name>SurfacePropTop</Name>
                    <Text></Text>
                    <Value></Value>
                    <ValueType>SurfaceElementProperties</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TextPropertiesExp</Name>
            <Text>Text Properties</Text>
            <ValueType>Expander</ValueType>
            <Value>True</Value> <!-- Should this expander be collapsed-->
            
            <Parameter>
                <Name></Name>
                <Text></Text>
                <Value>etc\PythonPartsFramework\ParameterIncludes\TextProperties.incl</Value>
                <ValueType>Include</ValueType>
                <Visible>HideTextProperties == False</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ChangeVisibilityExp</Name>
            <Text>Expanders visibility</Text>
            <ValueType>Expander</ValueType>
            <Value>False</Value> <!-- Should this expander be collapsed-->

            <Parameter>
                <Name>HideBottomColumns</Name>
                <Text>Hide expander Bottom Columns</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>HideTopColumns</Name>
                <Text>Hide expander Top Columns</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>HideSurfaceProperties</Name>
                <Text>Hide expanders Surface Properties</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>HideTextProperties</Name>
                <Text>Hide expander Text Properties</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
