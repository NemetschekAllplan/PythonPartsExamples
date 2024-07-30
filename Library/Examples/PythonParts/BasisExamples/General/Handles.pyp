<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\General\Handles.py</Name>
        <Title>Handles</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>CuboidExp</Name>
            <Text>Cuboid</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SlopeX</Name>
                <Text>Slope x</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>SlopeY</Name>
                <Text>Slope y</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>5000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Thickness</Name>
                <Text>Thickness</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
                <MaxValue>10000</MaxValue>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>100</IntervalValue>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>OffsetPoint</Name>
                <Text>Offset</Text>
                <Value></Value>
                <ValueType>Point3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ArcExp</Name>
            <Text>Arc with radio button handle</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>XPlacement</Name>
                <Text>X placement</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>
                <ValueList>-1|1</ValueList>

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
            </Parameter>

            <Parameter>
                <Name>YPlacement</Name>
                <Text>Y placement</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>
                <ValueList>-1|1</ValueList>

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
            </Parameter>

            <Parameter>
                <Name>DeltaAngle</Name>
                <Text>Delta angle</Text>
                <Value>90</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>PointListHandles</Name>
            <Text>Point list handles</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Row1</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

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
            </Parameter>

            <Parameter>
                <Name>PolyPoints</Name>
                <Text>PolyPoints</Text>
                <Value>[Point3D(500,-2000,0);Point3D(1000,-4000,0);Point3D(5000,-5000,0);Point3D(5000,-1000,0)]</Value>
                <ValueType>Point3D</ValueType>
            </Parameter>
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
        </Parameter>
        <Parameter>
            <Name>DistanceListHandles</Name>
            <Text>Distance list handles</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DistanceList</Name>
                <Text>Length</Text>
                <Value>[1000, 2000, 3000, 4000]</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>__HiddenPage__</Name>
        <Parameter>
            <Name>MirrorCuboid</Name>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>ShowInputControls</Name>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>ShowHandles</Name>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
</Element>
