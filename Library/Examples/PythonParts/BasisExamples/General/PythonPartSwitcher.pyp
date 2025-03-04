<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\General\PythonPartSwitcher.py</Name>
        <Title>PythonPartSwitcher</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page1</Text>

        <Parameter>
            <Name>PythonPartSelect</Name>
            <Text>Select</Text>
            <Value>None</Value>
            <ValueList>None|PythonPartWithAttributes|PythonPartGroup|PythonPartWithSubObjects|Column</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>AddCurrentToStack</Name>
            <Text>Add current to stack</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
</Element>
