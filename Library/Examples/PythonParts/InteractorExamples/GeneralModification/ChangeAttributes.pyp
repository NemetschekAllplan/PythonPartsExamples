<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\GeneralModification\ChangeAttributes.py</Name>
    <Title>Change attributes</Title>
    <Version>1.0</Version>
    <ShowFavoriteButtons>False</ShowFavoriteButtons>
  </Script>
  <Page>
    <Name>ChangeAttributes</Name>
    <Text>Change attributes</Text>
    <Parameters>
      <Parameter>
        <Name>AttributeValuesExpander</Name>
        <Text>Attribute values</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DynamicAttributeList</Name>
            <Text>Attributes</Text>
            <Value>[(0,)]</Value>
            <ValueType>AttributeIdValue</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
