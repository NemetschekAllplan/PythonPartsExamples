<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\IdenticalRotatedPlate.py</Name>
        <Title>Identical rotated plate</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page1</Text>

        <Parameter>
            <Text>Dimensions</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>500.</Value>
                <ValueType>Length</ValueType>
                <MinValue>10</MinValue>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>600.</Value>
                <ValueType>Length</ValueType>
                <MinValue>10</MinValue>
            </Parameter>

            <Parameter>
                <Name>Thickness</Name>
                <Text>Thickness</Text>
                <Value>20.</Value>
                <ValueType>Length</ValueType>
                <MinValue>1</MinValue>
            </Parameter>
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
                <ExcludeIdentical>True</ExcludeIdentical>
            </Parameter>
            <Parameter>
                <Name>RotationAngleY</Name>
                <Text>Rotation y-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
                <ExcludeIdentical>True</ExcludeIdentical>
            </Parameter>
            <Parameter>
                <Name>RotationAngleZ</Name>
                <Text>Rotation z-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
                <ExcludeIdentical>True</ExcludeIdentical>
            </Parameter>
        </Parameter>
    </Page>
</Element>
