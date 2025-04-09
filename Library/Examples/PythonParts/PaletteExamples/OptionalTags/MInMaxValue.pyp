<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\OptionalTags\MinMaxValue.py</Name>
    <Title>MinMaxValue</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>General</Text>
    <Parameters>
      <Parameter>
        <Name>MinMaxValueExp</Name>
        <Text>Min/max value</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>MinValue</Name>
            <Text>Min value</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>MaxValue</Name>
            <Text>Max value</Text>
            <Value>10000</Value>
            <ValueType>Length</ValueType>
            <MinValue>MinValue</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SingleValueExp</Name>
        <Text>Single value</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>2000</Value>
            <ValueType>Length</ValueType>
            <MinValue>MinValue</MinValue>
            <MaxValue>MaxValue</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>OneDimListExp</Name>
        <Text>One dimensional list</Text>
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
            <MinValue>MinValue</MinValue>
            <MaxValue>MaxValue</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TwoDimListExp</Name>
        <Text>Two dimensional list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>IntRowCount</Name>
            <Text>Row count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>IntColumnCount</Name>
            <Text>Column count</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>WidthList2Dim</Name>
            <Text>Width</Text>
            <Value>[[1000,2000],[3000,4000],[5000,6000]]</Value>
            <ValueType>Length</ValueType>
            <ValueListStartRow>1</ValueListStartRow>
            <MinValue>MinValue</MinValue>
            <MaxValue>MaxValue</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>NamedTupleExpander</Name>
        <Text>Named tuple</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>NamedTupleSizes</Name>
            <Text>Length,Width,Height</Text>
            <Value>1000|2000|3000</Value>
            <ValueType>namedtuple(Length,Length,Length)</ValueType>
            <NamedTuple>
              <TypeName>NamedTupleSizes</TypeName>
              <FieldNames>Length,Width,Height</FieldNames>
            </NamedTuple>
            <MinValue>MinValue,MinValue,0</MinValue>
            <MaxValue>MaxValue,MaxValue,5000</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TupleExpander</Name>
        <Text>Tuple</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>TupleSizes</Name>
            <Text>Length|Width|Height</Text>
            <Value>1000|2000|3000</Value>
            <ValueType>tuple(Length,Length,Length)</ValueType>
            <MinValue>MinValue,MinValue,0</MinValue>
            <MaxValue>MaxValue,MaxValue,5000</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeometryExp</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Point</Name>
            <Text>Point with min/max</Text>
            <Value>Point2D(1000,5000)</Value>
            <ValueType>Point2D</ValueType>
            <XYZinRow>True</XYZinRow>
            <MinValue>Point2D(MinValue,0)</MinValue>
            <MaxValue>Point2D(10000,20000)</MaxValue>
          </Parameter>
          <Parameter>
            <Name>Vector</Name>
            <Text>Vector with min/max</Text>
            <Value>Vector3D(0,10000,0)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <MinValue>Vector3D(0,0,0)</MinValue>
            <MaxValue>Vector3D(10000,MaxValue,30000)</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
