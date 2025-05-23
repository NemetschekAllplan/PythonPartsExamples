<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\Symbol3DCloud.py</Name>
    <Title>Symbol3D cloud</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>DgmType</Name>
        <Text>DGM Type</Text>
        <Value>Small DGM (~1600 symbols)</Value>
        <ValueList>Small DGM (~1600 symbols)|Medium DGM (~6400 symbols)|Large DGM (~40000 symbols)</ValueList>
        <ValueType>StringComboBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>SymbolId</Name>
        <Text>Symbol Id</Text>
        <Value>1</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <Text>Height</Text>
        <Value>10.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <Text>Width</Text>
        <Value>10.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>RotationAngle</Name>
        <Text>Rotation angle</Text>
        <Value>0</Value>
        <ValueType>Angle</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
