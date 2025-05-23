<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\ButtonControls\MaterialButtons.py</Name>
    <Title>MaterialButtons</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>MaterialButtonTest</Text>
    <Parameters>
      <Parameter>
        <Name>Length1</Name>
        <Text>Length</Text>
        <TextId>1001</TextId>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Surface1</Name>
        <Text>Surface 1</Text>
        <Value>30YearEdition Materials\\Wooden facades\\Wood_Boarding_01</Value>
        <DisableButtonIsShown>False</DisableButtonIsShown>
        <ValueType>MaterialButton</ValueType>
      </Parameter>
      <Parameter>
        <Name>Surface2</Name>
        <Text>Surface 2</Text>
        <Value>30YearEdition Materials\\Masonry\\Brick_wall_08</Value>
        <DisableButtonIsShown>True</DisableButtonIsShown>
        <ValueType>MaterialButton</ValueType>
      </Parameter>
      <Parameter>
        <Name>Surface3</Name>
        <Text>Surface 3</Text>
        <Value>Glass</Value>
        <DisableButtonIsShown>True</DisableButtonIsShown>
        <ValueType>MaterialButton</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
