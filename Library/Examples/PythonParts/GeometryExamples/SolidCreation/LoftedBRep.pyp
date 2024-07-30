<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\SolidCreation\LoftedBRep.py</Name>
        <Title>Lofted BRep</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page</Name>
        <Text>Lofted BRep</Text>

        <Parameter>
            <Name>ProfilesParameterExpander</Name>
            <Text>Parameters of the profiles</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SquareSide</Name>
                <Text>Square profile size</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>Radius</Name>
                <Text>Circular profile radius</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
            </Parameter>



        </Parameter>

        <Parameter>
            <Name>LoftedBRepParameterExpander</Name>
            <Text>Parameters of LoftedBRep3D</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Periodic</Name>
                <Text>Periodic</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>Linear</Name>
                <Text>Linear</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CloseCaps</Name>
                <Text>Close caps</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateProfileEdges</Name>
                <Text>Create profile edges</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>OtherParameterExpander</Name>
            <Text>Other options</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CreateProfileCurves</Name>
                <Text>Create profile curves</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
