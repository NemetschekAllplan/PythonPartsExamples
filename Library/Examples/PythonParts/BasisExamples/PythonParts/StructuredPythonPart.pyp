<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\PythonParts\StructuredPythonPart.py</Name>
        <Title>Structured PythonPart</Title>
        <Version>0.1</Version>
    </Script>
    <Page>
        <Name>FirstPage</Name>
        <Text>Structured PythonPart</Text>
        <Parameter>
            <Name>BoxCount</Name>
            <Text>Number of boxes</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>Spacing</Name>
            <Text>Spacing</Text>
            <Value>2000.0</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>BoxExpander</Name>
            <Text>Box properties</Text>
            <ValueType>Expander</ValueType>
            <Visible>True</Visible>

            <Parameter>
                <Name>BoxIndex</Name>
                <Text>Box index</Text>
                <Value>1</Value>
                <ValueType>MultiIndex</ValueType>
                <MinValue>1</MinValue>
                <MaxValue>BoxCount</MaxValue>
            </Parameter>
            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>[1000.0, 1500.0, 1300.0,]</Value>
                <ValueType>Length</ValueType>
                <ValueIndexName>BoxIndex</ValueIndexName>
                <Dimensions>BoxCount</Dimensions>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>[1000.0, 1500.0, 1300.0,]</Value>
                <ValueType>Length</ValueType>
                <ValueIndexName>BoxIndex</ValueIndexName>
                <Dimensions>BoxCount</Dimensions>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>[1000.0, 1500.0, 1300.0,]</Value>
                <ValueType>Length</ValueType>
                <ValueIndexName>BoxIndex</ValueIndexName>
                <Dimensions>BoxCount</Dimensions>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>CommonProps</Name>
                <Text></Text>
                <Value>[]*3</Value>
                <ValueType>CommonProperties</ValueType>
                <ValueIndexName>BoxIndex</ValueIndexName>
                <Dimensions>BoxCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>NestedHierarchyExpander</Name>
            <Text>Nested hierarchy</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CreateNestedHierarchy</Name>
                <Text>Create nested hierarchy</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateNestedHierarchyText</Name>
                <Text>Box index</Text>
                <Value>parent element</Value>
                <ValueType>Text</ValueType>
                <Visible>CreateNestedHierarchy</Visible>
            </Parameter>

            <Parameter>
                <Name>ParentElements</Name>
                <Text></Text>
                <Value>["None"]*3</Value>
                <ValueList>['None'] + [f'Box {i}' for i in range(BoxCount)]</ValueList>
                <ValueType>StringComboBox</ValueType>
                <Dimensions>BoxCount</Dimensions>
                <Visible>CreateNestedHierarchy</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ExtraOptionsExpander</Name>
            <Text>Additional options</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CreateBoundingBox</Name>
                <Text>Create simplified geometry</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>BoundingBoxFromScale</Name>
                <Text>From scale</Text>
                <Value>50.0</Value>
                <ValueType>Double</ValueType>
                <Visible>CreateBoundingBox</Visible>
            </Parameter>

        </Parameter>
    </Page>
</Element>