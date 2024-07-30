<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\Others\Fillet2D.py</Name>
        <Title>Fillet 2D</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>Fillet 2D</Name>
        <Text>Fillet of 2D lines and arcs</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>2D lines and arcs</Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>FilletPropertiesExpander</Name>
            <Text>Options of FilletCalculus2D</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>FilletRadius</Name>
                <Text>Radius</Text>
                <Value>200</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
