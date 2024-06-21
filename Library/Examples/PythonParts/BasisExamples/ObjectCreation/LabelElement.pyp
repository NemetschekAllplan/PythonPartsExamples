<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\ObjectCreation\LabelElement.py</Name>
        <Title>LabelElement</Title>
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
        <Text>Test</Text>
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
        </Parameter>

        <Parameter>
            <Name>AttributeListGroup</Name>
            <ValueType>ListGroup</ValueType>

            <Parameter>
                <Name>ParameterExp</Name>
                <Text>Attributes</Text>
                <TextDyn>GroupNames[$list_row]</TextDyn>
                <ValueType>Expander</ValueType>

                <Parameter>
                    <Name>AttributeListRow</Name>
                    <Text></Text>
                    <TextDyn>AttributeName[$list_row]</TextDyn>
                    <ValueType>Row</ValueType>

                    <Parameter>
                        <Name>Attributes</Name>
                        <Text></Text>
                        <TextDyn>"$Attribute_Name"</TextDyn>
                        <Value>[]</Value>
                        <ValueType>Attribute</ValueType>
                        <AttributeId>[]</AttributeId>
                        <Enable>False</Enable>
                        <Persistent>NO</Persistent>
                    </Parameter>

                    <Parameter>
                        <Name>AttributeLabel</Name>
                        <Text></Text>
                        <Value>[]</Value>
                        <ValueType>CheckBox</ValueType>
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
            <Value>[]</Value>
            <ValueType>String</ValueType>
            <Persistent>NO</Persistent>
        </Parameter>

        <Parameter>
            <Name>AttributeName</Name>
            <Text></Text>
            <Value>[]</Value>
            <ValueType>String</ValueType>
            <Persistent>NO</Persistent>
        </Parameter>

        <Parameter>
            <Name>GroupNames</Name>
            <Text></Text>
            <Value>[]</Value>
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
