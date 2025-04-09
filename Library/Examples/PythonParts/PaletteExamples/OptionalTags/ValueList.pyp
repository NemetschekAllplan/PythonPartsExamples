<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\OptionalTags\ValueList.py</Name>
    <Title>WidthValueList</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>List values</Text>
    <Parameters>
      <Parameter>
        <Name>ValueListExp</Name>
        <Text>Value list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ValueListCount</Name>
            <Text>Value count</Text>
            <Value>6</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>WidthValueList</Name>
            <Text>Value list</Text>
            <Value>[1000,2000,3000,4000,5000,6000]</Value>
            <ValueType>Length</ValueType>
            <Dimensions>ValueListCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SingleWidthExp</Name>
        <Text>Single width</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>2000</Value>
            <ValueType>Length</ValueType>
            <ValueList>WidthValueList</ValueList>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OneDimWidthListExp</Name>
        <Text>One dimensional width list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>WidthRowCount</Name>
            <Text>Row count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>WidthList</Name>
            <Text>Width</Text>
            <Value>[1000,2000,3000]</Value>
            <ValueType>Length</ValueType>
            <Dimensions>WidthRowCount</Dimensions>
            <ValueListStartRow>1</ValueListStartRow>
            <ValueList>WidthValueList</ValueList>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TwoDimLWidthistExp</Name>
        <Text>Two dimensional width list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Width2DimRowCount</Name>
            <Text>Row count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Width2DimColumnCount</Name>
            <Text>Column count</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>WidthList2Dim</Name>
            <Text>Width</Text>
            <Value>[[1000,2000],[3000,4000],[5000,6000]]</Value>
            <ValueType>Length</ValueType>
            <Dimensions>Width2DimRowCount,Width2DimColumnCount</Dimensions>
            <ValueListStartRow>1</ValueListStartRow>
            <ValueList>WidthValueList</ValueList>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Range</Name>
    <Text>By range</Text>
    <Parameters>
      <Parameter>
        <Name>RangeExp</Name>
        <Text>Range</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>HeightFrom</Name>
            <Text>Height from</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>HeightTo</Name>
            <Text>Height to</Text>
            <Value>10000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>HeightStep</Name>
            <Text>Height step</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SingleHeightExp</Name>
        <Text>Single height</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>2000</Value>
            <ValueType>Length</ValueType>
            <ValueList>[value for value in range(HeightFrom, HeightTo, HeightStep)]</ValueList>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OneDimHeightListExp</Name>
        <Text>One dimensional height list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>HeightRowCount</Name>
            <Text>Row count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>HeightList</Name>
            <Text>Height</Text>
            <Value>[1000,2000,3000]</Value>
            <ValueType>Length</ValueType>
            <Dimensions>HeightRowCount</Dimensions>
            <ValueListStartRow>1</ValueListStartRow>
            <ValueList>[value for value in range(HeightFrom, HeightTo, HeightStep)]</ValueList>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TwoDimLHeightistExp</Name>
        <Text>Two dimensional height list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Height2DimRowCount</Name>
            <Text>Row count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Height2DimColumnCount</Name>
            <Text>Column count</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>HeightList2Dim</Name>
            <Text>Height</Text>
            <Value>[[1000,2000],[3000,4000],[5000,6000]]</Value>
            <ValueType>Length</ValueType>
            <Dimensions>Height2DimRowCount,Height2DimColumnCount</Dimensions>
            <ValueListStartRow>1</ValueListStartRow>
            <ValueList>[value for value in range(HeightFrom, HeightTo, HeightStep)]</ValueList>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
