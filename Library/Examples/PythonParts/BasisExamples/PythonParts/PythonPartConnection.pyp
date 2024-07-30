<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Title>PythonPartConnection</Title>
        <Name>BasisExamples\PythonParts\PythonPartConnection.py</Name>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>PythonPartConnection</Name>
        <Text>Properties</Text>

        <Parameter>
            <Name>ObjectType</Name>
            <Text>Object type</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Visible>__is_input_mode()</Visible>

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
        </Parameter>

    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Parameter>
            <Name>__AddPypSubFile__</Name>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>
    </Page>
</Element>
