<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\BarPlacement\ExtrudeBarAlongPath.py</Name>
        <Title>ExtrudeBarAlongPath</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Geometry</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>Geometry</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>RampRadius</Name>
                <Text>Ramp radius</Text>
                <Value>5000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RampHeight</Name>
                <Text>Ramp height</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>PlateWidth</Name>
                <Text>Plate width</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>PlateHeight</Name>
                <Text>Plate height</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Path</Name>
            <Text>Path</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>BreakElimination</Name>
                <Text>Break elimination</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>MaxBreakAngle</Name>
                <Text>Max break angle</Text>
                <Value>25</Value>
                <ValueType>Angle</ValueType>
                <Visible>BreakElimination</Visible>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>PreviewColor</Name>
            <Text>Preview color</Text>
            <Value>5</Value>
            <ValueType>Color</ValueType>
            <Persistent>FAVORITE</Persistent>
        </Parameter>
    </Page>

    <Page>
        <Name>CrossBar</Name>
        <Text>Cross bar</Text>

        <Parameter>
            <Name>Bar</Name>
            <Text>Bar</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>4</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>Diameter</Name>
                <Text>Bar diameter</Text>
                <Value>10.0</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>30.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>Distance</Name>
                <Text>Bar distance</Text>
                <Value>200</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>BendingRoller</Name>
                <Text>Bending roller</Text>
                <Value>4.0</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Placement</Name>
            <Text>Placement</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ProfileRotation</Name>
                <Text>Profile rotation</Text>
                <Value>Z-Axis</Value>
                <ValueList>No rotation|Standard|Z-Axis</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCoverStart</Name>
                <Text>Concreate cover start</Text>
                <Value>50</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCoverEnd</Name>
                <Text>Concreate cover end</Text>
                <Value>50</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>

            <Parameter>
                <Name>EdgeOffsetType</Name>
                <Text>Edge offset</Text>
                <Value>0</Value>
                <ValueList>0|1|2|3|4</ValueList>
                <ValueTextList>Zero at start|Major value at start|Start equal end|Major at end|Zero at end</ValueTextList>
                <ValueList2>12145|12147|12149|12151|12153</ValueList2>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>
            <Parameter>
                <Name>EdgeOffsetStart</Name>
                <Text>Edge offset start</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Enable>EdgeOffsetType == 1</Enable>
            </Parameter>
            <Parameter>
                <Name>EdgeOffsetEnd</Name>
                <Text>Edge offset end</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Enable>EdgeOffsetType == 3</Enable>
            </Parameter>
            <Parameter>
                <Name>BarOffset</Name>
                <Text>Bar offset</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SectionExpander</Name>
            <Text>Sections</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SectionsHeaderRow</Name>
                <Text></Text>
                <Value>1</Value>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>SectionEnable</Name>
                    <Text> </Text>
                    <Value>Enable</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SectionLength</Name>
                    <Text> </Text>
                    <Value>Length</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SectionDistance</Name>
                    <Text> </Text>
                    <Value>Distance</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>SectionsRow</Name>
                <Value>1</Value>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>Sections</Name>
                    <Text></Text>
                    <Value>[False|0|0;
                            False|0|0;
                            False|0|0;
                            False|0|0]
                    </Value>
                    <ValueType>namedtuple(CheckBox,Length,Length)</ValueType>
                    <NamedTuple>
                        <TypeName>Sections</TypeName>
                        <FieldNames>IsEnabled,Length,Distance</FieldNames>
                    </NamedTuple>
                    <ValueListStartRow>1</ValueListStartRow>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>LongitudinalBar</Name>
        <Text>LongitudinalBar bar</Text>

        <Parameter>
            <Name>LongitudinalSteelGrade</Name>
            <Text>Steel grade</Text>
            <Value>4</Value>
            <ValueType>ReinfSteelGrade</ValueType>
        </Parameter>
        <Parameter>
            <Name>LongitudinalDiameter</Name>
            <Text>Bar diameter</Text>
            <Value>28.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
        </Parameter>
        <Parameter>
            <Name>IsOverlappingAtStart</Name>
            <Text>Is overlapping at start</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>OverlappingAtStart</Name>
            <Text>Overlapping at start</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <Enable>IsOverlappingAtStart</Enable>
        </Parameter>
        <Parameter>
            <Name>IsOverlappingAtEnd</Name>
            <Text>Is oerlapping at end</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>OverlappingAtEnd</Name>
            <Text>Overlapping at end</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <Enable>IsOverlappingAtEnd</Enable>
        </Parameter>
        <Parameter>
            <Name>OverlappingLength</Name>
            <Text>Overlapping length</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>StartLength</Name>
            <Text>Start length</Text>
            <Value>14000</Value>
            <ValueType>Length</ValueType>
            <MinValue>0.1</MinValue>
        </Parameter>
        <Parameter>
            <Name>DeliveryShapeType</Name>
            <Text>Delivery shape type</Text>
            <Value>Round</Value>
            <ValueList>Straight|Round</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>InsideBarsState</Name>
            <Text>Inside bars state</Text>
            <Value>Exact</Value>
            <ValueList>Exact|Shortened|Overlapped</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
    </Page>
</Element>