<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\PythonParts\ModifyPythonPartParameter.py</Name>
    <Title>ModifyPythonPartParameter</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>False</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>REF_PYP_SELECT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>PARAMETER_INPUT</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>PYP_SELECTION</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>MODIFY_MODIFIED</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>MODIFY_ALL</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters>
      <Parameter>
        <Name>ExecuteModification</Name>
        <Text>Parameter modification</Text>
        <Value>MODIFY_MODIFIED</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Visible>InputMode == PYP_SELECTION</Visible>
        <Parameters>
          <Parameter>
            <Name>ModifyModified</Name>
            <Text>Modify modified</Text>
            <Value>MODIFY_MODIFIED</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>ModifyAll</Name>
            <Text>Modify all</Text>
            <Value>MODIFY_ALL</Value>
            <ValueType>RadioButton</ValueType>
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
