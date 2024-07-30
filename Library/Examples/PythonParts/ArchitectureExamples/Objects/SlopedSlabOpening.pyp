<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\SlopedSlabOpening.py</Name>
        <Title>Sloped slab opening</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>START_AXIS_INPUT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>END_AXIS_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>OPENING_INPUT</Name>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>Sloped slab opening</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Text>Shape</Text>
                <Name>Shape</Name>
                <Value>AllplanArchEle.ShapeType.eRectangular</Value>
                <EnumList>AllplanArchEle.ShapeType.eRectangular|
                          AllplanArchEle.ShapeType.eCircular,
                          AllplanArchEle.ShapeType.eRegularPolygonCircumscribed|</EnumList>
                <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eCircle|
                                 AllplanSettings.TextResShapeType.eRegularPolygonCircumscribed</ValueTextIdList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle|
                           AllplanSettings.PictResShapeType.eRegularPolygonCircumscribed</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>

            <Parameter>
                <ValueType>ConditionGroup</ValueType>
                <Visible>Shape == AllplanArchEle.ShapeType.eRectangular</Visible>

                <Parameter>
                    <Name>CuboidWidth</Name>
                    <Text>Cuboid width</Text>
                    <Value>500</Value>
                    <ValueType>Length</ValueType>
                    <MinValue>10</MinValue>
                </Parameter>

                <Parameter>
                    <Name>CuboidHeight</Name>
                    <Text>Cuboid height</Text>
                    <Value>1000</Value>
                    <ValueType>Length</ValueType>
                    <MinValue>10</MinValue>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PipeRadius</Name>
                <Text>Pipe radius</Text>
                <Value>250</Value>
                <ValueType>Length</ValueType>
                <Visible>Shape in (AllplanArchEle.ShapeType.eCircular, AllplanArchEle.ShapeType.eRegularPolygonCircumscribed)</Visible>
            </Parameter>

            <Parameter>
                <Name>NumberOfCorners</Name>
                <Text>Number of corners (3-19)</Text>
                <Value>6</Value>
                <ValueType>Integer</ValueType>
                <MinValue>3</MinValue>
                <MaxValue>19</MaxValue>
                <Visible>Shape == AllplanArchEle.ShapeType.eRegularPolygonCircumscribed</Visible>
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
