<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ServiceExamples\ZoomService.py</Name>
        <Title>Zoom service</Title>
        <Version>1.0</Version>
    </Script>
    <Constants>
        <Constant>
            <Name>ZOOM</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>ELEMENT_SELECT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>ZoomService</Name>
        <Text>Zoom to element</Text>

        <Parameter>
            <Name>ZoomTo</Name>
            <Text>Zoom to</Text>
            <Value>ZoomToMinMaxBox</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>RadioButtonZoomToElement</Name>
                <Text>selected element</Text>
                <Value>ZoomToElement</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>RadioButtonZoomToElements</Name>
                <Text>selected elements</Text>
                <Value>ZoomToElements</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>RadioButtonZoomToMinMaxBox</Name>
                <Text>min/max box</Text>
                <Value>ZoomToMinMaxBox</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>MinPoint</Name>
            <Text>Min point</Text>
            <Value>Point3D(0,0,0)</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <Visible>ZoomTo == "ZoomToMinMaxBox"</Visible>
        </Parameter>
        <Parameter>
            <Name>MaxPoint</Name>
            <Text>Max point</Text>
            <Value>Point3D(1000,1000,1000)</Value>
            <ValueType>Point3D</ValueType>
            <XYZinRow>True</XYZinRow>
            <Visible>ZoomTo == "ZoomToMinMaxBox"</Visible>
        </Parameter>

        <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>ZoomBy</Name>
            <Text>Zoom by</Text>
            <Value>ZoomByInflateValue</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>RadioButtonZoomByInflateValue</Name>
                <Text>inflate value for min/max box</Text>
                <Value>ZoomByInflateValue</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>

            <Parameter>
                <Name>RadioButtonZoomByFactor</Name>
                <Text>factor</Text>
                <Value>ZoomByFactor</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>InflateValue</Name>
            <Text>Inflate value</Text>
            <Value>1.0</Value>
            <ValueType>Double</ValueType>
            <Visible>ZoomBy == "ZoomByInflateValue"</Visible>
        </Parameter>

        <Parameter>
            <Name>ZoomFactor</Name>
            <Text>Zoom factor</Text>
            <Value>1.0</Value>
            <ValueType>Double</ValueType>
            <Visible>ZoomBy == "ZoomByFactor"</Visible>
        </Parameter>

        <Parameter>
            <Name>ZoomInAllViews</Name>
            <Text>Zoom in all viewports</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>ZoomButtonRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>ZoomButton</Name>
                <Text>Zoom!</Text>
                <EventId>1001</EventId>
                <ValueType>Button</ValueType>
                <Enable>InputMode == ZOOM</Enable>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
