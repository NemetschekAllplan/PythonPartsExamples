<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ToolsAndStartExamples\StepByStep.py</Name>
    <Title>StepByStep</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>StepByStep</Text>
    <Parameters>
      <Parameter>
        <Name>Step</Name>
        <Text>Step</Text>
        <Value>EmptyScript</Value>
        <ValueList>EmptyScript|Polyhedron|TwoPolyhedrons|UnitePolyhedrons|PythonPartFix|PythonPartWithPalette|PythonPartWithHandles|PythonPartWithReinforcement</ValueList>
        <ValueType>StringComboBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>Expander1</Name>
        <Text>Foundation</Text>
        <ValueType>Expander</ValueType>
        <Visible>Step.find("With") != -1</Visible>
        <Parameters>
          <Parameter>
            <Name>FoundationLength</Name>
            <Text>Foundation length</Text>
            <Value>3000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1.</MinValue>
          </Parameter>
          <Parameter>
            <Name>FoundationWidth</Name>
            <Text>Foundation width</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1.</MinValue>
          </Parameter>
          <Parameter>
            <Name>FoundationHeight</Name>
            <Text>Foundation height</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1.</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander2</Name>
        <Text>Column</Text>
        <ValueType>Expander</ValueType>
        <Visible>Step.find("With") != -1</Visible>
        <Parameters>
          <Parameter>
            <Name>XOffset</Name>
            <Text>X offset </Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>0.</MinValue>
            <MaxValue>FoundationLength - ColumnLength</MaxValue>
          </Parameter>
          <Parameter>
            <Name>YOffset</Name>
            <Text>Y offset </Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>0.</MinValue>
            <MaxValue>FoundationWidth - ColumnWidth</MaxValue>
          </Parameter>
          <Parameter>
            <Name>ColumnLength</Name>
            <Text>Column length</Text>
            <Value>600.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1.</MinValue>
          </Parameter>
          <Parameter>
            <Name>ColumnWidth</Name>
            <Text>Column with</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1.</MinValue>
          </Parameter>
          <Parameter>
            <Name>ColumnHeight</Name>
            <Text>Column height</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1.</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander3</Name>
        <Text>Reinforcement</Text>
        <ValueType>Expander</ValueType>
        <Visible>Step.find("WithReinf") != -1</Visible>
        <Parameters>
          <Parameter>
            <Name>SteelGrade</Name>
            <Text>Steel grade</Text>
            <TextId>e_STEEL_GRADE</TextId>
            <Value>4</Value>
            <ValueType>ReinfSteelGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCover</Name>
            <Text>Concrete cover</Text>
            <TextId>e_CONCRETE_COVER</TextId>
            <Value>20</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>Diameter1</Name>
            <Text>Bar diameter 1</Text>
            <TextId>e_BAR_DIAMETER</TextId>
            <Value>10</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>Spacing1</Name>
            <Text>Bar spacing 1</Text>
            <TextId>e_BAR_SPACING</TextId>
            <Value>150</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>SideLength1</Name>
            <Text>Start length 1</Text>
            <Value>500</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>DiameterStirrup</Name>
            <Text>Bar diameter stirrup</Text>
            <TextId>e_BAR_DIAMETER</TextId>
            <Value>10</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>SpacingStirrup</Name>
            <Text>Bar spacing stirrup</Text>
            <TextId>e_BAR_SPACING</TextId>
            <Value>150</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>DiameterULink</Name>
            <Text>Bar diameter U-link</Text>
            <TextId>e_BAR_DIAMETER</TextId>
            <Value>10</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>CountULink</Name>
            <Text>Bar count U-link</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>SideLengthULink</Name>
            <Text>Start length U-link</Text>
            <Value>1500</Value>
            <ValueType>Length</ValueType>
            <MinValue>FoundationHeight + 100</MinValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
