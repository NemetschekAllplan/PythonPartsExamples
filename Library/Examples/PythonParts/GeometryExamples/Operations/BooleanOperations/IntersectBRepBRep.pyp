<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\BooleanOperations\IntersectBRepBRep.py</Name>
    <Title>IntersectBRepBRep</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters>
      <Parameter>
        <Name>Format</Name>
        <Text>Format</Text>
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
        <Name>BRepExp</Name>
        <Text>BRep-Cylinder</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CylinderSizes</Name>
            <Text>Radius,Height</Text>
            <Value>Vector2D(1000,6000)</Value>
            <ValueType>Vector2D</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlacementPoint</Name>
            <Text>Placement point</Text>
            <Value>Point3D(-3000, 0, 0)</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>AxisVector</Name>
            <Text>Axis vector</Text>
            <Value>Vector3D(1000, 0, 0)</Value>
            <ValueType>Vector3D</ValueType>
            <XYZinRow>True</XYZinRow>
          </Parameter>
          <Parameter>
            <Name>BRepColor</Name>
            <Text>Line color</Text>
            <Value>3</Value>
            <ValueType>Color</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SpereExp</Name>
        <Text>BRep-Sphere</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SphereRadius</Name>
            <Text>Radius</Text>
            <Value>2000</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>SphereColor</Name>
            <Text>Line color</Text>
            <Value>4</Value>
            <ValueType>Color</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
