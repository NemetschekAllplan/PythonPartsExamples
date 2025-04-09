<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\BasicControls\CheckBox.py</Name>
    <Title>CheckBox</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Single controls</Text>
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
        <Name>DrawCubeExp</Name>
        <Text>Check box</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawCube</Name>
            <Text>Draw cube</Text>
            <Value>1</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OneDimList</Name>
        <Text>One dimensional list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawCubeCount</Name>
            <Text>DrawCube count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>DrawCubeSep</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>DrawCubeList</Name>
            <Text/>
            <TextDyn>"Draw cube " + str($list_row + 1)</TextDyn>
            <Value>[1,0,1]</Value>
            <ValueType>CheckBox</ValueType>
            <Dimensions>DrawCubeCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TwoDimListExp</Name>
        <Text>Two dimensional list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DrawCubeList2Dim</Name>
            <Text/>
            <TextDyn>"Draw cube " + str($list_row + 1)</TextDyn>
            <Value>[[1,0],[0,1],[1,1]]</Value>
            <ValueType>CheckBox</ValueType>
            <Dimensions>DrawCubeCount,2</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
