<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ModelObjectExamples\SelectionExamples\PolyhedronFaceSelection.py</Name>
    <Title>PolyhedronFaceSelection</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>FirstPage</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>FaceSelectionSettingsExpander</Name>
        <Text>Settings of SelectPolyhedronFace</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>HighlightElement</Name>
            <Text>Highlight the polyhedron</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>HighlightFace</Name>
            <Text>Highlight face</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>SelectFaceIn</Name>
            <Text>Select face in</Text>
            <Value>InModel</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>SelectFaceInModel</Name>
                <Text>model</Text>
                <Value>InModel</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>SelectFaceInUVS</Name>
                <Text>UVS</Text>
                <Value>InUVS</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>SelectFaceInModelAndUVS</Name>
                <Text>model and UVS</Text>
                <Value>InModelAndUVS</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
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
