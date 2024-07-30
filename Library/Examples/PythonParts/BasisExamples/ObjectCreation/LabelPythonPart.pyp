<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\ObjectCreation\LabelPythonPart.py</Name>
        <Title>LabelPythonPart</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>ELEMENT_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>ELEMENT_LABEL</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Label</Text>
        <Visible>InputMode == ELEMENT_LABEL</Visible>

        <Parameter>
            <Name>LabelExp</Name>
            <Text>Label</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Frame</Name>
                <Text>Frame</Text>
                <Value>2</Value>
                <ValueList>0|1|2|3|4|5</ValueList>
                <ValueList2>9005|10903|10893|10897|11151|11149</ValueList2>
                <ValueType>PictureResourceComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>AddParameterText</Name>
                <Text>Add parameter text</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ParameterExp</Name>
            <Text>Parameter</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ParameterListGroup</Name>
                <ValueType>ListGroup</ValueType>

                <Parameter>
                    <Name>ParameterListRow</Name>
                    <Text></Text>
                    <TextDyn>ParameterText[$list_row]</TextDyn>
                    <ValueType>Row</ValueType>

                    <Parameter>
                        <Name>Parameters</Name>
                        <Text></Text>
                        <Value>[_]</Value>
                        <ValueType>AnyValueByType</ValueType>
                        <Enable>False</Enable>
                        <Persistent>NO</Persistent>
                    </Parameter>

                    <Parameter>
                        <Name>ParameterLabel</Name>
                        <Text></Text>
                        <Value>[_]</Value>
                        <ValueType>CheckBox</ValueType>
                        <Persistent>NO</Persistent>
                    </Parameter>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Text</Name>
        <Text>Text</Text>
        <Visible>InputMode == ELEMENT_LABEL</Visible>

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
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>

        <Parameter>
            <Name>ParameterText</Name>
            <Text></Text>
            <Value>[_]</Value>
            <ValueType>String</ValueType>
            <Persistent>NO</Persistent>
        </Parameter>

        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
