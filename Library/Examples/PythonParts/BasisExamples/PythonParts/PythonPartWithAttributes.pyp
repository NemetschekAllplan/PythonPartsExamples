<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\PythonParts\PythonPartWithAttributes.py</Name>
        <Title>PythonPart with attributes</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>PythonPart</Name>
        <Text>PythonPart</Text>
        <Parameter>
            <Name>GeometryExpander</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Dimensions</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(1000,1000,1000)</Value>
                <ValueType>Vector3D</ValueType>
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
                <Name>AppendGeometryAttributes</Name>
                <Text>Append geometry attributes</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>LayerThickness</Name>
                <Text>Layer thickness</Text>
                <Value>300</Value>
                <MaxValue>Dimensions.Z</MaxValue>
                <ValueType>Attribute</ValueType>
                <AttributeId>211</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>OtherAttributesText</Name>
                <Text>Append other attributes:</Text>
                <Value></Value>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>DynamicAttributeList</Name>
                <Text>Attributes</Text>
                <Value>[(AttributeIdEnums.FIRE_RISK_FACTOR,A1);(0,)]</Value>
                <ValueType>AttributeIdValue</ValueType>
                <ValueDialog>AttributeSelection</ValueDialog>
            </Parameter>

        </Parameter>
    </Page>
</Element>
