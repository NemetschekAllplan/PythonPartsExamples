<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\BarPlacement\LongitudinalBarPlacement.py</Name>
        <Title>RebarPlacement</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>
        <Parameter>
            <Name>PlacementPropertiesExpander</Name>
            <Text>BarShapePlacementUtil</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>PlacementType</Name>
                <Text>Place the longitudinal bar</Text>
                <Value>in_corner</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>InCorner</Name>
                    <Text>in corner</Text>
                    <Value>in_corner</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>OnSide</Name>
                    <Text>on side</Text>
                    <Value>on_side</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>AtIntersection</Name>
                    <Text>at intersection</Text>
                    <Value>at_intersection</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>OnSideBetweenLegs</Name>
                    <Text>on side, between legs</Text>
                    <Value>on_side_between_legs</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>BarCount</Name>
                <Text>Bar count</Text>
                <Value>6</Value>
                <MinValue>1</MinValue>
                <ValueType>Integer</ValueType>
                <Visible>PlacementType in ["on_side", "on_side_between_legs"]</Visible>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>LongitudinalBarPlacementLegend</Name>
                <Value>LongitudinalBarPlacementLegend.png</Value>
                <Orientation>Middle</Orientation>
                <ValueType>Picture</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            <Parameter>
                <Name>ReferenceShape</Name>
                <Text>First reference shape</Text>
                <Value>closed stirrup</Value>
                <ValueList>closed stirrup|horizontal S-hook|vertical S-hook</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>SideId</Name>
                <Text>Side number of first reference shape</Text>
                <Value>5</Value>
                <MinValue>2 if PlacementType == "on_side" else 1</MinValue>
                <ValueType>Integer</ValueType>
                <Visible>PlacementType != "in_corner"</Visible>
            </Parameter>

            <Parameter>
                <Name>CornerId</Name>
                <Text>Corner number</Text>
                <Value>2</Value>
                <MinValue>1</MinValue>
                <ValueType>Integer</ValueType>
                <Visible>PlacementType == "in_corner"</Visible>
            </Parameter>
            <Parameter>
                <Name>AboveFirstSide</Name>
                <Text>Place above first side</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
                <Visible>PlacementType == "at_intersection"</Visible>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
                <Visible>PlacementType in ["at_intersection", "on_side_between_legs"]</Visible>
            </Parameter>

            <Parameter>
                <Name>SecondReferenceShape</Name>
                <Text>Second reference shape</Text>
                <Value>horizontal S-hook</Value>
                <ValueList>closed stirrup|horizontal S-hook|vertical S-hook</ValueList>
                <ValueType>StringComboBox</ValueType>
                <Visible>PlacementType in ["at_intersection", "on_side_between_legs"]</Visible>
            </Parameter>

            <Parameter>
                <Name>SecondShapeSideId</Name>
                <Text>Side number of second reference shape</Text>
                <Value>3</Value>
                <MinValue>1</MinValue>
                <ValueType>Integer</ValueType>
                <Visible>PlacementType in ["at_intersection", "on_side_between_legs"]</Visible>
            </Parameter>
            <Parameter>
                <Name>AboveSecondSide</Name>
                <Text>Place above second side</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
                <Visible>PlacementType == "at_intersection"</Visible>
            </Parameter>
            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
                <Visible>PlacementType == "on_side_between_legs"</Visible>
            </Parameter>

            <Parameter>
                <Name>ThirdReferenceShape</Name>
                <Text>Third reference shape</Text>
                <Value>vertical S-hook</Value>
                <ValueList>closed stirrup|horizontal S-hook|vertical S-hook</ValueList>
                <ValueType>StringComboBox</ValueType>
                <Visible>PlacementType == "on_side_between_legs"</Visible>
            </Parameter>

            <Parameter>
                <Name>ThirdShapeSideId</Name>
                <Text>Side number of third reference shape</Text>
                <Value>3</Value>
                <MinValue>1</MinValue>
                <ValueType>Integer</ValueType>
                <Visible>PlacementType == "on_side_between_legs"</Visible>
            </Parameter>
            <Parameter>
                <Name>AboveThirdSide</Name>
                <Text>Place above third side</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
                <Visible>PlacementType == "on_side_between_legs"</Visible>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>ShapePropertiesExpander</Name>
            <Text>ReinforcementShapeProperties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DiameterLongitudinal</Name>
                <Text>Longitudinal bar diameter</Text>
                <Value>32</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>DiameterStirrups</Name>
                <Text>Stirrups diameter</Text>
                <Value>8</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>BendingRollerStirrups</Name>
                <Text>Stirrups bending roller</Text>
                <Value>4</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
