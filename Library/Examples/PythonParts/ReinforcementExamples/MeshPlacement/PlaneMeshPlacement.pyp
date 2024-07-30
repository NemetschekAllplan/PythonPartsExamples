<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\MeshPlacement\PlaneMeshPlacement.py</Name>
        <Title>PlaneMeshPlacement</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>Geometry</Name>
            <Text>Geometry</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>2000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>CornerRecessLength</Name>
                <Text>Corner recess length</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>CornerRecessWidth</Name>
                <Text>Corner recess width</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Reinforcement</Name>
            <Text>Reinforcement</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MeshGroup</Name>
                <Text>Cross-section catalog</Text>
                <Value>-1</Value>
                <ValueType>ReinfMeshGroup</ValueType>
            </Parameter>
            <Parameter>
                <Name>MeshType</Name>
                <Text>Meshtype</Text>
                <Value>-1</Value>
                <ValueType>ReinfMeshType</ValueType>
                <Constraint>MeshGroup</Constraint>
            </Parameter>
            <Parameter>
                <Name>PreviewColor</Name>
                <Text>Preview color</Text>
                <Value>4</Value>
                <ValueType>Color</ValueType>
                <Persistent>FAVORITE</Persistent>
            </Parameter>
        </Parameter>
    </Page>
</Element>
