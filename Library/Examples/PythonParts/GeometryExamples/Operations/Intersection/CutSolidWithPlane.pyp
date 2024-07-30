<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\Intersection\CutSolidWithPlane.py</Name>
        <Title>Cut solid</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>SelectGeometry</Name>
        <Text>Cut solid with plane</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>volumetric 3D objects</Value>
            <ValueType>Text</ValueType>
        </Parameter>

        <Parameter>
            <Name>CreateObjectsExpander</Name>
            <Text>Objects to create</Text>
            <ValueType>Expander</ValueType>
            <Visible>True</Visible>

            <Parameter>
                <Name>CreateSolidAbove</Name>
                <Text>Create solid above</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateSolidBelow</Name>
                <Text>Create solid below</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>DeleteOriginalObjects</Name>
                <Text>Delete original objects</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Separator</Name>
            <Text></Text>
            <ValueType>Separator</ValueType>
            <Visible>CreateSolidAbove == True or CreateSolidBelow == True</Visible>
        </Parameter>

        <Parameter>
            <Name>CommonProperties</Name>
            <Text></Text>
            <Value></Value>
            <ValueType>CommonProperties</ValueType>
            <Visible>CreateSolidAbove == True or CreateSolidBelow == True</Visible>
        </Parameter>

    </Page>
</Element>
