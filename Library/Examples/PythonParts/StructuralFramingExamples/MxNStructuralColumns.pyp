<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>StructuralFramingExamples\MxNStructuralColumns.py</Name>
    <Title>Hall of Structural Columns</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>General</Text>
    <!--<Parameter>
            <Name>Layer</Name>
            <Text>Layer</Text>
            <Value>3700</Value>
            <ValueType>Layer</ValueType>
        </Parameter>-->
    <Parameters>
      <Parameter>
        <Name>ColumType</Name>
        <Text>Type of column</Text>
        <Value>0</Value>
        <ValueList>0|1|2</ValueList>
        <ValueList2>15581|14587|14601</ValueList2>
        <ValueType>PictureResourceButtonList</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <Text>Width</Text>
        <Value>100</Value>
        <Visible>ColumType == 0</Visible>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness</Name>
        <Text>Thickness</Text>
        <Value>80</Value>
        <Visible>ColumType == 0</Visible>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Radius</Name>
        <Text>Radius</Text>
        <Value>500</Value>
        <Visible>ColumType == 1</Visible>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>ProfilePath</Name>
        <TextId>1005</TextId>
        <ValueType>Row</ValueType>
        <Visible>ColumType == 2</Visible>
        <Parameters>
          <Parameter>
            <Name>SymbolDialog</Name>
            <Value>Auswahl</Value>
            <ValueType>String</ValueType>
            <ValueDialog>SymbolDialog</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Row1</Name>
        <Text>Plane references</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>ColumnPlaneReferences</Name>
            <Text>Height</Text>
            <Value>None</Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Material</Name>
        <Text>Material</Text>
        <Value>beton</Value>
        <ValueType>String</ValueType>
      </Parameter>
      <Parameter>
        <Name>Number_X_Dir</Name>
        <Text>Number in X direction</Text>
        <Value>10</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>Space_X</Name>
        <Text>Space in X direction</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Number_Y_Dir</Name>
        <Text>Number in Y direction</Text>
        <Value>5</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>Space_Y</Name>
        <Text>Space in Y direction</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
