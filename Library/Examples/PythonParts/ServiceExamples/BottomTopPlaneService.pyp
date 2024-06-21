<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ServiceExamples\BottomTopPlaneService.py</Name>
        <Title>BottomTopPlaneService</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>BottomTopPlaneService</Name>
        <Text>Plane access</Text>

        <Parameter>
            <Name>Plane</Name>
            <Text>Bottom-top plane</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PlaneReferences</Name>
                <Text>Plane</Text>
                <Value></Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
            </Parameter>
            <Parameter>
                <Name>PlaneTextBottom</Name>
                <Text>Bottom plane</Text>
                <Value>as Plane3D</Value>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>ReferenePlaneBottomRow</Name>
                <Text>Bottom reference plane</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>ReferencePlaneBottom</Name>
                    <Text></Text>
                    <Value></Value>
                    <ValueType>GeometryObject</ValueType>
                    <Persistent>NO</Persistent>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PlaneTextTop</Name>
                <Text>Top plane</Text>
                <Value>as Plane3D</Value>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>ReferencePlaneTopRow</Name>
                <Text>Top reference plane</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>ReferencePlaneTop</Name>
                    <Text> </Text>
                    <Value></Value>
                    <ValueType>GeometryObject</ValueType>
                    <Persistent>NO</Persistent>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
