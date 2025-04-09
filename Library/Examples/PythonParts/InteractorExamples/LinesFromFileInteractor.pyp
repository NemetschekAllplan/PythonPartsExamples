<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\LinesFromFileInteractor.py</Name>
    <Title>LinesFromFileInteractor</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>HiddenPage</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>FileName</Name>
        <Text>File name</Text>
        <Value/>
        <ValueType>String</ValueType>
        <Enable>False</Enable>
        <Visible>VersionNumber &gt; 0</Visible>
      </Parameter>
      <Parameter>
        <Name>LineName</Name>
        <Text>Line name</Text>
        <Value/>
        <ValueType>String</ValueType>
        <Enable>False</Enable>
        <Visible>VersionNumber &gt; 0</Visible>
      </Parameter>
      <Parameter>
        <Name>VersionNumber</Name>
        <Text>Version number</Text>
        <Value>0</Value>
        <ValueType>Integer</ValueType>
        <Enable>False</Enable>
        <Visible>VersionNumber &gt; 0</Visible>
      </Parameter>
      <Parameter>
        <Name>ElementFilter</Name>
        <Text>Element filter</Text>
        <Value>0</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>RadioButton1</Name>
            <Text>Vertical lines</Text>
            <Value>0</Value>
            <ValueType>RadioButton</ValueType>
            <Visible>VersionNumber == 0</Visible>
          </Parameter>
          <Parameter>
            <Name>RadioButton2</Name>
            <Text>Horizontal lines</Text>
            <Value>1</Value>
            <ValueType>RadioButton</ValueType>
            <Visible>VersionNumber == 0</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Pen</Name>
        <Text>Pen</Text>
        <TextId>e_PEN</TextId>
        <Value>1</Value>
        <ValueType>Pen</ValueType>
        <Visible>VersionNumber &gt; 0</Visible>
      </Parameter>
      <Parameter>
        <Name>Stroke</Name>
        <Text>Linetype</Text>
        <TextId>e_LINETYPE</TextId>
        <Value>1</Value>
        <ValueType>Stroke</ValueType>
        <Visible>VersionNumber &gt; 0</Visible>
      </Parameter>
      <Parameter>
        <Name>Color</Name>
        <Text>Color</Text>
        <TextId>e_COLOR</TextId>
        <Value>7</Value>
        <ValueType>Color</ValueType>
        <Visible>VersionNumber &gt; 0</Visible>
      </Parameter>
      <Parameter>
        <Name>ExecuteUpdate</Name>
        <Text>Execute update</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>ExecuteUpdateButton</Name>
            <Text>Execute</Text>
            <EventId>1001</EventId>
            <ValueType>Button</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
