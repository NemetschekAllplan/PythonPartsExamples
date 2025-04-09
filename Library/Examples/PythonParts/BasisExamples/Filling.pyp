<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\Filling.py</Name>
    <Title>Filling</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <Text>Length</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <Text>Width</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>SeparatorLengthWidth</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>FirstColorRed</Name>
        <Text>First color red</Text>
        <Value>255</Value>
        <ValueType>Integer</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </Parameter>
      <Parameter>
        <Name>FirstColorGreen</Name>
        <Text>First color green</Text>
        <Value>0</Value>
        <ValueType>Integer</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </Parameter>
      <Parameter>
        <Name>FirstColorBlue</Name>
        <Text>First color blue</Text>
        <Value>0</Value>
        <ValueType>Integer</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
      </Parameter>
      <Parameter>
        <Name>AllplanColor</Name>
        <Text>Allplan color as result</Text>
        <Value>6</Value>
        <ValueType>Color</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>255</MaxValue>
        <Enable>False</Enable>
      </Parameter>
      <Parameter>
        <Name>SeparatorFirstColor</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>DefineGradientFilling</Name>
        <Text>Define gradient filling</Text>
        <Value>False</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>SeparatorDefineGradientFilling</Name>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>FirstColorAlpha</Name>
        <Text>Transparency from [0..100]</Text>
        <Value>0</Value>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>SecondColorAlpha</Name>
        <Text>             to [0..100]</Text>
        <Value>0</Value>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>SeparatorAlpha</Name>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>RotationAngle</Name>
        <Text>Rotation angle</Text>
        <Value>0</Value>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Angle</ValueType>
      </Parameter>
      <Parameter>
        <Name>UseDirectionToReferenceLine</Name>
        <Text>Use direction to reference line</Text>
        <Value>False</Value>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>DirectionToReferenceLine</Name>
        <Text>Direction to ref line</Text>
        <Value>1</Value>
        <ValueList>1|2|3|4</ValueList>
        <Visible>DefineGradientFilling == True and UseDirectionToReferenceLine == True</Visible>
        <ValueType>IntegerComboBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>SeparatorRotation</Name>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>ShadingType</Name>
        <Text>Shading type</Text>
        <!-- selected value -->
        <Value>0</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>ShadingTypeLinear</Name>
            <Text>Linear</Text>
            <Value>0</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShadingTypeFromCorner</Name>
            <Text>From corner</Text>
            <Value>1</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShadingTypeFromCenter</Name>
            <Text>From center</Text>
            <Value>2</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>ShadingTypeRound</Name>
            <Text>Round</Text>
            <Value>3</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>VariantType</Name>
        <Text>Variant type</Text>
        <!-- selected value -->
        <Value>0</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>VariantType1</Name>
            <Text>Variant1</Text>
            <Value>0</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>VariantType2</Name>
            <Text>Variant2</Text>
            <Value>1</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>VariantType3</Name>
            <Text>Variant3</Text>
            <Value>2</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>VariantType4</Name>
            <Text>Variant4</Text>
            <Value>3</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SeparatorShadingVariant</Name>
        <Visible>DefineGradientFilling == True</Visible>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>TransitionType</Name>
        <Text>Transition type</Text>
        <!-- selected value -->
        <Value>0</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>NoTransition</Name>
            <Text>No transition</Text>
            <Value>0</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>OneColorTransition</Name>
            <Text>One color transition</Text>
            <Value>1</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>TwoColorTransition</Name>
            <Text>Two color transition</Text>
            <Value>2</Value>
            <Visible>DefineGradientFilling == True</Visible>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SeparatorTransition</Name>
        <Visible>DefineGradientFilling == True and TransitionType in {1,2}</Visible>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Transition</Name>
        <Text>Transition [0..255]</Text>
        <Value>0</Value>
        <Visible>DefineGradientFilling == True and TransitionType == 1</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>SecondColorRed</Name>
        <Text>Second color red</Text>
        <Value>0</Value>
        <Visible>DefineGradientFilling == True and TransitionType == 2</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>SecondColorGreen</Name>
        <Text>Second color green</Text>
        <Value>255</Value>
        <Visible>DefineGradientFilling == True and TransitionType == 2</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>SecondColorBlue</Name>
        <Text>Second color blue</Text>
        <Value>0</Value>
        <Visible>DefineGradientFilling == True and TransitionType == 2</Visible>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
