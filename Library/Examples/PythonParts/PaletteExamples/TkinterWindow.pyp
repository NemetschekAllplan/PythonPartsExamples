<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\TkinterWindow.py</Name>
    <Title>TkinterWindow</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <Text>Length</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
        <Enable>False</Enable>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <Text>Length</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
        <Enable>False</Enable>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <Text>Length</Text>
        <Value>3000.</Value>
        <ValueType>Length</ValueType>
        <Enable>False</Enable>
      </Parameter>
      <Parameter>
        <Name>Row1</Name>
        <Text>Button - set dimensions</Text>
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
