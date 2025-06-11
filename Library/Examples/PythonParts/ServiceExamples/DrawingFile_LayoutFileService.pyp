<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ServiceExamples\DrawingFile_LayoutFileService.py</Name>
    <Title>DrawingFile_LayoutFileService</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Project</Name>
    <Text>Project attributes</Text>
    <Parameter>
      <Name>DrawingFileNumber</Name>
      <Text>Drawing File Number</Text>
      <Value></Value>
      <ValueType>Integer</ValueType>
    </Parameter>
    <Parameter>
      <Name>DrawingFileName</Name>
      <Text>Drawing File Name</Text>
      <Value></Value>
      <ValueType>String</ValueType>
    </Parameter>
    <Parameter>
      <Name>ButtonRowDF</Name>
      <Text>Button</Text> 
      <ValueType>Row</ValueType> 
      <Parameter>
        <Name>Button_DF_GetName</Name>
        <Text>Get Drawing File Name</Text> 
        <EventId>1001</EventId> 
        <ValueType>Button</ValueType>
      </Parameter>
      <Parameter>
        <Name>Button_DF_Rename</Name>
        <Text>Rename Drawing File</Text> 
        <EventId>1002</EventId> 
        <ValueType>Button</ValueType>
      </Parameter>
    </Parameter>
    <Parameter>
      <Name>LayoutFileNumber</Name>
      <Text>Layout File Number</Text>
      <Value></Value>
      <ValueType>Integer</ValueType>
    </Parameter>
    <Parameter>
      <Name>LayoutFileName</Name>
      <Text>Layout File Name</Text>
      <Value></Value>
      <ValueType>String</ValueType>
    </Parameter>
    <Parameter>
      <Name>ButtonRowLF</Name>
      <Text>Button</Text> 
      <ValueType>Row</ValueType> 
      <Parameter>
        <Name>Button_LF_GetName</Name>
        <Text>Get Layout Name</Text> 
        <EventId>1003</EventId> 
        <ValueType>Button</ValueType>
      </Parameter>
      <Parameter>
        <Name>Button_LF_Rename</Name>
        <Text>Rename Layout</Text> 
        <EventId>1004</EventId> 
        <ValueType>Button</ValueType>
      </Parameter>
    </Parameter>
  </Page>
</Element>
