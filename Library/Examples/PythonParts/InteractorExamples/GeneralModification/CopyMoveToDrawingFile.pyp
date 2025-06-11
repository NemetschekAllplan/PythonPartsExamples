<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\GeneralModification\CopyMoveToDrawingFile.py</Name>
    <Title>CopyMoveElementsToDrawingFile</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
      <Parameters>
        <Parameter>
          <Name>Command</Name>
          <Text>Command</Text>
          <Value>Copy</Value>
          <ValueList>Copy|Move</ValueList>
          <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
          <Name>TargetDrawingFile</Name>
          <Text>Target drawing file</Text>
          <Value></Value>
          <ValueType>Integer</ValueType>
        </Parameter>
      </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text>Hidden page</Text>
    <Parameters>
      <Parameter>
        <Name>IsInSelection</Name>
        <Text>State for selection</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
        <Persistent>NO</Persistent>
      </Parameter>
    </Parameters>
  </Page>
</Element>
