<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PrecastExamples\ElementplanUVS.py</Name>
        <Title>Elementplan UVS</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <TextId>1000</TextId>
        <Text>Elementplan UVS</Text>

        <Parameter>
            <Name>Layout</Name>
            <Text>Layout</Text>
            <TextId>1001</TextId>
            <Value>---</Value>
            <ValueType>MultiMaterialLayoutCatalogReference</ValueType>
        </Parameter>
        <Parameter>
            <Name>Page</Name>
            <Text>Page</Text>
            <TextId>1002</TextId>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Sheet</Name>
                <Text>Sheet</Text>
                <TextId>1003</TextId>
                <Value>0</Value>
                <ValueType>MultiIndex</ValueType>
                <MaxValue>0</MaxValue>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>Change</Name>
            <Text>Change</Text>
            <TextId>1004</TextId>
            <Value>Scale</Value>
            <ValueTextId>1005</ValueTextId>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>BorderSize</Name>
            <Text>Border size</Text>
            <TextId>1006</TextId>
            <Value>Automatic selection</Value>
            <ValueTextId>1007</ValueTextId>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>Scale</Name>
            <Text>Scale</Text>
            <TextId>1005</TextId>
            <Value>Automatic selection {1007}</Value>
            <ValueList>Maximum size|Automatic selection|Fixed</ValueList>
            <ValueList_TextIds>1008|1007|1009</ValueList_TextIds>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>FixedScale</Name>
            <Text>Fixed</Text>
            <TextId>1009</TextId>
            <Value>50</Value>
            <ValueType>Double</ValueType>
            <Visible>Scale == "Fixed"</Visible>
        </Parameter>
    </Page>
</Element>