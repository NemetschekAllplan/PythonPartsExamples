<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ModelObjectExamples\SelectionExamples\WallFaceSelection.py</Name>
    <Title>WallFaceSelection</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>SelectedFaceExpander</Name>
        <Text>Selected face</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>FacePolygonRow</Name>
            <Text>Face polygon</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>FacePolygon</Name>
                <Text>Point</Text>
                <Value/>
                <ValueType>Polygon3D</ValueType>
                <Enable>False</Enable>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>NormalVectorRow</Name>
            <Text>Normal vector</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>NormalVector</Name>
                <Text>Normal vector</Text>
                <Value>Vector3D()</Value>
                <ValueType>Vector3D</ValueType>
                <Enable>False</Enable>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
