<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\ObjectCreation\Dimensioning.py</Name>
    <Title>Dimensioning</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Dimensioning</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <Text>Length</Text>
        <Value>3000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <Text>Height</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>PointSymbolElevation</Name>
        <Text>Point symbol for elevation</Text>        
        <Value>1001</Value>
        <ValueList>ElevationDimension</ValueList>
        <ValueType>ConstructionPointSymbol</ValueType>
      </Parameter>
      <Parameter>
        <Name>PointSymbolLine</Name>
        <Text>Point symbol for line</Text>        
        <Value>1</Value>
        <ValueList>LineDimension</ValueList>
        <ValueType>ConstructionPointSymbol</ValueType>       
      </Parameter>
    </Parameters>
  </Page>
</Element>
