<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\BasicControls\MultiIndex.py</Name>
    <Title>EditControls</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>List controls</Text>
    <Parameters>
      <Parameter>
        <Name>Format</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>MultiIndexList</Name>
        <Text>Multi index list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SizeCount</Name>
            <Text>Size count</Text>
            <Value>5</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>SizeSep</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>IndexRow</Name>
            <Text>Cube index</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>InfoPicture</Name>
                <Text>Enter the index in the box. For example,
enter 1-4 or 1,3. Use the arrow keys to select the
previous or next index.</Text>
                <TextId>1005</TextId>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>SizeIndex</Name>
                <Text/>
                <Value>1-3</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>SizeCount</MaxValue>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>CubeSize</Name>
            <Text>Cube size</Text>
            <Value>[1000,1500,2000,2500,4000]</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
            <Dimensions>SizeCount</Dimensions>
            <ValueIndexName>SizeIndex</ValueIndexName>
          </Parameter>
          <Parameter>
            <Name>CubeHeight</Name>
            <Text>Cube height</Text>
            <Value>[1000,1500,2000,2500,4000]</Value>
            <ValueType>LengthComboBox</ValueType>
            <ValueList>1000|1500|2000|2500|4000</ValueList>
            <ValueListFile>usr\tmp\PypComboSettings\CubeHeight.val</ValueListFile>
            <MinValue>10</MinValue>
            <Dimensions>SizeCount</Dimensions>
            <ValueIndexName>SizeIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DynamicLRadiusistExp</Name>
        <Text>Dynamic radius list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DynamicRadiusListIndexRow</Name>
            <Text>Sphere index</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>DynamicListInfoPicture</Name>
                <Text>Select the position you want to modify. You can
select several positions to remove or replace
existing radii. The last available position
is always empty. Select it to add an additional
radius.</Text>
                <TextId>1005</TextId>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>RadiusIndex</Name>
                <Text/>
                <Value>1</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>len(SphereRadius) + 1</MaxValue>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>SphereRadius</Name>
            <Text>Sphere radius</Text>
            <Value>[_]</Value>
            <ValueType>DynamicList(Length)</ValueType>
            <ValueIndexName>RadiusIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DynamicSymbolListExp</Name>
        <Text>Dynamic symbol list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DynamicSymbolListIndexRow</Name>
            <Text>Symbol index</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>DynamicListInfoPictureSymbol</Name>
                <Text>Select the position you want to modify. You can
select several positions to remove or replace
existing symbols. The last available position
is always empty. Select it to add an additional
symbol.</Text>
                <TextId>1005</TextId>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>SymbolIndex</Name>
                <Text/>
                <Value>1</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>len(SymbolPath) + 1</MaxValue>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>SymbolPath</Name>
            <Text>Select symbol</Text>
            <Value>[_]</Value>
            <ValueType>DynamicList(String)</ValueType>
            <ValueDialog>SymbolDialog</ValueDialog>
            <ValueIndexName>SymbolIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
