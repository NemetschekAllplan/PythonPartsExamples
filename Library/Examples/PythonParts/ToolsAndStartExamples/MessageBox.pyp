<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ToolsAndStartExamples\MessageBox.py</Name>
    <Title>MessageBox</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Message box</Text>
    <Parameters>
      <Parameter>
        <Name>Row1</Name>
        <Text>Show messages</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Button1</Name>
            <Text>Press me!</Text>
            <EventId>1000</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
