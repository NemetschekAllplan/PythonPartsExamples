<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
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
    <Parameters>
      <Parameter>
        <Name>ConfigFile</Name>
        <Text>Config File Name</Text>
        <Value/>
        <ValueType>String</ValueType>
        <ValueDialog>OpenFileDialog</ValueDialog>
      </Parameter>
      <Parameter>
        <Name>reqFile</Name>
        <Text>Requiremets File</Text>
        <Value/>
        <ValueType>String</ValueType>
        <ValueDialog>OpenFileDialog</ValueDialog>
      </Parameter>
      <Parameter>
        <Name>allep</Name>
        <Text>Allep Folder</Text>
        <Value/>
        <ValueType>String</ValueType>
        <ValueDialog>OpenFileDialog</ValueDialog>
      </Parameter>
      <Parameter>
        <Name>StartExportRow</Name>
        <Text> </Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>StartNpdGeneration</Name>
            <Text>Generate NPD file</Text>
            <EventId>1002</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
          <Parameter>
            <Name>InstallReq</Name>
            <Text>Install Requirements</Text>
            <EventId>1003</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>StartExportRow</Name>
        <Text> </Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>MoveFiles</Name>
            <Text>Move files</Text>
            <EventId>1004</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
