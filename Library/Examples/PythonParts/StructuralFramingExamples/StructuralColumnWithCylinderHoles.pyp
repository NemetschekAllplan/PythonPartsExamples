﻿<?xml version="1.0" encoding="utf-8"?>
<Element>
    <LanguageFile>etc\Examples\PythonParts\StructuralFramingExamples\StructuralFraming</LanguageFile>

    <Script>
        <Name>StructuralFramingExamples\StructuralColumnWithCylinderHoles.py</Name>
        <GeometryExpand>0</GeometryExpand>
        <Title>Column</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>

    <Page>
        <Name>PageGeometrie</Name>
        <Text>Geometry</Text>
        <TextId>1000</TextId>

        <Parameter>
            <Name>ColumType</Name>
            <TextId>9901</TextId>
            <Value>0</Value>
            <ValueList>0|1|2</ValueList>
            <ValueList2>15581|14587|14601</ValueList2>
            <ValueType>PictureResourceButtonList</ValueType>
        </Parameter>

		<Parameter>
			<Name>Width</Name>
            <TextId>1002</TextId>
			<Value>100</Value>
            <MinValue>1</MinValue>
			<Visible>ColumType == 0</Visible>
			<ValueType>Length</ValueType>
		</Parameter>
		<Parameter>
			<Name>Thickness</Name>
            <TextId>1003</TextId>
			<Value>80</Value>
            <MinValue>1</MinValue>
			<Visible>ColumType == 0</Visible>
			<ValueType>Length</ValueType>
        </Parameter>

		<Parameter>
			<Name>Radius</Name>
            <TextId>1004</TextId>
			<Value>500</Value>
			<Visible>ColumType == 1</Visible>
			<ValueType>Length</ValueType>
		</Parameter>

        <Parameter>
            <Name>ProfilePath</Name>
            <TextId>1005</TextId>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>SymbolDialog</Name>
                <Value>Auswahl</Value>
                <ValueType>String</ValueType>
                <ValueDialog>SymbolDialog</ValueDialog>
            </Parameter>
            <Visible>ColumType == 2</Visible>
        </Parameter>

        <Parameter>
			<Name>Angle</Name>
            <TextId>1006</TextId>
			<Value>0</Value>
			<ValueType>Angle</ValueType>
        </Parameter>

		<Parameter>
            <Name>SkeletonPlaneReferences</Name>
            <ValueType>Row</ValueType>
			<Parameter>
				<Name>ColumnPlaneReferences</Name>
                <TextId>1008</TextId>
				<Value>None</Value>
				<ValueType>PlaneReferences</ValueType>
				<ValueDialog>PlaneReferences</ValueDialog>
			</Parameter>
        </Parameter>

        <Parameter>
            <Name>AnchorPointsExpander</Name>
            <TextId>1100</TextId>
            <ValueType>Expander</ValueType>
            <Visible>True</Visible>

            <Parameter>
                <Name>AnchorPoint</Name>
                <TextId>1101</TextId>
                <Value>top left</Value>
                <ValueTextId>1106</ValueTextId>
                <ValueList>top left|left in middle|left down|top in middle|in middle|in middle down|top right|right in middle|right down|in center of gravity</ValueList>
                <ValueList_TextIds>1102|1103|1104|1105|1106|1107|1108|1109|1110|1111</ValueList_TextIds>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>OffsetFromAnchorPoint</Name>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>Offset</Name>
                    <TextId>1112</TextId>
                    <Value>(0,0)</Value>
                    <ValueType>Point2D</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>ShowAxis</Name>
                <TextId>1113</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
	</Page>

    <Page>
        <Name>PageAttribute</Name>
        <Text>Attribute</Text>
        <TextId>3000</TextId>

        <Parameter>
            <Name>Material</Name>
            <TextId>3001</TextId>
            <Value>Steel_S355</Value>
	        <ValueType>String</ValueType>
        </Parameter>
    </Page>

    <Page>
        <Name>__HiddenPage__</Name>
        <Parameter>
            <Name>UseHeight</Name>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>

</Element>
