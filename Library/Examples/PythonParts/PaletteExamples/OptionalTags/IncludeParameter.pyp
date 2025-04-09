<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <LanguageFile>IncludeParameter</LanguageFile>
  <Script>
    <Name>PaletteExamples\OptionalTags\IncludeParameter.py</Name>
    <Title>IncludeParameter</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>GeneralParameter</Name>
    <Text>General</Text>
    <Parameters>
      <Parameter>
        <Name>Left;2-4;Right</Name>
        <Text/>
        <TextId>1002;;1003</TextId>
        <Value>IncludeParameter.incpyp</Value>
        <LanguageFile>IncludeParameter_incpyp</LanguageFile>
        <ValueType>Include</ValueType>
      </Parameter>
      <Parameter>
        <Name>Expander</Name>
        <TextId>1004</TextId>
        <Text>Cordinates</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CoordCount</Name>
            <Text>Number of coordinates</Text>
            <TextId>1007</TextId>
            <Value>10</Value>
            <MinValue>1</MinValue>
            <MaxValue>20</MaxValue>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>1-20</Name>
            <Value>IncludeParameterCount.incpyp</Value>
            <ValueType>Include</ValueType>
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
        <Name>InitCoord</Name>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
