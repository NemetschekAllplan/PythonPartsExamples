<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Title>PythonPartOpeningConnection.py</Title>
        <Name>BasisExamples\PythonParts\PythonPartOpeningConnection.py</Name>
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
            <Name>FrameExp</Name>
            <Text>Frame</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>FrameWidth</Name>
                <Text>Frame width</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>FrameThickness</Name>
                <Text>Frame thickness</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>FrameSurface</Name>
                <Text>Surface</Text>
                <Value>Materials\Plastic\Finishes\General_Plastic002</Value>
                <ValueType>MaterialButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PaneExp</Name>
            <Text>Pane</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PaneThickness</Name>
                <Text>Thickness</Text>
                <Value>20</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>PaneSurface</Name>
                <Text>Surface</Text>
                <Value>Materials\Glass\Transparent\Simple_Glass002</Value>
                <ValueType>MaterialButton</ValueType>
            </Parameter>
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
            <Name>OpeningConnection</Name>
            <Value></Value>
            <ValueType>TimeStampConnection</ValueType>
        </Parameter>
        <Parameter>
            <Name>GeometryElement</Name>
            <Value></Value>
            <ValueType>GeometryObject</ValueType>
        </Parameter>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>