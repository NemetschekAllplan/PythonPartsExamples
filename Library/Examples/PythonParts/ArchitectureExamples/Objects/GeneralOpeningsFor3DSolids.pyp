<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\GeneralOpeningsFor3DSolids.py</Name>
        <Title>Sloped general opening</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>SOLID_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>OPENING_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>

    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>ElementFilterExp</Name>
            <Text>Element filter</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Elements3D</Name>
                <Text>3D elements</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>PythonParts</Name>
                <Text>PythonParts</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSillProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>AttributesExp</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>HasIndependent2DInteraction</Name>
                <Text>Above/below section plane</Text>
                <Value></Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
    </Page>
</Element>
