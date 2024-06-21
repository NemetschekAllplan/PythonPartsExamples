<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Title>ModelPolygonExtrudeInteractor.py</Title>
        <Name>InteractorExamples\General\ModelPolygonExtrudeInteractor.py</Name>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>ExtrusionVector</Name>
            <Text>Extrusion vector</Text>
            <Value>Vector3D(0,0,2000)</Value>
            <ValueType>Vector3D</ValueType>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Parameter>
            <Name>PythonPartUUID</Name>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>PolygonUUID</Name>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>Polygon</Name>
            <Value></Value>
            <ValueType>Polygon2D</ValueType>
        </Parameter>
    </Page>
</Element>