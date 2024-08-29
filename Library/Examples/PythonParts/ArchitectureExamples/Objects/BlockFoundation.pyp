<?xml version="1.0" encoding="utf-8"?><Element>
    <Script>
        <Name>ArchitectureExamples\Objects\BlockFoundation.py</Name>
        <Title>BlockFoundation</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>
    <Page>

		<Name>Page1</Name>
        <Text>Geometry</Text>
        <Parameter>
			<Name>WallPlaneRef</Name>
			<Text>PlaneReferences</Text>
			<Value></Value>
			<ValueType>PlaneReferences</ValueType>
			<ValueDialog>PlaneReferences</ValueDialog>
        </Parameter>
        <Parameter>
            <Name>ShapeType</Name>
            <Text>Shape Type</Text>
            <Value>eRectangular</Value>
            <ValueList>|eRectangular|eCircular|eConical|ePolygonal|</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
		<Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>2000.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>10000</MaxValue>
            <Visible>ShapeType == "eRectangular" or ShapeType == "eConical"</Visible>
        </Parameter>
        <Parameter>
            <Name>Depth</Name>
            <Text>Depth</Text>
            <Value>2000.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>200</MinValue>
            <MaxValue>10000</MaxValue>
            <Visible>ShapeType == "eRectangular" or ShapeType == "eConical"</Visible>
        </Parameter>
		<Parameter>
            <Name>Radius</Name>
            <Text>Radius</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>3000</MaxValue>
            <Visible>ShapeType == "eCircular"</Visible>
        </Parameter>
		<Parameter>
            <Name>VouteBack</Name>
            <Text>Voute Back</Text>
            <Value>250.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>10000</MaxValue>
            <Visible>ShapeType == "eConical"</Visible>
        </Parameter>
		<Parameter>
            <Name>VouteFront</Name>
            <Text>Voute Front</Text>
            <Value>250.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>10000</MaxValue>
            <Visible>ShapeType == "eConical"</Visible>
        </Parameter>
		<Parameter>
            <Name>VouteLeft</Name>
            <Text>Voute Left</Text>
            <Value>250.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>10000</MaxValue>
            <Visible>ShapeType == "eConical"</Visible>
        </Parameter>
		<Parameter>
            <Name>VouteRight</Name>
            <Text>Voute Right</Text>
            <Value>250.0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>10000</MaxValue>
            <Visible>ShapeType == "eConical"</Visible>
        </Parameter>
        <Parameter>
            <Name>PointExpander</Name>
            <Text>Polygon Points</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                    <Name>ProfilePoints</Name>
                    <Text>Profile points</Text>
                    <Value>[Point2D( 0.0,  0.0);
                            Point2D(2000.0, 0.0);
                            Point2D(2000.0, 2000.0);
                            Point2D(0.0, 0.0);]</Value>
                    <ValueType>Point2D</ValueType>
                    <XYZinRow>False</XYZinRow>
                    <Visible>ShapeType == "ePolygonal"</Visible>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>CommonPropertiesExp</Name>
            <Text>CommonProperties</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value>CommonProperties(Color(1))</Value>
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

</Element>