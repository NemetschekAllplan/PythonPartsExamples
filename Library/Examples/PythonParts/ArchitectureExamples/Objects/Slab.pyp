<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\Slab.py</Name>
        <Title>Slab</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page</Name>
        <Text>Page</Text>

        <Parameter>
            <Name>HeightExpander</Name>
            <Text>Height</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PlaneReferences</Name>
                <Text>Height</Text>
                <Value></Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>FormatPropertiesExpander</Name>
            <Text>Format properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
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
                    <Value>True</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Hatch</Name>
                    <Text>Hatching</Text>
                    <Value>-1</Value>
                    <ValueType>Hatch</ValueType>
                    <Enable>UseHatch</Enable>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PatternRow</Name>
                <Text>Pattern</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UsePattern</Name>
                    <Text> </Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Pattern</Name>
                    <Text>Pattern</Text>
                    <Value>-1</Value>
                    <ValueType>Pattern</ValueType>
                    <Enable>UsePattern</Enable>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>FillingRow</Name>
                <Text>Filling</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UseFilling</Name>
                    <Text> </Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Filling</Name>
                    <Text>Filling</Text>
                    <Value>7</Value>
                    <ValueType>Color</ValueType>
                    <Enable>UseFilling</Enable>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>FaceStyleRow</Name>
                <Text>FaceStyle</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>UseFaceStyle</Name>
                    <Text> </Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>

                <Parameter>
                    <Name>FaceStyle</Name>
                    <Text>FaceStyle</Text>
                    <Value>-1</Value>
                    <ValueType>FaceStyle</ValueType>
                    <Enable>UseFaceStyle</Enable>

                </Parameter>

            </Parameter>

            <Parameter>
                <Name>ShowAreaElementInGroundView</Name>
                <Text>Show in plan view</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>Surface</Name>
                <Text>Surface</Text>
                <Value></Value>
                <ValueType>MaterialButton</ValueType>
                <DisableButtonIsShown>True</DisableButtonIsShown>
            </Parameter>

        </Parameter>
        <Parameter>
            <Name>AttributesExpander</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Trade</Name>
                <Text>Trade</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>Trade</ValueDialog>
            </Parameter>
            <Parameter>
                <Name>Priority</Name>
                <Text>Priority</Text>
                <Value>100</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>CalculationMode</Name>
                <Text>Calculation mode</Text>
                <Value>2</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>120</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Factor</Name>
                <Text>Factor</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
                <MinValue>0.0</MinValue>
            </Parameter>
        </Parameter>

    </Page>
</Element>
