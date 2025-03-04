<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\SlabFoundation.py</Name>
        <Title>Slab Foundation</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page</Name>
        <Text>Page</Text>

        <Parameter>
            <Name>SlabExpander</Name>
            <Text>Slab Foundation</Text>
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
            <Parameter>
                    <Name>VariableTier</Name>
                    <Text>Variable layer</Text>
                    <Value>1</Value>
                    <ValueType>Integer</ValueType>
                    <MinValue>1</MinValue>
                </Parameter>
            <Parameter>
                <Name>PlaneReferences</Name>
                <Text>Height</Text>
                <Value></Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SlabTiersExpander</Name>
            <Text>Slab foundation tiers</Text>
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
                <Name>Thickness</Name>
                <Text>Thickness</Text>
                <Value>[160,160]</Value>
                <ValueType>Double</ValueType>
                <MinValue>1.0</MinValue>
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
                <Value>[1.0,1.0]</Value>
                <ValueType>Double</ValueType>
                <MinValue>0.0</MinValue>
                <Dimensions>TierCount</Dimensions>
                <ValueIndexName>TierIndex</ValueIndexName>
            </Parameter>
        </Parameter>


    </Page>
</Element>
