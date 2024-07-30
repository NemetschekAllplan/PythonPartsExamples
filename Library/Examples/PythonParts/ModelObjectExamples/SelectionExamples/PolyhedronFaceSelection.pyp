<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ModelObjectExamples\SelectionExamples\PolyhedronFaceSelection.py</Name>
        <Title>PolyhedronFaceSelection</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Parameter>
            <Name>FaceSelectionSettingsExpander</Name>
            <Text>Settings of SelectPolyhedronFace</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>HighlightElement</Name>
                <Text>Highlight the polyhedron</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>HighlightFace</Name>
                <Text>Highlight face</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>


            <Parameter>
                <Name>SelectFaceIn</Name>
                <Text>Select face in</Text>
                <Value>InModel</Value>
                <ValueType>RadioButtonGroup</ValueType>

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
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SelectedFaceExpander</Name>
            <Text>Selected face</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>FacePolygonRow</Name>
                <Text>Face polygon</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>FacePolygon</Name>
                    <Text>Point</Text>
                    <Value></Value>
                    <ValueType>Polygon3D</ValueType>
                    <Enable>False</Enable>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>NormalVectorRow</Name>
                <Text>Normal vector</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>NormalVector</Name>
                    <Text>Normal vector</Text>
                    <Value>Vector3D()</Value>
                    <ValueType>Vector3D</ValueType>
                    <Enable>False</Enable>
                </Parameter>
            </Parameter>

        </Parameter>
    </Page>
</Element>
