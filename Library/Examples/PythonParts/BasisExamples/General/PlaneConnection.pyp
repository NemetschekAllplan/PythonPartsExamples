<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\General\PlaneConnection.py</Name>
    <Title>PlaneConnection</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page1</Text>
    <Parameters>
      <Parameter>
        <Name>RowPlaneReferences</Name>
        <Text>Planes</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlaneReferences</Name>
            <Text>Planes</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <Text>Width</Text>
        <Value>600.</Value>
        <ValueType>Length</ValueType>
        <MinValue>10</MinValue>
      </Parameter>
      <Parameter>
        <Name>Depth</Name>
        <Text>Depth</Text>
        <Value>400.</Value>
        <ValueType>Length</ValueType>
        <MinValue>10</MinValue>
      </Parameter>
    </Parameters>
  </Page>
</Element>
