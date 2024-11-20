<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\ModifyObjects\ModifyStripFoundation.py</Name>
        <Title>Modify StripFoundation</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <!-- Axis position types -->
        <Constant>
            <Name>LEFT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>CENTER</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>RIGHT</Name>
            <Value>4</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>FREE</Name>
            <Value>8</Value>
            <ValueType>Integer</ValueType>
        </Constant>        
        <Constant>
            <Name>STRIP_FOUND_SELECTED</Name>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
        </Constant>

        <!-- Button events -->
        <Constant>
            <Name>REVERSE_OFFSET_DIRECTION</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page</Name>
        <Text>Page</Text>
        <Visible>InputMode == STRIP_FOUND_SELECTED</Visible>
        <Parameter>
            <Name>AxisExpander</Name>
            <Text>Axis properties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>AxisPosition</Name>
                <Text>Axis position</Text>
                <Value>LEFT</Value>
                <ValueList>LEFT|CENTER|RIGHT|FREE</ValueList>
                <ValueTextList>Axis on the left|Axis in the center|Axis on the right|By offset</ValueTextList>
                <ValueList2>11249|11247|11245|10119</ValueList2>
                <ValueType>PictureButtonList</ValueType>
            </Parameter>
            <Parameter>
                <Name>AxisOffset</Name>
                <Text>Axis offset</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <MinValue>0</MinValue>
                <MaxValue>Width</MaxValue>
                <Visible>AxisPosition == FREE</Visible>
            </Parameter>
            <Parameter>
                <Name>ReverseOffsetDirection</Name>
                <Text>Reverse offset direction</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>ReverseOffsetDirectionButton</Name>
                    <Text> </Text>
                    <Value>12451</Value>
                    <EventId>REVERSE_OFFSET_DIRECTION</EventId>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CrossSectionExpander</Name>
            <Text>Cross section</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SectionType</Name>
                <Text>Section type</Text>
                <Value>AllplanArchEle.ShapeType.eRectangular</Value>
                <EnumList>AllplanArchEle.ShapeType.eRectangular|
                          AllplanArchEle.ShapeType.eArbitrary|
                          AllplanArchEle.ShapeType.eStep|
                          AllplanArchEle.ShapeType.eChamfer|
                          AllplanArchEle.ShapeType.eConical</EnumList>
                <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eArbitrary|
                                 AllplanSettings.TextResShapeType.eStep|
                                 AllplanSettings.TextResShapeType.eChamfer|
                                 AllplanSettings.TextResShapeType.eConical</ValueTextIdList>
                <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eArbitrary|
                           AllplanSettings.PictResShapeType.eStep|
                           AllplanSettings.PictResShapeType.eChamfer|
                           AllplanSettings.PictResShapeType.eConical</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
                <Enable>True</Enable>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eRectangular or SectionType == AllplanArchEle.ShapeType.eStep or SectionType == AllplanArchEle.ShapeType.eChamfer or SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
                <Name>PlaneReferences</Name>
                <Text>Height</Text>
                <Value></Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
            </Parameter>
            <Parameter>
                <Name>StepChamferWidth</Name>
                <Text>Step Chamfer Width</Text>
                <Value>50</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eStep or SectionType == AllplanArchEle.ShapeType.eChamfer or SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
                <Name>StepChamferHeight</Name>
                <Text>Step Chamfer Height</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eStep or SectionType == AllplanArchEle.ShapeType.eChamfer or SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
                <Name>StepChamferEccentricity</Name>
                <Text>Step Chamfer Eccentricity</Text>
                <Value>30</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eStep or SectionType == AllplanArchEle.ShapeType.eChamfer or SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
                <Name>StepBounce</Name>
                <Text>Step Bounce</Text>
                <Value>0.1</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eChamfer or SectionType == AllplanArchEle.ShapeType.eChamfer or SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
                <Name>LeftHaunch</Name>
                <Text>Left Haunch</Text>
                <Value>0.1</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
                <Name>RightHaunch</Name>
                <Text>Right Haunch</Text>
                <Value>0.1</Value>
                <ValueType>Length</ValueType>
                <Visible>SectionType == AllplanArchEle.ShapeType.eConical</Visible>
            </Parameter>
            <Parameter>
            <Name>ProfileRow</Name>
            <Text>Select profile</Text>
            <ValueType>Row</ValueType>
                <Parameter>
                <Name>Profile</Name>
                <Text>Select Profile</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <ValueDialog>SymbolDialog</ValueDialog>
                </Parameter>
            <Visible>SectionType == AllplanArchEle.ShapeType.eArbitrary</Visible>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>FormatPropertiesExpander</Name>
            <Text>Format properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>SurfaceElementsExp</Name>
            <Text>Surface elements</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>SurfaceElemProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>SurfaceElementProperties</ValueType>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>SurfaceRow</Name>
                <Text>Surface (Animation)</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsSurface</Name>
                    <Text>Surface</Text>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SurfaceName</Name>
                    <Text>Surface</Text>
                    <Value></Value>
                    <ValueType>MaterialButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>AttributesExpander</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Trade</Name>
                <Text>Trade</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>Trade</ValueDialog>
            </Parameter>
            <Parameter>
                <Name>Priority</Name>
                <Text>Priority</Text>
                <Value>100</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>CalculationMode</Name>
                <Text>Calculation mode</Text>
                <Value>2</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>120</AttributeId>
                </Parameter>
            <Parameter>
                <Name>Factor</Name>
                <Text>Factor</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
                <MinValue>0.0</MinValue>
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
