<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\Objects\Label.py</Name>
        <Title>Label</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Label</Text>

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
            <Name>VolumeExpander</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>500.</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreatePythonPart</Name>
                <Text>Create PythonPart</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ParameterLabel</Name>
            <Text>Parameter label</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ParameterName</Name>
                <Text>Parameter</Text>
                <Value>Length</Value>
                <ValueList>Length|Width|Height</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Frame</Name>
                <Text>Frame</Text>
                <Value>2</Value>
                <ValueList>0|1|2|3|4|5</ValueList>
                <ValueList2>9005|10903|10893|10897|11151|11149</ValueList2>
                <ValueType>PictureResourceComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>AttributeID</Name>
            <Text>Attribute labels</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AttributeList</Name>
                <Text>Attributes</Text>
                <Value>[(498,Box);(0,)]</Value>
                <ValueType>AttributeIdValue</ValueType>
                <ValueDialog>AttributeSelectionInsert</ValueDialog>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Text</Name>
        <Text>Text</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>TextCommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>|CommonProp.Stroke:False|CommonProp.StrokeByLayer:False</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\TextProperties.incl</Value>
            <ValueType>Include</ValueType>
            <Visible>Alignment:False</Visible>
        </Parameter>
    </Page>
</Element>
