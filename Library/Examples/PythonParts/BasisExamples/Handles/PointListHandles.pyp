<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>BasisExamples\Handles\PointListHandles.py</Name>
        <Title>PointListHandles</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>
        <Parameters>
            <Parameter>
                <Name>PointListHandles</Name>
                <Text>Point list handles</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>Row1</Name>
                        <Text> </Text>
                        <ValueType>Row</ValueType>
                        <Parameters>
                            <Parameter>
                                <Name>X</Name>
                                <Value>X</Value>
                                <ValueType>Text</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>Y</Name>
                                <Value>Y</Value>
                                <ValueType>Text</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>Z</Name>
                                <Value>Z</Value>
                                <ValueType>Text</ValueType>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                    <Parameter>
                        <Name>PointList</Name>
                        <Text>PointList</Text>
                        <Value>[Point3D(1000,-1000,0);Point3D(1000,1000,0);Point3D(3000,1000,0);Point3D(4500,1000,0)]</Value>
                        <ValueType>Point3D</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>DistanceList</Name>
                        <Text>Length</Text>
                        <Value>[1000, 2000, 3000, 4000]</Value>
                        <ValueType>Length</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>

            <Parameter>
                <Name>RotationExp</Name>
                <Text>Rotation</Text>
                <ValueType>Expander</ValueType>

                <Parameters>
                    <Parameter>
                        <Name>RotAngleY</Name>
                        <Text>Y rotation</Text>
                        <Value>0</Value>
                        <ValueType>Angle</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RotAngleZ</Name>
                        <Text>Z rotation</Text>
                        <Value>0</Value>
                        <ValueType>Angle</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>RotationPoint</Name>
                        <Text>Rotation point</Text>
                        <Value>Point3D(0, 0, 0)</Value>
                        <ValueType>Point3D</ValueType>
                        <XYZinRow>True</XYZinRow>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
</Element>