<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\FaceStyle.py</Name>
        <Title>FaceStyle</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

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
            <Name>FaceStyleID</Name>
            <Text>FaceStyle ID</Text>
            <Value>301</Value>
            <ValueType>FaceStyle</ValueType>
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

        
        <Parameter>
            <Name>DefineReferencePoint</Name>
            <Text>Define reference point</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReferencePointX</Name>
            <Text>Reference point X</Text>
            <Value>2000.0</Value>
            <Visible>DefineReferencePoint == 1</Visible>                    
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReferencePointY</Name>
            <Text>Reference point Y</Text>
            <Value>1000.0</Value>
            <Visible>DefineReferencePoint == 1</Visible>                    
            <ValueType>Length</ValueType>
        </Parameter>

    </Page>
</Element>
