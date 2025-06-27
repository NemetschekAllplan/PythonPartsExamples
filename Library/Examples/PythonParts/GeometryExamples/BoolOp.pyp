<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\BoolOp.py</Name>
    <Title>BoolOp</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Addition</Text>
    <!-- Dimensions for the first polyhedron -->
    <!-- Reference point for the first polyhedron -->
    <!-- Dimensions for the second polyhedron -->
    <!-- Reference point for the second polyhedron -->
    <Parameters>
      <Parameter>
        <Name>Color1</Name>
        <Text>Line color</Text>
        <Value>8</Value>
        <ValueType>Color</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator1_1</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Length1_1</Name>
        <Text>Base body length</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width1_1</Name>
        <Text>           width</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness1_1</Name>
        <Text>            thickness</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref1X_1</Name>
        <Text>Reference point x</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref1Y_1</Name>
        <Text>              y</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref1Z_1</Name>
        <Text>              z</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator1_2</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Length1_2</Name>
        <Text>Additional body length</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width1_2</Name>
        <Text>               width</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness1_2</Name>
        <Text>                thickness</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref1X_2</Name>
        <Text>Reference point x</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref1Y_2</Name>
        <Text>              y</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref1Z_2</Name>
        <Text>              z</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Page2</Name>
    <Text>Subtraction</Text>
    <!-- Dimensions for the first polyhedron -->
    <!-- Reference point for the first polyhedron -->
    <!-- Dimensions for the second polyhedron -->
    <Parameters>
      <Parameter>
        <Name>Color2</Name>
        <Text>Line color</Text>
        <Value>5</Value>
        <ValueType>Color</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator2_1</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Length2</Name>
        <Text>Base body length</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width2</Name>
        <Text>           width</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness2</Name>
        <Text>            thickness</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref2X_1</Name>
        <Text>Reference point x</Text>
        <Value>4000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref2Y_1</Name>
        <Text>              y</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref2Z_1</Name>
        <Text>              z</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator2_2</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2X1</Name>
        <Text>Body to deduct polygon point 1 x</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Y1</Name>
        <Text>                             y</Text>
        <Value>500.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Z1</Name>
        <Text>                             z</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2X2</Name>
        <Text>Point 2 x</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Y2</Name>
        <Text>        y</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Z2</Name>
        <Text>        z</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2X3</Name>
        <Text>Point 3 x</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Y3</Name>
        <Text>        y</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Z3</Name>
        <Text>        z</Text>
        <Value>-300.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2X4</Name>
        <Text>Point 4 x</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Y4</Name>
        <Text>        y</Text>
        <Value>500.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>BasePol2Z4</Name>
        <Text>        z</Text>
        <Value>-300.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator2_3</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Height2</Name>
        <Text>Body to subtract height</Text>
        <Value>3000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Page4</Name>
    <Text>Addition Brep and Polyhedron</Text>
    <!-- Dimensions for the first solid -->
    <!-- Reference point for the first solid -->
    <!-- Dimensions for the second solid (cylinder) -->
    <!-- Reference point for the second solid -->
    <Parameters>
      <Parameter>
        <Name>Color4</Name>
        <Text>Line color</Text>
        <Value>4</Value>
        <ValueType>Color</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator4_1</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Length4_1</Name>
        <Text>Base body length</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width4_1</Name>
        <Text>           width</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness4_1</Name>
        <Text>            thickness</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref4X_1</Name>
        <Text>Reference point x</Text>
        <Value>12000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref4Y_1</Name>
        <Text>              y</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref4Z_1</Name>
        <Text>              z</Text>
        <Value>0.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Separator4_2</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Radius4</Name>
        <Text>Cylinder radius</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Height4</Name>
        <Text>         height</Text>
        <Value>2000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref4X_2</Name>
        <Text>Reference point x</Text>
        <Value>12500.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref4Y_2</Name>
        <Text>              y</Text>
        <Value>1500.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Ref4Z_2</Name>
        <Text>              z</Text>
        <Value>1000.0</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
