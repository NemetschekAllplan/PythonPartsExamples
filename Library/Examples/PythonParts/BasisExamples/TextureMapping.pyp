<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\TextureMapping.py</Name>
    <Title>Examples for texture mapping</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Texture mapping</Text>
    <Parameters>
      <Parameter>
        <Name>Expander1</Name>
        <Text>Select surface</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Texture</Name>
            <Text>Texture</Text>
            <Value>klinker</Value>
            <DisableButtonIsShown>False</DisableButtonIsShown>
            <ValueType>MaterialButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>MappingType</Name>
            <Text>Mapping type</Text>
            <Value>eCube</Value>
            <ValueList>eCube|eWall|eRoof|eGround|eCylinder|eSphere</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>MappingAngle</Name>
            <Text>Mapping angle</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
          </Parameter>
          <Parameter>
            <Name>XScale</Name>
            <Text>X scale</Text>
            <Value>1.0</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>YScale</Name>
            <Text>Y scale</Text>
            <Value>1.0</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>XOffset</Name>
            <Text>X offset</Text>
            <Value>0.0</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>YOffset</Name>
            <Text>Y offset</Text>
            <Value>0.0</Value>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>ReferenceFace</Name>
            <Text>Reference face</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>ReferenceEdge</Name>
            <Text>Reference edge</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander2</Name>
        <Text>Color surface</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ColorID</Name>
            <Text>Line color</Text>
            <Value>255</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>RGBColorDialog</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander3</Name>
        <Text>Roof: Transparent surface</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>TransparentColorID</Name>
            <Text>Transparent color</Text>
            <Value>65280</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>RGBColorDialog</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>Transparency</Name>
            <Text>Transparency</Text>
            <Value>50</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>100</MaxValue>
          </Parameter>
          <Parameter>
            <Name>Refraction</Name>
            <Text>Refraction</Text>
            <Value>1.5</Value>
            <ValueType>Double</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>2.5</MaxValue>
          </Parameter>
          <Parameter>
            <Name>Roughness</Name>
            <Text>Roughness</Text>
            <Value>10</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>100</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander4</Name>
        <Text>Sphere: Diffuse reflection</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DiffuseReflection</Name>
            <Text>Diffuse reflection</Text>
            <Value>40</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>100</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander5</Name>
        <Text>Cylinder: Glossy reflection</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>GlossyReflection</Name>
            <Text>Glossy reflection</Text>
            <Value>60</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>100</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander6</Name>
        <Text>Cone: Lumiance</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Lumiance</Name>
            <Text>Lumiance</Text>
            <Value>30</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>100</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
