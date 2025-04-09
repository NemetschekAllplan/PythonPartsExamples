<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\PythonParts\PythonPartWithSubObjects.py</Name>
    <Title>PythonPart with child objects</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>PythonPart</Name>
    <Text>PythonPart with child objects</Text>
    <Parameters>
      <Parameter>
        <Name>GeometryExpander</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Dimensions</Name>
            <Text>Length,Width,Height</Text>
            <Value>Vector3D(1000,1000,1000)</Value>
            <ValueType>Vector3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CommonPropsExpander</Name>
        <Text>Common properties</Text>
        <Value>True</Value>
        <!-- displays the expander collapsed-->
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ElementsToCreateExpander</Name>
        <Text>Create child objects</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CreateReinforcement</Name>
            <Text>Reinforcement</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateArchitectureElement</Name>
            <Text>Architecture element</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>LibrarySymbolRow</Name>
            <Text>Library symbol</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>CreateLibrarySymbol</Name>
                <Text/>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
              </Parameter>
              <Parameter>
                <Name>SymbolPath</Name>
                <Text/>
                <Value>etc\Library\2D Objects\Exterior\2D animals\Cat.sym</Value>
                <ValueType>String</ValueType>
                <ValueDialog>SymbolDialog</ValueDialog>
                <Visible>CreateLibrarySymbol</Visible>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>CreateFixture</Name>
            <Text>Fixture</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
