<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\PythonParts\ViewSettings.py</Name>
    <Title>Place PythonPart</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>PythonPart</Name>
    <Text>Python Part</Text>
    <Parameters>
      <Parameter>
        <Name>GeometryExpander</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
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
        <Name>AdvancedViewpropertiesSphere</Name>
        <Text>View properties: sphere</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SphereVisibleIn2D</Name>
            <Text>Visible in 2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereVisibleIn3D</Name>
            <Text>Visible in 3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereStartScale</Name>
            <Text>Start scale</Text>
            <Value>0</Value>
            <MinValue>0</MinValue>
            <MaxValue>9999</MaxValue>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereEndScale</Name>
            <Text>End scale</Text>
            <Value>9999</Value>
            <MinValue>0</MinValue>
            <MaxValue>9999</MaxValue>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereRefPoint1</Name>
            <Text>Reference point 1</Text>
            <Value>Point3D(0,0,0)</Value>
            <XYZinRow>True</XYZinRow>
            <Enable>False</Enable>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereRefPoint2</Name>
            <Text>Reference point 2</Text>
            <Value>Point3D(0,0,0)</Value>
            <XYZinRow>True</XYZinRow>
            <Enable>False</Enable>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereVisibilityLayerA</Name>
            <Text>Visibility layer A</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereVisibilityLayerB</Name>
            <Text>Visibility layer B</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereVisibilityLayerC</Name>
            <Text>Visibility layer C</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereScaleX</Name>
            <Text>Scale X</Text>
            <Value>Vx</Value>
            <ValueList>Vx|Vy|Vz</ValueList>
            <Enable>False</Enable>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereScaleY</Name>
            <Text>Scale Y</Text>
            <Value>Vy</Value>
            <ValueList>Vx|Vy|Vz</ValueList>
            <Enable>False</Enable>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereScaleZ</Name>
            <Text>Scale Z</Text>
            <Value>Vz</Value>
            <ValueList>Vx|Vy|Vz</ValueList>
            <Enable>False</Enable>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AdvancedViewpropertiesCube</Name>
        <Text>View properties: cube</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CubeVisibleIn2D</Name>
            <Text>Visible in 2D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeVisibleIn3D</Name>
            <Text>Visible in 3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeStartScale</Name>
            <Text>Start scale</Text>
            <Value>0</Value>
            <MinValue>0</MinValue>
            <MaxValue>9999</MaxValue>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeEndScale</Name>
            <Text>End scale</Text>
            <Value>9999</Value>
            <MinValue>0</MinValue>
            <MaxValue>9999</MaxValue>
            <ValueType>Double</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeRefPoint1</Name>
            <Text>Reference point 1</Text>
            <Value>Point3D(0,0,0)</Value>
            <XYZinRow>True</XYZinRow>
            <Enable>False</Enable>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeRefPoint2</Name>
            <Text>Reference point 2</Text>
            <Value>Point3D(0,0,0)</Value>
            <XYZinRow>True</XYZinRow>
            <Enable>False</Enable>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeVisibilityLayerA</Name>
            <Text>Visibility layer A</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeVisibilityLayerB</Name>
            <Text>Visibility layer B</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeVisibilityLayerC</Name>
            <Text>Visibility layer C</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeScaleX</Name>
            <Text>Scale X</Text>
            <Value>Vx</Value>
            <ValueList>Vx|Vy|Vz</ValueList>
            <Enable>False</Enable>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeScaleY</Name>
            <Text>Scale Y</Text>
            <Value>Vy</Value>
            <ValueList>Vx|Vy|Vz</ValueList>
            <Enable>False</Enable>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CubeScaleZ</Name>
            <Text>Scale Z</Text>
            <Value>Vz</Value>
            <ValueList>Vx|Vy|Vz</ValueList>
            <Enable>False</Enable>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
