<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ModelObjectExamples\SelectionExamples\WallFaceSelection.py</Name>
        <Title>WallFaceSelection</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
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
