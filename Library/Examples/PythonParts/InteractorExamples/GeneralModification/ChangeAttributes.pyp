<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>InteractorExamples\GeneralModification\ChangeAttributes.py</Name>
        <Title>Change attributes</Title>
        <Version>1.0</Version>
        <ShowFavoriteButtons>False</ShowFavoriteButtons>
    </Script>
    <Page>
        <Name>ChangeAttributes</Name>
        <Text>Change attributes</Text>

        <Parameter>
            <Name>AttributeValuesExpander</Name>
            <Text>Attribute values</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DynamicAttributeList</Name>
                <Text>Attributes</Text>
                <Value>[(0,)]</Value>
                <ValueType>AttributeIdValue</ValueType>
                <ValueDialog>AttributeSelection</ValueDialog>
            </Parameter>

        </Parameter>

    </Page>
</Element>
