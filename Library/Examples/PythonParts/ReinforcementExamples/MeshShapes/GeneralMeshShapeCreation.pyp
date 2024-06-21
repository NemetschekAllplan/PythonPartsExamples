<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\MeshShapes\GeneralMeshShapeCreation.py</Name>
        <Title>GeneralShapeCreation</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>Reinforcement</Name>
            <Text>Reinforcement</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ConcreteGrade</Name>
                <Text>Concrete grade</Text>
                <Value>4</Value>
                <ValueType>ReinfConcreteGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>4</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
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
                <Name>MeshGroupDiamond</Name>
                <Text>Cross-section catalog diamond</Text>
                <Value>-1</Value>
                <ValueType>ReinfMeshGroup</ValueType>
            </Parameter>
            <Parameter>
                <Name>MeshTypeDiamond</Name>
                <Text>Meshtype diamond</Text>
                <Value>-1</Value>
                <ValueType>ReinfMeshType</ValueType>
                <Constraint>MeshGroupDiamond</Constraint>
            </Parameter>
            <Parameter>
                <Name>BendingRoller</Name>
                <Text>Bending roller</Text>
                <Value>4</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>
            <Parameter>
                <Name>Rearrange</Name>
                <Text>Rearrange</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

        </Parameter>
    </Page>
</Element>
