<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ArchitectureExamples\Objects\RoomInput.py</Name>
    <Title>RoomInput</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>POLYGON_INPUT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>ROOM_MODIFY</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Room</Name>
    <Text>Room</Text>
    <Parameters>
      <Parameter>
        <Name>Format</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RoomAttributes</Name>
        <Text>Room attributes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>StoreyCode</Name>
            <Text>Storey code</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>Name</Name>
            <Text>Name</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>Function</Name>
            <Text>Function</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeneralAttributes</Name>
        <Text>General attributes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Text</Name>
            <Text>Text</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>Texts</Name>
            <Text>Text</Text>
            <Value>[""] * 5</Value>
            <ValueType>String</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
          </Parameter>
          <Parameter>
            <Name>Attributes</Name>
            <Text>Attributes</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>Factor</Name>
            <Text>Factor</Text>
            <Value>1.0</Value>
            <ValueType>Double</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <Text>Height</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlaneReferences</Name>
            <Text>Room height</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>UserAttributesPage</Name>
    <Text>User attributes</Text>
    <Parameters>
      <Parameter>
        <Name>UserAttributes</Name>
        <Text/>
        <Value>[]</Value>
        <ValueType>AttributeIdValue</ValueType>
        <ValueDialog>AttributeSelectionInsert</ValueDialog>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value/>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
