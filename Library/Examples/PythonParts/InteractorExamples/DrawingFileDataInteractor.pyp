<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\DrawingFileDataInteractor.py</Name>
    <Title>DrawingFileDataInteractor</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Drawing</Name>
    <Text>Drawing file data</Text>
    <Parameters>
      <Parameter>
        <Name>DrawingFileButton1</Name>
        <Text>State of the loaded drawing files</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawingFileButton1</Name>
            <Text>Show</Text>
            <EventId>1001</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DrawingFileButton2</Name>
        <Text>Name of the active drawing file</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawingFileButton2</Name>
            <Text>Show</Text>
            <EventId>1002</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DrawingFileButton3</Name>
        <Text>Names of the loaded drawing files by file number</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawingFileButton3</Name>
            <Text>Show</Text>
            <EventId>1003</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DrawingFileButton4</Name>
        <Text>Names of the loaded drawing files by file index</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawingFileButton4</Name>
            <Text>Show</Text>
            <EventId>1004</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DrawingFileButton5</Name>
        <Text>Name and number of the loaded drawing files</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawingFileButton5</Name>
            <Text>Show</Text>
            <EventId>1005</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
