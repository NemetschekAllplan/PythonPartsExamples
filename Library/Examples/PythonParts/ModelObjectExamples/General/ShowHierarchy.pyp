<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ModelObjectExamples\General\ShowHierarchy.py</Name>
        <Title>Object hierarchy</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>PrintingOptions</Name>
        <Text/>

        <Parameter>
            <Name>PrintingOptionsExpander</Name>
            <Text>Printing options</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MaxTreeDepth</Name>
                <Text>Maximum tree depth</Text>
                <Value>10</Value>
                <MinValue>1</MinValue>
                <MaxValue>100</MaxValue>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>PrintHiddenElements</Name>
                <Text>Print hidden elements</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

        </Parameter>

    </Page>
</Element>
