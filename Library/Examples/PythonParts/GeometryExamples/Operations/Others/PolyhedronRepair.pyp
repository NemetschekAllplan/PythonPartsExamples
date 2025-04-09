<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Others\PolyhedronRepair.py</Name>
    <Title>Repair a polyhedron</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Polyhedronrepair</Name>
    <Text>Repair a polyhedron</Text>
    <Parameters>
      <Parameter>
        <Name>RepairType</Name>
        <Text>What to repair</Text>
        <Value>AllInOne</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>RepairCrossedLoopFaces</Name>
            <Text>crossed loop faces</Text>
            <Value>CrossedLoopFaces</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>RepairFaceNormals</Name>
            <Text>repair face normals</Text>
            <Value>RepairFaceNormals</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>RepairSplitFacesAtEdges</Name>
            <Text>split faces at edges</Text>
            <Value>SplitFacesAtEdges</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>RepairAllInOne</Name>
            <Text>all above</Text>
            <Value>AllInOne</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>RepairMergePlanarFaces</Name>
            <Text>merge planar faces</Text>
            <Value>MergePlanarFaces</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>SimplifyPolyhedron</Name>
            <Text>simplify polyhedron</Text>
            <Value>SimplifyPolyhedron</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
