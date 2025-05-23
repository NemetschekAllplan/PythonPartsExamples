<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\IdenticalRotatedPlate.py</Name>
    <Title>Identical rotated plate</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page1</Text>
    <Parameters>
      <Parameter>
        <Name>DimensionsExpander</Name>
        <Text>Dimensions</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
          </Parameter>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>600.</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
          </Parameter>
          <Parameter>
            <Name>Thickness</Name>
            <Text>Thickness</Text>
            <Value>20.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander</Name>
        <Text>Rotation</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RotationAngleX</Name>
            <Text>Rotation x-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <ExcludeIdentical>True</ExcludeIdentical>
          </Parameter>
          <Parameter>
            <Name>RotationAngleY</Name>
            <Text>Rotation y-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <ExcludeIdentical>True</ExcludeIdentical>
          </Parameter>
          <Parameter>
            <Name>RotationAngleZ</Name>
            <Text>Rotation z-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <ExcludeIdentical>True</ExcludeIdentical>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
