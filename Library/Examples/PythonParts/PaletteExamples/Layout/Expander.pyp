<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Layout\Expander.py</Name>
        <Title>Expander</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>Expander1</Name>
            <Text>First Cube</Text>
            <Value>True</Value> <!-- Should this expander be collapsed-->
            <ValueType>Expander</ValueType>
            <Visible>HideExpander1 == False</Visible>

            <Parameter>
                <Name>Length1</Name>
                <Text>Length</Text>
                <TextId>1001</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width1</Name>
                <Text>Width</Text>
                <TextId>1002</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height1</Name>
                <Text>Height</Text>
                <TextId>1003</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>HideExpander2</Name>
                <Text>Hide expander 'Second Cube'</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander2</Name>
            <Text>Second Cube</Text>
            <ValueType>Expander</ValueType>
            <Visible>HideExpander2 == False</Visible>

            <Parameter>
                <Name>HideExpander1</Name>
                <Text>Hide expander 'First Cube'</Text>
                <Value>False</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>Length2</Name>
                <Text>Length</Text>
                <TextId>1004</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width2</Name>
                <Text>Width</Text>
                <TextId>1005</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height2</Name>
                <Text>Height</Text>
                <TextId>1006</TextId>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>