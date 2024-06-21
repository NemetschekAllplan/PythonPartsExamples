<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\RoomInput.py</Name>
        <Title>RoomInput</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Room</Name>
        <Text>Room</Text>

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

        <Parameter>
            <Name>UserAttributes</Name>
            <Text></Text>
            <Value>[]</Value>
            <ValueType>AttributeIdValue</ValueType>
            <ValueDialog>AttributeSelectionInsert</ValueDialog>
        </Parameter>
    </Page>
</Element>
