<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\DivisionPoints.py</Name>
    <Title>DivisionPoints Test</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>DivisionPoints</Name>
    <Text>DivisionPoints</Text>
    <Parameters>
      <Parameter>
        <Name>UseCountForDivision</Name>
        <Text>Use count for division</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>CountDivisions</Name>
        <Text>Count of divisions</Text>
        <Value>20</Value>
        <Visible>UseCountForDivision == True</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>LengthDivisions</Name>
        <Text>Length of divisions</Text>
        <Value>100</Value>
        <Visible>UseCountForDivision == False</Visible>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Epsilon</Name>
        <Text>Epsilon</Text>
        <Value>0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>LineLineLine</Name>
        <Text>Use Line-Line-Line path</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>LineSplineLine</Name>
        <Text>Use Line-Spline-Line path</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>LineArcLine</Name>
        <Text>Use Line-Arc-Line path</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
