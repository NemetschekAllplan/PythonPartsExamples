<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ModelObjectExamples\SelectionExamples\SelectObjectsByAttributeID.py</Name>
        <Title>SelectObjectsByAttributeID</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

        <Parameter>
            <Name>AttributeFilter</Name>
            <Text>Filter:</Text>
            <Value>Attribute name</Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>AttributeIDFilter</Name>
            <Text></Text>
            <Value>[0]</Value>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
            <ValueListStartRow>-1</ValueListStartRow>
        </Parameter>

        <Parameter>
            <Name>SelectedElementsExpander</Name>
            <Text>Selected elements</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SelectedElements</Name>
                <Text></Text>
                <Value>[_]</Value>
                <ValueType>Text</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
