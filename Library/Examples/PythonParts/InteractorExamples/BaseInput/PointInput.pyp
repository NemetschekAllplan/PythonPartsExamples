<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>InteractorExamples\BaseInput\PointInput.py</Name>
        <Title>PointInput</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
        <ShowFavoriteButtons>False</ShowFavoriteButtons>
    </Script>
    <Page>
        <Name>PointInput</Name>
        <Text>Point input</Text>

        <Parameter>
            <Name>General</Name>
            <Text>General options</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CreateSymbol</Name>
                <Text>Create symbol on mouse click</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>SymbolCommonProps</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
                <Visible>CreateSymbol</Visible>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>CoordinateInputOptions</Name>
            <Text>Options of CoordinateInput</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>TrackTo</Name>
                <Text>Track to</Text>
                <Value>Nothing</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>Nothing</Name>
                    <Text>nothing</Text>
                    <Value>Nothing</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>LastInputPoint</Name>
                    <Text>last input point</Text>
                    <Value>LastInputPoint</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>DefinedPoint</Name>
                    <Text>defined point</Text>
                    <Value>DefinedPoint</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>TrackPoint</Name>
                <Text>Track point</Text>
                <Value>Point3D(0,0,0)</Value>
                <ValueType>Point3D</ValueType>
                <Visible>TrackTo == "DefinedPoint"</Visible>
                <XYZinRow>True</XYZinRow>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>EnableInputControl</Name>
                <Text>Enable input control</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>EnableZCoordinate</Name>
                <Text>Enable Z coordinate input</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>EnableUndoStep</Name>
                <Text>Enable undo step</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>EnableAssistWndClick</Name>
                <Text>Allow input in wizard window</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>SetProjectionBase0</Name>
                <Text>Set projection base to 0</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
                <Visible>SetInputPlane</Visible>
            </Parameter>

            <Parameter>
                <Name>SetInputPlane</Name>
                <Text>Set input plane</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>InputPlanePoint</Name>
                <Text>Input plane point</Text>
                <Value>Point3D(0,0,0)</Value>
                <XYZinRow>True</XYZinRow>
                <ValueType>Point3D</ValueType>
                <Visible>SetInputPlane</Visible>
            </Parameter>

            <Parameter>
                <Name>InputPlaneVector</Name>
                <Text>Plane normal vector</Text>
                <Value>Vector3D(0,0,1000)</Value>
                <XYZinRow>True</XYZinRow>
                <Visible>SetInputPlane</Visible>
                <ValueType>Vector3D</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>InputControlSettingsExpander</Name>
            <Text>Options of input control</Text>
            <ValueType>Expander</ValueType>
            <Visible>EnableInputControl</Visible>

            <Parameter>
                <Name>InputControlType</Name>
                <Text>Input control type</Text>
                <Value>eTEXT_EDIT</Value>
                <ValueList>"|".join(str(key) for key in AllplanIFW.eValueInputControlType.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>SetFocus</Name>
                <Text>Set focus on the input control</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>DisableCoord</Name>
                <Text>Disable coordinates during input</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>CoordinateInputModeSettingExpander</Name>
            <Text>Options of CoordinateInputMode</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DrawElementIdentPoint</Name>
                <Text>Draw element identification symbol</Text>
                <Value>eDRAW_IDENT_ELEMENT_POINT_SYMBOL_YES</Value>
                <ValueList>"|".join(str(key) for key in AllplanIFW.eDrawElementIdentPointSymbols.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>IndentificationMode</Name>
                <Text>Identification mode</Text>
                <Value>eIDENT_POINT</Value>
                <ValueList>"|".join(str(key) for key in AllplanIFW.eIdentificationMode.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

        </Parameter>


        <Parameter>
            <Name>SnoopElementGeometryFilterExpander</Name>
            <Text>Options of SnoopElementGeometryFilter</Text>
            <ValueType>Expander</ValueType>
            <Visible>IndentificationMode in ["eIDENT_POINT_ELEMENT","eIDENT_POINT_ELEMENT_CENTER","eIDENT_POINT_ELEMENT_ALWAYS","eIDENT_POINT_ELEMENT_ALWAYS_CENTER",] </Visible>

            <Parameter>
                <Name>FindBaseGeometry</Name>
                <Text>Find base geometry</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>FindAreaGeometry</Name>
                <Text>Find area geometry</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>PerpendicularOnElement</Name>
                <Text>Perpendicular on element</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>FindNonPassiveOnly</Name>
                <Text>Find non passive only</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>SplitAreaGeometries</Name>
                <Text>Split area geometries</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>IdentifyEmbeddedElement</Name>
                <Text>Identify embedded element</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>FindCompleteFootprint</Name>
                <Text>Find complete footprint</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>SplitElement3D</Name>
                <Text>Split element 3D</Text>
                <Value>ELEMENT3D_NO_SPLIT</Value>
                <ValueList>"|".join(str(key) for key in AllplanIFW.eSplitElement3D.names.keys())</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

        </Parameter>
    </Page>
</Element>
