<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ContentExamples\Table2.py</Name>
    <Title>Table2</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Picture1</Name>
        <Value>Table2Description.png</Value>
        <Orientation>Middle</Orientation>
        <ValueType>Picture</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator1</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Row1</Name>
        <Text>Length long</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>TableLengthLong</Name>
            <Text>Length long</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Param1Picture</Name>
            <Value>param01.png</Value>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Row2</Name>
        <Text>Width long</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>TableWidthLong</Name>
            <Text>Width long</Text>
            <Value>3000.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Param2Picture</Name>
            <Value>param02.png</Value>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Row3</Name>
        <Text>Length short</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>TableLengthShort</Name>
            <Text>Length short</Text>
            <Value>750.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Param3Picture</Name>
            <Value>param03.png</Value>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Row4</Name>
        <Text>Width short</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>TableWidthShort</Name>
            <Text>Width short</Text>
            <Value>750.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Param4Picture</Name>
            <Value>param04.png</Value>
            <ValueType>Picture</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TableHeight</Name>
        <Text>Height</Text>
        <Value>800.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BoardThickness</Name>
        <Text>Panel thickness</Text>
        <Value>20.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>ExcessLength</Name>
        <Text>Overlap</Text>
        <Value>100.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>LegWidth</Name>
        <Text>Table leg width</Text>
        <Value>40.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
