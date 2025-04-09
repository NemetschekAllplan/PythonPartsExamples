<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\PythonParts\MovePythonPart.py</Name>
    <Title>PlaceExistingPythonPart</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>ELEMENT_SELECT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>ELEMENT_PLACEMENT</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters>
      <Parameter>
        <Name>MoveOrCopy</Name>
        <Text>Action</Text>
        <Value>Move</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>RadioButtonMove</Name>
            <Text>Move</Text>
            <Value>Move</Value>
            <ValueType>RadioButton</ValueType>
            <Enable>InputMode == ELEMENT_SELECT</Enable>
          </Parameter>
          <Parameter>
            <Name>RadioButtonCopy</Name>
            <Text>Copy</Text>
            <Value>Copy</Value>
            <ValueType>RadioButton</ValueType>
            <Enable>InputMode == ELEMENT_SELECT</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>RotationAnglesExpander</Name>
        <Text>Rotation angles</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AngleX</Name>
            <Text>around X axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>AngleY</Name>
            <Text>around Y axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>AngleZ</Name>
            <Text>around Z axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
        </Parameters>
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
