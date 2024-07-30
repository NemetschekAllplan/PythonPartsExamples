<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\Objects\BitmapArea.py</Name>
        <Title>BitmapArea</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>GeneralSettings</Name>
            <Text>General settings</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>BitmapName</Name>
                <Text>Select bitmap</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <ValueDialog>BitmapResourceDialog</ValueDialog>
            </Parameter>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>XScalingFactor</Name>
                <Text>Scaling factor X</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>YScalingFactor</Name>
                <Text>Scaling factor Y</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>UseMetricalValues</Name>
                <Text>Use metrical values</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>UseRepeatTile</Name>
                <Text>Use repeat tile</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>RotationAngle</Name>
                <Text>Rotation angle</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>

            <Parameter>
                <Name>UseDirectionToReferenceLine</Name>
                <Text>Use direction to reference line</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>DirectionToReferenceLine</Name>
                <Text>Direction to ref line</Text>
                <Value>1</Value>
                <ValueList>1|2|3|4</ValueList>
                <Visible>UseDirectionToReferenceLine == True</Visible>
                <ValueType>IntegerComboBox</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>Transparency</Name>
            <Text>Transparency</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Transparency</Name>
                <Text>Transparency (%)</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <IntervalValue>1</IntervalValue>
            </Parameter>

            <Parameter>
                <Name>UsePixelMask</Name>
                <Text>Use pixel mask</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ColorToMask</Name>
                <Text>Color to mask</Text>
                <Value>255</Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>RGBColorDialog</ValueDialog>
                <Visible>UsePixelMask == True</Visible>
            </Parameter>
            <Parameter>
                <Name>TransparentColorTolerance</Name>
                <Text>Tolerance</Text>
                <Value>0</Value>
                <Visible>UsePixelMask == True</Visible>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <MinValue>0</MinValue>
                <MaxValue>255</MaxValue>
                <IntervalValue>1</IntervalValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Translation</Name>
            <Text>Translation</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Offset</Name>
                <Text>Offset</Text>
                <Value>Vector2D(0,0)</Value>
                <ValueType>Vector2D</ValueType>
            </Parameter>
        </Parameter>


        <Parameter>
            <Name>UseReferencePoint</Name>
            <Text>Define reference point</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReferencePoint</Name>
            <Text>Reference point</Text>
            <Value>Point2D(0.0, 0.0)</Value>
            <Visible>UseReferencePoint == 1</Visible>
            <ValueType>Point2D</ValueType>
        </Parameter>

    </Page>
</Element>
