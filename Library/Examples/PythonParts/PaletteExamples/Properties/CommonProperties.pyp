<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\Properties\CommonProperties.py</Name>
    <Title>CommonProperties</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <Text>Length</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>SingleParameterExp</Name>
        <Text>Single parameter</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>UseGlobalProperties</Name>
            <Text>Use global settings</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>Layer</Name>
            <Text>Layer</Text>
            <TextId>e_LAYER</TextId>
            <Value>-1</Value>
            <ValueType>Layer</ValueType>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>Pen</Name>
            <Text>Pen</Text>
            <TextId>e_PEN</TextId>
            <Value>1</Value>
            <ValueType>Pen</ValueType>
            <Enable>PenByLayer == False</Enable>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>PenByLayer</Name>
            <Text>Pen by layer</Text>
            <TextId>e_PEN_BY_LAYER</TextId>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
            <Enable>Layer != 0</Enable>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>Stroke</Name>
            <Text>Linetype</Text>
            <TextId>e_LINETYPE</TextId>
            <Value>1</Value>
            <ValueType>Stroke</ValueType>
            <Enable>StrokeByLayer == False</Enable>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>StrokeByLayer</Name>
            <Text>Linetype by layer</Text>
            <TextId>e_LINETYPE_BY_LAYER</TextId>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
            <Enable>Layer != 0</Enable>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>Color</Name>
            <Text>Color</Text>
            <TextId>e_COLOR</TextId>
            <Value>7</Value>
            <ValueType>Color</ValueType>
            <Enable>ColorByLayer == False</Enable>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>ColorByLayer</Name>
            <Text>Color by layer</Text>
            <TextId>e_COLOR_BY_LAYER</TextId>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
            <Enable>Layer != 0</Enable>
            <Visible>UseGlobalProperties == False</Visible>
          </Parameter>
          <Parameter>
            <Name>UseHelpConstruction</Name>
            <Text>Construction line</Text>
            <TextId>e_HELPCONSTRUCTION</TextId>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CommonPropertiesExp</Name>
        <Text>CommonProperties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value>CommonProperties(Color(3))</Value>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ComPropConditionExp</Name>
        <Text>CommonProperties with visible condition</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonPropCond</Name>
            <Text/>
            <Value>CommonProperties(Color(4))</Value>
            <ValueType>CommonProperties</ValueType>
            <Visible>|CommonPropCond.ColorByLayer:False|CommonPropCond.DrawOrder:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>List</Name>
    <Text>List</Text>
    <Parameters>
      <Parameter>
        <Name>CommonPropertiesListExp</Name>
        <Text>CommonProperties list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonPropCount</Name>
            <Text>Count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>CommonPropSep</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>CommonPropList</Name>
            <Text/>
            <TextDyn>"Box " + str($list_row + 1)</TextDyn>
            <Value>[CommonProperties();CommonProperties();CommonProperties()]</Value>
            <ValueType>CommonProperties</ValueType>
            <Dimensions>CommonPropCount</Dimensions>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
