<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Title>PythonPartPlacementPointConnection.py</Title>
        <Name>BasisExamples\PythonParts\PythonPartPlacementPointConnection.py</Name>
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
            <Name>PARAMETER_MODIFICATION</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>DimensionExp</Name>
            <Text>Dimensions</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>5000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>800</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PlacementPointExp</Name>
            <Text>Placement point</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>__PlacementPointConnection__</Name>
                <Text>Placement point connection</Text>
                <Value>False</Value>
                <ValueType>PointConnection</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
