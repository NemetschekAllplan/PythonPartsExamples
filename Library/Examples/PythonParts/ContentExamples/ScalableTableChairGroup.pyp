<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ContentExamples\TableChairGroupScalable.py</Name>
    <Title>TableChairGroupScale</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Ref_x</Name>
        <Text>Lenght</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref_y</Name>
        <Text>Width</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref_z</Name>
        <Text>Height</Text>
        <Value>800</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BoardThickness</Name>
        <Text>Board thickness</Text>
        <Value>20.</Value>
        <ValueType>Length</ValueType>
        <MinValue>1</MinValue>
        <MaxValue>200</MaxValue>
      </Parameter>
      <Parameter>
        <Name>XExcessLength</Name>
        <Text>X excess length</Text>
        <Value>100.</Value>
        <ValueType>Length</ValueType>
        <MinValue>1</MinValue>
        <MaxValue>Ref_x/2 - LegWidth</MaxValue>
      </Parameter>
      <Parameter>
        <Name>YExcessLength</Name>
        <Text>Y excess length</Text>
        <Value>100.</Value>
        <ValueType>Length</ValueType>
        <MinValue>1</MinValue>
        <MaxValue>Ref_y/2 - LegWidth</MaxValue>
      </Parameter>
      <Parameter>
        <Name>LegWidth</Name>
        <Text>Table leg width</Text>
        <Value>40.</Value>
        <ValueType>Length</ValueType>
        <MinValue>1</MinValue>
        <MaxValue>100</MaxValue>
      </Parameter>
    </Parameters>
  </Page>
</Element>
