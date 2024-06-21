<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ModelObjectExamples\General\ShowObjectInformation.py</Name>
        <Title>Object information</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Object information</Name>
        <Text>Object information</Text>

        <Parameter>
            <Name>GeneralInfoExpander</Name>
            <Text>General information</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DescriptiveData</Name>
                <Text>Descriptive data</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ParentObject</Name>
                <Text>Parent object</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ChildObjects</Name>
                <Text>Child object</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CommonProp</Name>
                <Text>Common properties</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>Attributes</Name>
                <Text>Attributes</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>GeometryExpander</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ElementGeometry</Name>
                <Text>Element geometry</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ModelGeometry</Name>
                <Text>Model element geometry</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>GroundViewGeo</Name>
                <Text>Ground view geometry</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

            <Parameter>
                <Name>PureArchEleGeometry</Name>
                <Text>Pure architecture geometry</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
        </Parameter>


        <Parameter>
            <Name>APIObjectExpander</Name>
            <Text>API object</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>APIObject</Name>
                <Text>Python API object</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>

        </Parameter>
    </Page>
</Element>
