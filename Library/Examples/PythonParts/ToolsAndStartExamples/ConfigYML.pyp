<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ToolsAndStartExamples\ConfigYML.py</Name>
        <Title>Test Script for Python Part SDK</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Drawing</Name>
        <Text>Drawing</Text>
        <Parameter>
            <Name>ConfigFile</Name>
            <Text>Config File Name</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
        </Parameter>
        <Parameter>
            <Name>reqFile</Name>
            <Text>Requiremets File</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
        </Parameter>
        <Parameter>
            <Name>allep</Name>
            <Text>Allep Folder</Text>
            <Value></Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
        </Parameter>
        <Parameter>
            <Name>StartExportRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Start NPD Generation</Name>
                <Text>Generate NPD file</Text>
                <EventId>1002</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
            <Parameter>
                <Name>Install req</Name>
                <Text>Install Requirements</Text>
                <EventId>1003</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>StartExportRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>Move files</Name>
                <Text>Move files</Text>
                <EventId>1004</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>