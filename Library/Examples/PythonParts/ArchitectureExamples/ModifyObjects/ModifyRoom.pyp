<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\ModifyObjects\ModifyRoom.py</Name>
        <Title>Modify Room</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>
    <Constants>  
        <Constant>
        <Name>ELEMENT_SELECT</Name>
        <Value>1</Value>
        <ValueType>Integer</ValueType>
        </Constant> 
        <Constant>
        <Name>ROOM_SELECTED</Name>
        <Value>3</Value>
        <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page</Name>
        <Text>Page</Text>
        <Visible>InputMode == ROOM_SELECTED</Visible>
        <Parameter>
            <Name>FormatPropertiesExpander</Name>
            <Text>Format properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>RoomAttributes</Name>
            <Text>Room attributes</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>StoreyCode</Name>
                <Text>Storey code</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>Name</Name>
                <Text>Name</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>Function</Name>
                <Text>Function</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>GeneralAttributes</Name>
            <Text>General attributes</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Text</Name>
                <Text>Text</Text>
                <Value></Value>
                <ValueType>Text</ValueType>
            </Parameter>
            <Parameter>
                <Name>Texts</Name>
                <Text>Text</Text>
                <Value>[""] * 5</Value>
                <ValueType>String</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
            </Parameter>
            <Parameter>
                <Name>Attributes</Name>
                <Text>Attributes</Text>
                <Value></Value>
                <ValueType>Text</ValueType>
            </Parameter>
            <Parameter>
                <Name>Factor</Name>
                <Text>Factor</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <ValueType>Expander</ValueType>
                <Parameter>
                    <Name>PlaneReferences</Name>
                    <Text>Room height</Text>
                    <Value></Value>
                    <ValueType>PlaneReferences</ValueType>
                    <ValueDialog>PlaneReferences</ValueDialog>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>UserAttributesPage</Name>
        <Text>User attributes</Text>
        <Visible>InputMode == ROOM_SELECTED</Visible>
        <Parameter>
            <Name>UserAttributes</Name>
            <Text></Text>
            <Value>[]</Value>
            <ValueType>AttributeIdValue</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
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
