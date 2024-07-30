<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\Joint.py</Name>
        <Title>Joint</Title>
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
        <Text>Main Page</Text>

        <Parameter>
            <Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
   
            <Parameter>
                <Name>Width</Name>
                <Text>Joint width</Text>
                <Value>1010</Value>
                <ValueType>Length</ValueType>
                <MinValue>10</MinValue>
            </Parameter>

            <Parameter>
                <Name>Depth</Name>
                <Text>Joint depth</Text>
                <Value>50</Value>
                <ValueType>Length</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>ElementThickness</MaxValue>
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

    </Page>
</Element>
