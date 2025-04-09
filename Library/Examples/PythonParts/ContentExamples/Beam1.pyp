<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ContentExamples\Beam1.py</Name>
    <Title>Beam1</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <Text>Length</Text>
        <Value>10000.</Value>
        <ValueType>Length</ValueType>
        <MinValue>LengthLeft + LengthFullBeamRight + LengthFullBeamWebRight</MinValue>
      </Parameter>
      <Parameter>
        <Name>LengthLeft</Name>
        <Text>Length left</Text>
        <Value>6000.</Value>
        <ValueType>Length</ValueType>
        <MaxValue>Length - LengthFullBeamRight - LengthFullBeamWebRight</MaxValue>
      </Parameter>
      <Parameter>
        <Name>HeightLeft</Name>
        <Text>Height left</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>HeightCenter</Name>
        <Text>Height center</Text>
        <Value>1500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>HeightRight</Name>
        <Text>Height right</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>LengthFullBeamLeft</Name>
        <Text>Full section left</Text>
        <Value>1500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>LengthFullBeamRight</Name>
        <Text>Full section right</Text>
        <Value>1500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>LengthFullBeamWebLeft</Name>
        <Text>Transition I shape left</Text>
        <Value>300.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>LengthFullBeamWebRight</Name>
        <Text>Transition I shape right</Text>
        <Value>300.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BottomFlangeWidth</Name>
        <Text>Flange width bottom</Text>
        <Value>400.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BottomFlangeHeight</Name>
        <Text>Flange height bottom</Text>
        <Value>300.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BottomBevelHeight</Name>
        <Text>Flange angle bottom</Text>
        <Value>200.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>WebWidth</Name>
        <Text>Web width</Text>
        <Value>200.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>TopBevelHeight</Name>
        <Text>Flange angle top</Text>
        <Value>100.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>TopFlangeWidth</Name>
        <Text>Flange width top</Text>
        <Value>600.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>TopFlangeHeight</Name>
        <Text>Flange height top</Text>
        <Value>200.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>OffsetTopFlangeLeft</Name>
        <Text>Flange offset left</Text>
        <Value>500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>OffsetTopFlangeRight</Name>
        <Text>Flange offset right</Text>
        <Value>500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
