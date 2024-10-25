<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\ModifyObjects\ModifyDoorOpening.py</Name>
        <Title>Modify door opening</Title>
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
            <Name>OPENING_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>
        <Visible>InputMode == OPENING_INPUT</Visible>

        <Parameter>
            <Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Shape</Name>
                <Text>Shape</Text>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eSemiDiamond|
                          AllplanArchEle.VerticalOpeningShapeType.eSemiCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eRiseBottomTop</EnumList>
                <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eSemiDiamond|
                                 AllplanSettings.TextResShapeType.eSemiCircle|
                                 AllplanSettings.TextResShapeType.eRiseBottomTop</ValueTextIdList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eSemiDiamond|
                           AllplanSettings.PictResShapeType.eSemiCircle|
                           AllplanSettings.PictResShapeType.eRiseBottomTop</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>

            <Parameter>
                <Name></Name>
                <Text></Text>
                <Value>etc\PythonPartsFramework\ParameterIncludes\VerticalOpeningGeometryProperties.incl</Value>
                <ValueType>Include</ValueType>
            </Parameter>

            <Parameter>
                <Name>SillHeight</Name>
                <Text>Sill height</Text>
                <Value></Value>
                <ValueType>Length</ValueType>
                <Constraint>HeightSettings.BottomElevation</Constraint>
                <Persistent>NO</Persistent>
            </Parameter>

            <Parameter>
                <Name>HeightSettings</Name>
                <Text>Opening height</Text>
                <Value>PlaneReferences(Height(2010))</Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
                <Constraint>BottomElevation=SillHeight;Height=HeightToRise + (RiseAtTop if Shape != AllplanArchEle.VerticalOpeningShapeType.eRiseBottomTop else RiseAtBottom + RiseAtTop)</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSillProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningRevealProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningDoorSwingProperties.incl</Value>
            <ValueType>Include</ValueType>
            <Visible>len(SmartSymbolGroup) == 0</Visible>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningTierOffsetProperties.incl</Value>
            <ValueType>Include</ValueType>
            <Visible>ElementTierCount &gt; 1</Visible>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSymbolsProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>AttributesExp</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>IsFrenchWindow</Name>
                <Text>French door</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
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

        <Parameter>
            <Name>ElementTierCount</Name>
            <Text>Element tier count</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>

        <Parameter>
            <Name>DoorSwingBasePointIndex</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
