<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ModelObjectExamples\General\ShowHierarchy.py</Name>
    <Title>Object hierarchy</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>PrintingOptions</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>PrintingOptionsExpander</Name>
        <Text>Printing options</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MaxTreeDepth</Name>
            <Text>Maximum tree depth</Text>
            <Value>10</Value>
            <MinValue>1</MinValue>
            <MaxValue>100</MaxValue>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>PrintHiddenElements</Name>
            <Text>Print hidden elements</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
