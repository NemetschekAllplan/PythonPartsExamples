<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\Column.py</Name>
        <Title>Column</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Page</Text>
        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\ShapeGeometryProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>
        <Parameter>
            <Name>PlaneReferences</Name>
            <Text>Height</Text>
            <Value></Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
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
            <Name>SurfaceElementsExp</Name>
            <Text>Surface elements</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SurfaceElemProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>SurfaceElementProperties</ValueType>
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
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SurfaceName</Name>
                    <Text>Surface</Text>
                    <Value></Value>
                    <ValueType>MaterialButton</ValueType>
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
