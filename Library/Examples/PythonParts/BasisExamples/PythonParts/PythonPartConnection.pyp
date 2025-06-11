<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd'>
    <Script>
        <Title>PythonPartConnection</Title>
        <Name>BasisExamples\PythonParts\PythonPartConnection.py</Name>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
        <CopyEvent>True</CopyEvent>
    </Script>
    <Page>
        <Name>PythonPartConnection</Name>
        <Text>Properties</Text>
        <Parameters>
            <Parameter>
                <Name>ObjectType</Name>
                <Text>Object type</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>
                <Visible>__is_input_mode()</Visible>
                <Parameters>
                    <Parameter>
                        <Name>RadioButton1</Name>
                        <Text>Plate</Text>
                        <Value>1</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RadioButton2</Name>
                        <Text>Hole</Text>
                        <Value>2</Value>
                        <ValueType>RadioButton</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text />
        <Parameters>
            <Parameter>
                <Name>__AddPypSubFile__</Name>
                <Value />
                <ValueType>String</ValueType>
            </Parameter>
        </Parameters>
    </Page>
</Element>