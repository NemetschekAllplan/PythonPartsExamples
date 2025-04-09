<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Title>PythonPart element connection</Title>
    <Name>BasisExamples\PythonParts\PythonPartElementConnection.py</Name>
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
      <Name>PARAMETER_MODIFICATION</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>ExtrusionVector</Name>
        <Text>Extrusion vector</Text>
        <Value>Vector3D(0,0,2000)</Value>
        <ValueType>Vector3D</ValueType>
        <Visible>InputMode == PARAMETER_MODIFICATION</Visible>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Parameters>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value/>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>ElementGeoConnection</Name>
        <Text>Element geometry connection</Text>
        <Value>[]</Value>
        <ValueType>ElementGeometryConnection</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
