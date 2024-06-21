<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ContentExamples\SleeveFoundation.py</Name>
        <Title>SleeveFoundation</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>Picture1</Name>
            <Value>SleeveFoundation_geom1.png</Value>
            <Orientation>Middle</Orientation>
            <ValueType>Picture</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>Row1</Name>
            <Text>Foundation length</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>FoundationLength</Name>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Param01Picture</Name>
                <Value>param01.png</Value>
                <ValueType>Picture</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Row2</Name>
            <Text>Foundation width</Text>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>FoundationWidth</Name>
                <Value>1800.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Param02Picture</Name>
                <Value>param02.png</Value>
                <ValueType>Picture</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Row3</Name>
            <Text>Foundation height</Text>
            <ValueType>Row</ValueType>
            
            <Parameter>
                <Name>FoundationHeight</Name>
                <Value>450.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Param03Picture</Name>
                <Value>param03.png</Value>
                <ValueType>Picture</ValueType>
            </Parameter>
        </Parameter>
        
        <Parameter>
            <Name>SleeveOutLength</Name>
            <Text>Sleeve length of exterior side</Text>
            <Value>1200.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>SleeveOutWidth</Name>
            <Text>Sleeve width of exterior side</Text>
            <Value>1100.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>SleeveHeight</Name>
            <Text>Sleeve height</Text>
            <Value>850.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>SleeveThickness</Name>
            <Text>Sleeve wall thickness</Text>
            <Value>250.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>SleeveChamfer</Name>
            <Text>Sleeve chamfer</Text>
            <Value>50.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Expander</Name>
            <Text>Rotation</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RotationAngleX</Name>
                <Text>Rotation x-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>RotationAngleY</Name>
                <Text>Rotation y-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>RotationAngleZ</Name>
                <Text>Rotation z-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Page2</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>SleeveUShapeDiameter</Name>
            <Text>Sleeve U shape</Text>
            <Value>12</Value>
            <ValueType>ReinfBarDiameter</ValueType>
        </Parameter>
        <Parameter>
            <Name>FoundMeshGroup</Name>
            <Text>Cross-section</Text>
            <Value>4</Value>
            <ValueType>ReinfMeshGroup</ValueType>
        </Parameter>
        <Parameter>
            <Name>FoundMeshType</Name>
            <Text>Mesh type foundation</Text>
            <Value>R335B</Value>
            <ValueType>ReinfMeshType</ValueType>
        </Parameter>
    </Page>
</Element>
