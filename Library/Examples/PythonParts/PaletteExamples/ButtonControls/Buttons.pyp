<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\ButtonControls\Buttons.py</Name>
        <Title>Buttons</Title>
        <Version>1.0</Version>
    </Script>
    <Constants>
        <Constant>
            <Name>SET_LENGTH_1000</Name>
            <Value>1000</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>SET_LENGTH_2000</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>SET_LENGTH_3000</Name>
            <Value>1002</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>CENTER_OF_GRAVITY</Name>
            <Value>1003</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>CENTER_OF_GRAVITY_SELECTED</Name>
            <Value>1004</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
            <Enable>False</Enable>
        </Parameter>

        <Parameter>
            <Name>Row1</Name>
            <Text>Button - set length to 1000mm</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Button1</Name>
                <Text>Press me!</Text>
                <EventId>SET_LENGTH_1000</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Row2</Name>
            <Text>PictureButton - set length to 2000mm</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Button2</Name>
                <Text></Text>
                <Value>ButtonImageReset16.png</Value>
                <EventId>SET_LENGTH_2000</EventId>
                <ValueType>PictureButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Row3</Name>
            <Text>PictureResourceButton - set length to 3000mm</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Button3</Name>
                <Text></Text>
                <Value>17027</Value>
                <EventId>SET_LENGTH_3000</EventId>
                <ValueType>PictureResourceButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RefPointButtonExp</Name>
            <Text>Refrence point button</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RefPointType</Name>
                <Text>Reference point type</Text>
                <Value>abc</Value>
                <ValueList>"|".join(str(item) for item in AllplanPalette.RefPointButtonType.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>RefPointButtonRow</Name>
                <Text>RefPointButton</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RefPointId</Name>
                    <Text>Reference point index</Text>
                    <Value>AllplanPalette.RefPointPosition.eCenterCenter</Value>
                    <ValueType>RefPointButton</ValueType>
                    <EnumList2>AllplanPalette.RefPointButtonType.names[RefPointType]</EnumList2>
                </Parameter>
                <Parameter>
                    <Name>CenterOfGravity</Name>
                    <Text>Center of gravity</Text>
                    <Value>AllplanSettings.PictResPalette.eCenterOfGravity</Value>
                    <EventId>CENTER_OF_GRAVITY</EventId>
                    <ValueType>PictureResourceButton</ValueType>
                    <Visible>RefPointId != 0</Visible>
                </Parameter>
                <Parameter>
                    <Name>CenterOfGravitySelected</Name>
                    <Text>Center of gravity selected</Text>
                    <Value>AllplanSettings.PictResPalette.eCenterOfGravitySelected</Value>
                    <EventId>CENTER_OF_GRAVITY_SELECTED</EventId>
                    <ValueType>PictureResourceButton</ValueType>
                    <Visible>RefPointId == 0</Visible>
                </Parameter>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>RefPointButtonListExp</Name>
            <Text>List of refrence point buttons</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RefPointButtonIndex</Name>
                <Text>Select list index</Text>
                <Value>2</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>3</MaxValue>
            </Parameter>

            <Parameter>
                <Name>RefPointButtonListRow</Name>
                <Text>RefPointButton</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RefPointIdList</Name>
                    <Text>Reference point list</Text>
                    <Value>[AllplanPalette.RefPointPosition.eCenterLeft,AllplanPalette.RefPointPosition.eCenterCenter,AllplanPalette.RefPointPosition.eCenterRight]</Value>
                    <ValueType>RefPointButton</ValueType>
                    <ValueIndexName>RefPointButtonIndex</ValueIndexName>
                </Parameter>
            </Parameter>
        </Parameter>

    </Page>
</Element>
