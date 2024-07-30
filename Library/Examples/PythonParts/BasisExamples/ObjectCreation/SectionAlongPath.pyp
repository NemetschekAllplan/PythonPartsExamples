<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\ObjectCreation\SectionAlongPath.py</Name>
        <Title>SectionAlongPath</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

        <Parameter>
            <Name>SectionPathInput</Name>
            <Text>Section path</Text>
            <Value>1</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>SectionPartByPolyline</Name>
                <Text>Polyline input</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>SectionPathSelect</Name>
                <Text>Select</Text>
                <Value>2</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>SectionPathInput == 1</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Labeling</Name>
            <Text>Labeling</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Header</Name>
                <Text>Header</Text>
                <Value>Section</Value>
                <ValueType>String</ValueType>
            </Parameter>

            <Parameter>
                <Name>SectionIdentifier</Name>
                <Text>Section identifier</Text>
                <Value>A</Value>
                <ValueType>String</ValueType>
            </Parameter>

        </Parameter>

    </Page>
</Element>
