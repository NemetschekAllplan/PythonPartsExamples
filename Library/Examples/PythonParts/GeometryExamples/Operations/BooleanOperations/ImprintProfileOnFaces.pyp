<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\BooleanOperations\ImprintProfileOnFaces.py</Name>
    <Title>ImprintProfileOnFaces</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
    <Parameters><Parameter><Name>Format</Name><Text>Format</Text><ValueType>Expander</ValueType><Parameters><Parameter><Name>CommonProp</Name><Text/><Value/><ValueType>CommonProperties</ValueType></Parameter></Parameters></Parameter>

        &gt;<Parameter><Name>CuboidExp</Name><Text>BRep-Cuboid</Text><ValueType>Expander</ValueType><Parameters><Parameter><Name>Cuboid</Name><Text>Length,Width,Height</Text><Value>Vector3D(5000,4000,2000)</Value><ValueType>Vector3D</ValueType></Parameter></Parameters></Parameter>

        <Parameter><Name>RectangleExp</Name><Text>Bottom rectangle imprint</Text><ValueType>Expander</ValueType><Parameters><Parameter><Name>Rectangle</Name><Text>Length,Width</Text><Value>Vector2D(3000,3000)</Value><ValueType>Vector2D</ValueType></Parameter></Parameters></Parameter>

        <Parameter><Name>CircleExp</Name><Text>Top circle imprint</Text><ValueType>Expander</ValueType><Parameters><Parameter><Name>Circle</Name><Text>Circle</Text><Value>Circle2D(CenterPoint(2500, 2000)MajorRadius(1000))</Value><ValueType>Circle2D</ValueType></Parameter></Parameters></Parameter>

        <Parameter><Name>PolylineExp</Name><Text>Left polyline imprint</Text><ValueType>Expander</ValueType><Parameters><Parameter><Name>Polyline</Name><Text>Polyline</Text><Value>Polyline3D(Points((0,0,-500)(0,2000,2500)(0,4000,-500)))</Value><ValueType>Polyline3D</ValueType><XYZinRow>True</XYZinRow></Parameter></Parameters></Parameter>
    </Parameters>
  </Page>
</Element>
