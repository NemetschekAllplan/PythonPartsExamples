<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ContentExamples\Chair.py</Name>
        <Title>Chair</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>
                
        <Parameter>
            <Name>SeatWidth</Name>
            <Text>Seat width</Text>
            <Value>450.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>10000</MaxValue>
        </Parameter>
        <Parameter>
            <Name>SeatDepth</Name>
            <Text>Seat depth</Text>
            <Value>450.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>10000</MaxValue>
        </Parameter>
        <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>1200.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>3000</MaxValue>
        </Parameter>
        <Parameter>
            <Name>SeatThickness</Name>
            <Text>Seat thickness</Text>
            <Value>30.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>200</MaxValue>
        </Parameter>
        <Parameter>
            <Name>SeatHeight</Name>
            <Text>Seat height</Text>
            <Value>600.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>Height + SeatThickness</MaxValue>
        </Parameter>
        <Parameter>
            <Name>LegWidth</Name>
            <Text>Chair leg width</Text>
            <Value>40.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>100</MaxValue>
        </Parameter>
    </Page>
</Element>