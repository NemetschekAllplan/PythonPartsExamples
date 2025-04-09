<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
<Script>
    <Name>BasisExamples\PythonParts\PythonPartGroup.py</Name>
    <Title>PythonPart group</Title>
    <Version>1.0</Version>
</Script>
<Page>
    <Name>Page1</Name>
    <Text>PythonPart group</Text>
    <Parameters>
        <Parameter>
            <Name>GeometryExpander</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
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
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>CommonPropsExpander</Name>
            <Text>Common properties</Text>
            <Value>True</Value>
            <!-- displays the expander collapsed-->
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>CommonProp</Name>
                    <Text/>
                    <Value/>
                    <ValueType>CommonProperties</ValueType>
                </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>AttributesExpander</Name>
                <Text>Attributes</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                <Parameter>
                    <Name>LayerThickness</Name>
                    <Text>Layer thickness</Text>
                    <Value>300</Value>
                    <ValueType>Length</ValueType>
                    <MaxValue>min([vec.Z for vec in BoxDimensions]) - 10</MaxValue>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>CopyExpander</Name>
            <Text>Copies</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>NumberOfCopies</Name>
                    <Text>Number of copies</Text>
                    <Value>1</Value>
                    <ValueType>Integer</ValueType>
                    <Persistent>FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>Distance</Name>
                    <Text>Distance</Text>
                    <Value>Vector3D(0, 2000, 0)</Value>
                    <ValueType>Vector3D</ValueType>
                    <XYZinRow>True</XYZinRow>
                    <Visible>NumberOfCopies &gt; 1</Visible>
                    <Persistent>FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>BoxDimensionsOffset</Name>
                    <Text>Box dimensions offset</Text>
                    <Value>100</Value>
                    <ValueType>Length</ValueType>
                    <Visible>NumberOfCopies &gt; 1</Visible>
                    <Persistent>FAVORITE</Persistent>
                </Parameter>
            </Parameters>
        </Parameter>
    </Parameters>
</Page>
</Element>
