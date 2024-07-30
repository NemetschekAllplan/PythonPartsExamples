<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ServiceExamples\ProjectAttributeService.py</Name>
        <Title>ProjectAttributeServices</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Project</Name>
        <Text>Project attributes</Text>

        <Parameter>
            <Name>ProjectButton1</Name>
            <Text>Attributes current project</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>ProjectButton1</Name>
                <Text>Show</Text>
                <EventId>1001</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ProjectButton2</Name>
            <Text>Attributes all projects</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>ProjectButton2</Name>
                <Text>Show</Text>
                <EventId>1002</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>


        <Parameter>
            <Name>ProjectExpander</Name>
            <Text>Set project attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ProjectAttributes</Name>
                <Text>Project attribute</Text>
                <Value>[(0,)]</Value>
                <ValueType>AttributeIdValue</ValueType>
                <ValueDialog>AttributeSelectionProject</ValueDialog>
            </Parameter>

            <Parameter>
                <Name>SetProjectAttributes</Name>
                <Text>Set project attributes</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>ProjectButton3</Name>
                    <Text>Execute</Text>
                    <EventId>1003</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
