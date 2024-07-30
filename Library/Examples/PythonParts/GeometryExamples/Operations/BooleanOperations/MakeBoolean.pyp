<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\BooleanOperations\MakeBoolean.py</Name>
        <Title>Make boolean operations</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>SelectGeometry</Name>
        <Text>Make boolean</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>3D objects and surfaces</Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>ObjectsToCreateExpander</Name>
            <Text>Objects to create</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CreateIntersectionSolid</Name>
                <Text>Create intersection solid</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>IntersectionCommonProp</Name>
                <Text></Text>
                <Value>-1</Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>CreateIntersectionSolid</Visible>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
                <Visible>CreateIntersectionSolid</Visible>
            </Parameter>

            <Parameter>
                <Name>CreateUnionSolid</Name>
                <Text>Create union solid</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>UnionCommonProp</Name>
                <Text></Text>
                <Value>-1</Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>CreateUnionSolid</Visible>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
                <Visible>CreateUnionSolid</Visible>
            </Parameter>

            <Parameter>
                <Name>CreateSubtraction1Solid</Name>
                <Text>Create subtraction first minus second</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Subtraction1CommonProp</Name>
                <Text></Text>
                <Value>-1</Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>CreateSubtraction1Solid</Visible>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
                <Visible>CreateSubtraction1Solid</Visible>
            </Parameter>

            <Parameter>
                <Name>CreateSubtraction2Solid</Name>
                <Text>Create subtraction second minus first</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Subtraction2CommonProp</Name>
                <Text></Text>
                <Value>-1</Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>CreateSubtraction2Solid</Visible>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>DeleteSourceElements</Name>
                <Text>Delete source solids</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
