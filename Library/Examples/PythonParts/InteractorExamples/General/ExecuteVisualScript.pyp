<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>InteractorExamples\General\ExecuteVisualScript.py</Name>
        <Title>ExecVisualScript</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>PythonPart</Name>
        <Text>General</Text>

        <Parameter>
            <Name>PlacementExpander</Name>
            <Text>Placement</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Script</Name>
                <Text>VS-script</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButton1</Name>
                    <Text>WireFrameDome</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton2</Name>
                    <Text>AugerPileReinforcement</Text>
                    <Value>3</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Distance</Name>
                <Text>Distance</Text>
                <Value>10000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
