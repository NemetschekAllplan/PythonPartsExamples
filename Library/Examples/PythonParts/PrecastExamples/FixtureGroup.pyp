<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PrecastExamples\FixtureGroup.py</Name>
        <Title>Fixture group</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <TextId>1000</TextId>
        <Text>Fixture group</Text>

        <Parameter>
            <Name>Name</Name>
            <TextId>1001</TextId>
            <Text>Name</Text>
            <Value>Fixture group 1</Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>Dynamic</Name>
            <TextId>1002</TextId>
            <Text>Dynamic</Text>
            <Value>False</Value>
            <ValueType>Checkbox</ValueType>
            <Enable>GroupLeading == False</Enable>
        </Parameter>
        <Parameter>
            <Name>GroupLeading</Name>
            <TextId>1003</TextId>
            <Text>Group leading</Text>
            <Value>False</Value>
            <ValueType>Checkbox</ValueType>
            <Enable>Dynamic == False</Enable>
        </Parameter>
        <Parameter>
            <Name>ReferencePoint</Name>
            <TextId>1004</TextId>
            <Text>ReferencePoint</Text>
            <Value>125,0,0</Value>
            <ValueType>Point3D</ValueType>
            <Enable>GroupLeading == True</Enable>
        </Parameter>
    </Page>
</Element>