<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>BasisExamples\Handles\ArcHandles.py</Name>
        <Title>ArcHandles</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>
        <Parameters>
            <Parameter>
                <Name>ArcExp</Name>
                <Text>Arc with radio button handle</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>XPlacement</Name>
                        <Text>X placement</Text>
                        <Value>1</Value>
                        <ValueType>RadioButtonGroup</ValueType>
                        <ValueList>-1|1</ValueList>
                        <Parameters>
                            <Parameter>
                                <Name>XMinus</Name>
                                <Text>X Minus</Text>
                                <Value>-1</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>XPlus</Name>
                                <Text>X plus</Text>
                                <Value>1</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                    <Parameter>
                        <Name>YPlacement</Name>
                        <Text>Y placement</Text>
                        <Value>1</Value>
                        <ValueType>RadioButtonGroup</ValueType>
                        <ValueList>-1|1</ValueList>
                        <Parameters>
                            <Parameter>
                                <Name>YMinus</Name>
                                <Text>Y minus</Text>
                                <Value>-1</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>YPlus</Name>
                                <Text>Y plus</Text>
                                <Value>1</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                    <Parameter>
                        <Name>GeometryExp</Name>
                        <Text>Geometry</Text>
                        <ValueType>Expander</ValueType>
                        <Parameters>
                            <Parameter>
                                <Name>Arc</Name>
                                <Text>Arc</Text>
                                <Value>Arc2D(CenterPoint()MinorRadius(1000)MajorRadius(1000)AxisAngle(0)StartAngle(0)EndAngle(pi / 2)IsCounterClockwise(1))</Value>
                                <ValueType>Arc2D</ValueType>
                                <Visible>|MinorRadius:False</Visible>
                                <Constraint>Arc.MinorRadius = Arc.MajorRadius</Constraint>
                                <XYZinRow>True</XYZinRow>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
</Element>