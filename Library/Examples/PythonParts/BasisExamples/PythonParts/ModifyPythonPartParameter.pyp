<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\PythonParts\ModifyPythonPartParameter.py</Name>
        <Title>ModifyPythonPartParameter</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>False</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>REF_PYP_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>PARAMETER_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>PYP_SELECTION</Name>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>MODIFY_MODIFIED</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>MODIFY_ALL</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

        <Parameter>
            <Name>ExecuteModification</Name>
            <Text>Parameter modification</Text>
            <Value>MODIFY_MODIFIED</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Visible>InputMode == PYP_SELECTION</Visible>

            <Parameter>
                <Name>ModifyModified</Name>
                <Text>Modify modified</Text>
                <Value>MODIFY_MODIFIED</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>ModifyAll</Name>
                <Text>Modify all</Text>
                <Value>MODIFY_ALL</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>

    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
