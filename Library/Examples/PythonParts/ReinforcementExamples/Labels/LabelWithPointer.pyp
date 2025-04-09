<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ReinforcementExamples\Labels\LabelWithPointer.py</Name>
    <Title>Label with pointer</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Label</Text>
    <Parameters>
      <Parameter>
        <Name>ReinforcementLabelExpander</Name>
        <Text>Reinforcement label</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>LabelPositionDefinition</Name>
            <Text>Define label position by</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>LabelPositionByPoint</Name>
                <Text>point</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>LabelPositionByOffset</Name>
                <Text>shape side and offset</Text>
                <Value>2</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>LabelPoint</Name>
            <Text>Label point</Text>
            <Value>Point2D(-200, 500)</Value>
            <XYZinRow>True</XYZinRow>
            <ValueType>Point2D</ValueType>
            <Visible>LabelPositionDefinition == 1</Visible>
          </Parameter>
          <Parameter>
            <Name>ShapeSide</Name>
            <Text>Shape side</Text>
            <Value>3</Value>
            <MinValue>1</MinValue>
            <MaxValue>6</MaxValue>
            <ValueType>Integer</ValueType>
            <Visible>LabelPositionDefinition == 2</Visible>
          </Parameter>
          <Parameter>
            <Name>ShapeSideFactor</Name>
            <Text>Shape side factor</Text>
            <Value>.3</Value>
            <MinValue>0</MinValue>
            <MaxValue>1</MaxValue>
            <ValueType>Double</ValueType>
            <Visible>LabelPositionDefinition == 2</Visible>
          </Parameter>
          <Parameter>
            <Name>LabelOffset</Name>
            <Text>Label offset</Text>
            <Value>Vector2D(-200, 0)</Value>
            <XYZinRow>True</XYZinRow>
            <ValueType>Vector2D</ValueType>
            <Visible>LabelPositionDefinition == 2</Visible>
          </Parameter>
          <Parameter>
            <Name>Angle</Name>
            <Text>Angle</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowTextPointer</Name>
            <Text>Show text pointer</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowTextPointerEndSymbol</Name>
            <Text>Show text pointer end symbol</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>ShowTextPointer</Visible>
          </Parameter>
          <Parameter>
            <Name>SetPointerStartPointRow</Name>
            <Text>Set pointer start point</Text>
            <ValueType>Row</ValueType>
            <Visible>ShowTextPointer</Visible>
            <Parameters>
              <Parameter>
                <Name>SetPointerStartPoint</Name>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
              </Parameter>
              <Parameter>
                <Name>PointerStartPoint</Name>
                <Value>Point2D(0,300)</Value>
                <ValueType>Point2D</ValueType>
                <Visible>SetPointerStartPoint</Visible>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>AdditionalTextRow</Name>
            <Text>Set additional text</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>SetAdditionalText</Name>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
              </Parameter>
              <Parameter>
                <Name>AdditionalText</Name>
                <Value/>
                <ValueType>String</ValueType>
                <Visible>SetAdditionalText</Visible>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ReinforcementLabelPropertiesExpander</Name>
        <Text>Reinforcement label properties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ShowPositionNumber</Name>
            <Text>Show position number</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowBarDiameter</Name>
            <Text>Show bar diameter</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowBarDistance</Name>
            <Text>Show bar distance</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowBarCount</Name>
            <Text>Show bar count</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowBendingShape</Name>
            <Text>Show bending shape</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowBarPlace</Name>
            <Text>Show bar place</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowBarLength</Name>
            <Text>Show bar length</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowSteelGrade</Name>
            <Text>Show steel grade</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowPositionAtEnd</Name>
            <Text>Show position at end</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShowTwoLineText</Name>
            <Text>Show two line text</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TextPropertiesExpander</Name>
        <Text>Text properties</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>TextAlignment</Name>
            <Text>Text alignment</Text>
            <Value>eRightMiddle</Value>
            <ValueList>"|".join(str(key) for key in AllplanBasisEle.TextAlignment.names.keys())</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
