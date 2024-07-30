<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Arc3D.py</Name>
        <Title>Arc3D examples</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>Some 3D arcs</Text>
        <Parameter>
            <Name>StartAngle</Name>
            <Text>Start angle</Text>
            <Value>0.</Value>
            <ValueType>Angle</ValueType>
        </Parameter>        

        <Parameter>
            <Name>DeltaAngle</Name>
            <Text>Delta angle</Text>
            <Value>360.</Value>
            <ValueType>Angle</ValueType>
        </Parameter>

        <Parameter>
            <Name>Minor</Name>
            <Text>Minor radius</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>Major</Name>
            <Text>Major radius</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>CCW</Name>
            <Text>Counter clock wise</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator1</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>ShowZAxis</Name>
            <Text>Show Z-axis</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>ShowXAxis</Name>
            <Text>Show X-axis</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>CreatePlanarBReps</Name>
            <Text>Create planar BReps</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
     </Page>
</Element>
