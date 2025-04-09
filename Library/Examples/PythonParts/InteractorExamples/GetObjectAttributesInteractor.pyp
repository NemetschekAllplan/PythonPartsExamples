<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\GetObjectAttributesInteractor.py</Name>
    <Title>GetObjectAttributesInteractor</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Attributes</Name>
    <Text>Attributes</Text>
    <Parameters>
      <Parameter>
        <Name>GetObjectAttributes</Name>
        <Text>Get the attribues from all objects</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Button1</Name>
            <Text>Execute</Text>
            <EventId>1001</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Button2</Name>
        <Text>Get reinforcement bars fixture attributes</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Button2</Name>
            <Text>Execute</Text>
            <EventId>1002</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Button3</Name>
        <Text>Get wall attributes by wall selection</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Button3</Name>
            <Text>Execute</Text>
            <EventId>1003</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Button4</Name>
        <Text>Get precast element attributes by wall selection</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Button4</Name>
            <Text>Execute</Text>
            <EventId>1004</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
