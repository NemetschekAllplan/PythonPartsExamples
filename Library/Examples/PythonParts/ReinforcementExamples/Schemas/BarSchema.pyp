<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>ReinforcementExamples\Schemas\BarSchema.py</Name>
        <Title>BarSchema</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>ReinforcementPage</Name>
        <Text>Reinforcement</Text>
        <Parameters>
            <Parameter>
                <Name>BarShapeExpander</Name>
                <Text>BarShapeProperties</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>SteelGrade</Name>
                        <Text>Steel grade</Text>
                        <Value>4</Value>
                        <ValueType>ReinfSteelGrade</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>ConcreteCover</Name>
                        <Text>Concrete cover</Text>
                        <Value>25</Value>
                        <ValueType>ReinfConcreteCover</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>DiameterStirrup</Name>
                        <Text>Stirrup diameter</Text>
                        <Value>10</Value>
                        <ValueType>ReinfBarDiameter</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>DiameterLongitudinal</Name>
                        <Text>Longitudinal bar diameter</Text>
                        <Value>20</Value>
                        <ValueType>ReinfBarDiameter</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>StirrupPlacementExpander</Name>
                <Text>BarPlacement properties for stirrup</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>DistanceStirrup</Name>
                        <Text>Distance</Text>
                        <Value>150</Value>
                        <MinValue>20</MinValue>
                        <ValueType>Length</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>PlacementRuleStirrup</Name>
                        <Text>Placement rule</Text>
                        <Value>AdditionalCover</Value>
                        <ValueList>AdaptDistance|AdditionalCover|AdditionalCoverLeft|AdditionalCoverRight</ValueList>
                        <ValueType>StringComboBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>PlacePerLinearMeter</Name>
                        <Text>Place per linear meter</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>LengthFactor</Name>
                        <Text>Length factor</Text>
                        <Value>1.1</Value>
                        <ValueType>Double</ValueType>
                        <Visible>PlacePerLinearMeter</Visible>
                        <MinValue>1</MinValue>
                        <MaxValue>2</MaxValue>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>LongitudinalExp</Name>
                <Text>BarPlacement properties for longitudinal bars</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>BarCountLongitudinal</Name>
                        <Text>Bar count</Text>
                        <Value>4</Value>
                        <MinValue>0</MinValue>
                        <ValueType>Integer</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>PlacePerLinearMeterLongitudinal</Name>
                        <Text>Place per linear meter</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>LengthFactorLongitudinal</Name>
                        <Text>Length factor</Text>
                        <Value>1.1</Value>
                        <ValueType>Double</ValueType>
                        <Visible>PlacePerLinearMeterLongitudinal</Visible>
                        <MinValue>1</MinValue>
                        <MaxValue>2</MaxValue>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>SchemaExp</Name>
                <Text>Schema</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>PlanarView</Name>
                        <Text>Planar view</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>ToScale</Name>
                        <Text>To scale</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>SegmentDimensioning</Name>
                        <Text>Segment dimensioning</Text>
                        <Value>True</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>Dimensioning</Name>
                        <Text>Dimensioning</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>AngleDimensioning</Name>
                        <Text>Angle dimensioning</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>BendingDimensioning</Name>
                        <Text>Bending dimensioning</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>Mirroring</Name>
                        <Text>Mirror</Text>
                        <Value>AllplanReinf.SchemaMirror.eXAxis</Value>
                        <ValueType>RadioButtonGroup</ValueType>
                        <EnumList>AllplanReinf.SchemaMirror.eNo|
                                  AllplanReinf.SchemaMirror.eXAxis|
                                  AllplanReinf.SchemaMirror.eYAxis|
                                  AllplanReinf.SchemaMirror.eXYAxis</EnumList>
                        <Visible>PlanarView</Visible>

                        <Parameters>
                            <Parameter>
                                <Name>MirrorNo</Name>
                                <Text>No</Text>
                                <Value>AllplanReinf.SchemaMirror.eNo</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>MirrorX</Name>
                                <Text>X-Axis</Text>
                                <Value>AllplanReinf.SchemaMirror.eXAxis</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>MirrorY</Name>
                                <Text>Y-Axis</Text>
                                <Value>AllplanReinf.SchemaMirror.eYAxis</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>MirrorXY</Name>
                                <Text>X- and Y-Axis</Text>
                                <Value>AllplanReinf.SchemaMirror.eXYAxis</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                    <Parameter>
                        <Name>RotationAngle</Name>
                        <Text>Rotation angle</Text>
                        <Value>0</Value>
                        <ValueType>Angle</ValueType>
                    </Parameter>
                    <Parameter>
                        <Name>StirrupUnfold</Name>
                        <Text>Stirrup unfold</Text>
                        <Value>AllplanReinf.SchemaStirrupUnfold.eNo</Value>
                        <ValueType>RadioButtonGroup</ValueType>
                        <EnumList>AllplanReinf.SchemaStirrupUnfold.eNo|
                                  AllplanReinf.SchemaStirrupUnfold.eFirstSegment|
                                  AllplanReinf.SchemaStirrupUnfold.eFirstLastSegment|
                                  AllplanReinf.SchemaStirrupUnfold.eLastSegment</EnumList>
                        <Visible>PlanarView</Visible>

                        <Parameters>
                            <Parameter>
                                <Name>UnfoldNo</Name>
                                <Text>No</Text>
                                <Value>AllplanReinf.SchemaStirrupUnfold.eNo</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>UnfoldFirst</Name>
                                <Text>First segment</Text>
                                <Value>AllplanReinf.SchemaStirrupUnfold.eFirstSegment</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>UnfoldFirstLast</Name>
                                <Text>First and last segment</Text>
                                <Value>AllplanReinf.SchemaStirrupUnfold.eFirstLastSegment</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                            <Parameter>
                                <Name>UnfoldLast</Name>
                                <Text>Last segment</Text>
                                <Value>AllplanReinf.SchemaStirrupUnfold.eLastSegment</Value>
                                <ValueType>RadioButton</ValueType>
                            </Parameter>
                        </Parameters>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
    <Page>
        <Name>OthersPage</Name>
        <Text>Others</Text>
        <Parameters>
            <Parameter>
                <Name>Format</Name>
                <Text>Format</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>CommonProp</Name>
                        <Text />
                        <Value />
                        <ValueType>CommonProperties</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>Geometry</Name>
                <Text>Geometry</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>Sizes</Name>
                        <Text>Length,Width,Height</Text>
                        <Value>Vector3D(300,1500,600)</Value>
                        <ValueType>Vector3D</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>ElementCreation</Name>
                <Text>Element creation</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>IsPythonPart</Name>
                        <Text>Create as PythonPart</Text>
                        <Value>False</Value>
                        <ValueType>CheckBox</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
</Element>