<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\LocalGlobalShapeCreation.py</Name>
        <Title>LocalGlobalShapeCreation</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>
        
        <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>4000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>AngleZ</Name>
            <Text>Rotation angle</Text>
            <Value>33</Value>
            <ValueType>Double</ValueType>
        </Parameter>
    </Page>
    
    <Page>
        <Name>Page2</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>ConcreteGrade</Name>
            <Text>Concrete grade</Text>
            <Value>-1</Value>
            <ValueType>ReinfConcreteGrade</ValueType>
        </Parameter>
        <Parameter>
            <Name>SteelGrade</Name>
            <Text>Steel grade</Text>
            <Value>4</Value>
            <ValueType>ReinfSteelGrade</ValueType>
        </Parameter>
        <Parameter>
            <Name>Diameter</Name>
            <Text>Bar diameter</Text>
            <Value>20</Value>
            <ValueType>ReinfBarDiameter</ValueType>
        </Parameter>
        <Parameter>
            <Name>ConcreteCover</Name>
            <Text>Concrete cover</Text>
            <Value>25</Value>
            <ValueType>ReinfConcreteCover</ValueType>
        </Parameter>
        <Parameter>
            <Name>Distance</Name>
            <Text>Bar spacing</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>BendingRoller</Name>
            <Text>Bending roller</Text>
            <Value>4</Value>
            <ValueType>ReinfBendingRoller</ValueType>
        </Parameter>
    </Page>
</Element>
