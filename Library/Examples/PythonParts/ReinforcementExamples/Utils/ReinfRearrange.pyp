<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\Utils\ReinfRearrange.py</Name>
        <Title>ReinfRearrange</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

        <Parameter>
            <Name>RearrangedLock</Name>
            <Text>Lock</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>FromBarPosition</Name>
            <Text>From bar position</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>FromMeshPosition</Name>
            <Text>From mesh position</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>ToBarPosition</Name>
            <Text>To bar position</Text>
            <Value>99999</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>ToMeshPosition</Name>
            <Text>To mesh position</Text>
            <Value>99999</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>AfterBarPosition</Name>
            <Text>After bar position</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>AfterMeshPosition</Name>
            <Text>After mesh position</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>IdenticalShapes</Name>
            <Text>Identical shapes</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>IdenticalPrefix</Name>
            <Text>Identical prefix</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Tolerance</Name>
            <Text>Tolerance</Text>
            <Value>1</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>RearrangeRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>Rearrange</Name>
                <Text>Rearrange</Text>
                <EventId>1000</EventId>
                <ValueType>Button</ValueType>
            </Parameter>
        </Parameter>

    </Page>
</Element>
