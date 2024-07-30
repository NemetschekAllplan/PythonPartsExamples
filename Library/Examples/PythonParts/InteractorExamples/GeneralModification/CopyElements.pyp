<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>InteractorExamples\GeneralModification\CopyElements.py</Name>
        <Title>CopyElements</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

        <Parameter>
            <Name>SelectionExpander</Name>
            <Text>Copy elements</Text>
            <ValueType>Expander</ValueType>
            <Visible>IsInSelection</Visible>

            <Parameter>
                <Name>Selection</Name>
                <Text>Select elements</Text>
                <Value></Value>
                <ValueType>Text</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CopyExpander</Name>
            <Text>Copy elements</Text>
            <ValueType>Expander</ValueType>
            <Visible>not IsInSelection</Visible>

            <Parameter>
                <Name>DistanceVectorRow</Name>
                <Text>Distance vector</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>DistanceVector</Name>
                    <Text>Distance vector</Text>
                    <Value>Vector3D(5000, 0, 0)</Value>
                    <ValueType>Vector3D</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>RotationVectorRow</Name>
                <Text>Rotation vector</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>RotationVector</Name>
                    <Text>Rotation vector</Text>
                    <Value>Vector3D(0, 0, 1000)</Value>
                    <ValueType>Vector3D</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>RotationAngle</Name>
                <Text>Rotation angle</Text>
                <Value>0</Value>
                <ValueList>0|45|90|180</ValueList>
                <ValueType>AngleComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>NumberOfCopies</Name>
                <Text>Number of copies</Text>
                <Value>5</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

        </Parameter>

    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Text>Hidden page</Text>
        <Parameter>
            <Name>IsInSelection</Name>
            <Text>State for selection</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Persistent>NO</Persistent>
        </Parameter>

    </Page>
</Element>
