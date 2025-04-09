<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\ButtonControls\PictureButtonList.py</Name>
    <Title>PictureButtonList</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>ARROW_UP</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>ARROW_DOWN</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>INDEX_1</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>INDEX_2</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>INDEX_3</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Button controls</Text>
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
        <Name>SingleButtonExp</Name>
        <Text>Single picture button</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>IntegerValueList</Name>
            <Text>Integer value list</Text>
            <Value>1</Value>
            <ValueList>1|2|3</ValueList>
            <ValueTextList>Value=1|Value=2|Value=3</ValueTextList>
            <ValueList2>..\param01.svg|..\param02.png|..\param03.png</ValueList2>
            <ValueType>PictureButtonList</ValueType>
          </Parameter>
          <Parameter>
            <Name>UpDown</Name>
            <Text>Constants value list</Text>
            <Value>ARROW_UP</Value>
            <ValueList>ARROW_UP|ARROW_DOWN</ValueList>
            <ValueTextList>Up|Down</ValueTextList>
            <ValueList2>..\..\..\..\PythonPartsFramework\GeneralScripts\Bitmaps\arrowup.png|
                            ..\..\..\..\PythonPartsFramework\GeneralScripts\Bitmaps\arrowdown.png</ValueList2>
            <ValueType>PictureButtonList</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ListButtonExp</Name>
        <Text>Picture button list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>IndexCount</Name>
            <Text>Index count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>LineSep</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>Indexes</Name>
            <TextDyn>"Index " + str($list_row + 1)</TextDyn>
            <Value>[INDEX_1,INDEX_2,INDEX_3]</Value>
            <ValueList>INDEX_1|INDEX_2|INDEX_3</ValueList>
            <ValueTextList>Index=1|Index=2|Index=3</ValueTextList>
            <ValueList2>..\param01.png|..\param02.png|..\param03.png</ValueList2>
            <ValueType>PictureButtonList</ValueType>
            <Dimensions>IndexCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
