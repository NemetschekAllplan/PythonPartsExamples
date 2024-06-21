<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\ButtonControls\PictureResourceButtonList.py</Name>
        <Title>PictureResourceButtonList</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>TIER_1</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>TIER_2</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>TIER_3</Name>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>TIER_4</Name>
            <Value>4</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>TIER_5</Name>
            <Value>5</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>

    <Page>
        <Name>Page1</Name>
        <Text>Button controls</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SingleButtonExp</Name>
            <Text>Single picture resource button</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>EdgeOffsetType</Name>
                <Text>Integer value list</Text>
                <Value>0</Value>
                <ValueList>0|1|2|3|4</ValueList>
                <ValueTextList>Zero at start|Major value at start|Start equal end|Major value at end|Zero at end</ValueTextList>
                <EnumList2>AllplanSettings.PictResEdgeOffsetType.eZeroAtStart|
                           AllplanSettings.PictResEdgeOffsetType.eMajorValueAtStart|
                           AllplanSettings.PictResEdgeOffsetType.eStartEqualEnd|
                           AllplanSettings.PictResEdgeOffsetType.eMajorValueAtEnd|
                           AllplanSettings.PictResEdgeOffsetType.eZeroAtEnd|</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>

            <Parameter>
                <Name>TierCount</Name>
                <Text>Constants value list</Text>
                <Value>TIER_2</Value>
                <ValueList>TIER_1|TIER_2|TIER_3|TIER_4|TIER_5</ValueList>
                <EnumList2>AllplanSettings.PictResWallTierCount.eOneTier|
                           AllplanSettings.PictResWallTierCount.eTwoTiers|
                           AllplanSettings.PictResWallTierCount.eThreeTiers|
                           AllplanSettings.PictResWallTierCount.eFourTiers|
                           AllplanSettings.PictResWallTierCount.eFiveTiers|</EnumList2>
                <ValueTextList>1 tier|2 tiers|3 tiers|4 tiers|5 tiers</ValueTextList>
                <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShapeType</Name>
                <Text>Enum list</Text>
                <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eSemiCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eArbitrary</EnumList>
                <ValueTextList>Rectangle|Round/oval|Arc at top|Profile from library</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle|
                           AllplanSettings.PictResShapeType.eSemiCircle|
                           AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
                    <ValueType>PictureResourceButtonList</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ListButtonExp</Name>
            <Text>Picture resource button list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ShapeCount</Name>
                <Text>Shape count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>LineSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>ShapeTypes</Name>
                <TextDyn>"Shape " + str($list_row + 1)</TextDyn>
                <Value>[AllplanArchEle.VerticalOpeningShapeType.eRectangle,
                        AllplanArchEle.VerticalOpeningShapeType.eCircle,
                        AllplanArchEle.VerticalOpeningShapeType.eSemiCircle]
                </Value>
                <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eSemiCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eArbitrary</EnumList>
                <ValueTextList>Rectangle|Round/oval|Arc at top|Profile from library</ValueTextList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle|
                           AllplanSettings.PictResShapeType.eSemiCircle|
                           AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <Dimensions>ShapeCount</Dimensions>
            </Parameter>
        </Parameter>

    </Page>
</Element>
