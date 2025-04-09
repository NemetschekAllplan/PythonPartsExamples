<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ServiceExamples\BottomTopPlaneService.py</Name>
    <Title>BottomTopPlaneService</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>BottomTopPlaneService</Name>
    <Text>Plane access</Text>
    <Parameters>
      <Parameter>
        <Name>Plane</Name>
        <Text>Bottom-top plane</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlaneReferences</Name>
            <Text>Plane</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>PlaneTextBottom</Name>
            <Text>Bottom plane</Text>
            <Value>as Plane3D</Value>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>ReferenePlaneBottomRow</Name>
            <Text>Bottom reference plane</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>ReferencePlaneBottom</Name>
                <Text/>
                <Value/>
                <ValueType>GeometryObject</ValueType>
                <Persistent>NO</Persistent>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>PlaneTextTop</Name>
            <Text>Top plane</Text>
            <Value>as Plane3D</Value>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>ReferencePlaneTopRow</Name>
            <Text>Top reference plane</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>ReferencePlaneTop</Name>
                <Text> </Text>
                <Value/>
                <ValueType>GeometryObject</ValueType>
                <Persistent>NO</Persistent>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
