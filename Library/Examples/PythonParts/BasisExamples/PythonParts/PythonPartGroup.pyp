<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\PythonParts\PythonPartGroup.py</Name>
        <Title>PythonPart group</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>PythonPart group</Text>

        <Parameter>
            <Name>GeometryExpander</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BoxCount</Name>
                <Text>Number of boxes</Text>
                <Value>5</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>Spacing</Name>
                <Text>Spacing</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>BoxIndex</Name>
                <Text>Choose box</Text>
                <Value>1</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>BoxCount</MaxValue>
            </Parameter>
            <Parameter>
                <Name>BoxDimensions</Name>
                <Text>Dimension</Text>
                <Value>[Vector3D(1000,1000,1000);Vector3D(1500,1500,1500);Vector3D(1000,1000,1000);Vector3D(1500,1500,1500);Vector3D(1000,1000,1000)]</Value>
                <ValueType>Vector3D</ValueType>
                <ValueIndexName>BoxIndex</ValueIndexName>
                <Dimensions>BoxCount</Dimensions>
            </Parameter>

        </Parameter>
        <Parameter>
            <Name>CommonPropsExpander</Name>
            <Text>Common properties</Text>
            <Value>True</Value> <!-- displays the expander collapsed-->
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>AttributesExpander</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>LayerThickness</Name>
                <Text>Layer thickness</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

    </Page>
</Element>
