<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\SlopedGeneralOpening.py</Name>
        <Title>General opening</Title>
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
            <Name>General sloped opening</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Text>Shape</Text>
                <Name>Shape</Name>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eCircle</EnumList>
                <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eCircle</ValueTextIdList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>

            <Parameter>
                <ValueType>ConditionGroup</ValueType>
                <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eRectangle</Visible>

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
                <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eCircle</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSillProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>AttributesExp</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>HasIndependent2DInteraction</Name>
                <Text>Above/below section plane</Text>
                <Value></Value>
                <ValueType>CheckBox</ValueType>
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

        <Parameter>
            <Name>ElementThickness</Name>
            <Text>Element thickness</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
        </Parameter>

    </Page>
</Element>
