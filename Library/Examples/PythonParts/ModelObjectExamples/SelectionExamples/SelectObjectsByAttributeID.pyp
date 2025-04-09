<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
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
    <Parameters>
      <Parameter>
        <Name>AttributeFilter</Name>
        <Text>Filter:</Text>
        <Value>Attribute name</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>AttributeIDFilter</Name>
        <Text/>
        <Value>[0]</Value>
        <ValueType>AttributeId</ValueType>
        <ValueDialog>AttributeSelection</ValueDialog>
        <ValueListStartRow>-1</ValueListStartRow>
      </Parameter>
      <Parameter>
        <Name>SelectedElementsExpander</Name>
        <Text>Selected elements</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SelectedElements</Name>
            <Text/>
            <Value>[_]</Value>
            <ValueType>Text</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
