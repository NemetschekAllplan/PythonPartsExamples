<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\MacroColumn.py</Name>
        <Title>MacroColumn</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page1</Text>

        <!-- Dimensions for the column  -->
        <Parameter>
            <Name>Height</Name>
            <Text>Column height</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
        </Parameter>
        <Parameter>
            <Name>Width</Name>
            <Text>       width</Text>
            <Value>200.</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
        </Parameter>
        <Parameter>
            <Name>Depth</Name>
            <Text>       depth</Text>
            <Value>300.</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
        </Parameter>

        <Parameter>
            <Name>Create3DBody</Name>
            <Text>Create 3D body</Text>
            <Value>True</Value>
            <ValueType>Checkbox</ValueType>
        </Parameter>

        #include RotationAngles.incpyp
    </Page>
</Element>
