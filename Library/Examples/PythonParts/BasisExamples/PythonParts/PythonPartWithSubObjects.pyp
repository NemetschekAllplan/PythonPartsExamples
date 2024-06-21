<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\PythonParts\PythonPartWithSubObjects.py</Name>
        <Title>PythonPart with child objects</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>PythonPart</Name>
        <Text>PythonPart with child objects</Text>
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
            <Name>ElementsToCreateExpander</Name>
            <Text>Create child objects</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CreateReinforcement</Name>
                <Text>Reinforcement</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateArchitectureElement</Name>
                <Text>Architecture element</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>LibrarySymbolRow</Name>
                <Text>Library symbol</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>CreateLibrarySymbol</Name>
                    <Text></Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>

                <Parameter>
                    <Name>SymbolPath</Name>
                    <Text></Text>
                    <Value>etc\Library\2D Objects\Exterior\2D animals\Cat.sym</Value>
                    <ValueType>String</ValueType>
                    <ValueDialog>SymbolDialog</ValueDialog>
                    <Visible>CreateLibrarySymbol</Visible>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>CreateFixture</Name>
                <Text>Fixture</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

        </Parameter>



    </Page>
</Element>
