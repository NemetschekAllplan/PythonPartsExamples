<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\AttributeControls\Attribute.py</Name>
        <Title>Attribute example</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Attributes</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Sizes</Name>
                <Text>Length,Width,Height</Text>
                <Value>Vector3D(5000,500,1000)</Value>
                <ValueType>Vector3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>AttributeExp</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SequenceNumber</Name>
                <Text>Sequence number</Text>
                <Value>1111</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>206</AttributeId>
            </Parameter>
            <Parameter>
                <Name>LayerThickness</Name>
                <Text>Layer thickness</Text>
                <Value>30</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>211</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Material</Name>
                <Text>Material</Text>
                <Value>Concrete</Value>
                <ValueList>Concrete|Steel|Wooden</ValueList>
                <ValueType>StringComboBox</ValueType>
                <ValueListFile>usr\tmp\PypComboSettings\Material.val</ValueListFile>
                <AttributeId>508</AttributeId>
            </Parameter>
            <Parameter>
                <Name>ApprovalDate</Name>
                <Text>Approval date</Text>
                <Value>date(2022,4,27)</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>386</AttributeId>
            </Parameter>
            <Parameter>
                <Name>LoadBearing</Name>
                <Text>Load bearing</Text>
                <Value>1</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>573</AttributeId>
            </Parameter>
            <Parameter>
                <Name>CalculationMode</Name>
                <Text>Calculation mode</Text>
                <Value>2</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>120</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Unit</Name>
                <Text>Unit</Text>
                <Value>m</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>202</AttributeId>
            </Parameter>
            <Parameter>
                <Name>LayoutFormat</Name>
                <Text>Layout format</Text>
                <Value>DIN A0</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>375</AttributeId>
            </Parameter>
            <Parameter>
                <Name>IfCObjectType</Name>
                <Text>IFC object type</Text>
                <Value>IfcBeam</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>684</AttributeId>
            </Parameter>
            <Parameter>
                <Name>AreaTypeFloorSpace</Name>
                <Text>Area type floor space</Text>
                <Value>WO</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>233</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Hatching</Name>
                <Text>Hatching</Text>
                <Value>301</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>5001</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Filling</Name>
                <Text>Filling</Text>
                <Value>4</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>5002</AttributeId>
            </Parameter>
            <Parameter>
                <Name>Pattern</Name>
                <Text>Pattern</Text>
                <Value>301</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>5003</AttributeId>
            </Parameter>
            <Parameter>
                <Name>IntegerCombo</Name>
                <Text>Integer value</Text>
                <Value>22</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>5004</AttributeId>
            </Parameter>
            <Parameter>
                <Name>DoubleCombo</Name>
                <Text>Double values</Text>
                <Value>33.3</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>5005</AttributeId>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>List</Name>
        <Text>Attribute list</Text>

        <Parameter>
            <Name>AttributeList</Name>
            <Text></Text>
            <TextDyn>"$Attribute_Name"</TextDyn>
            <Value>["A1","F30",2]</Value>
            <ValueType>Attribute</ValueType>
            <AttributeId>[1398, 935, 209]</AttributeId>
        </Parameter>
    </Page>
</Element>
