<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Others\Fillet3D.py</Name>
    <Title>Fillet 3D</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>Fillet3d</Name>
    <Text>Fillet of 3D lines and solid edges</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>solids
3D lines</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>FilletPropertiesExpander</Name>
        <Text>Options of FilletCalculus3D</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>FilletRadius</Name>
            <Text>Radius</Text>
            <Value>50</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>PolyhedronOptionsText</Name>
            <Text>For polyhedron only:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>EdgesToFillet</Name>
            <Text>Egdes to fillet (leave empty for all)</Text>
            <Value>1,2</Value>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>EdgePropagation</Name>
            <Text>Neighboring edges propagation</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
