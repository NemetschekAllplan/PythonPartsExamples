<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\Labels\LabelBarPlacementWithDimLine.py</Name>
    <Title>LabelBarPlacementWithDimLine</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>ELEMENT_SELECT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>LABEL_INPUT</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>LABEL_POSITION_BY_POINT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>LABEL_POSITION_BY_OFFSET</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Info</Name>
    <Text>Info</Text>
    <Visible>InputMode == ELEMENT_SELECT</Visible>
    <Parameters>
      <Parameter>
        <Name>InfoRow1</Name>
        <Text/>
        <Value>OVERALL</Value>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Info1</Name>
            <Text/>
            <Value>Create labels with dimension line</Value>
            <ValueType>Text</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>InfoRow2</Name>
        <Text>  </Text>
        <Value>OVERALL</Value>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Info2</Name>
            <Text/>
            <Value>for linear placements</Value>
            <ValueType>Text</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>DimensionLine</Name>
    <Text>Dimension line</Text>
    <Visible>InputMode == LABEL_INPUT</Visible>
    <Parameters>
      <Parameter>
        <Name>ReinforcementLabelExpander</Name>
        <Text>Dimension line placement</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DimLineOffset</Name>
            <Text>Dimension line offset</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>DimLineDistance</Name>
            <Text>Dimension line distance</Text>
            <Value>300</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
          </Parameter>
          <Parameter>
            <Name>DimLineAngleFrom</Name>
            <Text>Dimesion line angle from</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>DimLineAngleTo</Name>
            <Text>Dimesion line angle to</Text>
            <Value>360</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DimLine</Name>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\Reinforcement\DimensionLineProperties.incl</Value>
        <ValueType>Include</ValueType>
        <Visible>SetLabelOffset:False</Visible>
      </Parameter>
      <Parameter>
        <Name>DimLine</Name>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\Reinforcement\LabelProperties.incl</Value>
        <ValueType>Include</ValueType>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value/>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>ElementTierCount</Name>
        <Text>Element tier count</Text>
        <Value>1</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
