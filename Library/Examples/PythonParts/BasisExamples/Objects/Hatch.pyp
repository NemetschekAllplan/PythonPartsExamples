<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>BasisExamples\Objects\Hatch.py</Name>
        <Title>Hatch</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>POLYGON_INPUT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>PALETTE_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
<Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
        <Parameter>
            <Name>FormatExp</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>ComProp</Name>
                    <Text/>
                    <Value/>
                    <ValueType>CommonProperties</ValueType>
                    <Visible>|Color:False|HelpConstruction:False</Visible>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>ComPropGeo</Name>
                    <Text></Text>
                    <Value></Value>
                    <ValueType>CommonProperties</ValueType>
                    <Visible>|Pen:False|Stroke:False|Layer:False|DrawOrder:False</Visible>
                    <Constraint>
ComPropGeo.Pen           = ComProp.Pen
ComPropGeo.PenByLayer    = ComProp.PenByLayer
ComPropGeo.Stroke        = ComProp.Stroke
ComPropGeo.StrokeByLayer = ComProp.StrokeByLayer
ComPropGeo.Layer         = ComProp.Layer
ComPropGeo.DrawOrder     = ComProp.DrawOrder
                    </Constraint>
                </Parameter>
                <Parameter>
                    <Name>GeometrySep</Name>
                    <ValueType>Separator</ValueType>
                </Parameter>
                <Parameter>
                    <Name>ShowPolygon</Name>
                    <Text>Show polygon</Text>
                    <Value>True</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>HatchFormatExp</Name>
            <Text>Hatch format</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>ComPropHatch</Name>
                    <Text/>
                    <Value/>
                    <ValueType>CommonProperties</ValueType>
                    <Visible>|Pen:False|Stroke:False|Layer:False|DrawOrder:False|HelpConstruction:False</Visible>
                    <Constraint>
ComPropHatch.Pen           = ComProp.Pen
ComPropHatch.PenByLayer    = ComProp.PenByLayer
ComPropHatch.Stroke        = ComProp.Stroke
ComPropHatch.StrokeByLayer = ComProp.StrokeByLayer
ComPropHatch.Layer         = ComProp.Layer
ComPropHatch.DrawOrder     = ComProp.DrawOrder
                    </Constraint>
                </Parameter>
            </Parameters>
        </Parameter>
        <Parameter>
            <Name>HatchEleExp</Name>
            <Text>Hatch element</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
                <Parameter>
                    <Name>HatchId</Name>
                    <Text>Hatch ID</Text>
                    <Value>1</Value>
                    <ValueType>Hatch</ValueType>
                </Parameter>
                <Parameter>
                    <Name>DefineBackgroundColor</Name>
                    <Text>Define background color</Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BackgroundColor</Name>
                    <Text>Background color</Text>
                    <Value/>
                    <ValueType>Integer</ValueType>
                    <ValueDialog>RGBColorDialog</ValueDialog>
                    <Visible>DefineBackgroundColor == 1</Visible>
                </Parameter>
                <Parameter>
                    <Name>IsScaleDependent</Name>
                    <Text>Adjust to scale</Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RotationAngle</Name>
                    <Text>Angle</Text>
                    <Value>0</Value>
                    <ValueType>Angle</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SelectSide</Name>
                    <Text>Select side</Text>
                    <Value></Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>DirectionToReferenceLine</Name>
                    <Text>Edge number</Text>
                    <Value>0</Value>
                    <ValueType>Integer</ValueType>
                    <Enable>SelectSide</Enable>
                    <Constraint>max(DirectionToReferenceLine, 1) if SelectSide else 0</Constraint>
                    <MinValue>1 if SelectSide else 0</MinValue>
                    <MaxValue>PolygonSegmentCount</MaxValue>
                    <ValueSlider>True</ValueSlider>
                </Parameter>
                <Parameter>
                    <Name>DefineReferencePoint</Name>
                    <Text>Define reference point</Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>ReferencePoint</Name>
                    <Text>Reference point</Text>
                    <Value>Point2D()</Value>
                    <ValueType>Point2D</ValueType>
                    <Visible>DefineReferencePoint == 1</Visible>
                </Parameter>
            </Parameters>
        </Parameter>
    </Parameters>
</Page>
<Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
        <Parameter>
            <Name>InputMode</Name>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        <Parameter>
            <Name>PolygonSegmentCount</Name>
            <Text></Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
            <Persistent>NO</Persistent>
        </Parameter>
    </Parameters>
    </Page>
</Element>
