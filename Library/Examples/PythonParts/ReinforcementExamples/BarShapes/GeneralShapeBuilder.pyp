<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\BarShapes\GeneralShapeBuilder.py</Name>
    <Title>General shapes</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>GeneralShapes</Name>
    <Text>General shapes</Text>
    <Parameters>
      <Parameter>
        <Name>ShapeTypeExpander</Name>
        <Text>Shape type</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ShapeType</Name>
            <Text>Function of GeneralReinfShapeBuilder</Text>
            <Value>Straight bar with hooks</Value>
            <ValueList>Circle stirrup with user hooks|Straight bar with anchorage|Straight bar with hooks|Straight bar with user defined hooks|L-shape with hooks|Hook stirrup|Open stirrup|S-hook|Spacer|Stirrup|Stirrup with user hooks|U-link|U-link variable</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeometryParametersExpander</Name>
        <Text>Rebar geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>1000.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>ConcreteCoverLeft + ConcreteCoverRight + 10</MinValue>
            <Visible>ShapeType != "Circle stirrup with user hooks"</Visible>
          </Parameter>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>800.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>ConcreteCoverBottom + ConcreteCoverTop + 10</MinValue>
            <Visible>ShapeType not in ["Circle stirrup with user hooks", "Straight bar with anchorage", "Straight bar with hooks","Straight bar with user defined hooks","Hook stirrup","S-hook"]</Visible>
          </Parameter>
          <Parameter>
            <Name>SecondWidth</Name>
            <Text>SecondWidth</Text>
            <Value>500.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>ConcreteCoverBottom + ConcreteCoverTop + 10</MinValue>
            <Visible>ShapeType == "U-link variable"</Visible>
          </Parameter>
          <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>100.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
            <Visible>ShapeType == "Spacer"</Visible>
          </Parameter>
          <Parameter>
            <Name>Radius</Name>
            <Text>Radius</Text>
            <Value>800.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>2 * ConcreteCoverLeft + 10</MinValue>
            <Visible>ShapeType == "Circle stirrup with user hooks"</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeneralReinfShapeBuilderParametersExpander</Name>
        <Text>Parameters relevant for GeneralReinfShapeBuilder</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>StartAnchorage</Name>
            <Text>Start anchorage</Text>
            <Value>300</Value>
            <ValueType>Length</ValueType>
            <Visible>ShapeType == "Straight bar with anchorage"</Visible>
          </Parameter>
          <Parameter>
            <Name>EndAnchorage</Name>
            <Text>End anchorage</Text>
            <Value>300</Value>
            <ValueType>Length</ValueType>
            <Visible>ShapeType == "Straight bar with anchorage"</Visible>
          </Parameter>
          <Parameter>
            <Name>Overlap</Name>
            <Text>Overlap</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <Visible>ShapeType == "Circle stirrup with user hooks"</Visible>
          </Parameter>
          <Parameter>
            <Name>StartHook</Name>
            <Text>Start hook (0=calculate, -1=off)</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <Visible>ShapeType in ["Circle stirrup with user hooks", "Straight bar with hooks", "Straight bar with user defined hooks", "L-shape with hooks", "Open stirrup", "Stirrup with user hooks","U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>EndHook</Name>
            <Text>End hook (0=calculate, -1=off)</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <Visible>ShapeType in ["Circle stirrup with user hooks", "Straight bar with hooks", "Straight bar with user defined hooks", "L-shape with hooks", "Open stirrup", "Stirrup with user hooks","U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>StartHookAngle</Name>
            <Text>Start hook angle</Text>
            <Value>90</Value>
            <MinValue>-180</MinValue>
            <MaxValue>180</MaxValue>
            <ValueType>Angle</ValueType>
            <Visible>ShapeType in ["Circle stirrup with user hooks", "Straight bar with user defined hooks", "Hook stirrup", "Open stirrup", "Stirrup with user hooks","U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>EndHookAngle</Name>
            <Text>End hook angle</Text>
            <Value>90</Value>
            <MinValue>-180</MinValue>
            <MaxValue>180</MaxValue>
            <ValueType>Angle</ValueType>
            <Visible>ShapeType in ["Circle stirrup with user hooks", "Straight bar with user defined hooks", "Hook stirrup", "Open stirrup", "Stirrup with user hooks","U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>StartHookType</Name>
            <Text>Start hook type</Text>
            <Value>based on hook angle</Value>
            <ValueType>StringComboBox</ValueType>
            <ValueList>"based on hook angle|" + "|".join(str(key) for key in AllplanReinf.HookType.names.keys())</ValueList>
            <Visible>ShapeType in ["Straight bar with user defined hooks","Open stirrup","U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>EndHookType</Name>
            <Text>End hook type</Text>
            <Value>based on hook angle</Value>
            <ValueType>StringComboBox</ValueType>
            <ValueList>"based on hook angle|" + "|".join(str(key) for key in AllplanReinf.HookType.names.keys())</ValueList>
            <Visible>ShapeType in ["Straight bar with user defined hooks","U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>HookLength</Name>
            <Text>Hook length (0=calculate)</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <Visible>ShapeType in ["Hook stirrup", "S-hook", "Stirrup", "U-link", "U-link variable"]</Visible>
          </Parameter>
          <Parameter>
            <Name>StirrupType</Name>
            <Text>Stirrup type</Text>
            <Value>Normal</Value>
            <ValueType>StringComboBox</ValueType>
            <ValueList>"|".join(str(key) for key in AllplanReinf.StirrupType.names.keys())</ValueList>
            <Visible>ShapeType in ["Stirrup with user hooks","Stirrup"]</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ShapePropertiesExpander</Name>
        <Text>ReinforcementShapeProperties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Diameter</Name>
            <Text>Bar diameter</Text>
            <Value>10.0</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>BendingRoller</Name>
            <Text>Bending roller</Text>
            <Value>4.0</Value>
            <ValueType>ReinfBendingRoller</ValueType>
          </Parameter>
          <Parameter>
            <Name>SteelGrade</Name>
            <Text>Steel grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfSteelGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteGrade</Name>
            <Text>Concrete grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfConcreteGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>BendingShapeType</Name>
            <Text>Bending shape type</Text>
            <Value>LongitudinalBar</Value>
            <ValueList>"|".join(str(key) for key in AllplanReinf.BendingShapeType.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ConcreteCoverPropertiesExpander</Name>
        <Text>ConcreteCoverProperties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ConcreteCoverLeft</Name>
            <Text>Left</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverBottom</Name>
            <Text>Bottom</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverRight</Name>
            <Text>Right</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverTop</Name>
            <Text>Top</Text>
            <Value>25.0</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
