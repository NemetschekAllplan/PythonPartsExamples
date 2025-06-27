<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\BasicControls\ConstructionPointSymbol.py</Name>
    <Title>Construction Point Symbol</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Construction point symbols</Text>
    <Parameters>
      <Parameter>
        <Name>BaseSelectionExp</Name>
        <Text>Symbol selection of different types</Text>
        <ValueType>Expander</ValueType>
        <Parameters>     
          <Parameter>
            <Name>PointSymbolElevation</Name>
            <Text>Elevation dimension</Text>        
            <Value>1001</Value>
            <ValueList>ElevationDimension</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>
          </Parameter>
          <Parameter>
            <Name>PointSymbolLine</Name>
            <Text>Line dimension</Text>        
            <Value>1</Value>
            <ValueList>LineDimension</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>       
          </Parameter>
          <Parameter>
            <Name>PointSymbolAlignment</Name>
            <Text>Alignment dimension</Text>
            <Value>1</Value>
            <ValueList>AlignmentDimension</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>
          </Parameter>
          <Parameter>
            <Name>PointSymbolConstruction</Name>
            <Text>Construction elements</Text>
            <Value>13</Value>
            <ValueList>ConstructionElement</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>
          </Parameter>
          <Parameter>
            <Name>PointSymbolCombined</Name>
            <Text>Line and elevation dimension</Text>
            <Value>1</Value>
            <ValueList>LineDimension|ElevationDimension</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>     
      <Parameter>
        <Name>OptionalTagsExp</Name>
        <Text>Symbol selection with special options</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PointSymbolOptionOff</Name>
            <Text>With "ShowSymbolOff" option</Text>            
            <ValueList>LineDimension|ElevationDimension|ShowSymbolOff</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>
          </Parameter>
          <Parameter>
            <Name>PointSymbolOptionShowID</Name>
            <Text>With "ShowSymbolID" option</Text>
            <Value>1</Value>
            <ValueList>LineDimension|ElevationDimension|ShowSymbolID</ValueList>
            <ValueType>ConstructionPointSymbol</ValueType>
          </Parameter>
        </Parameters>
       </Parameter>
      <Parameter>
        <Name>GeometryExp</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
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
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
