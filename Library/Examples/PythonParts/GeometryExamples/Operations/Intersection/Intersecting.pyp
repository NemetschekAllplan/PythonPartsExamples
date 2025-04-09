<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Intersection\Intersecting.py</Name>
    <Title>Check intersection</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>SelectGeometry</Name>
    <Text>Calculate intersection</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>3D object
Arc (3D)
Line (2D)
Hatching, Filling, etc.
Splines (3D)
            </Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>IntersectingOptions</Name>
        <Text>Options of the Intersecting function</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PolygonOptionsText</Name>
            <Text>For 2D lines and polygons only:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>Tolerance</Name>
            <Text>Tolerance</Text>
            <Value>0.0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
