<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ModelObjectExamples\SelectionExamples\SingleSelection.py</Name>
    <Title>SingleSelection</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>SingleSelection</Name>
    <Text>Single object selection</Text>
    <Parameters>
      <Parameter>
        <Name>CoordinateInputOptions</Name>
        <Text>Options of CoordinateInput</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ElementSearchType</Name>
            <Text>Type of element search</Text>
            <Value>ElementSearch</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>ElementSearch</Name>
                <Text>element</Text>
                <Value>ElementSearch</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>ElementGeometrySearch</Name>
                <Text>element geometry</Text>
                <Value>ElementGeometrySearch</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>PointSearch</Name>
            <Text>Perform point search</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SelectAlways</Name>
            <Text>Select, when end point was clicked</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>PointSearch</Visible>
          </Parameter>
          <Parameter>
            <Name>AllowCenter</Name>
            <Text>Select, when middle point was clicked</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>PointSearch</Visible>
            <Enable>not SelectAlways</Enable>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>HighlightElements</Name>
            <Text>Highlight elements</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>ElementSearchType == "ElementSearch"</Visible>
          </Parameter>
          <Parameter>
            <Name>HighlightCompleteElement</Name>
            <Text>Highlight complete element</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>ElementSearchType == "ElementGeometrySearch"</Visible>
          </Parameter>
          <Parameter>
            <Name>EnableInputControl</Name>
            <Text>Enable input control</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>InputControlType</Name>
            <Text>Input control type</Text>
            <Value>eTEXT_EDIT</Value>
            <ValueList>"|".join(str(key) for key in AllplanIFW.eValueInputControlType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
            <Visible>EnableInputControl</Visible>
          </Parameter>
          <Parameter>
            <Name>EnableAssistWndClick</Name>
            <Text>Allow selection in wizard window</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
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
