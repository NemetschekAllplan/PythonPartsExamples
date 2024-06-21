<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\Wall.py</Name>
        <Title>Wall</Title>
        <Version>1.0</Version>
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


        <Parameter>
            <Name>WallExpander</Name>
            <Text>Wall</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>TierCountRow</Name>
                <Text>Number of tiers</Text>
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
                <ValueType>PictureButtonList</ValueType>
            </Parameter>
            <Parameter>
                <Name>AxisOnTier</Name>
                <Text>Axis on tier</Text>
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
            <Text>Wall tiers</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>TierIndex</Name>
                <Text>Select tier</Text>
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
            <Name>SurfaceElementsExpander</Name>
            <Text>Surface elements</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>HatchRow</Name>
                <Text>Hatch</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UseHatch</Name>
                    <Text> </Text>
                    <Value>[True,False]</Value>
                    <ValueType>CheckBox</ValueType>
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>

                <Parameter>
                    <Name>Hatch</Name>
                    <Text>Hatching</Text>
                    <Value>[303,1]</Value>
                    <ValueType>Hatch</ValueType>
                    <!-- <Enable>UseHatch</Enable> -->
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PatternRow</Name>
                <Text>Pattern</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UsePattern</Name>
                    <Text> </Text>
                    <Value>[False,True]</Value>
                    <ValueType>CheckBox</ValueType>
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>

                <Parameter>
                    <Name>Pattern</Name>
                    <Text>Pattern</Text>
                    <Value>[1,301]</Value>
                    <ValueType>Pattern</ValueType>
                    <!-- <Enable>UsePattern</Enable> -->
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>FillingRow</Name>
                <Text>Filling</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UseFilling</Name>
                    <Text> </Text>
                    <Value>[False,False]</Value>
                    <ValueType>CheckBox</ValueType>
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>

                <Parameter>
                    <Name>Filling</Name>
                    <Text>Filling</Text>
                    <Value>[7,7]</Value>
                    <ValueType>Color</ValueType>
                    <!-- <Enable>UseFilling</Enable> -->
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>FaceStyleRow</Name>
                <Text>FaceStyle</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UseFaceStyle</Name>
                    <Text> </Text>
                    <Value>[False,False]</Value>
                    <ValueType>CheckBox</ValueType>
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>

                <Parameter>
                    <Name>FaceStyle</Name>
                    <Text>FaceStyle</Text>
                    <Value>[301,301]</Value>
                    <ValueType>FaceStyle</ValueType>
                    <!-- <Enable>UseFaceStyle</Enable> -->
                    <Dimensions>TierCount</Dimensions>
                    <ValueIndexName>TierIndex</ValueIndexName>
                </Parameter>

            </Parameter>

            <Parameter>
                <Name>ShowAreaElementInGroundView</Name>
                <Text>Show in plan view</Text>
                <Value>[True,True]</Value>
                <ValueType>CheckBox</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>

            <Parameter>
                <Name>Surface</Name>
                <Text>Surface</Text>
                <Value>["",""]</Value>
                <ValueType>MaterialButton</ValueType>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
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
</Element>