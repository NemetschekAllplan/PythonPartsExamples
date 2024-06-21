<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\PythonParts\MovePythonPart.py</Name>
        <Title>PlaceExistingPythonPart</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>ELEMENT_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>ELEMENT_PLACEMENT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>
        <Parameter>
            <Name>MoveOrCopy</Name>
            <Text>Action</Text>
            <Value>Move</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>RadioButtonMove</Name>
                <Text>Move</Text>
                <Value>Move</Value>
                <ValueType>RadioButton</ValueType>
                <Enable>InputMode == ELEMENT_SELECT</Enable>
            </Parameter>
            <Parameter>
                <Name>RadioButtonCopy</Name>
                <Text>Copy</Text>
                <Value>Copy</Value>
                <ValueType>RadioButton</ValueType>
                <Enable>InputMode == ELEMENT_SELECT</Enable>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>RotationAnglesExpander</Name>
            <Text>Rotation angles</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AngleX</Name>
                <Text>around X axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>AngleY</Name>
                <Text>around Y axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>AngleZ</Name>
                <Text>around Z axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
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
