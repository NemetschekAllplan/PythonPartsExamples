<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ModelObjectExamples\SelectionExamples\MultiSelection.py</Name>
    <Title>MultiSelection</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>MultiSelection</Name>
    <Text>Multiple object selection</Text>
    <Parameters>
      <Parameter>
        <Name>InputFunctionStarterOptions</Name>
        <Text>Options of InputFunctionStarter</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MarkSelectedElements</Name>
            <Text>Mark selected elements</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SelectionMode</Name>
            <Text>Selection mode</Text>
            <Value>eSelectGeometry</Value>
            <ValueList>"|".join(str(key) for key in AllplanIFW.SelectionMode.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ElementFilterSettingsExpander</Name>
        <Text>Options of ElementFilterSetting</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DocumentSnoopType</Name>
            <Text>DocumentSnoopType</Text>
            <Value>eSnoopActiveDocuments</Value>
            <ValueList>"|".join(str(key) for key in AllplanIFW.eDocumentSnoopType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>LayerSnoopType</Name>
            <Text>LayerSnoopType</Text>
            <Value>eSnoopActiveLayers</Value>
            <ValueList>"|".join(str(key) for key in AllplanIFW.eLayerSnoopType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
