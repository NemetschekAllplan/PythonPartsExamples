<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\ModifyObjects\ModifyWall.py</Name>
        <Title>ModifyWall</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>
    <Constants>

        <!-- Axis position types -->
        <Constant>
            <Name>LEFT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>CENTER</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>RIGHT</Name>
            <Value>4</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>FREE</Name>
            <Value>8</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>WALL_SELECTED</Name>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Constant>

        <!-- Button events -->
        <Constant>
            <Name>REVERSE_OFFSET_DIRECTION</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>

    </Constants>

    <Page>
        <Name>Page</Name>
        <Text>Page</Text>
        <Visible>InputMode == WALL_SELECTED</Visible>

        <Parameter>
            <Name>WallExpander</Name>
            <Text>Wall</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>TierCountRow</Name>
                <Text>Number of layers</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>TierCount</Name>
                    <Text>Integer</Text>
                    <Value>2</Value>
                    <ValueType>Integer</ValueType>
                    <MinValue>1</MinValue>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>AxisExpander</Name>
            <Text>Axis properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AxisPosition</Name>
                <Text>Axis position</Text>
                <Value>LEFT</Value>
                <ValueList>LEFT|CENTER|RIGHT|FREE</ValueList>
                <ValueTextList>Axis on the left|Axis in the center|Axis on the right|By offset</ValueTextList>
                <ValueList2>11249|11247|11245|10119</ValueList2>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>
            <Parameter>
                <Name>AxisOnTier</Name>
                <Text>Axis on layer</Text>
                <Value>1</Value>
                <ValueType>Integer</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>TierCount</MaxValue>
                <Visible>AxisPosition != FREE</Visible>
            </Parameter>
            <Parameter>
                <Name>AxisOffset</Name>
                <Text>Axis offset</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
                <MaxValue>sum(Thickness)</MaxValue>
                <Visible>AxisPosition == FREE</Visible>
            </Parameter>

            <Parameter>
                <Name>ReverseOffsetDirection</Name>
                <Text>Reverse offset direction</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>ReverseOffsetDirectionButton</Name>
                    <Text> </Text>
                    <Value>12451</Value>
                    <EventId>REVERSE_OFFSET_DIRECTION</EventId>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>WallTiersExpander</Name>
            <Text>Wall layers</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>TierIndex</Name>
                <Text>Select layer</Text>
                <Value>1</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>TierCount</MaxValue>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>Thickness</Name>
                <Text>Thickness</Text>
                <Value>[300.0,200.0]</Value>
                <ValueType>Double</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
            <Parameter>
                <Name>PlaneReferences</Name>
                <Text>Height</Text>
                <Value>[;]</Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
        </Parameter>


        <Parameter>
            <Name>FormatPropertiesExpander</Name>
            <Text>Format properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value>[;]</Value>
                <ValueType>CommonProperties</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SurfaceElementsExp</Name>
            <Text>Surface elements</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SurfaceElemProp</Name>
                <Text></Text>
                <Value>[;]</Value>
                <ValueType>SurfaceElementProperties</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>SurfaceRow</Name>
                <Text>Surface (Animation)</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsSurface</Name>
                    <Text>Surface</Text>
                    <Value>[False,False]</Value>
                    <ValueType>CheckBox</ValueType>
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>
                <Parameter>
                    <Name>SurfaceName</Name>
                    <Text>Surface</Text>
                    <Value>["",""]</Value>
                    <ValueType>MaterialButton</ValueType>
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>AttributesExpander</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Trade</Name>
                <Text>Trade</Text>
                <Value>[0,0]</Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>Trade</ValueDialog>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
            <Parameter>
                <Name>Priority</Name>
                <Text>Priority</Text>
                <Value>[100,100]</Value>
                <ValueType>Integer</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
            <Parameter>
                <Name>CalculationMode</Name>
                <Text>Calculation mode</Text>
                <Value>["m","m"]</Value>
                <ValueList>m³|m²|m|Pcs|kg</ValueList>
                <ValueType>StringComboBox</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
            <Parameter>
                <Name>Factor</Name>
                <Text>Factor</Text>
                <Value>[1.0, 1.0]</Value>
                <ValueType>Double</ValueType>
                <MinValue>0.0</MinValue>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
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
    </Page>
</Element>
