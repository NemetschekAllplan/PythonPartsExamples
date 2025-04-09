<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\Layout\NestedExpanders.py</Name>
    <Title>Nested Expanders</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page1</Text>
    <Parameters>
      <Parameter>
        <Name>CommonPropertiesExp</Name>
        <Text>Common Properties</Text>
        <ValueType>Expander</ValueType>
        <Value>True</Value>
        <!-- Should this expander be collapsed-->
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value>CommonProperties(Color(3))</Value>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ExpanderBottomColumns</Name>
        <Text>Bottom columns (Expander level 1)</Text>
        <Value>False</Value>
        <!-- Should this expander be collapsed-->
        <ValueType>Expander</ValueType>
        <Visible>HideBottomColumns == False</Visible>
        <Parameters>
          <Parameter>
            <Name>ExpanderBottomLeftColumn</Name>
            <Text>Left Column (Expander level 2)</Text>
            <Value>False</Value>
            <!-- Should this expander be collapsed-->
            <ValueType>Expander</ValueType>
            <Parameters>
              <Parameter>
                <Name>GeometryBottomLeftExp</Name>
                <Text>Geometry (Expander level 3)</Text>
                <ValueType>Expander</ValueType>
                <Value>False</Value>
                <!-- Should this expander be collapsed-->
                <Parameters>
                  <Parameter>
                    <Name>Width1_1</Name>
                    <Text>Width of left column</Text>
                    <Value>2000.</Value>
                    <ValueType>Length</ValueType>
                  </Parameter>
                  <Parameter>
                    <Name>Depth1_1</Name>
                    <Text>Depth of left column</Text>
                    <Value>1000.</Value>
                    <ValueType>Length</ValueType>
                  </Parameter>
                </Parameters>
              </Parameter>
              <Parameter>
                <Name>SurfacePropBottomLeftExp</Name>
                <Text>Surface Properties (Expander level 3)</Text>
                <ValueType>Expander</ValueType>
                <Value>True</Value>
                <!-- Should this expander be collapsed-->
                <Visible>HideSurfaceProperties == False</Visible>
                <Parameters>
                  <Parameter>
                    <Name>SurfacePropBottomLeft</Name>
                    <Text/>
                    <Value/>
                    <ValueType>SurfaceElementProperties</ValueType>
                  </Parameter>
                </Parameters>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ExpanderBottomRightColumn</Name>
            <Text>Right Column (Expander level 2)</Text>
            <Value>False</Value>
            <!-- Should this expander be collapsed-->
            <ValueType>Expander</ValueType>
            <Parameters>
              <Parameter>
                <Name>Width1_2</Name>
                <Text>Width of right column</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>Depth1_2</Name>
                <Text>Depth of right column</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
              </Parameter>
              <Parameter>
                <Name>SurfacePropBottomRightExp</Name>
                <Text>Surface Properties (Expander level 3)</Text>
                <ValueType>Expander</ValueType>
                <Value>True</Value>
                <!-- Should this expander be collapsed-->
                <Visible>HideSurfaceProperties == False</Visible>
                <Parameters>
                  <Parameter>
                    <Name>SurfacePropBottomRight</Name>
                    <Text/>
                    <Value/>
                    <ValueType>SurfaceElementProperties</ValueType>
                  </Parameter>
                </Parameters>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ExpanderTopColumns</Name>
        <Text>Top columns (Expander level 1)</Text>
        <Value>True</Value>
        <!-- Should this expander be collapsed-->
        <ValueType>Expander</ValueType>
        <Visible>HideTopColumns == False</Visible>
        <Parameters>
          <Parameter>
            <Name>Width2</Name>
            <Text>Width of top columns</Text>
            <Value>1500.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Depth2</Name>
            <Text>Depth of top columns</Text>
            <Value>1500.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>SurfacePropTopExp</Name>
            <Text>Surface Properties (Expander level 2)</Text>
            <ValueType>Expander</ValueType>
            <Value>False</Value>
            <!-- Should this expander be collapsed-->
            <Visible>HideSurfaceProperties == False</Visible>
            <Parameters>
              <Parameter>
                <Name>SurfacePropTop</Name>
                <Text/>
                <Value/>
                <ValueType>SurfaceElementProperties</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>TextPropertiesExp</Name>
        <Text>Text Properties</Text>
        <ValueType>Expander</ValueType>
        <Value>True</Value>
        <!-- Should this expander be collapsed-->
        <Parameters>
          <Parameter>
            <Name/>
            <Text/>
            <Value>etc\PythonPartsFramework\ParameterIncludes\TextProperties.incl</Value>
            <ValueType>Include</ValueType>
            <Visible>HideTextProperties == False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ChangeVisibilityExp</Name>
        <Text>Expanders visibility</Text>
        <ValueType>Expander</ValueType>
        <Value>False</Value>
        <!-- Should this expander be collapsed-->
        <Parameters>
          <Parameter>
            <Name>HideBottomColumns</Name>
            <Text>Hide expander Bottom Columns</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>HideTopColumns</Name>
            <Text>Hide expander Top Columns</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>HideSurfaceProperties</Name>
            <Text>Hide expanders Surface Properties</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>HideTextProperties</Name>
            <Text>Hide expander Text Properties</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
