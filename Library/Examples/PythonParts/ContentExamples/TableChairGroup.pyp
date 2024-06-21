<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ContentExamples\TableChairGroup.py</Name>
        <Title>TableChairGroup</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>TableLength</Name>
            <Text>Length</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>10000</MaxValue>
        </Parameter>
        <Parameter>
            <Name>TableWidth</Name>
            <Text>Width</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>10000</MaxValue>
        </Parameter>
        <Parameter>
            <Name>TableHeight</Name>
            <Text>Height</Text>
            <Value>800.</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
            <MaxValue>3000</MaxValue>
        </Parameter>
        <Parameter>
            <Name>BoardThickness</Name>
            <Text>Board thickness</Text>
            <Value>20.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>200</MaxValue>
        </Parameter>
        <Parameter>
            <Name>XExcessLength</Name>
            <Text>X excess length</Text>
            <Value>100.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>TableLength/2 - LegWidth</MaxValue>
        </Parameter>
        <Parameter>
            <Name>YExcessLength</Name>
            <Text>Y excess length</Text>
            <Value>100.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>TableWidth/2 - LegWidth</MaxValue>
        </Parameter>
        <Parameter>
            <Name>LegWidth</Name>
            <Text>Table leg width</Text>
            <Value>40.</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>100</MaxValue>
        </Parameter>
    </Page>
</Element>
