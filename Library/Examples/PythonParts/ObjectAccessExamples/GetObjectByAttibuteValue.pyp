<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <LanguageFile>AllControls</LanguageFile>
  <Script>
    <Name>ObjectAccessExamples\GetObjectByAttributeValue.py</Name>
    <Title>GetObjectByAttributeValue</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Input</Name>
    <Text>Input</Text>
    <Parameters>
      <Parameter>
        <Name>AttributeID</Name>
        <Text>Attribute</Text>
        <Value>0</Value>
        <ValueType>Integer</ValueType>
        <ValueDialog>AttributeSelection</ValueDialog>
      </Parameter>
      <Parameter>
        <Name>AttributeValue</Name>
        <Text>Attribute value</Text>
        <Value/>
        <ValueType>Attribute</ValueType>
        <AttributeId>508</AttributeId>
        <Visible>AttributeID</Visible>
      </Parameter>
    </Parameters>
  </Page>
</Element>
