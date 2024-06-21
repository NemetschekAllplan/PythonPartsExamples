<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ReinforcementExamples\BarShapes\CorbelBar3D.py</Name>
        <Title>3D corbel bar</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Column geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * ConcreteCover + 2 * Diameter + (BendingRoller + 1) * Diameter</MinValue>
            </Parameter>

            <Parameter>
                <Name>Thickness</Name>
                <Text>Thickness</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * ConcreteCover + 2 * Diameter + (BendingRoller + 1) * Diameter</MinValue>
            </Parameter>

            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>5000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * ConcreteCover + 2 * Diameter + (BendingRoller + 1) * Diameter</MinValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Corbel geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CorbelWidth</Name>
                <Text>Corbel width</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * ConcreteCover + 2 * Diameter + (BendingRoller + 1) * Diameter</MinValue>
            </Parameter>
            <Parameter>
                <Name>CorbelHeight</Name>
                <Text>Corbel height</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>2 * ConcreteCover + 2 * Diameter + (BendingRoller + 1) * Diameter</MinValue>
            </Parameter>
            <Parameter>
                <Name>ElevationCorbel1</Name>
                <Text>Elevation corbel 1</Text>
                <Value>2500.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>ElevationCorbel2</Name>
                <Text>Elevation corbel 2</Text>
                <Value>3500.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
       </Parameter>

        <Parameter>
            <Name>Expander2</Name>
            <Text>Reinforcement</Text>
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
                <Name>BendingRoller</Name>
                <Text>Bending roller</Text>
                <Value>4.0</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>

            <Parameter>
                <Name>Diameter</Name>
                <Text>Bar diameter</Text>
                <Value>10.0</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>PreviewColor</Name>
                <Text>Preview color</Text>
                <Value>4</Value>
                <ValueType>Color</ValueType>
                <Persistent>FAVORITE</Persistent>
            </Parameter>

            <Parameter>
                <Name>DiameterInside</Name>
                <Text>Bar diameter inside</Text>
                <Value>10.0</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCoverInside</Name>
                <Text>Concrete cover inside</Text>
                <Value>100.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>PreviewColorInside</Name>
                <Text>Preview color</Text>
                <Value>5</Value>
                <ValueType>Color</ValueType>
                <Persistent>FAVORITE</Persistent>
            </Parameter>

            <Parameter>
                <Name>BarStartEndLength</Name>
                <Text>Bar start/end length</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>