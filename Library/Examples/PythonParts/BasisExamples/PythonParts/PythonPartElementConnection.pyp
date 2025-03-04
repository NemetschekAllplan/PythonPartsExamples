<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Title>PythonPart element connection</Title>
        <Name>BasisExamples\PythonParts\PythonPartElementConnection.py</Name>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>ELEMENT_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>PARAMETER_MODIFICATION</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>ExtrusionVector</Name>
            <Text>Extrusion vector</Text>
            <Value>Vector3D(0,0,2000)</Value>
            <ValueType>Vector3D</ValueType>
            <Visible>InputMode == PARAMETER_MODIFICATION</Visible>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Parameter>
            <Name>SourceElementHash</Name>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
