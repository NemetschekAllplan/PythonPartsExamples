<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\General\PythonPartSwitcher.py</Name>
    <Title>PythonPartSwitcher</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page1</Text>
    <Parameters>
      <Parameter>
        <Name>PythonPartSelect</Name>
        <Text>Select</Text>
        <Value>None</Value>
        <ValueList>None|PythonPartWithAttributes|PythonPartGroup|PythonPartWithSubObjects|Column</ValueList>
        <ValueType>StringComboBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>AddCurrentToStack</Name>
        <Text>Add current to stack</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
